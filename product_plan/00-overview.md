# 00 — Overview: Specification Set for "Roamly" (working title)

> **Purpose:** Entry point for the complete specification set of the online vacation & road-trip
> planning service. Explains how the documents fit together, the conventions they follow, and the
> decisions taken so far. Start here.

---

## 1. The product in one paragraph

An online service where families plan road trips and vacations the way the sommerferie2026 site
worked for one family — interactive route map, day-by-day itinerary, checklists, budget, weather,
practical info — but as a multi-user product. Each user builds their own trip assisted by an
**AI travel guide** (Claude API) that researches, suggests and edits the plan through conversation.
Crowd-sourced community data (destination heatmap, campsite and activity recommendations) makes
every plan better. The owner (Arne) controls structure and design; users fill in their own content.
Revenue comes from subscriptions.

## 2. Document map

| Doc | Title | Answers |
| --- | --- | --- |
| [01](01-product-vision.md) | Product vision | Why build this, for whom, how it makes money |
| [02](02-user-journeys.md) | User journeys | Who the users are and how they move through the product |
| [03](03-functional-spec.md) | Functional specification | What the product does, feature by feature, phase by phase |
| [04](04-architecture.md) | Architecture | How the system is built, which stack and why |
| [05](05-data-model.md) | Data model | What data exists, who owns it, how it relates |
| [06](06-ai-agent-spec.md) | AI travel agent | What the AI guide can do, its tools, rules and guardrails |
| [07](07-auth-security.md) | Auth & security | How users sign up/in, authorization, GDPR |
| [08](08-subscription-payments.md) | Subscription & payments | Tiers, Stripe integration, billing lifecycle |
| [09](09-ux-design-spec.md) | UX & design | Desktop and mobile layouts, design tokens, components |
| [10](10-roadmap.md) | Roadmap | Build order, MVP cut, risks |
| [11](11-legal-terms.md) | Legal & terms | Liability protection, draft T&C, acceptance mechanism |
| [12](12-testing-verification.md) | Testing & verification | Test strategy, CI, automatic verification |
| [13](13-dev-workflow.md) | Development workflow | Git/GitHub practice for building with Claude |
| [14](14-claude-setup.md) | Claude project setup | New repo structure and the new project's CLAUDE.md |

Reading order for a newcomer: 01 → 02 → 03, then 04/05/06 for the technical core, the rest by need.
Dependency order (a change upstream may ripple down): 01 → 02 → 03 → 04 → 05 → {06, 07, 08} → 09 → 10;
11–14 hang off the whole set.

The `design-system/` folder holds the HTML component library that is synced to the Claude Design
project (see [09](09-ux-design-spec.md) §6).

## 3. Document conventions

All specification documents in this folder follow these rules:

1. **Language:** English prose. The product UI is English-first (D-01); UI copy examples in the
   specs and design system are therefore English.
2. **Numbered sections** (`## 1.`, `### 1.1`) so requirements can be referenced as `03 §2.4`.
3. **Changelog table** at the bottom of every document (`| Date | Change | By |`), newest first —
   same discipline as `docs/Teknisk-spesifikasjon.md` in this repo.
4. **Decision callouts:** open questions for the product owner are marked in place as
   > **Decision needed:** question — *working assumption: X*
   and mirrored in the decision log below. The working assumption applies until overridden.
5. **Phase tags:** every feature/requirement in [03](03-functional-spec.md) carries exactly one tag:
   `[MVP]`, `[v1.x]` or `[Later]`.
6. **Cross-references** are relative markdown links to the sibling doc (optionally with a section,
   e.g. `[05 §3](05-data-model.md)`).
7. **Mermaid diagrams** are used wherever a picture beats prose:
   `flowchart` (flows, pipelines), `sequenceDiagram` (auth/payment/agent exchanges),
   `erDiagram` (data model), `stateDiagram-v2` (subscription lifecycle), `journey` (user journeys),
   `C4Context`/`C4Container` (architecture), `gantt` (roadmap). Keep diagrams renderable by
   standard mermaid (GitHub-flavored) — no experimental syntax.
8. **Verified facts only:** external URLs and factual claims (pricing of third-party services,
   legal thresholds) must be verified against live sources before being stated as fact, or
   explicitly marked *(unverified)*. This carries over the sommerferie2026 URL-verification rule
   to the spec work itself.

## 4. Decision log

