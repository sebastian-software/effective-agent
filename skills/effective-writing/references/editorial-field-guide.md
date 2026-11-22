# A field guide to technology articles

Use this shelf when a blog assignment would benefit from a sharper angle,
a better headline, or more room for the author's judgment. The notes compare
several pieces from each source and explain the choices in place. For routine
drafting, read the local section that fits the material. The article links are
for attribution and deeper reading. Technical claims in a new piece still
come from its own reporting.

## Find a useful neighbor

| What you have in hand | Where to look | What to look for |
| --- | --- | --- |
| A decision the author can defend, including a choice to stop | [Evil Martians](editorial-engineering-publications.md#evil-martians), [DHH](editorial-personal-publications.md#david-heinemeier-hansson) | Which observation made the other option untenable? How much of that verdict depends on this team's circumstances? |
| Something that behaved differently from your prediction | [Overreacted](editorial-personal-publications.md#overreacted), [Julia Evans](editorial-reviews-and-explanations.md#julia-evans) | Let the reader try the plausible explanation before introducing the detail that changes it. |
| A feature whose value depends on a reader's environment | [Josh W. Comeau, Piccalilli, and Kent C. Dodds](editorial-engineering-publications.md) | Look for a revealing change of conditions, a fallback, or a model with enough limits to guide a decision. |
| A small interface change, a physical interaction, or a visual artifact | [iA](editorial-product-publications.md#ia), [Daring Fireball and The Verge](editorial-reviews-and-explanations.md) | Follow a hand, a glance, or a window. What did the reader just see that a feature name would leave out? |
| Something you shipped that existing users must understand | [Tailwind and Vercel](editorial-product-publications.md), [Marco Arment](editorial-personal-publications.md#marco-arment) | Put the consequence for a returning user early. A rejected design or a removed feature may explain the release better than its longest feature list. |
| A recommendation between credible options | [Wirecutter and TechCrunch](editorial-reviews-and-explanations.md) | Who would reasonably choose differently? Which part did the writer use, and which is still a promise? |
| Several independent finds worth a reader's time | [Labnotes](editorial-personal-publications.md#labnotes-weekend-reading) | Keep the recognition of a recurring series. Give each item its own reason to click, including a reservation where useful. |
| A number the reader understands on paper but consistently misjudges | [Wait But Why](editorial-personal-publications.md#wait-but-why) | Keep the quantity fixed and change what the reader measures it against. |

For an article written in German, the [German-language readings](editorial-german-publications.md)
work through a clock change, a misleading measurement, and a dry aside
using German journalism handbooks. The same shelf compares ADAC tests,
heise news, WELT criticism, and F.A.Z. commentary.

For a reported feature, essay, or review, the
[American nonfiction readings](editorial-american-nonfiction.md) offer ways
to find a narrative in the reporting, make a technical discovery land at the
end of a sentence, and recognize a joke already present in the material.

The same writer can write an affectionate remembrance and a brisk release note.
Choose a particular editorial move for the current piece. A contributor's own
words, taste, and experiences supply the voice.

## One set of notes, four possible articles

Suppose the author supplies these notes: *Our importer used to wait until the
end of the file to report a duplicate. Yesterday it read all 80,000 rows to
tell me row 12 repeated row 4. I wanted my afternoon back. In the new preview,
it stops at the first duplicate and prints both row numbers. The old mode still
collects every error for overnight jobs.* The headlines and excerpts below
are original illustrations based on these fictional notes.

| Editorial choice | Possible title | What the reader is owed |
| --- | --- | --- |
| Explain the symptom | Why did the importer read 80,000 rows to report an error on row 12? | Walk one duplicate through detection and reporting. A reader should be able to predict the next run. |
| Tell the author's story | I wanted my afternoon back | Introduce the import immediately. Show how one irritating wait changed the author's opinion about a reasonable design. |
| Help someone choose | When should an import stop at the first error? | Give both users a seat at the table. A developer correcting a file at a desk and an unattended overnight job have different costs. |
| Announce a release | Import previews now stop at the first duplicate | Show the two row numbers the user needs and explain what happens to an existing batch job. |

The difference reaches beyond the headline. A personal opening can spend its
first breath on the absurdity: “Row 12 repeated row 4. The importer read the
remaining 79,988 rows before it broke the news to me.” A release can spend
those words on the reader's next action: “Run the file in preview mode. At
the first duplicate, the importer prints the two row numbers and stops.”
A comparative piece might open with the overnight operator: “If I'm going
to leave a job running overnight, I'd like the whole list of errors in the
morning.” That last line is a hypothetical user's reasoning. Attribute it
to a real person only if they actually said it.

The personal essay could end with the author's new appreciation for the old
mode. The release note could end as soon as a returning user knows how to keep
getting the full report. A tutorial could end with a tiny file the reader can
try. Each ending finishes a different job.

## Carry a choice into the prose

**Title and lead.** A reader seeing the headline in a feed has little context.
A blunt product name can work for a familiar device. A pun can work for an
unfamiliar one when the subtitle or opening names the subject. A question
works when the reader can imagine at least two answers and the body settles
something. Check the title against the finished piece: what would someone
reasonably click expecting to learn?

**Pace and emphasis.** Give the hard part space. Two sentences might cover the
release and ten paragraphs the decision behind it. A review can pause over a
small annoyance if it explains the verdict. A digest can keep a delightful
find to one line. Spend the reader's attention where it changes what they see.

**Combining approaches.** An engineering case study can open with the operator's
complaint, use a demonstration to explain the cause, and close with a bounded
recommendation. Use another approach where the material calls for it. The
existing publication voice and the author's account have precedence. Familiar
phrasing can stay when it does the work this piece needs.
