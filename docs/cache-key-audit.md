# Audit guide: persisted data keyed by a volatile identifier

A portable guide for finding and fixing one specific, high-severity bug class. Written after fixing a live instance; every trap listed in §5 is one that actually bit, not a hypothetical.

This file is self-contained — drop it into any repo and point an agent at it. A ready-to-use prompt is in §7.

---

## 1. The pattern in one sentence

> **Cached data keyed by an identifier that can later be reassigned to different content.**

Two ingredients:

1. **State that outlives the process** — `localStorage`, `sessionStorage`, IndexedDB, `AsyncStorage`, a Redis key, a file on disk, a memoisation map that survives a route change.
2. **A volatile key** — an identifier that is a *label for a position*, not a property of the thing itself. Array indices, ordinals, hand-numbered ids, "step 3", row numbers, tab order.

When they meet, editing the underlying list doesn't invalidate the cache — it **re-points** it. Entry `16` was written for one thing and is now read as another.

### Why this class is worse than it looks

Most stale-cache bugs show up as **missing** data. This one shows up as **misattributed** data: a plausible-looking value under the wrong label. Nobody files a bug for weather that is merely *wrong by 200 km*, because it looks fine.

That asymmetry is the whole reason to hunt for it deliberately.

### The concrete instance (for pattern-matching)

A travel-planner app cached per-stop weather as `weather[stop.id]` in `localStorage` with a 1-hour TTL. A stop was split in two, which pushed every later stop's id up by one. Devices holding a <1h-old cache then had `weather[16]` = the *ferry's* forecast while stop 16 was now *a hotel 200 km away*:

- Dates only the hotel had → **blank** (visible, mildly annoying)
- The one date both had → **the ferry's weather displayed under the hotel's heading** (invisible, actually wrong)

---

## 2. How to find it — ranked by signal strength

### Signal 1 (strongest): a version constant that has been bumped more than once

```bash
git log -p --all -S"CACHE_VERSION" -- . | grep -E '^\+.*(VERSION|-v[0-9]|schema)'
git log --oneline --all | grep -iE 'bump|cache.?version|invalidate|force refresh'
```

Look for a constant like `CACHE_VERSION = 5`, `'myapp-data-v4'`, `SCHEMA = 3`.

**Every bump is a recorded instance of a human hitting this bug and papering over it.** A constant at v4 means it has been hit at least three times. The commit messages usually describe the symptom precisely — read them; they tell you which cache is affected and how it manifests.

If the bump commits say things like *"the shape didn't change so the loader couldn't tell old from new"* — that is this bug, verbatim.

### Signal 2: key construction from positional values

```bash
# keys built from ids / indices
grep -rnE '\[(.*\.)?(id|index|idx|i|position|order|key)\]\s*=' --include='*.{js,ts,jsx,tsx,py,rb,go}'
grep -rnE '(setItem|getItem|cache\[|store\[|\.set\(|\.get\()' --include='*.{js,ts,jsx,tsx}'

# the storage layer itself
grep -rn 'localStorage\|sessionStorage\|indexedDB\|AsyncStorage\|createCache\|memoize' --include='*.{js,ts,jsx,tsx}'
```

### Signal 3: the three questions

For each cache found, ask:

1. **What is the key derived from?**
2. **Can that value later point at different content?**
   Yes if it is an array position, an ordinal, a hand-assigned id, or anything renumbered when the list is edited. No if it is derived from the content itself (coordinates, a SKU, a URL, a content hash).
3. **When it does, does a read return _nothing_ or _something wrong_?**

Question 3 is the severity test. "Something wrong" = fix now. "Nothing" = fix when convenient.

---

## 3. The fix: key on intrinsic identity

Replace the volatile key with **the tuple that actually determines the value.** Ask: *what does this value physically depend on?*

| Cached thing | Volatile key (wrong) | Intrinsic key (right) |
|---|---|---|
| Weather forecast | `stop.id` | `(lat, lng, date)` |
| Price | `row index` | `(sku, currency, date)` |
| Translated string | `slot number` | `(locale, message_id)` |
| Rendered thumbnail | `upload order` | `(content_hash, width)` |
| Route/directions | `leg index` | `(origin, destination, mode)` |

Then **derive the key at read time from the object in hand**, never from a stored index:

```js
// before — the id decides what you get back
getEntry(stopId, date) { return this.cache[stopId]?.days.find(d => d.date === date); }

// after — the thing itself decides
entryKey(stop, date) { return `${round(stop.lat)},${round(stop.lng)}|${date}`; }
getEntry(stop, date)  { return this.cache[this.entryKey(stop, date)] ?? null; }
```

**The guarantee this buys:** a renumbering can now only ever produce a *miss* (blank, self-correcting on next fetch). It can no longer produce a *hit on the wrong record*. You have converted a silent correctness bug into a loud, harmless one.

Notes on constructing the key:

