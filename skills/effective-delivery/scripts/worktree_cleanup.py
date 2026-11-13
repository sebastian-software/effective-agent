#!/usr/bin/env python3
"""Classify linked Git worktrees below a folder and remove the finished ones.

scan    Read-only apart from an optional `git fetch origin`. Classifies every
        linked worktree of every repository below the root and writes a JSON
        report.
remove  Rechecks each selected worktree, then removes it. A dirty or busy
        worktree is never removed; no flag overrides that.

Classes
  done      clean, idle, and every commit is contained in the base branch
            -> worktree removed, local branch deleted
  unmerged  clean and idle, but the branch has commits the base branch lacks
            -> only when named with --include; the branch stays
  dirty     uncommitted or untracked changes, an operation in progress, or
            local work inside a submodule
  busy      a process works in it, it is locked, protected, recently active,
            or unreadable
  missing   registered, but the folder is gone -> `git worktree prune`

Python 3.9+, standard library only. Requires git 2.38 or newer for the content
check; uses lsof or /proc, du, and the GitHub CLI when they are available.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

SKIP_DIRS = {"node_modules", "target", "dist", "build", "vendor"}
# Ignored entries that are build output or tool state, never worth a warning.
NOISE = {
    "node_modules", "target", "dist", "build", "out", "coverage", "tmp", "temp",
    ".next", ".nuxt", ".turbo", ".cache", ".parcel-cache", ".vite", ".svelte-kit",
    ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".tox", ".gradle", ".idea", ".vscode", ".DS_Store", ".claude", ".codex",
    ".eslintcache", ".tsbuildinfo", "DerivedData", ".build", "Pods", ".terraform",
}
# Untracked entries that never hold work; a worktree with only these is clean.
UNTRACKED_NOISE = {
    "node_modules", ".venv", "__pycache__", ".DS_Store", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".turbo", ".next", ".parcel-cache",
}
NOISE_SUFFIXES = (".log", ".tsbuildinfo", ".pyc", ".o", ".a", ".d", ".tmp", ".lock")
KEEP_BRANCHES = {"main", "master", "develop", "development", "trunk", "staging", "production"}
ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0", LC_ALL="C")


def run(cmd, cwd=None, timeout=120):
    try:
        proc = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True,
                              errors="replace", timeout=timeout)
        return proc.returncode, proc.stdout.rstrip("\n"), proc.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except OSError as error:
        return 127, "", str(error)


def git(cwd, *args, timeout=120):
    return run(["git", *args], cwd=cwd, timeout=timeout)


def inside(path, folder):
    return path == folder or path.startswith(folder + os.sep)


def find_repos(root, max_depth):
    """Main checkouts below root: folders whose `.git` is a directory."""
    repos, stack = [], [(root, 0)]
    while stack:
        folder, depth = stack.pop()
        try:
            entries = list(os.scandir(folder))
        except OSError:
            continue
        if any(entry.name == ".git" for entry in entries):
            if os.path.isdir(os.path.join(folder, ".git")):
                repos.append(folder)
            continue  # a linked worktree or submodule; its repository reports it
        if depth >= max_depth:
            continue
        for entry in entries:
            if (entry.is_dir(follow_symlinks=False) and not entry.name.startswith(".")
                    and entry.name not in SKIP_DIRS):
                stack.append((entry.path, depth + 1))
    return sorted(repos)


def list_worktrees(repo):
    rc, out, _ = git(repo, "worktree", "list", "--porcelain")
    if rc:
        return []
    items, current = [], {}
    for line in out.splitlines() + [""]:
        if not line:
            if current:
                items.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value if value else True
    return items


def ref_exists(repo, ref):
    return git(repo, "rev-parse", "--verify", "--quiet", ref + "^{commit}")[0] == 0


def base_refs(repo, main_item):
    """The default branch and the refs that count as 'merged into it'."""
    rc, out, _ = git(repo, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD")
    default = out.split("/", 1)[1] if rc == 0 and "/" in out else None
    if not default:
        for candidate in ("main", "master"):
            if (ref_exists(repo, "refs/remotes/origin/" + candidate)
                    or ref_exists(repo, "refs/heads/" + candidate)):
                default = candidate
                break
    if not default and isinstance(main_item.get("branch"), str):
        default = main_item["branch"].replace("refs/heads/", "", 1)
    if not default:
        return None, []
    refs = [ref for ref in ("refs/remotes/origin/" + default, "refs/heads/" + default)
            if ref_exists(repo, ref)]
    return default, refs


def short(ref):
    return ref.replace("refs/remotes/", "").replace("refs/heads/", "")


def contained(repo, tip, bases, branch, use_gh):
    """Why every commit of `tip` is already in a base ref, or None."""
    for base in bases:
        if git(repo, "merge-base", "--is-ancestor", tip, base)[0] == 0:
            return "ancestor of " + short(base)
    for base in bases:
        rc, out, _ = git(repo, "cherry", base, tip)
        if rc == 0 and not any(line.startswith("+") for line in out.splitlines()):
            return "same patches in " + short(base)
    for base in bases:
        # A merge that changes nothing in the base: squash merges, and
        # cherry-picks that were adjusted while resolving a conflict.
        rc, out, _ = git(repo, "merge-tree", "--write-tree", base, tip)
        if rc == 0 and out:
            rc2, tree, _ = git(repo, "rev-parse", base + "^{tree}")
            if rc2 == 0 and out.splitlines()[0] == tree:
                return "content already in " + short(base)
    if use_gh and branch:
        rc, out, _ = run(["gh", "pr", "list", "--head", branch, "--state", "merged",
                          "--json", "number,headRefOid", "--limit", "10"],
                         cwd=repo, timeout=30)
        if rc == 0 and out:
            try:
                for pull in json.loads(out):
                    if pull.get("headRefOid") == tip:
                        return "merged pull request #%s" % pull.get("number")
            except ValueError:
                pass
    return None


def pid_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False


def own_ancestors():
    pids, pid = set(), os.getpid()
    for _ in range(64):
        pids.add(pid)
        rc, out, _ = run(["ps", "-o", "ppid=", "-p", str(pid)], timeout=10)
        if rc or not out.strip().isdigit() or int(out) <= 1:
            break
        pid = int(out)
    return pids


def process_cwds():
    """(cwd, pid, command) of the user's processes, or None when unavailable."""
    result = []
    if shutil.which("lsof"):
        _, out, _ = run(["lsof", "-a", "-d", "cwd", "-F", "pcn", "-u", str(os.getuid())],
                        timeout=60)
        pid, command = None, ""
        for line in out.splitlines():
            if line.startswith("p") and line[1:].isdigit():
                pid, command = int(line[1:]), ""
            elif line.startswith("c"):
                command = line[1:]
            elif line.startswith("n") and pid:
                result.append((os.path.realpath(line[1:]), pid, command))
    elif os.path.isdir("/proc/self"):
        for name in os.listdir("/proc"):
            if not name.isdigit():
                continue
            try:
                cwd = os.readlink("/proc/%s/cwd" % name)
                with open("/proc/%s/comm" % name) as handle:
                    command = handle.read().strip()
            except OSError:
                continue  # another user's process, or it just exited
            result.append((os.path.realpath(cwd), int(name), command))
    return result or None


