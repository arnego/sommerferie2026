# Teknisk spesifikasjon — Sommerferie 2026

## Webside for familie-roadtrip med campingvogn

> **Formål:** Teknisk og funksjonell spesifikasjon for websiden som bygges med Claude Code og hostes på GitHub Pages. Websiden hjelper familien med å planlegge, forberede og gjennomføre sommerferien 2026.

---

## 1. Prosjektoversikt

### 1.1 Bakgrunn
Familien Goderstad ønsker en flott sommerferie i år! For reisen ønsker vi en god plan med flotte overnattingssteder, aktiviteter og severdigheter som er tilpasset familiens behov og ønsker.

### 1.2 Målgruppe
Websiden er kun for familien — ingen ekstern deling. Den skal fungere som et felles oppslagsverk og verktøy under hele planleggings- og reisefasen.
Websiden må være på norsk, men lokale navn kan benyttes.

### 1.3 Bruksscenarier
- Planlegging hjemme på PC i ukene før avreise
- Sjekke neste stopp fra mobilen mens man er underveis
- Slå opp aktiviteter og reservasjoner for dagen
- Pakkeliste-gjennomgang kvelden før avreise

### 1.4 Mål og suksesskriterier
- All relevant ferieinfo samlet på ett sted
- Enkel å tilpasse for Claude underveis med nye ønsker fra familien
- Presenterer informasjon om lokale aktiviteter og severdigheter tilpasset familien i forbindelse med overnattingssteder
- Gir godt overblikk over reiseruten
- Viser ikke alt for mye informasjon på én gang, men gir mulighet for å grave dypere i detaljene

---

## 2. Funksjonelle krav

### 2.1 Rutekart
Krav til kartvisning av reiseruten:
- Interaktivt kart
- Markører for overnattingssteder, severdigheter, etc.
- Klikk på markørene gir mer informasjon og lenker til de offisielle websidene for disse.
- Siden burde be om GPS-posisjon fra enheten og markere posisjonen til brukeren på kartet.

### 2.2 Dag-for-dag / uke-for-uke plan
- Dagens plan burde fremheves og vises i en egen seksjon basert på datoen til enheten når websiden lastes.
- Kjøretider og avstander mellom stopp.
- Planlagte aktiviteter og severdigheter
- Overnattingsinfo (campingplasser, reservasjoner)
- Fleksibilitet: "must-do" vs. "nice-to-have"

### 2.3 Sjekklister
- Pakkeliste (klær, utstyr, dokumenter, mat, underholdning for barna)
- Klargjøring av bil og campingvogn
- Før-avreise (stoppe post, vanne planter, etc.)
- Daglig sjekkliste for av- og påstigning campingplass

### 2.4 Budsjett og økonomi
- Estimert kostnad per kategori (drivstoff, overnatting, mat, aktiviteter)
- Valutainformasjon for ulike land med vekslingskurs mot NOK — **live dagskurser** (se §2.7 Valutakurser og kalkulator), ikke hardkodet
- Big Mac Index for ulike land (fra worldpopulationreview.com) for å lettere forstå kostnadsnivået i landet.

### 2.5 Praktisk informasjon
Referanseinformasjon som er nyttig underveis:
- Nødnumre per land
- Viktige adresser og telefonnumre
- Forsikringsinformasjon
- Bompenger, vignetter, miljøsoner
- Fartsbegrensninger med henger per land
- **Promillegrenser per land** — tabell over tillatt promille (‰) i de 8 landene ruten går gjennom. Eget accordion-kort etter Fartsgrenser, synlig i begge moduser.
- Campingplass-regler og sjekk-inn/ut-tider

### 2.6 Værvarsel
Værvarsel for hvert overnattingssted, hentet ved sideåpning fra **Open-Meteo** (`https://api.open-meteo.com/v1/forecast`) — gratis, krever ingen API-nøkkel, full CORS-støtte og dekker hele ruten (DK/DE/NO).

**Temperatur:** Temperatur vises sammen med værsymbolet overalt, hentet fra samme Open-Meteo-kall (`hourly=...,temperature_2m` + `daily=weather_code,temperature_2m_max,temperature_2m_min`). Temperatur vises i hele grader med `°C` etter verdien, og utelates diskret når den mangler.

**Dager som vises:** Fra ankomstdato t.o.m. avreisedato for stoppet (`datesForStop()`) — altså overnattingsdagene pluss selve avreisedagen på destinasjonen. Gjelder alle tre visningssteder under.

