# 01 — Product Vision

> **Purpose:** Why this product should exist, for whom, what makes it different, and how it makes
> money. Everything downstream (features, architecture, design) must trace back to this document.

---

## 1. Background

In 2026 the Goderstad family planned a 29-day caravan road trip from Kongsberg to Croatia and back
using a single-page website built and continuously updated by Claude (the sommerferie2026 repo).
The experience showed something repeatable: an AI acting as a **travel consultant** — researching
campsites, verifying URLs and driving distances, curating activities per stop, generating
checklists, tracking bookings, pulling live weather and currency — combined with a **map-centric,
mode-aware website** produced a plan of a quality that normally takes weeks of evenings to build.

The product generalizes this: the same structure and quality, but every family builds **their own**
trip, assisted by the same kind of AI travel guide, on a platform the owner designs and controls.

## 2. Vision statement

> **Every family gets the trip plan a professional travel consultant would build — by having a
> conversation, on a site that works at the kitchen table and in the passenger seat.**

## 3. Target users

Primary launch market: **Norway** (D-06), expanding to the Nordics and Europe later.

| Segment | Description | Priority |
| --- | --- | --- |
| **Caravan/campervan families** | Families with children touring Europe by car with caravan, campervan or roof tent. Plan for weeks, need per-stop detail, checklists, practical info. | Primary |
| **Road-trip couples** | No children, more spontaneous, shorter horizon, care about routes and experiences over logistics. | Secondary |
| **Cabin-and-day-trip planners** | Domestic vacations with a base and day excursions. Lighter use of routing, heavy use of activities. | Later |

Anti-target (for now): business travel, flight-based itineraries, group tours.

## 4. Problem

1. **Planning is scattered.** Routes in Google Maps, campsites in ADAC/park4night tabs, bookings in
   e-mail, checklists in notes apps, budget in a spreadsheet. Nothing is connected.
2. **Research is slow and unreliable.** Finding family-fit campsites and activities per stop takes
   evenings; distances and opening info are often wrong or stale.
3. **Generic tools stop at the route.** Existing road-trip planners draw the line on the map but
   don't carry the family through preparation (checklists, budget, documents) and the trip itself
   (today's plan, arrival/departure routines, practical info per country).
4. **Plans go stale.** A plan made in March needs to adapt in July; nobody updates seventeen
   documents from a campsite. A conversational agent can.

## 5. Value proposition and differentiation

**One connected plan, built by conversation, useful before and during the trip.**

| Differentiator | Details |
| --- | --- |
| **AI travel agent that edits the plan** | Not a chatbot beside the product — an agent with tools that reads and writes the user's actual trip: adds stops, verifies distances and URLs, curates activities, fills checklists. See [06](06-ai-agent-spec.md). |
| **Whole-journey scope** | Planning mode (research, booking status, budget, packing) and travel mode (today's plan, next leg, arrival/departure checklists, country info) in one product — proven structure from sommerferie2026. |
| **Verified information culture** | The agent must verify URLs and distances against live sources and mark what it couldn't verify — a trust feature competitors lack ([06 §4](06-ai-agent-spec.md)). |
| **Community-informed** | Aggregated heatmap of where users travel, campsite and activity recommendations sourced from real user plans and ratings ([03 §7](03-functional-spec.md)). |
| **Owner-curated structure** | The owner controls layout, templates and quality bars; users control content. Keeps every plan legible and every feature coherent. |

Competitive landscape (qualitative; detailed teardown is a roadmap task, [10](10-roadmap.md)):
**Roadtrippers** (US-centric route planning, weak on camping logistics and no plan-editing agent),
**Wanderlog** (strong itinerary collaboration, generic AI suggestions, not caravan-focused),
**The Dyrt / park4night / PiNCAMP** (campsite discovery, not end-to-end trip planning),
**ADAC Trips** (German market, editorial content, no personal AI). None combine an agent that
*edits* the plan, caravan-family focus, and the planning/travel dual mode.

## 6. Business model

Subscription SaaS (D-07):

| Tier | Price (working numbers) | Includes |
| --- | --- | --- |
| **Free** | 0 | 1 trip, core planner, ~20 AI messages/month, community data read-only |
| **Premium** | ≈ 99 NOK/mo or 799 NOK/yr | Unlimited trips, full AI guide (~500 msgs/mo fair use), contributing + full community features, offline/PDF export (v1.x) |

> **Decision needed:** confirm tier structure and price points before implementing payments —
> *working assumption: the table above (D-07). Alternatives considered: trial-then-paid,
> two paid tiers, seasonal pass (249 NOK / 3 months) — the seasonal pass fits vacation rhythm and
> is kept as a candidate add-on in [08](08-subscription-payments.md).*

Unit economics guardrail: AI cost per premium user must stay well under subscription revenue; the
message quota (D-08) plus model routing keeps worst-case API cost bounded — modeled in
[06 §8](06-ai-agent-spec.md).

## 7. Success metrics

| Horizon | Metric | Target (working) |
| --- | --- | --- |
| MVP (first season) | Registered users | 500 |
| | Free → Premium conversion | ≥ 4 % |
| | Trips that reach "travel mode" (actually used on the road) | ≥ 30 % of created trips |
| | AI guide satisfaction (thumbs up on agent edits) | ≥ 80 % positive |
| v1.x | Monthly churn (premium) | ≤ 3 % |
| | Community: share of stops with ≥ 1 community recommendation | ≥ 50 % for top-100 destinations |

## 8. Guiding principles

1. **The plan is the product.** Every feature must make the user's plan better, faster or more
   trustworthy; chrome that doesn't serve the plan is cut.
2. **Show little, allow deep.** Inherited from sommerferie2026: compact overview first, detail on
   demand (accordions, popups, modes).
3. **Trust through verification.** Never present unverified facts as facts — the agent marks them.
4. **Desktop plans, mobile travels.** Desktop is the planning workbench (use the real estate);
   mobile is the on-the-road companion mirroring the proven sommerferie2026 single-column structure.
5. **Private by default.** User content is private; community data is aggregated and anonymized,
   opt-out available ([05 §4](05-data-model.md), [07](07-auth-security.md)).

---

## Changelog

| Date | Change | By |
| --- | --- | --- |
| 2026-07-16 | Document created — vision, targets, problem, differentiation, business model (D-06/07/08), metrics, principles | Claude + Arne |
