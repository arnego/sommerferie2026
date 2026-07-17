# 11 — Legal & Terms

> **Purpose:** Protect the owner from liability for bad planning, misleading or outdated
> information, AI-generated suggestions, and trips gone wrong — via Terms & Conditions every user
> must accept before using the service, plus supporting disclaimers and a privacy-policy outline.
>
> ⚠️ **STATUS: DRAFT — NOT LEGAL ADVICE.** Written by Claude as a working draft. A qualified
> lawyer (Norwegian consumer/IT law) must review before public launch — this is a Phase 2 gate
> ([10 §1](10-roadmap.md)).

---

## 1. Legal posture (what the product is, and is not)

The strongest protection is positioning, consistently expressed in product copy, marketing and
terms:

1. **An information and planning tool — not a travel agency.** We do not sell, arrange or broker
   travel, lodging, or activities; we are not part of any transaction between the user and
   campsites/attractions/ferries. This keeps the service outside package-travel regulation
   (pakkereiseloven) *(lawyer to confirm)* and outside payment flows for travel services.
2. **The user decides and verifies.** Plans are suggestions and organization aids; the user is
   responsible for verifying bookings, routes, prices, opening hours, and travel requirements
   before relying on them.
3. **AI output is clearly labeled assistance,** with visible verification status
   ([06 §4](06-ai-agent-spec.md)) — honesty in the UI supports the disclaimer in the terms.

## 2. Risk → protection map

| Risk scenario | Protection |
| --- | --- |
| Campsite full / closed despite plan; wrong opening hours or prices | Accuracy disclaimer (T&C §5); verification badges show data age/status; "verify before you go" copy at export/travel-mode entry |
| Route impassable, wrong distance/time, vehicle damage | Accuracy + routing disclaimer; caravan-profile routing is best-effort (T&C §5.3); user responsible for road/vehicle legality |
| AI suggests something unsuitable or unsafe | AI-content clause (T&C §6): assistance, may err, must be verified; not professional advice |
| Trip ruined, costs incurred, missed ferry | Limitation of liability (T&C §8): no liability for indirect/consequential loss; cap at 12 months' fees *(enforceability vs consumers — lawyer)* |
| Crowd-sourced recommendation is bad | UGC clause (T&C §7): community content is other users' opinion, not ours |
| User content lost | Service-availability clause (T&C §9): reasonable efforts, backups, but no guarantee; export tool provided |
| Charge disputes / refund demands | Subscription terms (T&C §10) + angrerett handling (§6 below) |
| User misuse (scraping, reselling, abuse of AI) | Acceptable-use clause (T&C §4), termination right |

## 3. Draft Terms & Conditions — structure and key clauses

Full text to be drafted in **English (binding)** — the product is Europe-first and English-first
(D-01/D-06); translations are courtesy versions. Note for the lawyer: under Rome I / the EU
Consumer Rights framework, mandatory consumer protections of the customer's country of residence
apply regardless of choice of law — the terms must acknowledge this. Structure and normative
content of each clause:

1. **Parties & definitions** — the service (working title, D-05), the operator (owner's entity —
   *decide sole proprietorship (ENK) vs AS before launch; AS recommended for liability isolation —
   lawyer/accountant question*), "Content", "AI Guide", "Community Content".
2. **The service** — description per §1 above, including the not-a-travel-agency clause and that
   the service may change.
3. **Account & eligibility** — 18+, accurate info, credential responsibility.
4. **Acceptable use** — personal, non-commercial; no scraping/reselling/abuse; no unlawful content;
   AI guide used for travel planning only.
5. **Information accuracy** — 5.1 all content (own, AI, community, third-party such as weather/FX/
   maps) is provided "as is" without warranty of accuracy or fitness; 5.2 user must verify all
   critical facts (bookings, prices, opening hours, routes, entry/vehicle requirements) with the
   provider/authority; 5.3 driving distances and times are estimates; road choice and vehicle
   compliance are the driver's responsibility.
6. **AI-generated content** — the AI Guide is an automated assistant; output may be incorrect,
   incomplete or outdated even when marked "verified"; it is not professional (legal, medical,
   safety, financial) advice; the user approves all changes to their plan (undo provided).
7. **Community content** — recommendations/ratings originate from other users; not endorsed by
   us; report function; we may remove content.
8. **Liability** — to the extent permitted by law: no liability for indirect or consequential
   losses (ruined vacations, missed transport, extra lodging costs, loss of enjoyment); total
   liability capped at the greater of amounts paid in the last 12 months or 500 NOK; **nothing
   limits liability for gross negligence, intent, or mandatory consumer rights** (this carve-out
   is what keeps the rest enforceable — lawyer to tune against forbrukerkjøpsloven/avtaleloven §36).
9. **Availability & data** — reasonable-efforts uptime, maintenance windows, backup, export tool;
   no compensation for downtime beyond mandatory rights.