def lock_state(item, ancestors):
    if "locked" not in item:
        return None
    reason = item["locked"] if isinstance(item["locked"], str) else ""
    match = re.search(r"\bpid (\d+)", reason)
    if not match:
        return {"kind": "manual", "reason": reason}
    pid = int(match.group(1))
    if not pid_alive(pid):
        kind = "stale"
    elif pid in ancestors:
        kind = "own-session"
    else:
        kind = "foreign"
    return {"kind": kind, "pid": pid, "reason": reason}


def notable_ignored(path, main_path):
    """Ignored files a removal would delete and the main checkout lacks."""
    _, out, _ = git(path, "status", "--porcelain", "--ignored=traditional",
                    "--untracked-files=normal", timeout=180)
    found = []
    for line in out.splitlines():
        if not line.startswith("!! "):
            continue
        rel = line[3:].strip('"')
        name = os.path.basename(rel.rstrip("/"))
        if name in NOISE or name.endswith(NOISE_SUFFIXES) or any(
                part in NOISE for part in rel.rstrip("/").split("/")):
            continue
        mine, theirs = os.path.join(path, rel), os.path.join(main_path, rel)
        if rel.endswith("/"):
            if os.path.isdir(theirs):
                continue
        elif os.path.isfile(theirs):
            try:
                if os.path.getsize(mine) == os.path.getsize(theirs):
                    with open(mine, "rb") as a, open(theirs, "rb") as b:
                        if a.read() == b.read():
                            continue
            except OSError:
                pass
        found.append(rel)
    return found[:12]