- **Quantise continuous components deliberately**, below the resolution of the underlying data. Coordinates rounded to 2 dp ≈ 1.1 km, while the weather model's own resolution is 1–11 km — so rounding cannot lose real information, and nearby entities correctly share one entry and one request.
- **Pick a delimiter that cannot occur in any component.** `|` is safe between a fixed-precision number and an ISO date; `-` and `,` are not.
- Beware `(-0.001).toFixed(2) === "-0.00"`, which is a different string from `"0.00"`.
- Coerce before formatting: `Number(x).toFixed(2)` — a string coordinate that used to flow straight into a URL will now throw.

---

## 4. Invalidation: fingerprint, not a version constant

Keying fixes *correctness*. You still need something to trigger a refetch when the inputs change, or new entries stay blank until the TTL expires.

**Do not add another manually-bumped constant.** That is the thing that already failed N times — it only catches *shape* changes, while the changes that actually keep happening are *data* changes (new dates, moved coordinates, a split record), which never alter the shape.

Instead store a **fingerprint of the inputs that determine what you need**:

```js
fingerprint() {
  const parts = this.targets().map(t => `${this.locKey(t)}:${t.start}:${t.end ?? ''}`);
  parts.sort();                              // stable across reordering
  parts.push(`cfg=${this.hours.join(',')}`); // config that shapes the stored record
  return parts.join('|');
}
```

Store it in the payload; on load, mismatch ⇒ treat the cache as empty.

Three rules that matter more than they look:

- **Exclude the volatile id from the fingerprint.** A pure renumbering doesn't change the data, so it must not trigger a refetch. Excluding it is the point, not an oversight.
- **Include config that shapes the stored record.** If the record stores hourly buckets `09/12/15/18/21` and someone adds `06`, every cached entry is *present but missing a column* — invisible to any presence-based check.
- **Record the fingerprint after the _attempt_, not after success.** See trap 5.1 — this is the difference between a working design and a refetch storm.

Keep a `schema` integer too, for genuine shape changes. It's cheap. Just don't mistake it for the mechanism that solves the recurring problem — it isn't.

---

## 5. Traps encountered during the real fix

These cost real debugging time. Skipping them produces a *worse* bug than the original.

### 5.1 Invalidation satisfied by outcome ⇒ refetch storm ⚠️ the big one

The tempting design is a **coverage check**: "if any needed key is missing from the cache, refetch."

It is satisfied by **outcome**. So any key that can never be filled — an API 4xx for one region, a date the provider omits, an off-by-one in a horizon calculation, an entity that leaks into the "needed" set but is excluded from fetching — makes coverage **permanently unsatisfiable**, and you refetch *everything on every single page load, forever*. The TTL is silently dead.

A fingerprint is satisfied by **attempt**: you record it after trying, so an unfillable key costs one retry on the next load, not one per load forever.

> Rule: **invalidation must be satisfiable by something entirely under your control.**

### 5.2 Reactive frameworks: early `return` skips dependency registration

Alpine, Vue, MobX, Solid and similar track dependencies by *observing which properties are actually read* during evaluation. A helper that returns before touching the reactive store registers **no dependency** — so when data arrives, that view never re-renders.

The refactor invites exactly this, because intrinsic keys encourage guard clauses:

```js
// BROKEN: on the pre-fetch pass this returns without ever reading this.cache,
// so the binding has no dependency and stays blank forever after data arrives.
getEntry(item, date) {
  if (!item?.lat) return null;
  return this.cache[key(item, date)];
}

// CORRECT: touch the reactive property before any early return.
getEntry(item, date) {
  const all = this.cache;
  if (!item?.lat) return null;
  return all[key(item, date)] ?? null;
}
```

Same trap in `list.some(...)` / `.find(...)` over a possibly-empty list — the callback never runs, so nothing is read. Make it an explicit invariant in the code and in your docs.

### 5.3 "Present but empty" and "absent" must stay distinguishable

Materialise an entry for every **requested** key, regardless of what the source returned. If you only store what came back, a provider that omits a date leaves a hole — indistinguishable from "never fetched", which feeds straight back into 5.1.

Correspondingly, test presence with `Object.prototype.hasOwnProperty.call(obj, k)`, not `if (obj[k])` — truthiness conflates "absent" with "stored a legitimate falsy value".

### 5.4 Merge + one timestamp = stale data that looks fresh

Flat maps make partial merging tempting: keep old entries, overlay what succeeded. But with a single top-level `fetchedAt`, one region that fails every time keeps its entries *present* while the timestamp is refreshed by its successful neighbours. Result: arbitrarily old data, presented as current, indefinitely.

That is the original bug displaced from space to time. Pick one:

- **Wholesale replace** (simplest — a failing region goes blank, which is honest), or
- **per-entry timestamps**, with staleness checked per entry.

### 5.5 Date arithmetic in milliseconds breaks across DST

