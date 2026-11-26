# Technical Concept Precision

These examples apply the
[precision pass](technical-subject-matter.md#run-a-precision-pass-on-concepts)
to a fictional German integration concept. Every name in it is invented. Each
"After" sentence restates a fact from the source concept below and adds none.
The rows illustrate decisions, not a template to copy.

## Source concept

Beispielwerk GmbH, a fictional customer, connects its own chat agent to the
fictional Musterhaus Suite through the suite's Model Context Protocol (MCP)
service. The MCP service exposes only the suite's contract-review module; no
other module is reachable through MCP. It calls only the backend endpoints of
that module that the backend's OpenAPI description documents.

Beispielwerk submits a data processing agreement (Auftragsverarbeitungsvertrag,
AVV) for review. The backend runs the pre-check on the submitted contract
version. The chat model relays the result and does not assess the AVV. The MCP
service calls the backend API on behalf of Beispielwerk's data protection
officer (Datenschutzbeauftragter, DSB), and the backend checks the DSB's
rights. The team has not decided how the MCP service transmits the DSB's
identity. The DSB reviews the pre-check result in the suite's web interface and
decides whether to accept the contract version.

AI suggestions expire after 24 hours. That expiry does not cover the stored
contract version. The retention period for the stored AVV is still to be set.

## Before and after

| Before | After | Why |
| --- | --- | --- |
| „Weitere Module über die Tür“ | „Kein MCP-Zugriff auf weitere Module.“ | Name the interface rather than a metaphor. |
| „Die Vorprüfung rechnet die Suite selbst.“ | „Das Backend prüft die vorgelegte Vertragsfassung. Das Chat-Modell bewertet den AVV nicht.“ | Name the responsible component and keep the negative scope. |
| „Fachaufrufe erfolgen im Auftrag des verbundenen DSB.“ | „Der MCP-Dienst ruft die API im Auftrag des DSB auf. Das Backend prüft dessen Rechte. Wie der Dienst die DSB-Identität übermittelt, ist offen.“ | Separate the actor, the authorization decision, and the unresolved mechanism. |
| „Die Vertragsfassung bleibt dauerhaft in der Ablage.“ | „Die 24-Stunden-Frist gilt für KI-Vorschläge, nicht für die abgelegte Vertragsfassung. Die Aufbewahrungsfrist des AVV ist separat festzulegen.“ | Avoid turning a scoped expiry rule into an unsupported retention claim. |

The third row calls the mechanism open because the source says it is
undecided. If the source were silent on it, the pass would keep the sentence's
claim and ask the author instead.

The fourth row is not legal advice. It proposes no retention period; the period
stays with the author and the source that will set it.

## Leave precise text unchanged

This sentence already names the actor, the interface, and the decision owner,
and it keeps the terms AVV, MCP, and OpenAPI:

> Der MCP-Dienst ruft nur die Endpunkte des Prüfmoduls auf, die in der
> OpenAPI-Beschreibung des Backends dokumentiert sind. Das Backend prüft die
> vorgelegte Fassung des AVV; über die Annahme entscheidet der DSB in der
> Weboberfläche.

The pass leaves it as written.
