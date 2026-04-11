# Spesifikasjon for ferieplan-webside

## Sommerferie 2026 — Familie-roadtrip med campingvogn

> **Formål med dette dokumentet:** Komplett spesifikasjon for en statisk webside som skal bygges med Claude Code og hostes på GitHub Pages. Websiden skal hjelpe familien med å planlegge, forberede og gjennomføre en fire ukers sommerferie med campingvogn i juli 2026.
> Claude skal til enhver tid holde denne spesifikasjonen oppdatert med all informasjon om reiseplan og ønsker for websiden slik at websiden kan genereres på nytt utfra denne uten å miste for mye informasjon. 

---

## 1. Prosjektoversikt

### 1.1 Bakgrunn
Familien Goderstad ønsker en flott sommerferie i år! For reisen ønsker vi en  god plan med flotte overnattingssteder, aktiviteter og severdigheter som er tilpasset familiens behov og ønsker. 

### 1.2 Målgruppe
Websiden er kun for familien — ingen ekstern deling. Den skal fungere som et felles oppslagsverk og verktøy under hele planleggings- og reisefasen.
Websiden må være på Norsk men lokale navn kan benyttes.

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

## 2. Reiseoversikt

### 2.1 Fakta om turen
- **Avreisedato:** Tidligst 4 juli
- **Returdato:** Senest 1 august
- **Varighet:** ca. 4 uker
- **Startpunkt:** Kongsberg, Norge
- **Kjøretøy:** Campingvogn Knaus Sport 400 LK, trukket av en bil type Land Rover Discovery 4
- **Deltakere:** Ann Kristin (42 år), Arne (40 år) og William (5 år)

### 2.2 Kriterier for reiseplan
- Start og slutt i Kongsberg, Norge.
- Et besøk til familie (André og Lucia) i Tyskland i løpet av ferien på adresse: Fischerinsel 9, 10179 Berlin, Tyskland.
- Ingen overnattinger kortere enn 3 netter med mindre vi eksplisitt har kommet med ønske om det for spesifikke destinasjoner.
- Kjøreetapper må være under 6 timer per dag med minimum ett stopp underveis.

#### William-hensyn (5 år)
William er 5 år og er en viktig del av planleggingen:
- Prioriter campingplasser med lekeplass og sandstrand/bademuligheter i nærhet.
- Kjøreetapper brytes opp med barnevennlige stopp underveis (rasteplasser, lekeplasser).
- Aktivitetsforslag inkluderer barnevennlige attraksjoner og opplevelser tilpasset 5-åring.
- Dagsetapper tilpasses barnets rytme — tidlig ankomst til campingplass er å foretrekke.

### 2.3 Detaljplan
Dette er en initiell grov fordeling av ruten på 4 uker:
Uke 1: Danmark: Strand, Bading, Legoland
Uke 2: Tyskland: Berlin, Kultur
Uke 3: Tyskland: Bohemian Switzerland National Park, Slott
Uke 4: Danmark: Strand, Bading, Copenhagen

Dette kapittelet oppdateres underveis i planleggingen etterhvert som detaljene for ønskede destinasjoner, severdigheter og overnattingssteder faller på plass, og legges detaljert ut i tid.

**Plassholdersstrategi:** Websiden bygges med plassholdere for destinasjoner og campingplasser. Spesifikke steder, bookinger og aktiviteter legges til etterhvert som de bestemmes. Claude foreslår konkrete campingplasser og aktiviteter for godkjenning av Arne og Ann Kristin.

---

## 3. Funksjonelle krav

### 3.1 Rutekart
Krav til kartvisning av reiseruten:
- Interaktivt kart 
- Markører for overnattingssteder, severdigheter, etc.
- Klikk på markørene gir mer informasjon og lenker til de offisielle websidene for disse.
- Siden burde be om GPS posisjon fra enheten og markere posisjonen til bruekren på kartet.