**Tre visningssteder:**
1. **Kart-popup** — når man klikker en stopp-markør vises en kompakt rad med ett dagssammendrag per dag (ankomst t.o.m. avreise): symbol fra Open-Meteos daglige «mest signifikante» værkode + dagens maks/min-temperatur (`maks°/min°C`), der maks vises i rød (`#C0392B`) og min i petrol (`#1B4F72`).
2. **Reiseplan, kollapset bar** — samme kompakte rad under datolinjen i den klikkbare overskriften.
3. **Reiseplan, utvidet detaljvisning** — egen «Værvarsel»-seksjon med tabell: én rad per dag (ankomst t.o.m. avreise), kolonner for dato/ukedag og for kl. 09 / 12 / 15 / 18 / 21 — hver celle viser timesymbol med timestemperatur stablet under.

**Manglende data:** Hvis forecast er utilgjengelig for et tidspunkt (utenfor prognosehorisont, nettverksfeil osv.), vises et diskret «ikke tilgjengelig»-symbol (kort vannrett strek). Den kompakte raden i popup og kollapset bar skjules helt når ingen data er tilgjengelig for stoppet (unngå støy av kun streker); tabellen vises alltid og fyller cellene med streker der data mangler.

**Ikoner:** Inline SVG i samme flate stil som øvrige ikoner i fila — ingen ekstern ikonpakke. 10 kategorier dekker WMO weather interpretation codes: klart, stort sett klart, delvis skyet, overskyet, tåke, yr, regn, snø, tordenvær, ikke tilgjengelig. Sol-elementer i `#F4A621` (sunshine), nedbør/sky-elementer i `#1B4F72` (petrol) eller `#607080` (muted).

**Hentestrategi:**
- Henting skjer ved sideåpning. Resultater lagres i `localStorage` (nøkkel `sommerferie2026-weather`) med 1 times TTL — ny henting kun hvis cache er eldre.
- Open-Meteo støtter prognose ~16 dager fram. Stopp som ligger lengre fram enn dette hopper over fetch-kallet (returnerer tom dataliste); cellene viser «ikke tilgjengelig» til turen nærmer seg.
- Ved nettverksfeil eller API-feil brukes eventuell eldre cache uavhengig av alder. Hvis ingen cache finnes, vises «ikke tilgjengelig» overalt. Ingen feilmelding vises til bruker.

**Mock-modus:** En `weatherMock`-flagg på Alpine-komponenten kan settes til `true` for å bygge deterministisk mock-data som dekker alle 10 visningskategorier — brukes ved utvikling/UI-verifisering uten å treffe API-et.

### 2.7 Valutakurser og kalkulator
Valutakurser-kortet henter **live dagskurser** ved sideåpning i stedet for hardkodede verdier, etter samme hente-/cache-mønster som værvarselet (§2.6).

**Datakilde:**
- Primær: **frankfurter.dev** (`https://api.frankfurter.dev/v1/latest?base=NOK&symbols=EUR,DKK,CZK`) — ECB-dagskurser, gratis, ingen API-nøkkel, CORS-støtte. Returnerer `{ base, date, rates: { EUR, DKK, CZK } }` der hver kurs er utenlandsk valuta per 1 NOK.
- Fallback ved feil: **open.er-api.com** (`https://open.er-api.com/v6/latest/NOK`) — samme retning (rates per NOK).

**Hentestrategi (`loadFxRates()`):** Kurser lagres i `localStorage` (nøkkel `sommerferie2026-fx-v1`) med **1 times TTL** — ny henting kun hvis cachen er eldre. Ved nettverks-/API-feil brukes eventuell eldre cache; finnes ingen cache settes `fxError` og tabellen viser en diskret melding om å sjekke kurser før avreise. Ingen blokkerende feilmelding.

**Tabell:** De tre radene (EUR/DKK/CZK) er datadrevet via `x-for` over `fxRows`. «Kurs»-kolonnen viser `1 X = (1/rate) NOK`, «100 NOK =»-kolonnen viser `100·rate X`. Tall formateres med `formatFx()` (norsk locale, 0 desimaler ≥ 100, ellers 2).

**Kalkulator:** Under tabellen. Hver tabellrad er valgbar (`role=button`, tastaturstøtte, `aria-pressed`) og setter `fxSelected`. Inndatafelt (`type=number`, `x-model.number="fxAmount"`) til venstre; utdata til høyre viser `fxConverted` = `fxAmount / rate` (utenlandsk beløp → NOK) via computed getter. Tomt/ugyldig felt eller manglende kurser gir `–`.

**Forhåndsvalgt valuta:** Ved sideåpning settes `fxSelected` i `init()` til valutaen for landet vi er i på dagens dato — kun **under turen** (`todayStatus === 'during'`). Hjelperen `countryToCurrency(currentStop.country)` mapper land → valuta (Danmark → DKK, Tsjekkia → CZK, Tyskland/Østerrike/Slovenia/Kroatia → EUR; Norge → `null` siden NOK er basisvaluta uten rad). **Før avreise** (`before`) og **etter hjemkomst** (`after`) er `fxSelected = null`, dvs. ingen rad er markert og labelen viser «Beløp i valuta». Brukeren kan når som helst overstyre ved å klikke en rad.

