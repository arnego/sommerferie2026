# Implementasjonsplan: Sommerferie 2026 webside

## Kontekst

Eksisterende `index.html` er ufullstendig og bruker feil tech stack. **Fullstendig omskriving fra scratch** — ingenting gjenbrukes fra eksisterende fil.

Prosjektet starter med at Claude som reisekonsulent utarbeider et initielt ruteforslag basert på kriteriene i spesifikasjonen (seksjon 2.2) og de grove innspillene (seksjon 2.3). Dette forslaget oppdateres direkte i spesifikasjonens kapittel 2.3 og brukes som innhold i websiden.

---

## Gjenopprettingsinstruksjoner

Hver fase markeres med status etter fullføring i denne planen (se "Fasestatus" nederst). Dersom Claude blir avbrutt, les fasetatus for å forstå hvor arbeidet stoppet, og fortsett derfra. Alle endringer committes etter hver fullført fase.

---

## Teknisk arkitektur

### CDN-biblioteker (i `<head>`)
- Tailwind CSS play-cdn (`cdn.tailwindcss.com`)
- Alpine.js 3.x (`cdn.jsdelivr.net`, defer)
- Leaflet.js 1.9 CSS + JS (`unpkg.com`)
- Google Fonts: Playfair Display + Inter

### Tailwind-konfigurasjon
Utvid tema med spesifikasjonens fargepalett i en `<script>` blokk:

| Rolle | Variabel | Hex |
|-------|----------|-----|
| Primær | `petrol` | `#1B4F72` |
| Sekundær bakgrunn | `sand` | `#F5DEB3` |
| Bakgrunn | `cream` | `#FBF5E6` |
| Aksent/i dag | `sunshine` | `#F4A621` |
| Tekst | `charcoal` | `#2C3E50` |
| Fullført | `success` | `#27AE60` |
| Ikke startet | `muted` | `#95A5A6` |

Fonter: `heading: 'Playfair Display'`, `body: 'Inter'`

### Alpine.js applikasjonstilstand
En `x-data` på rot-`<div>` med:
- `activeSection` — navigasjon mellom 4 seksjoner (smooth scroll)
- `mobileMenuOpen` — hamburgermeny
- `stops[]` — sentral datastruktur for alle stopp
- `expandedWeek` — hvilken uke som er utvidet
- `checklists{}` — 4 sjekklister med localStorage-persistering
- `init()` — initialiserer kart, laster sjekklister fra localStorage

### Sentral datastruktur: `stops`-array
All rutedata i ett JS-array for enkel oppdatering:
```javascript
{
  id, name, country, countryCode,
  lat, lng,                        // For kartmarkører
  arrivalDate, departureDate, nights, week,
  camping: { name, address, url, booked, bookingRef },
  driveFromPrevious: { km, hours, route },
  description,                     // Norsk beskrivelse
  activities: [{ name, type, priority, description, url }],
  tips: [],
  imageUrl: ''                     // Fylles inn etterhvert
}
```

---

## Fase 1: Ferieplanlegging — initielt ruteforslag

Claude utarbeider et konkret ruteforslag som oppdateres i spesifikasjonens seksjon 2.3. Krever ingen videre godkjenning — fungerer som demonstrasjonsinnhold.

### Oppgaver

1.1. **Planlegg ruten** — lag en dag-for-dag plan som oppfyller alle kriterier:
   - Start Kongsberg tidligst 4. juli, retur senest 1. august
   - Besøk André og Lucia i Berlin (Fischerinsel 9, 10179 Berlin)
   - Min. 3 netter per stopp
   - Kjøreetapper under 6 timer med min. ett stopp underveis
   - William-vennlige campingplasser (lekeplass, strand/bading)

1.2. **Finn campingplasser** for hvert stopp:
   - Søk etter egnede campingplasser med fasiliteter for barnefamilier
   - Inkluder navn, adresse, nettside, og kort beskrivelse av fasiliteter
   - Sjekk at campingplassene tar imot campingvogn

1.3. **Finn aktiviteter og severdigheter** per stopp:
   - Min. 3-5 aktiviteter per destinasjon, merket som must-do eller nice-to-have
   - Tilpasset 5-åring der relevant
   - Uke 1: Strand, bading, Legoland (Danmark)
   - Uke 2: Berlin, kultur, familiebesøk
   - Uke 3: Bohemian Switzerland, slott
   - Uke 4: Strand, bading, København (Danmark)