### 3.2 Dag-for-dag / uke-for-uke plan
- Dagens plan burde fremheves og vises i en egen seksjon basert på datoen til enheten når websiden lastes. 
- Kjøretider og avstander mellom stopp.
- Planlagte aktiviteter og severdigheter
- Overnattingsinfo (campingplasser, reservasjoner)
- Fleksibilitet: "must-do" vs. "nice-to-have"

### 3.3 Sjekklister
- Pakkeliste (klær, utstyr, dokumenter, mat, underholdning for barna)
- Klargjøring av bil og campingvogn
- Før-avreise (stoppe post, vanne planter, etc.)
- Daglig sjekkliste for av- og påstigning campingplass

### 3.4 Budsjett og økonomi
- Estimert kostnad per kategori (drivstoff, overnatting, mat, aktiviteter)
- Valutainformasjon for ulike land med vekslingskurs mot NOK, 
- Big mac index resultat for ulike land (fra worldpopulationreview.com) for å lettere forstå kostnadsnivået i landet.

### 3.5 Praktisk informasjon
Referanseinformasjon som er nyttig underveis:
- Nødnumre per land
- Viktige adresser og telefonnumre
- Forsikringsinformasjon
- Bompenger, vignetter, miljøsoner
- Fartsbegrensninger med henger per land
- Campingplass-regler og sjekk-inn/ut-tider

---

## 4. Innholdsstruktur (Informasjonsarkitektur)

Toppmeny med fire seksjoner i rekkefølge:

1. **Kart** — interaktivt rutekart (Leaflet + OpenStreetMap) med markører for alle stopp. Klikk på markør gir info-popup. GPS-posisjon vises på kartet.
2. **Reiseplan** — dag/uke-plan der dagens plan fremheves basert på enhetens dato. Ukevis visning med etapper, kjøretid/avstand, aktiviteter og campingplass per uke.
3. **Pakkelister** — fire sjekklister (pakking, campingvogn, før avreise, daglig). Avkryssinger lagres i localStorage. Nullstill-knapp per liste.
4. **Budsjett & Praktisk** — kostnadsestimater per kategori, valutatabell (NOK → EUR/DKK/CZK) med Big Mac Index, fartsgrenser med henger, nødnumre, bompenger/vignetter, miljøsoner.

---

## 5. Interaktivitet og datalagring

### 5.1 Interaktive elementer
- Ekspanderbare/sammenklappbare seksjoner

### 5.2 Datalagring (localStorage)
Websiden hostes på GitHub Pages (statisk), så det finnes ingen server-side lagring. Klientside-lagring via `localStorage` skal brukes for sjekklister, men synkroniserer ikke mellom enheter.
Vi lager ingen eksport/import-funksjon for manuell synk mellom enheter foreløpig.
Vi ønsker en diskre "nullstill"-knapp per sjekkliste.
Hvis nettleserdata tømmes er de lokale dataene tapt.

### 5.3 Oppdateringsflyt
- Claude oppdaterer spesifikasjonen og endringsloggen i spesifikasjonen. 
- Claude oppdaterer reiseplanen og websiden i henhold til de ny ønskene og spesifikasjonen.
- I det lokale repoet så gjør Claude git commit med med beskrivelse av endringene som ble utført inklusive det nye tillegget i endringsloggen i spesifikasjonen
- Claude gjør git push på det lokale repoet for å publisere endringene til Github pages i github-repo: arnego/sommerferie2026


---

## 6. Designkrav

### 6.1 Designprinsipper
Overordnede prinsipper for det visuelle uttrykket:
- Enkelt og ryddig — lett å skanne raskt
- Ferie- og naturstil — sommerlig og innbydende
- Mobil-vennlig — touch-vennlige elementer
- Lett å lese i sollys

### 6.2 Sidestruktur
Én lang side (SPA)

### 6.3 Navigasjon
Toppmeny / hamburgermeny på mobil

### 6.4 Innholdshierarki
Kart > Dagens plan > Neste kjøreetappe > Sjekklister > Budsjett

### 6.5 Fargepalett
Stemning: kart-sentrert, ferie- og naturstil, lett å lese i sollys. Kun lys modus.