**Kreditering:** Datakilden (Open-Meteo) er dokumentert her i spesifikasjonen; den tidligere «Værdata: Open-Meteo»-linjen under værtabellen er fjernet som overflødig.

---

## 3. Innholdsstruktur (Informasjonsarkitektur)

Toppmeny med fire seksjoner i rekkefølge:

1. **Kart** — interaktivt rutekart (Leaflet + OpenStreetMap) med markører for alle stopp. Klikk på markør gir info-popup med kompakt værstrip per dag. GPS-posisjon vises på kartet.
2. **Reiseplan** — dag/uke-plan der dagens plan fremheves basert på enhetens dato. Ukevis visning med etapper, kjøretid/avstand, aktiviteter, campingplass og værvarsel (kompakt strip i kollapset bar, full tabell i utvidet visning).
3. **Pakkelister** — fire sjekklister (pakking, campingvogn, før avreise, daglig). Avkryssinger lagres i localStorage. Nullstill-knapp per liste.
4. **Praktisk info** (samme tittel i begge moduser) — valutatabell med kalkulator (NOK ↔ EUR/DKK/CZK), promillegrenser, fartsgrenser med henger, nødnumre, bompenger/vignetter, miljøsoner. Kostnadsestimatet «Estimert budsjett» ligger i planleggings-seksjonen **Booking & Planlegging**.

---

## 4. Interaktivitet og datalagring

### 4.1 Interaktive elementer
- Ekspanderbare/sammenklappbare seksjoner

### 4.2 Datalagring (localStorage)
Websiden hostes på GitHub Pages (statisk), så det finnes ingen server-side lagring. Klientside-lagring via `localStorage` skal brukes for sjekklister, men synkroniserer ikke mellom enheter.
Vi lager ingen eksport/import-funksjon for manuell synk mellom enheter foreløpig.
Vi ønsker en diskre "nullstill"-knapp per sjekkliste.
Hvis nettleserdata tømmes er de lokale dataene tapt.

### 4.3 Oppdateringsflyt
- Claude oppdaterer spesifikasjonen og endringsloggen i spesifikasjonen.
- Claude oppdaterer reiseplanen og websiden i henhold til de nye ønskene og spesifikasjonen.
- I det lokale repoet gjør Claude git commit med beskrivelse av endringene som ble utført, inklusive det nye tillegget i endringsloggen i spesifikasjonen.
- Claude gjør git push på det lokale repoet for å publisere endringene til GitHub Pages i github-repo: arnego/sommerferie2026

---

## 5. Designkrav

### 5.1 Designprinsipper
Overordnede prinsipper for det visuelle uttrykket:
- Enkelt og ryddig — lett å skanne raskt
- Ferie- og naturstil — sommerlig og innbydende
- Mobil-vennlig — touch-vennlige elementer
- Lett å lese i sollys

### 5.2 Sidestruktur
Én lang side (SPA)

### 5.3 Navigasjon
Toppmeny / hamburgermeny på mobil

### 5.4 Innholdshierarki
Kart > Dagens plan > Neste kjøreetappe > Sjekklister > Budsjett

### 5.5 Fargepalett
Stemning: kart-sentrert, ferie- og naturstil, lett å lese i sollys. Kun lys modus.

| Rolle | Farge | Hex |
| --- | --- | --- |
| Primær (kart/navigasjon) | Dyp petrol/havblå | `#1B4F72` |
| Sekundær (bakgrunn) | Varm sand | `#F5DEB3` |
| Bakgrunn (lysere) | Kremhvit sand | `#FBF5E6` |
| Aksent / «i dag»-markør | Solskinnsgult | `#F4A621` |
| Tekst | Mørk koksgrå | `#2C3E50` |
| Status: fullført | Grønn | `#27AE60` |
| Status: ikke startet | Grå | `#607080` (oppjustert fra `#95A5A6` for WCAG AA) |

### 5.6 Typografi
Fonter lastes via Google Fonts CDN.

- **Overskrifter:** Playfair Display (serif) — gir ferie- og reisestemning
- **Brødtekst:** Inter (sans-serif) — god lesbarhet på skjerm og i sollys
- **Minimumsstørrelser mobil:** 16px brødtekst, 14px metainfo og etiketter

### 5.7 Ikoner og grafikk
- Unngå bruk av emoji
- Bruk fotografier fra de aktuelle destinasjonene i presentasjonen av disse. Fotografiene burde gi oversikt over overnattingssted eller et godt bilde av attraksjonen.
- Flagg kan brukes for landoversikt
- Bruk logoer fra de aktuelle attraksjonene eller overnattingsstedene der de er tilgjengelig

### 5.8 Responsivt design
Krav til ulike skjermstørrelser:
- Mobil (primær bruksenhet underveis og ved gjennomgang av sjekklister)
- Nettbrett
- Desktop (planleggingsfasen)