def idle_hours(gitdir):
    newest = 0.0
    for name in ("HEAD", "index", os.path.join("logs", "HEAD")):
        try:
            newest = max(newest, os.path.getmtime(os.path.join(gitdir, name)))
        except OSError:
            pass
    return round((time.time() - newest) / 3600, 1) if newest else None


def classify(repo, main_item, item, bases, ctx):
    path = item["worktree"]
    real = os.path.realpath(path)
    branch_ref = item.get("branch") if isinstance(item.get("branch"), str) else None
    branch = branch_ref.replace("refs/heads/", "", 1) if branch_ref else None
    info = {
        "repo": repo, "path": path, "name": os.path.basename(path), "branch": branch,
        "tip": item.get("HEAD"), "class": None, "reasons": [], "merged_via": None,
        "ahead": None, "same_subject_on_base": None, "on_remote": None,
        "lock": lock_state(item, ctx["ancestors"]), "has_submodules": False,
        "notable_ignored": [], "untracked_noise": [], "idle_hours": None, "size_kb": None,
    }
    if not os.path.isdir(path):
        info["class"] = "missing"
        info["reasons"].append("folder is gone; `git worktree prune` clears the entry")
        return info

    busy, dirty = [], []
    for protected in ctx["protect"]:
        if inside(protected, real):
            busy.append("protected: " + protected)
    if ctx["cwds"] is None:
        info["reasons"].append("process check unavailable (no lsof or /proc)")
    else:
        users = sorted({"%s (pid %d)" % (cmd or "?", pid)
                        for cwd, pid, cmd in ctx["cwds"] if inside(cwd, real)})
        if users:
            busy.append("in use by " + ", ".join(users[:4]))
    lock = info["lock"]
    if lock:
        if lock["kind"] == "manual":
            busy.append("locked by hand: " + (lock["reason"] or "no reason given"))
        elif lock["kind"] == "foreign":
            busy.append("locked by running process %d" % lock["pid"])
        elif lock["kind"] == "own-session" and not ctx["own_locks_finished"]:
            busy.append("locked by the calling session (pid %d)" % lock["pid"])

    rc, gitdir, _ = git(path, "rev-parse", "--absolute-git-dir")
    if rc:
        info["class"] = "busy"
        info["reasons"] = busy + ["git cannot read this worktree (broken link? "
                                  "`git worktree repair` in the repository may fix it)"]
        return info
    info["idle_hours"] = idle_hours(gitdir)
    if ctx["min_idle_hours"] and info["idle_hours"] is not None \
            and info["idle_hours"] < ctx["min_idle_hours"]:
        busy.append("active %.1f h ago" % info["idle_hours"])

    rc, out, err = git(path, "status", "--porcelain", "--ignore-submodules=none",
                       "--untracked-files=normal", timeout=300)
    if rc:
        busy.append("git status failed: " + err[:80])
    elif out:
        changed, untracked = [], []
        for line in out.splitlines():
            rel = line[3:].strip('"').rstrip("/")
            if not line.startswith("??"):
                changed.append(rel)
            elif os.path.basename(rel) in UNTRACKED_NOISE:
                info["untracked_noise"].append(rel)  # dependency folders and caches
            else:
                untracked.append(rel)
        if changed or untracked:
            sample = ", ".join((changed + untracked)[:3])
            dirty.append("%d changed, %d untracked (%s%s)" % (
                len(changed), len(untracked), sample,
                ", ..." if len(changed) + len(untracked) > 3 else ""))
    for marker in ("rebase-merge", "rebase-apply", "MERGE_HEAD", "CHERRY_PICK_HEAD",
                   "REVERT_HEAD", "BISECT_LOG"):
        if os.path.exists(os.path.join(gitdir, marker)):
            dirty.append("operation in progress: " + marker)

    if os.path.exists(os.path.join(path, ".gitmodules")):
        probe = ('echo "$displaypath|$(git stash list | wc -l | tr -d " ")|'
                 '$(git rev-list --count --branches --not --remotes HEAD 2>/dev/null)"')
        rc, out, _ = git(path, "submodule", "foreach", "--quiet", "--recursive", probe,
                         timeout=300)
        if rc:
            dirty.append("submodules could not be checked")
        for line in out.splitlines():
            parts = line.rsplit("|", 2)
            if len(parts) != 3:
                continue
            info["has_submodules"] = True
            if parts[1] not in ("", "0"):
                dirty.append("submodule %s has a stash" % parts[0])
            if parts[2] not in ("", "0"):
                dirty.append("submodule %s has %s local commit(s)" % (parts[0], parts[2]))

    tip = info["tip"]
    if tip and bases:
        info["merged_via"] = contained(repo, tip, bases, branch, ctx["use_gh"])
        rc, out, _ = git(repo, "rev-list", "--count", "%s..%s" % (bases[0], tip))
        info["ahead"] = int(out) if rc == 0 and out.isdigit() else None
    if tip:
        rc, out, _ = git(repo, "for-each-ref", "--count=1", "--contains", tip,
                         "--format=%(refname:short)", "refs/remotes")
        info["on_remote"] = out or None
        if not info["merged_via"] and not branch:
            # Detached HEAD: nothing is lost if another ref holds the commit.
            rc, out, _ = git(repo, "for-each-ref", "--count=1", "--contains", tip,
                             "--format=%(refname:short)", "refs/heads", "refs/remotes",
                             "refs/tags")
            if rc == 0 and out:
                info["merged_via"] = "detached; commit is on " + out
    if tip and bases and not info["merged_via"]:
        rc, out, _ = git(repo, "cherry", "-v", bases[0], tip)
        subjects = [line[2:].split(" ", 1)[1] for line in out.splitlines()
                    if line.startswith("+ ") and " " in line[2:]]
        if rc == 0 and subjects:
            _, log, _ = git(repo, "log", bases[0], "--format=%s", "-n", "3000")
            known = set(log.splitlines())
            hits = sum(1 for subject in subjects if subject in known)
            info["same_subject_on_base"] = "%d of %d" % (hits, len(subjects))

    if not dirty:
        info["notable_ignored"] = notable_ignored(path, main_item["worktree"])

    if busy:
        info["class"] = "busy"
    elif dirty:
        info["class"] = "dirty"
    elif info["merged_via"]:
        info["class"] = "done"
    else:
        info["class"] = "unmerged"
        if not bases:
            dirty.append("no base branch found")
    info["reasons"] += busy + dirty
    return info