| Rolle | Farge | Hex |
| --- | --- | --- |
| Primær (kart/navigasjon) | Dyp petrol/havblå | `#1B4F72` |
| Sekundær (bakgrunn) | Varm sand | `#F5DEB3` |
| Bakgrunn (lysere) | Kremhvit sand | `#FBF5E6` |
| Aksent / «i dag»-markør | Solskinnsgult | `#F4A621` |
| Tekst | Mørk koksgrå | `#2C3E50` |
| Status: fullført | Grønn | `#27AE60` |
| Status: ikke startet | Grå | `#95A5A6` |

### 6.6 Typografi
Fonter lastes via Google Fonts CDN.

- **Overskrifter:** Playfair Display (serif) — gir ferie- og reisestemning
- **Brødtekst:** Inter (sans-serif) — god lesbarhet på skjerm og i sollys
- **Minimumsstørrelser mobil:** 16px brødtekst, 14px metainfo og etiketter

### 6.7 Ikoner og grafikk
- Unngå bruk av emoji
- Bruk fotografier fra de aktuelle destinasjonene i presentasjonen av disse. Fotografiene burde gi oversikt over overnattingssted eller et godt bilde av attraksjonen.
- Flagg kan brukes for landoversikt
- Bruk logoer fra de aktuelle attraksjonene eller overnattingsstedene der de er tilgjengelig 

### 6.8 Responsivt design
Krav til ulike skjermstørrelser:
- Mobil (primær bruksenhet underveis og ved gjennomgang av sjekklister)
- Nettbrett
- Desktop (planleggingsfasen)

### 6.9 Referansedesign / inspirasjon
Lenker til eksempler nettsider som har en stil vi liker:
https://www.hotelcanferrereta.com/es/
https://maps.roadtrippers.com/trips/30411788
https://thedyrt.com/


---

## 7. Tekniske krav

### 7.1 Hosting og infrastruktur
- **Hosting:** GitHub Pages
- **Repository:** `arnego/sommerferie2026`
- **Domene:** `https://arnego.github.io/sommerferie2026/`

### 7.2 Teknologivalg
- **Stack:** Ren HTML-fil med CDN-baserte biblioteker — ingen build-steg, ingen npm
- **Kart:** Leaflet.js + OpenStreetMap — gratis, ingen API-nøkkel nødvendig
- **CSS-rammeverk:** Tailwind CSS via CDN (play-cdn)
- **Reaktivitet:** Alpine.js via CDN — trekkspill, tabs, sjekklister, mobilmeny
- **Fonter:** Google Fonts via CDN (Playfair Display + Inter)
- **Ingen PWA** — kun Chrome (iOS + desktop)
- **Nettleserkompatibilitet:** Chrome på iOS og desktop

### 7.7 Sikkerhet og personvern
Websiden inneholder personlig reiseinformasjon så repoet skal være privat.
Websiden kan få inneholde sensitiv info i koden (passord, bookingref, etc.).

#### Sensitive data — tillatt direkte i koden
Repoet er privat. Følgende kan ligge direkte i `index.html` uten hashing eller kryptering:
- Adresser og kontaktinformasjon (f.eks. familiebesøk)
- Booking-referanser og reservasjonsnumre
- Passord og PIN-koder (campingplass-porter, safe-koder, Wi-Fi-passord)

### 7.8 Sjekkliste-innhold
Claude genererer komplette sjekklister tilpasset campingvogn-tur med 5-åring:
- **Pakkeliste** — klær per person, utstyr, dokumenter, underholdning for William
- **Campingvogn-sjekkliste** — teknisk klargjøring (koblinger, lys, gass, vann, sikkerhet), nødvendige vignetter og plaketter
- **Før avreise** — post, planter, hus, strøm, alarm
- **Daglig sjekkliste** — av-/påstigning campingplass (ankomst og avreise)

---

## 9. Fremtidige muligheter (utenfor scope)
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
| 2026-04-10 | Ny index.html bygget med Leaflet, Tailwind, Alpine.js og plassholder-rute | Claude |
