const root = document.documentElement
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)")

const copyText = async (text) => {
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await Promise.race([
        navigator.clipboard.writeText(text),
        new Promise((_, reject) => {
          window.setTimeout(() => reject(new Error("Clipboard timed out")), 600)
        }),
      ])
      return
    } catch {
      // Continue with the selection-based fallback below.
    }
  }

  const textArea = document.createElement("textarea")
  textArea.value = text
  textArea.setAttribute("readonly", "")
  textArea.style.position = "fixed"
  textArea.style.opacity = "0"
  document.body.append(textArea)
  textArea.select()
  const copied = document.execCommand("copy")
  textArea.remove()

  if (!copied) {
    throw new Error("Copy command was rejected")
  }
}

const copyStatus = document.querySelector("[data-copy-status]")

for (const button of document.querySelectorAll("[data-copy-target]")) {
  const target = document.getElementById(button.dataset.copyTarget)
  const label = button.querySelector("[data-copy-label]")

  if (!target || !label) continue

  const originalLabel = label.textContent
  let resetTimer

  button.addEventListener("click", async () => {
    window.clearTimeout(resetTimer)

    try {
      await copyText(target.textContent.trim())
      label.textContent = "Copied"
      if (copyStatus) copyStatus.textContent = "Command copied to clipboard."
    } catch {
      label.textContent = "Select"
      window.getSelection()?.selectAllChildren(target)
      if (copyStatus) copyStatus.textContent = "Copy was unavailable. Command selected."
    }

    resetTimer = window.setTimeout(() => {
      label.textContent = originalLabel
    }, 1800)
  })
}

// Tab groups: arrow keys, Home, and End move between tabs; one panel is visible.
for (const group of document.querySelectorAll("[data-tabs]")) {
  const tabs = [...group.querySelectorAll('[role="tab"]')]

  const activate = (tab, moveFocus = false) => {
    for (const candidate of tabs) {
      const selected = candidate === tab
      candidate.setAttribute("aria-selected", String(selected))
      candidate.tabIndex = selected ? 0 : -1
      const panel = document.getElementById(candidate.getAttribute("aria-controls"))
      if (panel) panel.hidden = !selected
    }
    if (moveFocus) tab.focus()
  }

  for (const [index, tab] of tabs.entries()) {
    tab.addEventListener("click", () => activate(tab))
    tab.addEventListener("keydown", (event) => {
      let nextIndex

      if (event.key === "ArrowRight" || event.key === "ArrowDown") {
        nextIndex = (index + 1) % tabs.length
      } else if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
        nextIndex = (index - 1 + tabs.length) % tabs.length
      } else if (event.key === "Home") {
        nextIndex = 0
      } else if (event.key === "End") {
        nextIndex = tabs.length - 1
      } else {
        return
      }

      event.preventDefault()
      activate(tabs[nextIndex], true)
    })
  }
}

const revealElements = [...document.querySelectorAll(".reveal")]

if (!reduceMotion.matches && "IntersectionObserver" in window) {
  root.classList.add("reveal-ready")

  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue
        entry.target.classList.add("is-visible")
        observer.unobserve(entry.target)
      }
    },
    { rootMargin: "0px 0px -8%", threshold: 0.08 },
  )

  for (const element of revealElements) revealObserver.observe(element)
}

const header = document.querySelector("[data-header]")

const updateHeader = () => {
  header?.classList.toggle("is-scrolled", window.scrollY > 12)
}

updateHeader()
window.addEventListener("scroll", updateHeader, { passive: true })

const year = document.querySelector("[data-year]")
if (year) year.textContent = String(new Date().getFullYear())
