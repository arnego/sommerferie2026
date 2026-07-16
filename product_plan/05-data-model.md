# 05 — Data Model

> **Purpose:** What data exists, who owns it, and how it relates. Two clearly separated domains:
> **user-owned data** (private by default, RLS-protected) and **shared/community data** (owner- or
> pipeline-written aggregates). Implements [03](03-functional-spec.md); enforced per
> [04 §3](04-architecture.md) and [07](07-auth-security.md).

---

## 1. Domain overview

```mermaid
flowchart LR
    subgraph U[User-owned - schema app]
        direction TB
        u1[accounts & profiles]
        u2[trips, stops, legs, activities]
        u3[checklists, budgets]
        u4[agent conversations & change-sets]
        u5[terms acceptances]
    end
    subgraph S[Shared - schema community + owner]
        direction TB
        s1[owner content: templates, country info, places]
        s2[aggregates: heatmap, usage stats]
        s3[ratings - contributed, anonymized]
    end
    U -- nightly anonymized aggregation --> s2
    U -- opt-in post-trip ratings --> s3
    s1 -- read by all users & agent --> U
```

Ownership rule: rows in the `app` schema always carry the owning `user_id` and are RLS-guarded to
that user. Rows in `community`/`owner` schemas contain **no user identifiers** (aggregates) or only
owner authorship (curated content); they are world-readable inside the product, and written only by
the aggregation jobs, the ratings endpoint (which strips identity), or the owner.

## 2. User-owned data (ER)

```mermaid
erDiagram
    USER ||--o{ TRIP : owns
    USER ||--|| TRIP_PROFILE_DEFAULTS : has
    USER ||--o{ TERMS_ACCEPTANCE : signed
    USER ||--o{ AGENT_CONVERSATION : has
    USER ||--|| ENTITLEMENT : has
    TRIP ||--o{ STOP : contains
    TRIP ||--|| TRIP_PROFILE : "interview answers"
    TRIP ||--o{ CHECKLIST : has
    TRIP ||--o{ BUDGET_ITEM : has
    TRIP ||--o{ AGENT_CHANGESET : modified_by
    STOP ||--o{ ACTIVITY : offers
    STOP ||--o| BOOKING : has
    STOP ||--o{ LEG : "arrives via"
    CHECKLIST ||--o{ CHECKLIST_ITEM : contains
    AGENT_CONVERSATION ||--o{ AGENT_MESSAGE : contains
    AGENT_CONVERSATION ||--o{ AGENT_CHANGESET : produced

    USER { uuid id PK
           text email
           text display_name
           timestamptz created_at }
    TERMS_ACCEPTANCE { uuid id PK
           uuid user_id FK
           text terms_version
           timestamptz accepted_at
           inet ip }
    TRIP { uuid id PK
           uuid user_id FK
           text title
           date start_date
           date end_date
           text status "draft|planning|traveling|done"
           text mode_override "auto|planning|travel" }
    TRIP_PROFILE { uuid trip_id PK
           jsonb travelers "ages, names optional"
           text vehicle "car|caravan|campervan|ev..."
           int max_drive_min_per_day
           jsonb interests
           text booking_style }
    STOP { uuid id PK
           uuid trip_id FK
           int position
           text name
           text country
           float lat
           float lng
           date arrival
           date departure
           text kind "campsite|ferry|visit|home"
           jsonb camping "name,address,url,phone,private notes: gate code, wifi"
           uuid place_id FK "optional link to owner PLACE" }
    LEG { uuid id PK
           uuid trip_id FK
           uuid to_stop_id FK
           int distance_km
           int est_minutes
           text verification "verified|unverified"
           text source }
    ACTIVITY { uuid id PK
           uuid stop_id FK
           text title
           text priority "must|nice"
           text url
           text url_verification "verified|unverified"
           jsonb booking "needed, ref, deadline" }
    BOOKING { uuid stop_id PK
           text status "none|requested|confirmed"
           text reference
           text notes }
    CHECKLIST { uuid id PK
           uuid trip_id FK
           text kind "packing|vehicle|predeparture|arrival|departure|custom"
           text title
           uuid template_id FK "origin template, nullable"
           text visibility_mode "planning|travel|both" }
    CHECKLIST_ITEM { uuid id PK
           uuid checklist_id FK
           text label
           text category
           bool checked
           timestamptz checked_at }
    BUDGET_ITEM { uuid id PK
           uuid trip_id FK
           text category
           int amount_nok
           text note }
    AGENT_CONVERSATION { uuid id PK
           uuid user_id FK
           uuid trip_id FK
           timestamptz started_at }
    AGENT_MESSAGE { uuid id PK
           uuid conversation_id FK
           text role "user|assistant|tool"
           jsonb content
           int tokens_in
           int tokens_out
           timestamptz at }
    AGENT_CHANGESET { uuid id PK
           uuid conversation_id FK
           uuid trip_id FK
           jsonb operations "list of tool ops"
           jsonb inverse "for undo"
           text status "applied|undone"
           int feedback "-1|0|1"
           timestamptz applied_at }
    ENTITLEMENT { uuid user_id PK
           text tier "free|premium"
           text stripe_customer_id
           text stripe_subscription_id
           text sub_status "active|past_due|canceled|none"
           timestamptz current_period_end
           int ai_msgs_used_this_period
           int ai_msg_quota }
```