### 5.9 Referansedesign / inspirasjon
Lenker til eksempler på nettsider som har en stil vi liker:
- https://www.hotelcanferrereta.com/es/
- https://maps.roadtrippers.com/trips/30411788
- https://thedyrt.com/

---

## 6. Tekniske krav

### 6.1 Hosting og infrastruktur
- **Hosting:** GitHub Pages
- **Repository:** `arnego/sommerferie2026`
- **Domene:** `https://arnego.github.io/sommerferie2026/`

### 6.2 Teknologivalg
- **Stack:** Ren HTML-fil med CDN-baserte biblioteker — ingen build-steg, ingen npm
- **Kart:** Leaflet.js + OpenStreetMap — gratis, ingen API-nøkkel nødvendig
- **Værvarsel:** Open-Meteo (`api.open-meteo.com`) — gratis, ingen API-nøkkel, full CORS, opptil 16-dagers prognose
- **CSS-rammeverk:** Tailwind CSS via CDN (play-cdn)
- **Reaktivitet:** Alpine.js via CDN — trekkspill, tabs, sjekklister, mobilmeny
- **Fonter:** Google Fonts via CDN (Playfair Display + Inter)
- **Ingen PWA** — kun Chrome (iOS + desktop)
- **Nettleserkompatibilitet:** Chrome på iOS og desktop

### 6.3 Lokal testserver
For lokal utvikling og automatisert verifisering i Chrome brukes `setup/test-server/https_server.py` (HTTPS, port 3000). Sertifikatfilene ligger i samme mappe som skriptet.
```
python setup/test-server/https_server.py
```
Åpne `https://localhost:3000/index.html` i Chrome. Bruk aldri `python -m http.server` eller `file://`-URLer.

### 6.4 Sikkerhet og personvern
Websiden inneholder personlig reiseinformasjon, så repoet skal være privat.
Websiden kan inneholde sensitiv info i koden (passord, bookingref, etc.).

#### Sensitive data — tillatt direkte i koden
Repoet er privat. Følgende kan ligge direkte i `index.html` uten hashing eller kryptering:
- Adresser og kontaktinformasjon (f.eks. familiebesøk)
- Booking-referanser og reservasjonsnumre
- Passord og PIN-koder (campingplass-porter, safe-koder, Wi-Fi-passord)

### 6.5 Sjekkliste-innhold
Claude genererer komplette sjekklister tilpasset campingvogn-tur med 5-åring:
- **Pakkeliste** — klær per person, utstyr, dokumenter, underholdning for William
- **Campingvogn-sjekkliste** — teknisk klargjøring (koblinger, lys, gass, vann, sikkerhet), nødvendige vignetter og plaketter
- **Før avreise** — post, planter, hus, strøm, alarm
- **Daglig sjekkliste** — av-/påstigning campingplass (ankomst og avreise)

---

## 7. Verifisering (automatisert av Claude)

All verifisering utføres automatisert av Claude. På Windows brukes **Claude in Chrome**-connector (MCP) for visuell og funksjonell testing direkte i brukerens Chrome-nettleser.

**Testserver:** Start `setup/test-server/https_server.py` før alle Chrome-tester (`python setup/test-server/https_server.py`), naviger til `https://localhost:3000/index.html`.

### Verktøyvalg

| Prioritet | Verktøy | Når |
| --- | --- | --- |
| 1 | **Claude in Chrome** | Windows-sesjon med Chrome åpen. Start `setup/test-server/https_server.py` og naviger til `https://localhost:3000/index.html`. |
| 2 | **Statisk kodeanalyse** | Fallback når Claude in Chrome ikke er tilgjengelig. Grep, Read og manuell gjennomgang av HTML/JS-kode. |

### Verifiseringssteg

**Statisk analyse (alltid):**
1. HTML-validering: sjekk at filen er velformet (ingen ulukkede tags, korrekt nesting)
2. CDN-URLer: verifiser at alle 4 CDN-lenker er korrekte og tilgjengelige
3. Farger: søk etter hex-verdier og bekreft samsvar med spesifikasjonens palett
4. Fonter: bekreft at Google Fonts-lenken inkluderer Playfair Display og Inter
5. Ingen emojier: søk etter unicode emoji-sekvenser
6. Alpine.js-struktur: sjekk `x-data`, `x-show`, `x-on:click` etc.
7. Leaflet-oppsett: sjekk kartcontainer, tile layer URL og markør-logikk
8. localStorage: sjekk save/load-funksjoner med riktig nøkkel

