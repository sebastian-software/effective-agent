# German-language readings for technology authors

When writing for readers in Germany, choose a German lead from the material
at hand. An impatient observation, a buying decision, and a piece of news
about an unverified claim each give the opening sentence a different job.

## From a log entry to a story

Peter Linden's *Handbuch Stilsicher schreiben* takes the writer's position
seriously. Someone reporting a fault, someone explaining it, and someone who
designed the faulty system each have a different claim on the reader's
attention. Decide what the reader has come for before choosing the opening.
Linden also attends to the sound of the language. A narrator can change pace
without changing the difficulty of the subject.
[Duden on Linden's handbook](https://www.duden.de/presse/Wie-wirkt-Sprache-und-wie-setzt-man-sie-ein-%E2%80%9EHandbuch-stilsicher-schreiben%E2%80%9C-neu-bei-Duden)

Take a fictional service that runs a job whenever the Berlin clock reads
02:15. On the autumn clock change, its log shows two runs with different UTC
offsets, an hour apart. Here is an opening for readers who like a puzzle:

> Der Auftrag lief am Sonntag um 2.15 Uhr. Eine Stunde später lief er wieder.
> Es war immer noch 2.15 Uhr.

Give readers a moment with the two times. The next paragraph can put the two
offsets side by side. The scheduling condition now answers a question the
reader already has. For an operator who opened the page to decide what to
check, lead with the consequence instead: „Beim Zurückstellen der Uhr lief
unser Sonntagsjob zweimal. Im Protokoll unterscheiden sich die beiden Starts
nur am UTC-Offset.“ Both openings can carry the same evidence.

The Reporterfabrik workshop *Fesselnde Stories aus Akten* asks how to find
the people inside a pile of documents. In a reconstruction, a commit can
establish when the schedule changed. A ticket can show when someone noticed.
Only a comment or an interview might tell you why the author chose local
time. If all you have are two timestamps, they already make a good explainer.
If the author also recalls the moment they realized both log entries were
right, that realization could carry a personal essay. Let the account
determine how much of the story belongs to a person.
[Tina Kaiser and Marc Neller's workshop outline](https://akademie.reporterfabrik.org/courses/course-v1%3AReporterfabrik%2B379%2B2025/about)

## Give technical language some range

The NaWik's *ABC der guten Sprache* enlarges a speck of soot and a human hair
by the same factor until the reader can picture their proportions. A
comparison earns its space when the reader can use it to reason. For
instance, at one sample per minute, a monitor can miss a ten-second outage
entirely. Give it a clock: the service answers at 12:00, fails from 12:00:20
to 12:00:30, and answers again at 12:01. „Zwei grüne Punkte. Dazwischen war
der Dienst zehn Sekunden weg.“ For an operations audience the times do the
work. A broad audience may also need a sentence about what a sample is.
[NaWik's ABC](https://www.nawik.de/know-how-news/know-how-tipps/abc-der-guten-sprache/)

Use Wolf Schneider's *Deutsch für junge Profis* as a companion for the
sentence edit. Try the verbs at the point where the system promises
something. „Der Server hat den Auftrag angenommen“ and „Der Server hat den
Auftrag erledigt“ leave the customer in very different positions. In a
review, an adjective can be just as precise. A configuration dialog might
deserve *kapriziös* if changing the language also clears the saved printer.
Show the reader the vanishing printer. They can decide whether the word fits.
[Schneider's book and sample at Rowohlt](https://www.rowohlt.de/buch/wolf-schneider-deutsch-fuer-junge-profis-9783499626296)

## Leave room for the laugh

The Deutsche Journalisten-Akademie builds a *Glosse* from a missing paving
stone. Each imagined consequence takes the reader a little farther, until a
local nuisance has become a matter for the federal finance minister. For a
technical column, a real detail can sustain a much shorter excursion.
Suppose a team allows faults into production any day and ships fixes on
Fridays. An author who finds that arrangement absurd might write:

> Der Fehler hatte gegenüber seiner Korrektur einen organisatorischen
> Vorsprung. Er durfte jederzeit in Produktion.

The stiff *organisatorischen Vorsprung* briefly gives the bug the dignity of
an officeholder. Read the next sentence aloud. A gloss about the importance
of flexible release policies would explain the pleasure out of the line.
If the account calls for a sober judgment, „Der Fix lag seit Dienstag fertig
da. Freitags war Release.“ gives a reader plenty to think about, too.
[Deutsche Journalisten-Akademie on the Glosse](https://deutschejournalistenakademie.de/journalismus-lexikon/glosse/)

## ADAC

The Model 3 catalog entry pins down the exact variant, equipment, and scores.
Wolfgang Rudschies turns that material into a buyer's question in a separate
comparison. What would another 8,000 euros buy? More range, certainly. The
extra power is much harder to feel in everyday driving. His verdict gives
readers permission to keep their money. Jochen Wieler approaches range from
another direction. A shopper already knows how to compare two packages by
price per kilo. That familiar calculation makes euros per kilometer of rated
range intelligible. The official range supplies the denominator. A separate
ADAC winter test makes the distinction tangible: 702 kilometers on the
spec sheet, 423 under the conditions of that test.
[Model 3 catalog entry](https://www.adac.de/rund-ums-fahrzeug/autokatalog/marken-modelle/tesla/model-3/1generation-facelift/347729/) ·
[Base or premium?](https://www.adac.de/rund-ums-fahrzeug/autokatalog/marken-modelle/tesla/tesla-model-3-test/) ·
[Price per kilometer of range](https://www.adac.de/rund-ums-fahrzeug/elektromobilitaet/elektroauto/elektroautos-preis-reichweiten-verhaeltnis/) ·
[Model 3 winter test](https://www.adac.de/rund-ums-fahrzeug/elektromobilitaet/elektroauto/e-auto-reichweiten-test-im-winter/tesla-model-3-maximale-reichweite-hinterradantrieb-id-4950/)

For a hosting comparison, put the extra euros next to the job they buy. If
the expensive runner finished nine minutes earlier, did anyone get to go home
earlier? The answer can justify an opinionated subhead. Leave enough of the
test conditions beside the result for a team with a different workload.

## heise online

Two news headlines use small German verbs to make different promises.
In the Internet Archive story, *soll* looks ahead to a possible union. The
first paragraph reports the signatures already collected and names the person
who can act on them. In the Riemann story, *will … gefunden haben* assigns the
claim to the mathematician. The reader learns what was published, what a
proof assistant checks, and why specialists still have a question to settle.
The mathematical background comes after the reader knows why to care.
[Internet Archive](https://www.heise.de/news/Internet-Archive-soll-Gewerkschaft-bekommen-11533592.html) ·
[Riemann hypothesis](https://www.heise.de/news/Riemannsche-Vermutung-Anthropic-Mathematiker-will-KI-Beweis-gefunden-haben-11533452.html)

In Malte Kirchner's piece on AI and workload, the headline can state a
surprising result because the story soon gives it an address: researchers
followed work at one company over eight months. For a German engineering
article, choose the verb according to who knows what. „Der Anbieter verspricht
kürzere Builds“ can be followed by a result from the author's own repository
as soon as one exists. At that point a direct „Bei uns …“ moves the story on.
[AI and workload](https://www.heise.de/news/Studie-KI-macht-Arbeit-nicht-leichter-sondern-intensiver-11171221.html)

## WELT

Andreas Rosenfelder begins an argument about authorship with a brain in a vat.
The imaginary person can smell the morning air and joke with colleagues. By
the time the essay reaches the letters on a screen, the reader has already
experienced the problem of telling where a signal came from. Juleanna Glover's
guest essay gives journalism a sensory organ's job. The metaphor gets more
precise when she asks what each assignment takes. A model can read a
financial report. Interviewing the chief executive puts a reporter in a
position to judge the person behind it.
[Rosenfelder on authorship](https://www.welt.de/debatte/article6a2fb7897e682fc37fbfa796/politik-und-medien-die-ki-ist-nicht-der-tod-des-autors.html) ·
[Glover on reporting](https://www.welt.de/debatte/article69e4e8a4064e04c985e992b9/ki-wie-reporter-ploetzlich-zur-wichtigsten-ressource-der-tech-welt-werden.html)

Hanns-Georg Rodek can be tart about a documentary because he tells us what
appears on screen. Musk declines an interview. The filmmaker puts an avatar
in a chair and has it speak Musk's recorded words. Rodek makes a judgment
about that choice and gives the reader the scene needed to dispute it. For a
signed review, find the equivalent moment in the author's test. A demo that
quietly switches to a prepared result may deserve a sharp sentence. Describe
the switch precisely enough that someone watching could spot it too.
[Rodek's documentary review](https://www.welt.de/kultur/article6a9fab74181cb962d48877a0/entlarvende-dokumentation-der-elon-musk-schwindel.html)

## Frankfurter Allgemeine Zeitung

In a short media commentary, Sebastian Eder grants his opponent's larger
point and picks a fight with one premise about speed. A motionless progress
bar sets up a small test. Five minutes pass before the first sentence
appears. Even *gar nicht* in the headline sounds like someone answering
back. That's a register a technical columnist can use when the disagreement
is narrow enough to test in public.
[Eder on waiting for AI](https://www.faz.net/aktuell/feuilleton/medien-und-film/medienpolitik/florian-illies-und-chatgpt-wie-schnell-ist-ki-wirklich-201101826.html)

Hans-Heinrich Pardey spends thousands of kilometers with three touring
e-bikes. His final paragraph follows the batteries into the inn. Charge one
before dinner and another at bedtime. A third might mean setting an alarm.
In the separate Kaufkompass microphone guide, a pickup pattern becomes
audible once the reader knows where the keyboard sits. Both details tell us
what a specification costs someone. For a migration story, follow the
maintenance window just as far. Who has to be awake when it ends? If the
reporting supplies that answer, it may be your last line.
[Pardey, “Abgefahren” (print page hosted by Idworx)](https://www.idworx-bikes.de/wp-content/uploads/2018/05/F1805221.t01.pdf) ·
[Kaufkompass USB microphone test](https://www.faz.net/kaufkompass/test/das-beste-usb-mikrofon/)

## One German example in three registers

Suppose the author's build log shows that a cache cuts a repeat build from
nine minutes to two. The cache lives on the runner. The author's first build
on a fresh runner still took nine minutes.
These are original openings for different assignments.

- **Release news.** „Der zweite Build dauert bei uns jetzt zwei Minuten. Beim
  ersten bleibt es bei neun.“ *Bei uns* gives the measurement an owner.
- **Practical review.** „Wer für jeden Build einen frischen Runner startet,
  kann sich diesen Cache sparen.“ The reader can tell immediately whether
  the article applies to their setup.
- **Signed column.** „Sieben Minuten gespart, hieß es. Mein erster Build
  wusste davon offenbar nichts.“ This opening needs the author's own run and
  a real claim to push back on. The next line owes the reader the distinction
  between a cold cache and a warm one.