1.4. **Beregn kjøretider og avstander** mellom alle stopp med campingvogn (lavere hastigheter)

1.5. **Oppdater spesifikasjonen** — skriv det detaljerte forslaget inn i seksjon 2.3 i `docs/Spesifikasjon-ferieplan-webside.md` og legg til endringslogg-oppføring

1.6. **Commit**: `git add` + `git commit` med beskrivelse av ruteforslaget

---

## Fase 2: Sideskall og navigasjon

Bygg grunnstrukturen i `index.html` fra scratch med alle CDN-avhengigheter.

### Oppgaver

2.1. **Opprett `index.html`** med HTML-boilerplate:
   - `<!DOCTYPE html>`, `<html lang="no">`, meta-tags (charset, viewport)
   - CDN-lenker: Tailwind play-cdn, Alpine.js (defer), Leaflet CSS+JS, Google Fonts

2.2. **Tailwind config** i `<script>` blokk:
   - Utvid fargepaletten med alle 7 prosjektfarger
   - Konfigurer fontfamilier (heading + body)

2.3. **Alpine.js app-skjelett**:
   - `x-data` med komplett tilstandsobjekt (stops, checklists, navigasjon)
   - Populer `stops`-arrayet med data fra fase 1
   - `init()` metode (tom foreløpig — fylles i fase 3)

2.4. **Sticky toppmeny**:
   - Desktop: horisontale lenker — Kart, Reiseplan, Pakkelister, Budsjett & Praktisk
   - Mobil (<768px): hamburgermeny-knapp med Alpine.js toggle
   - Aktiv seksjon markert med sunshine-gul understreking
   - Klikk → smooth scroll til seksjonens `id`

2.5. **Hero-seksjon**:
   - Tittel "Sommerferie 2026" i Playfair Display
   - Undertittel med turinfo
   - Stats-bar: uker / land / km / stopp (beregnet fra `stops`-data)

2.6. **Seksjon-placeholders**: Tomme `<section>` elementer med `id` for kart, reiseplan, pakkelister, budsjett

2.7. **Verifiser** (Claude: kodesjekk, bruker: nettleser): Åpne filen, sjekk at fonter laster, farger stemmer, navigasjon scroller, hamburgermeny fungerer

2.8. **Commit**: `git add` + `git commit`

---

## Fase 3: Kart (Leaflet)

Implementer interaktivt kart med markører, polylinje og GPS.

### Oppgaver

3.1. **Leaflet-initialisering**:
   - I `init()`, bruk `$nextTick` for å vente på DOM
   - Kartcontainer med passende høyde (60vh desktop, 40vh mobil)
   - Sentrer kart på omtrentlig rutemidtpunkt, zoom 5-6

3.2. **Stoppmarkører**:
   - Iterer over `stops`-arrayet og legg til markører
   - Tilpassede `divIcon`-markører i petrol-farge med stoppnummer
   - Egen stil for start/slutt (Kongsberg)

3.3. **Popups ved klikk**:
   - Vis stoppnavn, datoer, antall netter
   - Campingplass-navn med lenke til nettside
   - Kort beskrivelse

3.4. **Polylinje**:
   - Tegn linje mellom alle stopp i rekkefølge
   - Petrol-farge, stiplet linje

3.5. **GPS-posisjon**:
   - Be om `navigator.geolocation.getCurrentPosition()`
   - Vis "du er her"-markør i sunshine-gul
   - Håndter avslag gracefully (ingen feilmelding)

3.6. **Kartresize**:
   - Kall `map.invalidateSize()` ved scroll til kart-seksjonen
   - Sikre at kartet rendres korrekt etter initial hidden state

3.7. **Verifiser** (Claude: kodesjekk, bruker: nettleser): Kart vises, markører klikkes, polylinje tegnes

3.8. **Commit**: `git add` + `git commit`

---

## Fase 4: Reiseplan

Bygg dag/uke-plan med "i dag"-markering og ekspanderbare ukekort.

### Oppgaver