Decisions D-01…D-08 were first taken as recommended defaults, then reviewed by the product owner on
2026-07-17. All are now **confirmed** in the form below; any later change is recorded here and
rippled to the affected docs.

| ID | Decision | Status | Where used |
| --- | --- | --- | --- |
| D-01 | Spec language is **English**, and the product UI is **English-first** (other languages via the i18n layer later) | Confirmed 2026-07-17 | All docs |
| D-02 | Specs **prescribe a concrete stack**, argued in [04](04-architecture.md) | Confirmed 2026-07-17 | 04, 05, 12, 13, 14 |
| D-03 | **Phased scope with explicit MVP cut**, delivered as **several tagged internal releases (v0.x) of testable increments before the public MVP release v1.0.0** | Confirmed 2026-07-17 | 03, 10, 13 |
| D-04 | **Evolve the sommerferie2026 visual identity** (petrol/sand/sunshine, Playfair + Inter) | Confirmed 2026-07-17 | 09, design-system/ |
| D-05 | Working name **"Roamly"** (working title only; note: collides with an existing US RV-insurance brand at roamly.com — trademark/domain check before public launch is a [10](10-roadmap.md) gate) | Confirmed 2026-07-17 | All docs |
| D-06 | **Europe-first launch**: the product addresses travel across the whole pan-European continent from day one; Norway alone is too small a market | Confirmed 2026-07-17 | 01, 02, 03, 08, 11 |
| D-07 | **7-day free trial + one paid subscription** ≈ 99 NOK (~€9)/mo or 799 NOK (~€70)/yr; no permanent free tier | Confirmed 2026-07-17 | 01, 03, 08 |
| D-08 | **AI usage metered as token budgets** (owner-side cost control): small fixed trial budget; subscription budget that **unlocks in proportion to the amount paid** (yearly-upfront → large immediate grant; monthly → smaller monthly grants); visible usage bar; hard stop at zero; budget sizes finalized only after token-usage-per-message data is collected in the v0.x releases; a behind-the-scenes **model-evaluation router** to stretch tokens is a later roadmap feature | Confirmed 2026-07-17 | 03, 05, 06, 08, 10 |

## 5. Glossary

| Term | Meaning |
| --- | --- |
| **Trip** | One user's plan for one vacation: ordered stops with dates, activities, checklists, budget |
| **Stop** | A location within a trip (campsite, ferry, family visit, home) with arrival/departure dates |
| **Activity** | Something to do at or near a stop; can be must-do or nice-to-have |
| **AI travel agent / guide** | The Claude-powered assistant that researches and edits the user's trip through conversation and tools |
| **Planning mode / Travel mode** | The two UI modes inherited from sommerferie2026: preparing at home vs. on the road |
| **Community data** | Anonymized, aggregated cross-user data: destination heatmap, campsite/activity recommendations, ratings |
| **Owner content** | Structure, templates, design and curated seed content controlled by the product owner |
| **User content** | Everything a user enters or the agent creates on their behalf — private by default |
| **MVP** | The smallest publicly releasable product (v1.0.0): landing + auth + trip planner + AI guide, preceded by tagged internal v0.x increments (see [10](10-roadmap.md)) |
| **Token budget** | The metered allowance of AI usage (input+output tokens) a trial or subscription unlocks; tracked by the usage bar, hard stop at zero (D-08) |

## 6. Relationship to the sommerferie2026 repo

This spec set lives in the sommerferie2026 repo (folder `product_plan/`) because the product idea
grew out of it, but it describes a **new, separate product and repo** (see [14](14-claude-setup.md)).
The sommerferie2026 site (`index.html`, `docs/`) is untouched and continues to serve the 2026 trip.
It serves the new product in three ways: as the **feature baseline** (03), as the **design origin**
(09), and as a **development-history corpus** the AI agent spec mines for travel-consultant
know-how (06 §7).

---

## Changelog

| Date | Change | By |
| --- | --- | --- |
| 2026-07-17 | Owner review of the decision log: D-01 English-first UI; D-03 internal v0.x releases before public v1.0.0; D-05 working name "Roamly"; D-06 Europe-first launch; D-07 7-day trial + single subscription; D-08 token budgets with paid-proportional unlock, usage bar, hard stop, and later model-router. All decisions marked Confirmed; glossary + language convention updated | Claude + Arne |
| 2026-07-16 | Document created — document map, conventions, decision log D-01…D-08, glossary | Claude + Arne |
