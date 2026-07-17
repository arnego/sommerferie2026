# 14 — Claude Project Setup (new repo, CLAUDE.md, structure)

> **Purpose:** Instructions for bootstrapping the new product repo so Claude is maximally
> effective from commit one: the repository structure, what belongs in the project's CLAUDE.md
> (with a ready-to-use draft), and the recommended `.claude/` extras.

---

## 1. Scope rule: two kinds of Claude rules

- **Developer-facing rules** (how to build, test, commit) → CLAUDE.md in the repo root.
- **The travel agent's working rules** (URL verification, distance verification, own-trip scope,
  citing sources) → **[06 — AI Agent Spec](06-ai-agent-spec.md)**, implemented as the agent's
  system prompt and tool guards in `agent/`. CLAUDE.md does **not** restate them; it points to 06
  as the source of truth for agent behavior. This keeps one authority per rule and lets agent
  rules evolve without touching developer docs.

## 2. Repository structure

Annotated tree for the new repo (Next.js App Router per [04](04-architecture.md)); create it in
this shape from day one:

```
roamly/                          # name per D-05 (working title)
├── CLAUDE.md                    # §3 below — developer rules, command map, doc pointers
├── README.md                    # human quickstart: what, stack, how to run
├── .env.example                 # every env var, no values (13 §6)
├── package.json
├── next.config.ts / tsconfig.json / tailwind.config.ts
├── src/
│   ├── app/                     # Next.js routes
│   │   ├── (marketing)/         # landing, pricing, terms, privacy (public, SSR)
│   │   ├── (app)/               # authenticated shell: trips/[id]/{map,plan,checklists,budget,info}
│   │   ├── api/                 # route handlers: trips, agent (SSE), stripe/webhook, export
│   │   └── auth/                # signup/login/reset/accept-terms
│   ├── components/              # React components; mirrors design-system/ components 1:1
│   ├── lib/                     # domain logic (pure, unit-testable):
│   │   │                        #   legs.ts (distance/time, ÷73 rule), dates.ts, tokens.ts,
│   │   │                        #   entitlements.ts, weather.ts, fx.ts, i18n/
│   │   └── db/                  # typed queries, RLS-aware client helpers
│   └── styles/                  # tokens.css generated from design-system/tokens
├── agent/                       # AI travel guide (implements product_plan 06)
│   ├── system-prompt.md         # the agent constitution (06 §4) — versioned prose
│   ├── tools/                   # one file per tool: schema + handler + guard
│   ├── runtime.ts               # tool-runner loop, streaming, change-sets, token-budget gate
│   └── fixtures/                # recorded tool-call fixtures for tests (12 §2)
├── db/
│   ├── migrations/              # numbered SQL, RLS policy in same file as table (07 §4)
│   └── seed/                    # owner templates, country facts, PLACE rows, demo trip (05 §5)
├── tests/
│   ├── unit/                    # Vitest
│   ├── integration/             # API + RLS + webhooks vs local Supabase
│   └── e2e/                     # Playwright specs + fixtures
├── docs/
│   ├── product_plan/            # THIS spec set, copied over — living documents with changelogs
│   └── decisions.md             # continuation of the decision log (00 §4)
├── design-system/               # moved from product_plan/design-system; synced to Claude Design
├── scripts/                     # dev-stack up/down, seed, canary runner
├── public/                      # static assets, photos, icons
├── .github/workflows/           # ci.yml, claude.yml, claude-code-review.yml, nightly.yml (13 §5)
└── .claude/
    ├── settings.json            # permissions (test/lint/dev-server allowed), env
    ├── skills/verify/           # project verify skill (12 §5)
    └── plans/                   # plan-mode outputs (gitignored ok)
```

**What-goes-where rule:** UI in `src/app`+`src/components`; anything with business meaning and no
JSX in `src/lib` (unit-testable); everything the agent is or does in `agent/`; schema truth in
`db/migrations`; product truth in `docs/product_plan`. If a change spans layers, the PR is
probably too big ([13 §2](13-dev-workflow.md)).

## 3. CLAUDE.md — content requirements