4.1. **"I dag"-kort**:
   - Sammenlign `new Date()` med stoppenes `arrivalDate`/`departureDate`
   - Før tur: vis "X dager til avreise" med nedtelling
   - Under tur: vis "I dag er dere i [Sted]" med stoppdetaljer og neste kjøreetappe
   - Etter tur: vis "Ferien er over — vel hjem!"
   - Bruk sunshine-gul aksent for å fremheve

4.2. **Ukekort (4 stk)**:
   - Kollapsbare kort med Alpine.js `x-show` + overgangsanimasjon
   - Header: ukenummer, datoperiode, landsflagg, oppsummeringstekst
   - Klikk på header toggler `expandedWeek`

4.3. **Stoppdetaljer inne i ukekort**:
   - Per stopp: kort med campingplass-info, kjøretid fra forrige stopp
   - Aktivitetsliste med visuell markering av must-do vs nice-to-have
   - Praktiske tips per stopp
   - Alle data hentet fra `stops`-arrayet

4.4. **Kjøreetappe-visning**:
   - Mellom stopp: kompakt visning av km, timer, rute
   - Synlig både i kollapset og utvidet tilstand

4.5. **Verifiser** (Claude: kodesjekk, bruker: nettleser): Ukekort ekspanderer/kollapser, "i dag" vises korrekt, innhold fra fase 1 er synlig

4.6. **Commit**: `git add` + `git commit`

---

## Fase 5: Pakkelister

Implementer 4 sjekklister med localStorage-persistering.

### Oppgaver

5.1. **Tab-navigasjon**: 4 faner — Pakkeliste / Campingvogn / Før avreise / Daglig
   - Alpine.js `activeChecklist` variabel
   - Visuell markering av aktiv fane

5.2. **Generer sjekklisteinnhold** (norsk, tilpasset campingvogn med 5-åring):
   - **Pakkeliste**: Klær Ann Kristin, klær Arne, klær William, dokumenter (pass, forsikring, førerkort), toalettsaker, medisin/førstehjelp, elektronikk (ladere, kamera), kjøkkenutstyr, underholdning William (tegnesaker, bøker, nettbrett), uteutstyr (solkrem, insektmiddel, paraply)
   - **Campingvogn**: Teknisk sjekk (hjul, lys, bremser), koblinger (strøm, vann), gass (flaske, regulator), vannpumpe/slange, sikkerhet (brannslukker, røykvarsler), vignetter og miljøplaketter
   - **Før avreise**: Stoppe post, vanne planter/ordne med nabo, sikre hus (vinduer, dører, alarm), slå av unødvendig strøm, tømme kjøleskap, levere nøkler til nabo
   - **Daglig**: Ankomst (nivellere vogn, koble strøm/vann, sjekk gass, åpne markise) og avreise (steng vann, sikre skap/skuffer, lukk vinduer, koble fra strøm, sjekk at ingenting glemmes ute)

5.3. **Checkbox-logikk**:
   - Hver item har `done`-property
   - Toggle ved klikk, kall `saveChecklists()`
   - Visuell gjennomstreking for fullførte items

5.4. **localStorage-persistering**:
   - Nøkkel: `sommerferie2026-checklists`
   - Lagre boolean-arrays per liste
   - `loadChecklists()` i `init()` — merge med HTML-definerte items
   - Nye items (lagt til senere) får `done: false` som default

5.5. **Fremgangsindikator**: "X av Y fullført" tekst + progress-bar per liste

5.6. **Nullstill-knapp**: Per liste, med visuell bekreftelse (f.eks. "Er du sikker?")

5.7. **Verifiser** (Claude: kodesjekk, bruker: nettleser): Avkrysning overlever page reload, nullstill fungerer, faner bytter korrekt

5.8. **Commit**: `git add` + `git commit`

---

## Fase 6: Budsjett & Praktisk

Implementer kostnadsoversikt og praktisk referanseinformasjon.

### Oppgaver

6.1. **Budsjett-grid**:
   - Kort per kategori: Drivstoff, Overnatting, Mat, Aktiviteter, Ferge/bom, Buffer
   - Estimerte NOK-beløp (Claude beregner rimelige estimater basert på 4 uker, campingvogn, 3 personer)
   - Total-sum nederst
   - Visuell progress-bar per kategori