**Visuell og funksjonell testing (via Claude in Chrome):**
1. Start `setup/test-server/https_server.py`, naviger til `https://localhost:3000/index.html` og ta screenshot — bekreft at siden rendres korrekt
2. Navigasjon: klikk på menylenker, verifiser smooth scroll til riktig seksjon
3. Hamburgermeny: resize til mobilbredde, klikk hamburger-ikon, verifiser at meny åpner/lukker
4. Kart: scroll til kart-seksjonen, bekreft markører og polylinje. Klikk på markør og verifiser popup-innhold
5. Reiseplan: klikk på ukekort-headere, bekreft expand/collapse og innhold
6. Pakkelister: klikk på checkbokser, reload siden, bekreft at avkrysninger er bevart (localStorage). Test nullstill og fanebytte
7. Budsjett: scroll til seksjonen, verifiser at tabeller og kort rendres korrekt
8. Responsiv: test ved 375px (mobil), 768px (nettbrett) og 1280px (desktop) — bekreft at layout tilpasser seg
9. Kontrast: beregn kontrastforhold for kritiske tekst/bakgrunn-kombinasjoner og verifiser WCAG AA (4.5:1)

---

## 8. Fremtidige muligheter (utenfor scope)
Her kan vi legge idéer som kan vurderes senere, men som foreløpig ikke skal inkluderes i implementasjonen.

- **Offline-støtte** — service worker / PWA for bruk uten internett underveis
- **Eksport/import av sjekklistestatus** — manuell synkronisering mellom enheter (f.eks. JSON-fil)

---

## Endringslogg