def measure(path):
    _, out, _ = run(["du", "-sk", path], timeout=120)
    first = out.split("\t", 1)[0] if out else ""
    return int(first) if first.isdigit() else None


def human(kilobytes):
    if kilobytes is None:
        return "?"
    value = float(kilobytes) * 1024
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return "%.0f %s" % (value, unit) if unit in ("B", "KB") else "%.1f %s" % (value, unit)
        value /= 1024


def make_context(args):
    # The caller's own working folder is protected even when no process list
    # is available to detect it.
    protect = [os.getcwd()] + list(args.protect or [])
    return {
        "protect": sorted({os.path.realpath(os.path.expanduser(p)) for p in protect}),
        "cwds": process_cwds(),
        "ancestors": own_ancestors(),
        "own_locks_finished": args.own_locks_finished,
        "min_idle_hours": args.min_idle_hours,
        "use_gh": not args.no_gh and bool(shutil.which("gh")),
    }


def scan_repo(repo, ctx, fetch):
    items = list_worktrees(repo)
    if not items:
        return None
    main_item = items[0]
    linked = [item for item in items[1:] if "bare" not in item]
    registered = {os.path.realpath(item["worktree"]) for item in items}
    orphans = []
    for parent in ctx.get("orphan_dirs", []):
        agent_dir = os.path.join(repo, parent)
        if not os.path.isdir(agent_dir):
            continue
        for entry in os.scandir(agent_dir):
            if entry.is_dir(follow_symlinks=False) and os.path.realpath(entry.path) not in registered:
                orphans.append(entry.path)
    if not linked and not orphans:
        return None
    fetched = None
    if fetch and linked and git(repo, "remote", "get-url", "origin")[0] == 0:
        fetched = git(repo, "fetch", "--quiet", "origin", timeout=90)[0] == 0
    default, bases = base_refs(repo, main_item)
    return {
        "repo": repo, "default_branch": default, "bases": [short(base) for base in bases],
        "fetched": fetched, "orphans": sorted(orphans),
        "worktrees": [classify(repo, main_item, item, bases, ctx) for item in linked],
    }