`today.getTime() + 16 * 86400000` is 16×24h, but a calendar window containing a DST transition is not. Verified: 24 Oct 2026 in `Europe/Oslo` yields **8 Nov**, not 9 Nov.

Use calendar arithmetic — `new Date(y, m, d + 16)` — and compare `YYYY-MM-DD` strings. Harmless on its own; combined with 5.1 it becomes a permanent refetch loop.

### 5.6 Grouping widens ranges past API limits

Batching by intrinsic key is a real win (fewer requests). But a group's date span is the **union** of its members', so it is always ≥ any individual span and can exceed a provider's max-range limit — a 4xx that wipes out the whole group. Clip to the allowed window **when building the groups**, not after.

### 5.7 Derive "which entities need this" from one shared helper

Have exactly one `targets()` filter used by fetching, invalidation *and* any mock/fixture builder. Re-deriving the predicate at each site is how an entity ends up in the "needed" set but excluded from fetching → 5.1.

Watch for entities that look like valid targets but are excluded by one flag. In the real case, the "home" stop had perfectly good coordinates and dates and was excluded *only* by `isHome` — a filter written from scratch at a second call site would have included it and produced a permanently unfillable key.

### 5.8 Fixture/mock builders share the key scheme

Any mock-data path must produce the **same key shape**, or dev/demo mode silently renders nothing. Easy to miss because it isn't exercised by normal runs.

---

## 6. How to verify

Stub storage and network in a headless harness and assert behaviour, not implementation. The high-value cases, in rough priority order:

1. **Direct regression.** Two entities that previously shared a key now produce **different** keys for the same date; each resolves to its own data.
2. **Old cache rejected.** Write a payload in the *pre-fix* format, load, assert it is discarded rather than misread.
3. **No storm.** Two consecutive loads with no changes ⇒ exactly one round of fetches.
4. **Data change invalidates.** Change a date; assert a refetch, and that the new date resolves.
5. **Id change does _not_ invalidate.** Renumber every id; assert **zero** fetches and that data still resolves. This is the one that proves the volatile key is truly gone.
6. **Partial failure.** Make one request throw; assert the rest still populate and nothing crashes.
7. **Boundaries.** DST window edge; empty list; single-element range (`start === end`).

For a single-file front-end with no test runner, extracting the component factory and `new Function(...)`-ing it under Node with stubbed `localStorage`/`fetch` is enough to cover all of the above — no browser needed.

---

## 7. Prompt to hand to the agent

````text
Read docs/cache-key-audit.md, then audit THIS repository for the bug class it describes:
persisted data keyed by a volatile identifier (array index, ordinal, or hand-assigned id
that gets renumbered when the underlying list is edited).

Work in this order:

1. RECONNAISSANCE — do not change anything yet.
   - Search git history for a cache/schema version constant that has been bumped more
     than once. Read those commit messages; they usually name the affected cache and
     describe the symptom.
   - Inventory every cache that outlives a page load (localStorage, sessionStorage,
     IndexedDB, disk, long-lived module state).
   - For each, answer the three questions in §2: what is the key derived from, can that
     value later point at different content, and does a stale read then return NOTHING
     or SOMETHING WRONG?

2. REPORT before fixing. List each cache with its key, a verdict of
   safe / stale-blank / MISATTRIBUTES-DATA, and the reasoning. Rank by severity —
   misattribution first, since that is the silent one. Tell me which you propose to fix
   and wait for my go-ahead.

3. FIX the ones I approve, following §3 and §4: intrinsic key derived at read time,
   plus a fingerprint over the inputs that determine what is needed (excluding the
   volatile id, including any config that shapes the stored record).

4. Re-read §5 BEFORE you finish and confirm each trap explicitly. 5.1 (invalidation
   satisfied by outcome rather than attempt) and 5.2 (early return skipping reactive
   dependency registration) are the two that turn this fix into a worse bug than the
   original. Say which of the eight apply here and how you handled them.

5. VERIFY per §6. The load-bearing tests are: two previously-colliding entities now key
   differently; a pre-fix cache payload is rejected; two consecutive loads cause exactly
   one round of fetches; changing a date invalidates but renumbering ids does NOT.
   Show me the output.

Constraints: do not add another manually-bumped version constant as the primary fix —
that is the mechanism that already failed. If you conclude the repo does not have this
bug, say so plainly and show the evidence rather than inventing a fix.
````

---

## 8. The generalisation worth keeping

> **Cache keys should be derived from what the data _is_, not from where it currently sits.**
>
> Anything positional — an index, an ordinal, a hand-assigned id — is a label that can be reassigned. Intrinsic identity cannot. When they diverge, an intrinsic key degrades to a harmless miss; a positional key degrades to a confident lie.

The same reasoning applies well beyond caches: URL slugs, database foreign keys, filenames for generated artefacts, diff anchors, and idempotency keys all fail the same way when they encode position instead of identity.