Notes:
- `AGENT_CHANGESET.inverse` powers IT-7/AI-4 (visible diff + one-click undo) without full trip
  versioning in MVP.
- `LEG.verification` and `ACTIVITY.url_verification` make the agent's verification duty
  ([06 §4](06-ai-agent-spec.md)) a **data property the UI can render** (badge/asterisk), not just a
  process rule.
- Sensitive per-stop secrets (gate codes, Wi-Fi passwords) live inside the user's own `STOP.camping`
  jsonb — unlike sommerferie2026 they are per-user private rows, never in code (contrast:
  old repo's §6.4 private-repo exception).
- `ENTITLEMENT` is the single read model for tier gating; it is written only by Stripe webhook
  handlers and the quota accountant ([08](08-subscription-payments.md)).

## 3. Owner content (curated, world-readable)

```mermaid
erDiagram
    TEMPLATE_CHECKLIST ||--o{ TEMPLATE_ITEM : contains
    PLACE ||--o{ PLACE_LINK : has
    COUNTRY_INFO ||--o{ COUNTRY_FACT : contains

    TEMPLATE_CHECKLIST { uuid id PK
           text kind
           text title
           jsonb applicability "trip profile conditions: caravan, kids, ev" }
    TEMPLATE_ITEM { uuid id PK
           uuid template_id FK
           text label
           text category
           jsonb applicability }
    PLACE { uuid id PK
           text name
           text kind "campsite|attraction|ferry"
           text country
           float lat
           float lng
           text address
           text url
           text url_verification
           timestamptz last_verified_at }
    PLACE_LINK { uuid id PK
           uuid place_id FK
           text kind "booking|official|maps"
           text url
           text url_verification }
    COUNTRY_INFO { text country_code PK
           text name }
    COUNTRY_FACT { uuid id PK
           text country_code FK
           text kind "emergency|speed_limits|alcohol_limit|tolls|env_zones|tipping|camping_rules"
           jsonb data
           text source_url
           timestamptz last_verified_at }
```

`PLACE` is the shared registry the agent and community stats hang on: when two users camp at the
same site, both stops link the same `place_id` — that linkage (not user rows) feeds recommendations.
`COUNTRY_FACT` generalizes sommerferie2026's practical-info tables (emergency numbers, rig speed
limits, alcohol limits, tipping…) with per-fact source and verification timestamp (PR-1/PR-3).

## 4. Community aggregates (anonymized)

```mermaid
erDiagram
    DEST_HEAT { text geohash PK
           text month PK
           int trip_count "k-anonymity: published only if >= 5" }
    PLACE_STATS { uuid place_id PK
           int trips_used
           int nights_total
           float avg_rating
           int rating_count }
    RATING { uuid id PK
           uuid place_id FK
           int score "1-5"
           jsonb tags
           text trip_month "coarse time, no user id" }
```

Privacy rules (bind [07 §5](07-auth-security.md) and [11](11-legal-terms.md)):
1. Aggregation pipeline (nightly job) is the **only** reader of `app` data that writes to
   `community`; it strips all identifiers and coarsens location (geohash ~10 km) and time (month).
2. **k-anonymity ≥ 5**: heatmap cells and place stats are published only above the threshold.
3. Users can opt out (CM-5): their trips are excluded from the next pipeline run.
4. Ratings are voluntary, stored without user linkage beyond an internal dedup hash.

## 5. Migration & seed strategy

- Schema migrations are SQL files in the new repo (`db/migrations`, [14 §4](14-claude-setup.md)),
  applied via Supabase CLI; every migration PR-reviewed like code ([13](13-dev-workflow.md)).
- Seed data: owner templates converted from sommerferie2026's checklists, the 8 route countries'
  `COUNTRY_FACT`s, and ~15 verified `PLACE` rows from the 2026 trip — giving the agent and demo
  trip real, verified content on day one ([06 §7](06-ai-agent-spec.md)).

---

## Changelog

| Date | Change | By |
| --- | --- | --- |
| 2026-07-16 | Document created — user/owner/community domains, ER diagrams, verification-as-data, privacy rules, seed strategy | Claude + Arne |