6.2. **Valutatabell**:
   - NOK → EUR, DKK, CZK med omtrentlige kurser
   - Eksempel-beregninger (f.eks. "100 NOK ≈ X EUR")

6.3. **Big Mac Index**:
   - Norge, Danmark, Tyskland, Tsjekkia
   - Pris i lokal valuta og NOK for sammenligning
   - Kort forklaring av hva indeksen viser

6.4. **Fartsgrenser med henger** — tabell per land:
   - Norge, Sverige, Danmark, Tyskland, Tsjekkia
   - Kolonner: Tettbebygd / Landevei / Motorvei
   - Spesifikt for bil med campingvogn/henger

6.5. **Nødnumre per land**: 112 (felles), pluss lokale numre for politi/ambulanse der relevant

6.6. **Bompenger/vignetter/miljøsoner**:
   - Krav per land (AutoPASS, BroBizz, Umweltplakette, etc.)
   - Hvor og hvordan kjøpe/bestille
   - Miljøsoner i tyske byer (Umweltzone) — hvilke byer, plaketttype

6.7. **Viktige adresser**: André og Lucia — Fischerinsel 9, 10179 Berlin

6.8. **Verifiser** (Claude: kodesjekk, bruker: nettleser): Alle tabeller og kort vises korrekt, responsivt layout

6.9. **Commit**: `git add` + `git commit`

---

## Fase 7: Finpuss

Kvalitetssikring og siste justeringer.

### Oppgaver

7.1. **Responsiv testing**: Sjekk layout ved 375px (mobil), 768px (nettbrett), 1280px (desktop)

7.2. **Kontrast og lesbarhet**: Verifiser at tekst er lesbar på alle bakgrunnsfarger, spesielt i sollys (høy kontrast)

7.3. **Ingen emojier**: Søk gjennom hele filen og fjern eventuelle emojier — bruk tekst eller CSS-styling i stedet

7.4. **Smooth scroll**: Verifiser at navigasjonsklikk gir smooth scroll-oppførsel

7.5. **Kodeorganisering**: Legg til tydelige seksjonkommentarer (`<!-- ===== SEKSJON: KART ===== -->`) for vedlikeholdbarhet

7.6. **Oppdater spesifikasjonen**: Legg til endringslogg-oppføring i `docs/Spesifikasjon-ferieplan-webside.md`

7.7. **Endelig commit og push**: `git add` + `git commit` + `git push`

---

## Bilder
- Start med placeholder gradient-bokser i fargepaletten
- Erstatt med reelle foto-URLer etterhvert
- Flagg fra CDN (f.eks. flagcdn.com)

---

## Filer som endres
- `docs/Spesifikasjon-ferieplan-webside.md` — seksjon 2.3 oppdateres med detaljert ruteforslag + endringslogg
- `index.html` — fullstendig omskriving fra scratch

## Verifisering (endelig)

Claude kjører i WSL og kan ikke åpne nettleser direkte. Verifisering deles i to:

**Claude verifiserer (automatisk):**
1. HTML-validering: sjekk at filen er velformet HTML (ingen ulukkede tags, korrekt nesting)
2. CDN-URLer: verifiser at alle 4 CDN-lenker er korrekte og tilgjengelige (WebFetch)
3. Farger: søk i filen etter hex-verdier og bekreft at de matcher spesifikasjonens palett
4. Fonter: bekreft at Google Fonts-lenken inkluderer Playfair Display og Inter
5. Ingen emojier: søk gjennom hele filen etter unicode emoji-sekvenser
6. Alpine.js-struktur: sjekk at `x-data`, `x-show`, `x-on:click` etc. er korrekt brukt
7. Leaflet-oppsett: sjekk at kartcontainer, tile layer URL og markør-logikk er på plass
8. localStorage: sjekk at save/load-funksjoner refererer riktig nøkkel og håndterer manglende data

**Bruker verifiserer i nettleser (manuelt):**
1. Åpne `index.html` i Chrome (fra Windows: `\\wsl$\...` eller via GitHub Pages etter push)
2. Navigasjon scroller til riktig seksjon på desktop og mobil
3. Hamburgermeny fungerer på mobil (Chrome DevTools → responsive mode)
4. Kart vises med markører og polylinje
5. Kart-popups viser stoppinfo ved klikk
6. Ukekort ekspanderer/kollapser
7. Sjekkliste-avkrysninger overlever page reload
8. Nullstill-knapp tømmer én sjekkliste
9. Responsiv ved 375px, 768px og 1280px

