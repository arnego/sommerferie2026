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
- Valutainformasjon for ulike land med vekslingskurs mot NOK
- Big Mac Index for ulike land (fra worldpopulationreview.com) for å lettere forstå kostnadsnivået i landet.

### 2.5 Praktisk informasjon
Referanseinformasjon som er nyttig underveis:
- Nødnumre per land
- Viktige adresser og telefonnumre
- Forsikringsinformasjon
- Bompenger, vignetter, miljøsoner
- Fartsbegrensninger med henger per land
- Campingplass-regler og sjekk-inn/ut-tider

---

## 3. Innholdsstruktur (Informasjonsarkitektur)

Toppmeny med fire seksjoner i rekkefølge:

1. **Kart** — interaktivt rutekart (Leaflet + OpenStreetMap) med markører for alle stopp. Klikk på markør gir info-popup. GPS-posisjon vises på kartet.
2. **Reiseplan** — dag/uke-plan der dagens plan fremheves basert på enhetens dato. Ukevis visning med etapper, kjøretid/avstand, aktiviteter og campingplass per uke.
3. **Pakkelister** — fire sjekklister (pakking, campingvogn, før avreise, daglig). Avkryssinger lagres i localStorage. Nullstill-knapp per liste.
4. **Budsjett & Praktisk** — kostnadsestimater per kategori, valutatabell (NOK → EUR/DKK/CZK) med Big Mac Index, fartsgrenser med henger, nødnumre, bompenger/vignetter, miljøsoner.

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
- **Værvarsel-widget** — automatisk værvarsel for neste destinasjon

---

## Endringslogg

| Dato | Endring | Av |
| --- | --- | --- |
| 2026-04-09 | Dokumentet opprettet — struktur og tomme seksjoner | Claude + Arne |
| 2026-04-10 | Teknologivalg, navigasjonsstruktur, designprinsipper, sjekkliste-strategi avklart via intervju | Claude + Arne |
| 2026-04-14 | DFDS erstattet med Go Nordic Cruiseline gjennomgående i index.html og docs | Claude |
| 2026-04-14 | Warnemünde droppes; Bad Schandau 4 netter; Møns Klint reiser direkte fra Bad Schandau via Scandlines Rostock→Gedser; stops renummerert id:7–10 | Claude |
| 2026-04-13 | Løkken campingplass korrigert: Løkken Klit Camping og Hytteby, Jørgen Jensensvej 2, 9480 Løkken. Kartnavigasjon peker nå til riktig adresse. | Claude |
| 2026-04-13 | Nytt stopp 2 Silkeborg (id:2, 7.–10. juli). 11 stopp totalt. mapsQuery-felt på alle aktiviteter. getMapsUrl/getActivityMapsUrl hjelpefunksjoner. Stop-header endret fra button til div for gyldig a-nesting. Kartikon (SVG pin) i stop-header og aktivitetstemplate åpner Google Maps navigasjon. MTB-aktivitet i Bad Schandau. Alle datoer for stopp 3–11 +3 dager. | Claude |
| 2026-04-13 | 10 stopp i stops-arrayet: Lübeck (nytt), Møns Klint (nytt), Kongsberg hjemkomst (nytt, isHome:true). Berlin 4 netter, Naturkundemuseum must-do. Datoer for alle stopp 4–9 oppdatert. Kart lukker polylinjen tilbake til Kongsberg. Template og kart håndterer camping:null og isHome. | Claude |
| 2026-04-11 | Fullstendig implementasjon av index.html: kart (Leaflet), reiseplan med ukekort, pakkelister med localStorage, budsjett og praktisk info. Responsiv testing (375/768/1280px), kontrastforbedring (muted #95A5A6 oppjustert til #607080 for WCAG AA). | Claude |
| 2026-04-11 | Dokument opprettet ved splitting av Spesifikasjon-ferieplan-webside.md. Testserver-krav presisert til https_server.py. | Claude |