| Dato | Endring | Av |
| --- | --- | --- |
| 2026-07-12 | §2.6 Værvarsel: cache-nøkkel bumpet `sommerferie2026-weather-v3` → `-v4`. Etter forrige endring (ekte vær for passerte dager) beholdt enheter med en under-1-time gammel v3-cache fortsatt den gamle blobben — skrevet av den forrige koden som klippet `start_date` til «i dag» — der passerte dager var `null` og viste strek. Siden datformen er uendret kunne ikke `loadWeather` skille gammelt fra nytt innhold, så cachen ble servert direkte uten ny henting. Bump til v4 tvinger fram én ny henting på alle enheter, som nå fyller passerte dager med ekte observert vær (samme mønster som tidligere v1→v2→v3-bumper ved utdatert cache-innhold). | Claude |
| 2026-07-12 | **Valutakalkulator forhåndsvelger valuta.** Ved sideåpning settes `fxSelected` til valutaen for landet vi er i på dagens dato — men kun under turen (`todayStatus === 'during'`). Ny hjelper `countryToCurrency()` + getter `currentFxCurrency` mapper `currentStop.country` → valuta (Danmark → DKK, Tsjekkia → CZK, Tyskland/Østerrike/Slovenia/Kroatia → EUR, Norge → ingen). Før avreise og etter hjemkomst er ingen kurs valgt (`fxSelected = null`), labelen viser da «Beløp i valuta» og utdata «–». Standardverdien `fxSelected` endret fra `'EUR'` til `null`. | Claude |
| 2026-07-12 | **Seksjonsomorganisering.** «Estimert budsjett»-kortet flyttet fra Praktisk info til planleggings-seksjonen **Booking & Planlegging** (som siste kort; kortets egne mode-guard fjernet siden seksjonen alt er planleggings-only). Seksjonstittelen «Budsjett & Praktisk / Praktisk info» er forenklet til alltid **«Praktisk info»** i begge moduser, og den forklarende underteksten («Klikk på en seksjon …» / «Mest brukt underveis …») er fjernet. Menyetiketten i `sections` (desktop + hamburger) endret tilsvarende til «Praktisk info». | Claude |
| 2026-07-12 | **Fjernet overflødig værtabell-fotnote.** Linjen «Værdata: Open-Meteo (oppdatert ved sideåpning)» under den utvidede værtabellen per stopp er fjernet — informasjonen er allerede dokumentert i spesifikasjonen (§2.6) og ga unødig støy i visningen. | Claude |
| 2026-07-12 | **Valutakort — visuell finpuss (§2.7).** (1) Fjernet den overflødige footnoten «Dagskurser fra ECB … oppdatert … Caches 1 time.»; kun en diskret statuslinje ved lasting/feil vises nå, og den forsvinner når kursene er hentet. (2) Fjernet «valgt»-teksten ved siden av valutanavnet. (3) Tydeligere markering av valgt valutarad: en avrundet petrol-pille (`bg-petrol/10` + `rounded-l/r-full` på endecellene) rundt hele raden i stedet for den svake ring-/tint-markeringen. Tabellen bruker nå `border-separate border-spacing-0` slik at Tailwind v3 Preflights `border-collapse: collapse` ikke hindrer avrundede hjørner. | Claude |
| 2026-07-12 | **To nye funksjoner i Praktisk info.** (1) Nytt **Promillegrenser**-kort (§2.5) etter Fartsgrenser, synlig i begge moduser: enkel tabell over generell promillegrense i de 8 landene ruten går gjennom (Norge 0,2 ‰, Tsjekkia 0,0 ‰ nulltoleranse, øvrige 0,5 ‰), med footnote om strengere grenser for ferske/unge/profesjonelle sjåfører. Verdier verifisert mot kilde. (2) **Valutakurser** (ny §2.7) henter nå **live ECB-dagskurser** fra frankfurter.dev (fallback open.er-api.com) ved sideåpning med 1 times `localStorage`-cache (`sommerferie2026-fx-v1`) i stedet for hardkodede kurser — samme hente-/cache-mønster som værvarselet. Tabellen er datadrevet via `x-for` over `fxRows`, og under den ligger en **valutakalkulator**: velg valuta ved å klikke en rad (`fxSelected`, tastaturtilgjengelig), skriv inn beløp (`fxAmount`), og se det konvertert til NOK via computed getter `fxConverted` (`beløp / rate`). Nye hjelpere: `fetchFxRates`, `saveFxCache`, `loadFxCache`, `applyFxData`, `loadFxRates`, `formatFx`; `loadFxRates()` kalles i `init()`. | Claude |
| 2026-07-12 | §2.6 Værvarsel, to forbedringer i detaljtabellen per stopp. (1) Raden for dagens dato utheves nå diskré med `bg-sunshine/10` (samme aksent som aktivt stopp-kort og «I dag»-markører) slik at blikket lettere finner i dag. Ny delt getter `todayStr` (lokal dato `YYYY-MM-DD`) erstatter inline-`toISOString()`-beregninger; radbindingen er `:class="date === todayStr && 'bg-sunshine/10'"`. (2) Passerte reisedager viste tidligere kun grå strek fordi `fetchWeatherForStop` klippet `start_date` til «i dag», så Open-Meteo aldri ble spurt om fortiden. Testing viste at forecast-endepunktet faktisk returnerer ekte observerte verdier ~92 dager tilbake — `start_date` settes nå til reisens første dag, klippet til en trygg nedre grense på 90 dager (`today − 90 dager`) for å holde seg innenfor API-ets tillatte vindu og unngå «out of allowed range»-feil. Passerte dager viser dermed ekte observert vær (ikon + temperatur) i stedet for strek. Ingen cache-endring nødvendig; eksisterende `sommerferie2026-weather-v3` beholdes. | Claude |
| 2026-07-03 | Kvalitetssikring av alle kartpinner: campingplass-pinnene i stopp-headerne pekte tidligere kun på en gateadresse (uten bedriftsnavn) og traff derfor ofte feil sted i Google Maps — f.eks. landet Hirtshals-pinnen på boliger i gaten «Kystvejen» (uten husnummer) og Graz-pinnen på det offentlige badet «Bad Straßgang» i Martinhofstraße 3. Ny hjelper `campingMapsQuery(c)` bygger nå et søk som lander på selve virksomheten: bedriftsnavn + ren adresse, der parenteser («(ved havet …)») og tankestrek-merknader («— avgang kl. 17:35») strippes bort, med fallback til lat/lng. Brukes av `getMapsUrl` i begge moduser (forbedrer også navigasjonsnøyaktigheten underveis). Alle 15 campingplasser/ferger verifisert mot eksterne kilder (offisielle nettsteder, ADAC/PiNCAMP, promobil, park4night m.fl.). Rettet dataafeil: Camping Island Bamberg hadde feil adresse «Campinginsel, 96052 Bamberg» → korrigert til verifisert «Am Campingplatz 1, 96049 Bamberg» (vises også i stoppdetaljene). Aktivitetspinnene inneholdt allerede stedsnavn og var korrekte. | Claude |
| 2026-07-03 | Kartikon-lenkene («Naviger i Google Maps») i stopp-headere og aktivitetsrader skiller nå på modus: i underveis-modus starter de fortsatt navigasjon direkte (`maps/dir/...&travelmode=driving`, evt. campingplassens `navUrl`), mens de i planleggingsmodus kun åpner Google Maps med stedet valgt (`maps/search/?api=1&query=...`) uten å starte navigasjon. `getMapsUrl` og `getActivityMapsUrl` er nå modusbevisste. | Claude |
| 2026-07-02 | Tre rettelser: (1) Nedtellingen «X dager til avreise» viste 1 dag for mye — `daysUntilDeparture` parset ankomstdatoen som UTC-midnatt (`new Date('YYYY-MM-DD')`) mens dagens dato ble satt til lokal midnatt, som ga et kunstig ~2-timers gap i sommertid. Fikset ved å parse med `+'T00:00:00'` (lokal tid, samme mønster som `totalTripDays`) og bruke `Math.round` i stedet for `Math.ceil`. (2) §2.6 Værvarsel: `datesForStop()` viste tidligere kun overnattingsdager (ankomst t.o.m. avreise−1), slik at selve avreisedagen manglet vær i alle tre visningssteder (kart-popup, kollapset bar, detaljtabell) — og stopp med 0 netter (samme ankomst- og avreisedato, f.eks. fergeoverfarter) fikk ingen værdata i det hele tatt. Utvidet til å inkludere avreisedatoen (`d <= end` i stedet for `d < last`). (3) Etter (2) viste avreisedagen fortsatt strek («ikke tilgjengelig») for gjeldende stopp, mens neste stopp viste samme dato korrekt — skyldtes at nettlesernes eksisterende 1-times `localStorage`-cache (fra før datamodell-endringen) manglet data-oppføring for den nytilkomne datoen på forrige stopp, mens neste stopp alltid hadde datoen som sin ankomstdato. Cache-nøkkelen bumpet til `sommerferie2026-weather-v3` for å tvinge fram ny henting (samme mønster som v1→v2). | Claude |
| 2026-06-23 | Ny underseksjon «Aktiviteter å booke på forhånd» i Booking & Planlegging-seksjonen (kun planleggingsmodus). Lister 6 populære attraksjoner som anbefales/krever forhåndsbooking: Postojnahulen (stopp 8), Dinopark Funtana (9), Bayerische Zugspitzbahn + Neuschwanstein (11), Miniatur Wunderland (14) og Legoland Billund (15). Hvert kort viser aktivitetsbeskrivelse, et klikkbart stopp-merke som åpner og scroller til reiserute-kortet (`openStop`), en «Book online»-knapp med verifisert billett-URL, samt telefon (`tel:`) og e-post (`mailto:`) som alternativ. Drevet av ny `advanceBookings`-datamodell + `stopById`-hjelper. Alle bookinglenker verifisert via Tavily (bl.a. Neuschwanstein → hohenschwangau.de offisiell billettshop, Dinopark → dinopark-funtana.com). | Claude |
| 2026-06-23 | §2.6 Værvarsel: temperatur vises nå sammen med værsymbolene overalt, fra samme Open-Meteo-kall. Stripene (kart-popup + kollapset bar) bruker daglig totalvurdering (`daily.weather_code` + maks/min-temp) i stedet for kl. 12-symbol, vist som `maks°/min°C` med rød maks (`#C0392B`, ~5:1 kontrast) og blå/petrol min (`#1B4F72`, WCAG AA). Den utvidede tabellen viser timestemperatur stablet under hvert timesymbol. Ny `temps`-map og `daily`-objekt per dag i datamodellen; cache-nøkkel bumpet til `sommerferie2026-weather-v2`. Nye hjelpere `getHourTemp`, `getDaily`, `formatTemp`, `formatTempRange`, `weatherCellHtml`; mock-data utvidet med temperatur og dagssammendrag. | Claude |
| 2026-05-11 | Pakkelister flyttet til siste hovedseksjon (etter Budsjett & Praktisk) i begge moduser. Tab-raden vises alltid — i underveis-modus med én synlig tab er etiketten endret til «Daglig sjekkliste» som fungerer som overskrift. Hero-tittel forkortet til «Fra Kongsberg til Kroatia» (uten «og tilbake») og brytes ikke lenger på flere linjer — `clamp(1.4rem, 7vw, 3.75rem)` + `whitespace-nowrap` gir én linje fra ~340 px viewport opp til 1280+ px. | Claude |
| 2026-05-11 | Pakkelister filtreres nå på modus: Planlegging viser Pakkeliste/Campingvogn/For avreise; Underveis viser kun Daglig. Tab-raden skjules når kun én liste er synlig — i underveis-modus vises «Daglig sjekkliste» som h3-overskrift istedenfor en enslig tab. `syncActiveChecklist()` kjøres ved oppstart og via `$watch('mode')` for å auto-bytte aktiv tab når modus endres. Fjernet overflødig «SOMMERFERIE 2026»-pill over hero-tittelen (duplikat av logoen i navbaren). | Claude |
| 2026-05-11 | Ny hovedseksjon «Booking & Planlegging» — kun synlig i planleggingsmodus. Bookingstatus-tabellen (overnattinger og ferger) er flyttet ut av Budsjett & Praktisk og vises alltid utvidet i den nye seksjonen (ikke i accordion). Istria-alternativene flyttet til samme seksjon som accordion med ny tittel «Planlegging: Istria — 10 familievennlige alternativer». Navbar fikk en ny lenke mellom Pakkelister og Budsjett & Praktisk som filtreres bort i underveis-modus. Filteret styres av `planleggingOnly`-flagg på sections-array og en `visibleSections`-getter som brukes i både desktop- og mobil-meny. | Claude |
| 2026-05-11 | **Stor designoppgradering basert på /design-critique.** (1) Modus-toggle «Planlegging / Underveis» i navbaren — Underveis-modus skjuler budsjett, kostnadsnivå, bookingstatus og Istria-alternativer; viser kun valuta, fartsgrenser, nødnumre, bompenger og adresser. Smart default basert på dato. (2) Budsjett & Praktisk er nå én accordion med 9 underseksjoner — alle lukket som default. Mobilhøyden gikk fra ~9 100 px (11 viewports) til ~700 px. (3) Quick-access-ikoner i navbar: valuta (€) og SOS (telefon) — åpner relevant accordion-seksjon og scroller til den. (4) Sticky «I dag»-pinne under navbar når turen pågår (todayStatus === 'during') med dag X/29 og snarvei til dagens stopp. (5) Kart-markører fargekodet etter status: besøkt (muted), aktiv (sunshine med pulse-ring), kommende (petrol). (6) Kart-popup: stopp-tittel er nå lenke som åpner accordion-stoppet og scroller til det; beskrivelse-utdraget fjernet; værvarsel beholdt med tydelig «Værvarsel kommer nærmere reisen»-fallback. (7) Auto-utvid dagens stopp ved sideåpning under turen. (8) A11y: stopp-accordion fikk role=button + tabindex + Enter/Space-keydown + aria-expanded + aria-controls; alle `<th>` har scope=col; sjekkboks 16→20 px med 44 px min-row-høyde. (9) Visuelt: hero-undertittel kontrast white/60→white/85 (WCAG AA), sunshine-aksent flyttet fra «Kongsberg» til «Kroatia», pakkeliste-prefiks strippet («Klær Ann Kristin: Shorts…» → «Shorts…»), tab-labels forkortet på mobil. (10) Tabeller med horisontal scroll fikk gradient-fade på høyre kant. | Claude |
| 2026-05-05 | Budsjett-template oppdatert: lagt til `note`-felt per budsjett-post som vises diskret under beløpet. Drivstoffpost oppdatert til 11 500 NOK med forklarende note (5 500 km × 11 L/100 km × ~19 NOK/L). Alle budsjettpostene har nå kortforklaringer. | Claude |
| 2026-05-03 | §2.6 Værvarsel lagt til. Open-Meteo (gratis, ingen API-nøkkel) henter prognose ved sideåpning og cacher 1 time i localStorage. Tre visningssteder: kart-popup, kollapset Reiseplan-bar (kompakt strip med ett midday-symbol per dag) og utvidet detaljvisning (tabell med 5 tidspunkt per dag). Inline SVG-ikoner i 10 kategorier inkl. «ikke tilgjengelig». «Værvarsel-widget» fjernet fra §8 Fremtidige muligheter. | Claude |
| 2026-04-09 | Dokumentet opprettet — struktur og tomme seksjoner | Claude + Arne |
| 2026-04-10 | Teknologivalg, navigasjonsstruktur, designprinsipper, sjekkliste-strategi avklart via intervju | Claude + Arne |
| 2026-04-14 | København campingplass byttet til DCU-Camping København - Absalon, Korsdalsvej 132, Rødovre | Claude |
| 2026-04-14 | DFDS erstattet med Go Nordic Cruiseline gjennomgående i index.html og docs | Claude |
| 2026-04-14 | Warnemünde droppes; Bad Schandau 4 netter; Møns Klint reiser direkte fra Bad Schandau via Scandlines Rostock→Gedser; stops renummerert id:7–10 | Claude |
| 2026-04-13 | Løkken campingplass korrigert: Løkken Klit Camping og Hytteby, Jørgen Jensensvej 2, 9480 Løkken. Kartnavigasjon peker nå til riktig adresse. | Claude |
| 2026-04-13 | Nytt stopp 2 Silkeborg (id:2, 7.–10. juli). 11 stopp totalt. mapsQuery-felt på alle aktiviteter. getMapsUrl/getActivityMapsUrl hjelpefunksjoner. Stop-header endret fra button til div for gyldig a-nesting. Kartikon (SVG pin) i stop-header og aktivitetstemplate åpner Google Maps navigasjon. MTB-aktivitet i Bad Schandau. Alle datoer for stopp 3–11 +3 dager. | Claude |
| 2026-04-13 | 10 stopp i stops-arrayet: Lübeck (nytt), Møns Klint (nytt), Kongsberg hjemkomst (nytt, isHome:true). Berlin 4 netter, Naturkundemuseum must-do. Datoer for alle stopp 4–9 oppdatert. Kart lukker polylinjen tilbake til Kongsberg. Template og kart håndterer camping:null og isHome. | Claude |
| 2026-04-11 | Fullstendig implementasjon av index.html: kart (Leaflet), reiseplan med ukekort, pakkelister med localStorage, budsjett og praktisk info. Responsiv testing (375/768/1280px), kontrastforbedring (muted #95A5A6 oppjustert til #607080 for WCAG AA). | Claude |
| 2026-04-11 | Dokument opprettet ved splitting av Spesifikasjon-ferieplan-webside.md. Testserver-krav presisert til https_server.py. | Claude |