---

## Fasestatus

| Oppgave | Status | Notater |
|---------|--------|---------|
| **Fase 1: Ferieplanlegging** | | |
| 1.1 Planlegg ruten (dag-for-dag) | Ikke startet | |
| 1.2 Finn campingplasser | Ikke startet | |
| 1.3 Finn aktiviteter og severdigheter | Ikke startet | |
| 1.4 Beregn kjøretider og avstander | Ikke startet | |
| 1.5 Oppdater spesifikasjonen (seksjon 2.3) | Ikke startet | |
| 1.6 Commit | Ikke startet | |
| **Fase 2: Sideskall og navigasjon** | | |
| 2.1 Opprett index.html med boilerplate + CDN | Ikke startet | |
| 2.2 Tailwind config (farger, fonter) | Ikke startet | |
| 2.3 Alpine.js app-skjelett med stops-data | Ikke startet | |
| 2.4 Sticky toppmeny + hamburgermeny | Ikke startet | |
| 2.5 Hero-seksjon med stats-bar | Ikke startet | |
| 2.6 Seksjon-placeholders | Ikke startet | |
| 2.7 Verifiser i nettleser | Ikke startet | |
| 2.8 Commit | Ikke startet | |
| **Fase 3: Kart (Leaflet)** | | |
| 3.1 Leaflet-initialisering | Ikke startet | |
| 3.2 Stoppmarkører fra stops-array | Ikke startet | |
| 3.3 Popups ved klikk | Ikke startet | |
| 3.4 Polylinje mellom stopp | Ikke startet | |
| 3.5 GPS-posisjon | Ikke startet | |
| 3.6 Kartresize ved scroll | Ikke startet | |
| 3.7 Verifiser i nettleser | Ikke startet | |
| 3.8 Commit | Ikke startet | |
| **Fase 4: Reiseplan** | | |
| 4.1 "I dag"-kort med datosammenligning | Ikke startet | |
| 4.2 Ukekort (4 stk) med expand/collapse | Ikke startet | |
| 4.3 Stoppdetaljer inne i ukekort | Ikke startet | |
| 4.4 Kjøreetappe-visning | Ikke startet | |
| 4.5 Verifiser i nettleser | Ikke startet | |
| 4.6 Commit | Ikke startet | |
| **Fase 5: Pakkelister** | | |
| 5.1 Tab-navigasjon (4 faner) | Ikke startet | |
| 5.2 Generer sjekklisteinnhold | Ikke startet | |
| 5.3 Checkbox-logikk | Ikke startet | |
| 5.4 localStorage-persistering | Ikke startet | |
| 5.5 Fremgangsindikator | Ikke startet | |
| 5.6 Nullstill-knapp | Ikke startet | |
| 5.7 Verifiser i nettleser | Ikke startet | |
| 5.8 Commit | Ikke startet | |
| **Fase 6: Budsjett & Praktisk** | | |
| 6.1 Budsjett-grid | Ikke startet | |
| 6.2 Valutatabell | Ikke startet | |
| 6.3 Big Mac Index | Ikke startet | |
| 6.4 Fartsgrenser med henger | Ikke startet | |
| 6.5 Nødnumre per land | Ikke startet | |
| 6.6 Bompenger/vignetter/miljøsoner | Ikke startet | |
| 6.7 Viktige adresser | Ikke startet | |
| 6.8 Verifiser i nettleser | Ikke startet | |
| 6.9 Commit | Ikke startet | |
| **Fase 7: Finpuss** | | |
| 7.1 Responsiv testing | Ikke startet | |
| 7.2 Kontrast og lesbarhet | Ikke startet | |
| 7.3 Fjern emojier | Ikke startet | |
| 7.4 Smooth scroll | Ikke startet | |
| 7.5 Kodeorganisering (seksjonkommentarer) | Ikke startet | |
| 7.6 Oppdater spesifikasjonen (endringslogg) | Ikke startet | |
| 7.7 Endelig commit og push | Ikke startet | |