def cmd_scan(args):
    root = os.path.realpath(os.path.expanduser(args.root))
    ctx = make_context(args)
    ctx["orphan_dirs"] = args.worktree_dir
    repos = [result for result in (scan_repo(repo, ctx, not args.no_fetch)
                                   for repo in find_repos(root, args.depth)) if result]
    everything = [wt for repo in repos for wt in repo["worktrees"]]
    if not args.no_sizes:
        present = [wt for wt in everything if wt["class"] != "missing"]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            for wt, size in zip(present, pool.map(measure, [wt["path"] for wt in present])):
                wt["size_kb"] = size
    report = {
        "created": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "root": root,
        "options": {"protect": ctx["protect"], "own_locks_finished": ctx["own_locks_finished"],
                    "min_idle_hours": ctx["min_idle_hours"], "use_gh": ctx["use_gh"],
                    "fetch": not args.no_fetch},
        "repos": repos,
    }
    out = args.out or os.path.join(tempfile.gettempdir(),
                                   "worktree-cleanup-%d.json" % int(time.time()))
    with open(out, "w") as handle:
        json.dump(report, handle, indent=1)

    print("root: %s   repositories with linked worktrees: %d   linked worktrees: %d"
          % (root, len(repos), len(everything)))
    for name in ("done", "unmerged", "dirty", "busy", "missing"):
        group = [wt for wt in everything if wt["class"] == name]
        if group:
            sizes = [wt["size_kb"] for wt in group if wt["size_kb"]]
            print("  %-9s %3d   %s" % (name, len(group), human(sum(sizes)) if sizes else ""))
    for repo in repos:
        print("\n%s   (base: %s%s)" % (repo["repo"], ", ".join(repo["bases"]) or "none",
                                      "" if repo["fetched"] is not False else "; fetch failed"))
        for wt in sorted(repo["worktrees"], key=lambda w: (w["class"], w["name"])):
            detail = "; ".join(wt["reasons"])
            if wt["class"] == "done":
                detail = wt["merged_via"]
            elif wt["class"] == "unmerged":
                detail = "%s commit(s) not in base" % (wt["ahead"] if wt["ahead"] is not None else "?")
                if wt["on_remote"]:
                    detail += ", pushed (%s)" % wt["on_remote"]
                else:
                    detail += ", only local"
                if wt["same_subject_on_base"]:
                    detail += ", same subject on base: " + wt["same_subject_on_base"]
            extra = ""
            if wt["notable_ignored"]:
                extra = "   ignored files only here: " + ", ".join(wt["notable_ignored"][:4])
            print("  %-9s %9s  %-34s %-38s %s%s" % (
                wt["class"], human(wt["size_kb"]), wt["name"][:34],
                (wt["branch"] or "(detached)")[:38], detail, extra))
        for orphan in repo["orphans"]:
            print("  orphan               %s   (folder without a registered worktree; not touched)"
                  % orphan)
    print("\nreport: " + out)
    return 0