The new CLAUDE.md must contain (and little else — link, don't duplicate):

1. **Project overview** (3 lines) + pointer: *"the spec set in `docs/product_plan/` is the source
   of truth; 00-overview.md is the index."*
2. **Command map:** dev stack up, test suites, lint/typecheck, db migrate/seed, stripe-cli
   webhook forwarding, canary.
3. **Doc discipline:** every functional change updates the relevant spec doc's changelog;
   decisions go to `docs/decisions.md`.
4. **Workflow rules:** the Claude loop from [13 §3](13-dev-workflow.md) (plan mode → implement →
   verify → /code-review → PR); commit/push allowed on feature branches, never to `main`.
5. **Verification duty:** run the `verify` skill + CI command set before committing UI/flow
   changes ([12 §5](12-testing-verification.md)).
6. **Agent-behavior pointer:** *"Rules for the AI travel guide live in
   `docs/product_plan/06-ai-agent-spec.md` and are implemented in `agent/system-prompt.md` —
   change them there, never inline elsewhere."*
7. **Secrets rule:** never write credentials into the repo; `.env.example` only ([13 §6](13-dev-workflow.md)).
8. **Language rule:** code/identifiers/commits in English; UI copy English-first via i18n files.

## 4. Draft CLAUDE.md (appendix — ready to copy into the new repo)

```markdown
# CLAUDE.md

## Project
Roamly (working title): online vacation & road-trip planning service — Next.js +
Supabase + Stripe + Claude API. The specification set in `docs/product_plan/` is the
source of truth; start at `docs/product_plan/00-overview.md`. Product decisions live in
`docs/decisions.md`.

## Commands
- `npm run dev` — app + local Supabase (`scripts/dev-up.sh` starts db, seeds)
- `npm run test` / `test:unit` / `test:integration` / `test:e2e`
- `npm run lint && npm run typecheck` — must be clean before any commit
- `npm run db:migrate` / `db:seed`
- `npm run stripe:listen` — forward test-mode webhooks
- `/verify` — project skill: exercise the changed flow in Chromium before committing

## Workflow
- Plan mode for nontrivial work; implement on `claude/<topic>` branches; small PRs.
- Before committing: lint + typecheck + relevant tests + `/verify` for UI/flow changes.
- Run `/code-review` before pushing. Never push to `main`; owner merges PRs.
- Conventional commits (`feat:`, `fix:`, `docs:` …), imperative subject.
- Every functional change updates the matching spec in `docs/product_plan/` including its
  changelog table, in the same PR.

## Rules
- **Agent behavior:** the AI travel guide's rules (URL/distance verification, own-trip
  scope, citations) are defined in `docs/product_plan/06-ai-agent-spec.md` and implemented
  in `agent/system-prompt.md` + tool guards. Change them there only.
- **Secrets:** never in code, docs, or fixtures. `.env.example` documents variables.
  User secrets (gate codes, booking refs) are per-user DB data, never in the repo.
- **Data access:** every new `app.*` table ships RLS policies in the same migration.
- **Language:** code, identifiers and commits in English; user-facing English-first copy
  through `src/lib/i18n/`.
- **UI:** design tokens from `design-system/tokens` only — no ad-hoc colors/fonts.
  WCAG 2.1 AA; no emoji in product UI.
```

## 5. `.claude/` extras

- **settings.json:** allow `npm run *`, `npx vitest*`, `npx playwright*`, `supabase *`,
  `stripe listen*` without prompts; deny network-mutating commands beyond those; set
  `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`.
- **skills/verify:** per [12 §5](12-testing-verification.md) — boot stack, drive the changed flow,
  screenshot at 375/768/1280, report console errors.
- **Optional skills** as the repo matures: `db-migration` (expand-migrate-contract checklist),
  `release` (tag + notes).
- **Bootstrap task list** (first session in the new repo): scaffold per §2 → commit → wire CI →
  copy `docs/product_plan` → seed db → hello-world page deployed → Phase 0 exit
  ([10 §1](10-roadmap.md)).

---

## Changelog

| Date | Change | By |
| --- | --- | --- |
| 2026-07-17 | Renamed to Roamly (D-05); language rules English-first (D-01); quota.ts → tokens.ts and token-budget gate in the repo tree (D-08) | Claude + Arne |
| 2026-07-16 | Document created — rule-scope split (dev vs agent), annotated repo tree, CLAUDE.md content requirements + ready-to-use draft, .claude extras and bootstrap list | Claude + Arne |