10. **Trial, subscription, payment, renewal** — 7-day free trial terms (one trip, limited AI
    token allowance, no card required, lapse to read-only); subscription prices incl. applicable
    VAT; **AI token allowance terms**: tokens unlock per the paid plan (yearly grant vs monthly
    grants), are consumed by actual AI usage shown in the usage bar, stop the AI guide at zero,
    and are forfeited when the subscription ends (no cash value); auto-renewal with pre-renewal
    notice *(several EU markets are strict on auto-renewal transparency — lawyer)*; cancel any
    time effective at period end via self-service portal ([08 §4](08-subscription-payments.md));
    price-change notice ≥ 30 days before next renewal.
11. **Withdrawal right (angrerett)** — see §6 below.
12. **IP** — we own the platform/design/templates; user owns their trip content and grants us the
    license needed to operate the service + (unless opted out) to produce anonymized aggregates
    ([05 §4](05-data-model.md)).
13. **Termination** — user may delete account any time; we may suspend/terminate for breach with
    notice where required.
14. **Changes to terms** — versioned; material changes notified and re-accepted (§4 below);
    continued use after non-material changes constitutes acceptance.
15. **Governing law & venue** — Norwegian law; Forbrukertilsynet/Forbrukerklageutvalget and EU ODR
    references for consumers; courts of the operator's venue otherwise.

## 4. Acceptance mechanism (binds [07 §2](07-auth-security.md), [05 §2](05-data-model.md))

- Terms are **versioned** (`terms_version`, semantic date-based e.g. `2027-03-01`).
- Signup requires an explicit, **unchecked-by-default** checkbox: "Jeg har lest og godtar
  vilkårene (v…)" with the full text one click away; account creation is blocked without it.
- Acceptance stored as `TERMS_ACCEPTANCE(user, version, timestamp, ip)` — provable per user.
- **Material changes** (liability, price mechanics, data use): next login is gated by a
  re-acceptance screen summarizing the change; declining = read-only account + export offered.
  Non-material changes: banner notice only.
- The T&C are also permanently reachable from the landing page and app footer (LP-6).

## 5. Privacy policy (outline — full text with lawyer; operative rules in [07 §5](07-auth-security.md))

Controller identity; data categories (account, trip content, agent conversations, usage, billing
via Stripe); purposes & lawful bases; processors (Supabase, Vercel, Stripe, Anthropic, e-mail) and
transfer safeguards; retention periods; the anonymized-aggregates boundary and opt-out (CM-5);
data-subject rights incl. self-service export/deletion; cookies (essential only at launch);
contact & complaint route (Datatilsynet).

## 6. Consumer-law notes (Norway/EEA)

- **Withdrawal right:** 14-day withdrawal for distance purchase of digital services across the
  EEA (EU Consumer Rights Directive; angrerettloven is the Norwegian implementation). The 7-day
  card-free trial reduces practical exposure (customers try before paying). Standard approach: at
  checkout the user expressly consents to immediate delivery and acknowledges the withdrawal
  right is lost on full delivery / adjusted for partial use — exact mechanism (and refund of
  unused period as goodwill) **to be settled with the lawyer**; Stripe Checkout supports the
  consent text.
- **VAT:** B2C digital service sold Europe-wide from day one — **EU VAT via OSS (One Stop Shop)
  from launch**, charged at each customer's local rate through Stripe automatic tax; Norwegian
  MVA (25 %) for Norwegian customers; registration sequence is an accountant task before Phase 2.
- **Marketing:** markedsføringsloven — no dark patterns in subscription flows (cancel as easy as
  subscribe — the Stripe portal satisfies this); e-mail marketing requires consent.
- **Universal design (WCAG):** likestillings- og diskrimineringsloven/UU-tilsynet requirements for
  ICT aimed at consumers — NF-3 compliance also has a legal side *(confirm applicability — lawyer)*.

## 7. Lawyer review checklist (Phase 2 gate)

1. Entity choice (ENK vs AS) and its effect on the liability cap.
2. Enforceability of §8 cap and consequential-loss exclusion against consumers.
3. Package-travel-law non-applicability confirmation.
4. Angrerett mechanism wording at checkout.
5. Auto-renewal notice compliance.
6. AI-content clause vs coming EU AI-transparency duties (AI Act timeline for such assistants).
7. Privacy policy full text + DPA inventory.
8. UU/WCAG legal applicability.

---

## Changelog

| Date | Change | By |
| --- | --- | --- |
| 2026-07-17 | Europe-first ripple (D-06/D-07/D-08): binding T&C language changed to English with Rome I note; clause 10 extended with trial terms and AI token-allowance terms; withdrawal-right and VAT notes broadened from Norway to EEA-wide (OSS from launch) | Claude + Arne |
| 2026-07-16 | Document created — legal posture, risk map, draft T&C structure (15 clauses), versioned acceptance mechanism, privacy outline, Norwegian consumer-law notes, lawyer checklist. Marked DRAFT / not legal advice | Claude + Arne |