def cmd_remove(args):
    with open(args.report) as handle:
        report = json.load(handle)
    wanted_paths = {os.path.realpath(os.path.expanduser(p)) for p in (args.include or [])}
    classes = set(args.classes.split(",")) if args.classes else set()
    if classes - {"done", "missing"}:
        print("--classes accepts done and missing only; name unmerged worktrees with --include",
              file=sys.stderr)
        return 2
    ctx = make_context(args)
    ctx["protect"] = sorted(set(ctx["protect"]) | set(report["options"].get("protect", [])))
    ctx["own_locks_finished"] = (ctx["own_locks_finished"]
                                 or report["options"].get("own_locks_finished", False))
    ctx["min_idle_hours"] = args.min_idle_hours or report["options"].get("min_idle_hours", 0)
    ctx["use_gh"] = ctx["use_gh"] and report["options"].get("use_gh", True)
    free_before = shutil.disk_usage(report["root"]).free
    log_path = args.log or os.path.splitext(args.report)[0] + ".removed.json"
    entries, skipped = [], 0

    for repo_report in report["repos"]:
        repo = repo_report["repo"]
        items = list_worktrees(repo)
        if not items:
            continue
        current = {item["worktree"]: item for item in items}
        default, bases = base_refs(repo, items[0])
        touched = False
        for old in repo_report["worktrees"]:
            explicit = os.path.realpath(old["path"]) in wanted_paths
            if not (old["class"] in classes or explicit):
                continue
            if old["class"] == "missing":
                touched = True
                continue
            if old["class"] not in ("done", "unmerged"):
                print("skip    %s: class %s is never removed" % (old["path"], old["class"]))
                skipped += 1
                continue
            item = current.get(old["path"])
            if not item:
                print("skip    %s: no longer registered" % old["path"])
                skipped += 1
                continue
            now = classify(repo, items[0], item, bases, ctx)
            if now["class"] != old["class"] or now["tip"] != old["tip"]:
                print("skip    %s: changed since the scan (%s -> %s; %s)" % (
                    old["path"], old["class"], now["class"],
                    "; ".join(now["reasons"]) or "new commits"))
                skipped += 1
                continue
            if now["notable_ignored"] and not explicit:
                print("skip    %s: ignored files that exist only here (%s); name it with --include"
                      % (old["path"], ", ".join(now["notable_ignored"][:4])))
                skipped += 1
                continue
            delete_branch = bool(now["class"] == "done" and now["branch"]
                                 and now["branch"] not in KEEP_BRANCHES
                                 and now["branch"] != default)
            entry = {"repo": repo, "path": old["path"], "branch": now["branch"],
                     "tip": now["tip"], "class": now["class"],
                     "merged_via": now["merged_via"], "branch_deleted": False}
            if args.dry_run:
                print("would remove %s%s" % (old["path"], " and delete branch " + now["branch"]
                                             if delete_branch else " (branch stays)"))
                entries.append(entry)
                continue
            if now["lock"]:
                git(repo, "worktree", "unlock", old["path"])
            command = ["worktree", "remove"]
            if now["has_submodules"] or now["untracked_noise"]:
                # git refuses submodules and untracked dependency folders
                # otherwise; the recheck above found nothing else in the way
                command.append("--force")
            rc, _, err = git(repo, *command, old["path"], timeout=1800)
            if rc:
                print("FAILED  %s: %s" % (old["path"], err))
                skipped += 1
                continue
            touched = True
            if delete_branch and git(repo, "rev-parse", "refs/heads/" + now["branch"])[1] == now["tip"]:
                entry["branch_deleted"] = git(repo, "branch", "-D", now["branch"])[0] == 0
            print("removed %s%s" % (old["path"], "; branch %s deleted" % now["branch"]
                                    if entry["branch_deleted"] else "; branch stays"))
            if entry["branch_deleted"]:
                entry["restore"] = "git -C '%s' branch '%s' %s" % (repo, now["branch"], now["tip"])
                print("        restore: " + entry["restore"])
            entries.append(entry)
        if touched and not args.dry_run:
            git(repo, "worktree", "prune")

    print("\n%s: %d   skipped: %d" % ("would remove" if args.dry_run else "removed",
                                      len(entries), skipped))
    if not args.dry_run:
        free_after = shutil.disk_usage(report["root"]).free
        print("free space: %s -> %s" % (human(free_before // 1024), human(free_after // 1024)))
        with open(log_path, "w") as handle:
            json.dump({"report": args.report, "removed": entries}, handle, indent=1)
        print("removal record: " + log_path)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p):
        p.add_argument("--protect", action="append", metavar="PATH",
                       help="never remove the worktree that contains PATH, for example the "
                            "folder another session works in (repeatable)")
        p.add_argument("--own-locks-finished", action="store_true",
                       help="treat locks held by the calling session as stale; only when no "
                            "subagent or background task of this session is still running")
        p.add_argument("--min-idle-hours", type=float, default=0,
                       help="count a worktree with git activity in the last N hours as busy")
        p.add_argument("--no-gh", action="store_true",
                       help="do not ask GitHub for merged pull requests")

    scan = sub.add_parser("scan", help="classify worktrees (read-only)")
    scan.add_argument("--root", default=".", help="folder that contains the repositories")
    scan.add_argument("--depth", type=int, default=4, help="how deep to look for repositories")
    scan.add_argument("--out", help="where to write the JSON report")
    scan.add_argument("--no-fetch", action="store_true", help="do not fetch origin first")
    scan.add_argument("--no-sizes", action="store_true", help="skip measuring folder sizes")
    scan.add_argument("--worktree-dir", action="append", metavar="DIR",
                      default=[os.path.join(".claude", "worktrees")],
                      help="repository-relative folder to check for leftover folders "
                           "without a registered worktree (repeatable)")
    common(scan)
    scan.set_defaults(func=cmd_scan)

    remove = sub.add_parser("remove", help="remove worktrees named by a scan report")
    remove.add_argument("--report", required=True)
    remove.add_argument("--classes", default="", help="comma list of done, missing")
    remove.add_argument("--include", action="append", metavar="PATH",
                        help="also remove this worktree: an unmerged one (its branch stays) or "
                             "a done one that holds ignored files found nowhere else (repeatable)")
    remove.add_argument("--log", help="where to write the removal record "
                                      "(default: next to the report)")
    remove.add_argument("--dry-run", action="store_true")
    common(remove)
    remove.set_defaults(func=cmd_remove)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
