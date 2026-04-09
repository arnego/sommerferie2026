# Spesifikasjon for ferieplan-webside

## Sommerferie 2026 — Familie-roadtrip med campingvogn

> **Formål med dette dokumentet:** Komplett spesifikasjon for en statisk webside som skal bygges med Claude Code og hostes på GitHub Pages. Websiden skal hjelpe familien med å planlegge, forberede og gjennomføre en fire ukers sommerferie med campingvogn i juli 2026.

---

## 1. Prosjektoversikt

### 1.1 Bakgrunn
<!-- Kort beskrivelse av ferien og hvorfor vi lager en webside for den -->

### 1.2 Målgruppe
Websiden er kun for familien — ingen ekstern deling. Den skal fungere som et felles oppslagsverk og verktøy under hele planleggings- og reisefasen.

### 1.3 Bruksscenarier
<!-- Beskriv typiske situasjoner der websiden brukes, f.eks.: -->
<!-- - Planlegging hjemme på PC i ukene før avreise -->
<!-- - Sjekke neste stopp fra mobilen mens man er underveis -->
<!-- - Slå opp aktiviteter og reservasjoner for dagen -->
<!-- - Pakkeliste-gjennomgang kvelden før avreise -->

### 1.4 Mål og suksesskriterier
<!-- Hva betyr det at websiden er "vellykket"? F.eks.: -->
<!-- - All relevant ferieinfo samlet på ett sted -->
<!-- - Fungerer godt på mobil uten nettilgang (offline) -->
<!-- - Enkel å oppdatere underveis -->

---

## 2. Reiseoversikt

### 2.1 Fakta om turen
<!-- Fyll inn når kjent: -->
- **Avreisedato:** <!-- TBD -->
- **Returdato:** <!-- TBD -->
- **Varighet:** ca. 4 uker
- **Startpunkt:** Kongsberg, Norge
- **Kjøretøy:** Personbil med campingvogn
- **Deltakere:** <!-- Antall voksne og barn, barnas alder -->

### 2.2 Ruteplan (overordnet)
<!-- Hovedruten med stoppesteder, f.eks.: -->
<!-- Kongsberg → Danmark → Nord-Tyskland → Nederland → Schwarzwald → Østerrike/Alpene → retur -->

### 2.3 Ukeoversikt
<!-- Grov fordeling av ruten på 4 uker: -->
<!-- Uke 1: ... -->
<!-- Uke 2: ... -->
<!-- Uke 3: ... -->
<!-- Uke 4: ... -->

---

## 3. Funksjonelle krav

### 3.1 Rutekart
<!-- Krav til kartvisning av reiseruten. Vurder: -->
<!-- - Interaktivt kart vs. statisk bilde -->
<!-- - Markører for overnattingssteder, severdigheter, etc. -->
<!-- - Kartleverandør (Leaflet/OpenStreetMap, Google Maps, etc.) -->

### 3.2 Dag-for-dag / uke-for-uke plan
<!-- Hvordan skal den detaljerte planen presenteres? -->
<!-- - Kjøretider og avstander mellom stopp -->
<!-- - Planlagte aktiviteter og severdigheter -->
<!-- - Overnattingsinfo (campingplasser, reservasjoner) -->
<!-- - Fleksibilitet: "must-do" vs. "nice-to-have" -->

### 3.3 Sjekklister
<!-- Hvilke sjekklister trengs? F.eks.: -->
<!-- - Pakkeliste (klær, utstyr, dokumenter, mat, underholdning for barna) -->
<!-- - Campingvogn-klargjøring -->
<!-- - Bil-klargjøring -->
<!-- - Før-avreise (stoppe post, vanne planter, etc.) -->
<!-- - Daglig sjekkliste for av- og påstigning campingplass -->

### 3.4 Budsjett og økonomi
<!-- Hvordan skal budsjettet presenteres? -->
<!-- - Budsjettramme per kategori (drivstoff, overnatting, mat, aktiviteter) -->
<!-- - Forhåndsbetalt vs. løpende kostnader -->
<!-- - Valutainformasjon for ulike land -->

### 3.5 Praktisk informasjon
<!-- Referanseinformasjon som er nyttig underveis: -->
<!-- - Nødnumre per land -->
<!-- - Viktige adresser og telefonnumre -->
<!-- - Forsikringsinformasjon -->
<!-- - Bompenger, vignetter, miljøsoner -->
<!-- - Fartsbegrensninger med henger per land -->
<!-- - Campingplass-regler og sjekk-inn/ut-tider -->

### 3.6 Notater og logg
<!-- Mulighet for å skrive notater? -->
<!-- - Reisedagbok -->
<!-- - Endringer i planen underveis -->
<!-- - Tips og erfaringer for neste tur -->

### 3.7 Offline-tilgang
<!-- Krav til bruk uten internett: -->
<!-- - Service worker for offline caching -->
<!-- - Nedlastbart innhold -->
<!-- - Hva MÅ fungere offline? -->

---

## 4. Innholdsstruktur (Informasjonsarkitektur)

### 4.1 Sidestruktur
<!-- Skal det være én lang side (SPA) eller flere sider? -->
<!-- Foreslått navigasjonsstruktur: -->

### 4.2 Navigasjon
<!-- Hvordan finner brukeren frem? -->
<!-- - Toppmeny / hamburgermeny på mobil -->
<!-- - Hurtignavigasjon til "i dag" / neste stopp -->
<!-- - Breadcrumbs eller tilbake-knapp -->

### 4.3 Innholdshierarki
<!-- Prioritering av informasjon — hva er viktigst å se først? -->
<!-- F.eks.: Dagens plan > Neste kjøreetappe > Kart > Sjekklister > Budsjett -->

---

## 5. Interaktivitet og datalagring

### 5.1 Interaktive elementer
<!-- Hvilke UI-elementer skal være interaktive? F.eks.: -->
<!-- - Ekspanderbare/sammenklappbare seksjoner -->
<!-- - Faner (tabs) for å bytte mellom uker/dager -->
<!-- - Avhukbare sjekklister -->
<!-- - Filtrering (f.eks. vis kun "must-do" aktiviteter) -->
<!-- - Søkefunksjon -->

### 5.2 Datalagring (localStorage)
**Viktig teknisk begrensning:** Websiden hostes på GitHub Pages (statisk), så det finnes ingen server-side lagring. Klientside-lagring via `localStorage` kan brukes, men synkroniserer **ikke** mellom enheter.

<!-- Avgjørelser som må tas: -->
<!-- - Hvilke data skal lagres i localStorage? (sjekklistestatus, notater, preferanser) -->
<!-- - Skal det bygges eksport/import-funksjon (JSON) for manuell synk mellom enheter? -->
<!-- - Skal det være en "nullstill"-knapp? -->
<!-- - Hvordan håndteres tap av data (tømming av nettleserdata)? -->

### 5.3 Oppdateringsflyt
<!-- Hvordan oppdateres websiden med nytt innhold? -->
<!-- - GitHub-repo: arnego/sommerferie2026 -->
<!-- - Prosess for å pushe oppdateringer (Claude in Chrome, manuell Git, etc.) -->
<!-- - Versjonering av innhold -->

---

## 6. Designkrav

### 6.1 Designprinsipper
<!-- Overordnede prinsipper for det visuelle uttrykket, f.eks.: -->
<!-- - Enkelt og ryddig — lett å skanne raskt -->
<!-- - Ferie- og naturstil — varm og innbydende -->
<!-- - Mobil-først — touch-vennlige elementer -->
<!-- - Godt lesbart i sterkt sollys -->

### 6.2 Fargepalett
<!-- Definer farger. Vurder: -->
<!-- - Primærfarge, sekundærfarge, aksentfarge -->
<!-- - Bakgrunnsfarger (lys og mørk modus?) -->
<!-- - Farger for statusindikatorer (fullført, pågående, ikke startet) -->

### 6.3 Typografi
<!-- Skriftvalg: -->
<!-- - Overskrifter -->
<!-- - Brødtekst -->
<!-- - Web-safe fonter eller Google Fonts? -->
<!-- - Minimumsstørrelse for lesbarhet på mobil -->

### 6.4 Ikoner og grafikk
<!-- Bruk av ikoner (emoji, SVG-ikoner, ikonbibliotek?) -->
<!-- Illustrasjoner eller fotografier? -->
<!-- Flagg for landoversikt? -->

### 6.5 Responsivt design
<!-- Krav til ulike skjermstørrelser: -->
<!-- - Mobil (primær bruksenhet underveis) -->
<!-- - Nettbrett -->
<!-- - Desktop (planleggingsfasen) -->
<!-- - Breakpoints -->

### 6.6 Mørk modus
<!-- Skal websiden støtte mørk modus? -->
<!-- - Automatisk basert på systeminnstillinger? -->
<!-- - Manuell veksling? -->

### 6.7 Referansedesign / inspirasjon
<!-- Lenker til eksempler eller skjermbilder av nettsider som har en stil vi liker -->

---

## 7. Tekniske krav

### 7.1 Hosting og infrastruktur
- **Hosting:** GitHub Pages
- **Repository:** `arnego/sommerferie2026`
- **Domene:** `https://arnego.github.io/sommerferie2026/`

### 7.2 Teknologivalg
<!-- Avgjørelser som må tas: -->
<!-- - Ren HTML/CSS/JS, eller rammeverk (React, Vue, Svelte, Astro, etc.)? -->
<!-- - CSS-rammeverk (Tailwind, Bootstrap, etc.)? -->
<!-- - Bundler/build-steg, eller direkte i nettleseren? -->
<!-- - Skal Claude Code kunne bygge og deploye direkte? -->

### 7.3 Ytelse
<!-- Krav til lastetid og størrelse: -->
<!-- - Maks buntstørrelse -->
<!-- - Bildeoptimalisering -->
<!-- - Lazy loading -->

### 7.4 Nettleserkompatibilitet
<!-- Hvilke nettlesere og versjoner skal støttes? -->
<!-- - Chrome (Android/desktop) -->
<!-- - Safari (iOS/macOS) -->
<!-- - Firefox -->

### 7.5 PWA (Progressive Web App)
<!-- Skal websiden kunne installeres som en app? -->
<!-- - Web App Manifest -->
<!-- - Service Worker for offline-bruk -->
<!-- - Ikon for hjemskjerm -->

### 7.6 Tilgjengelighet
<!-- Grunnleggende tilgjengelighetskrav: -->
<!-- - Semantisk HTML -->
<!-- - ARIA-labels der nødvendig -->
<!-- - Tastaturnavigasjon -->

### 7.7 Sikkerhet og personvern
<!-- Websiden inneholder personlig reiseinformasjon: -->
<!-- - Skal repoet være privat eller offentlig? -->
<!-- - Ingen sensitiv info i koden (passord, bookingref, etc.) -->

---

## 8. Innholdsplan og tidslinje

### 8.1 Innhold som må produseres
<!-- Liste over alt innhold som skal lages, f.eks.: -->
<!-- - Detaljert ruteplan med koordinater -->
<!-- - Campingplassinformasjon per stopp -->
<!-- - Aktivitetsliste per destinasjon -->
<!-- - Pakkelister -->
<!-- - Budsjettoversikt -->
<!-- - Praktisk info per land -->

### 8.2 Tidslinje
<!-- Milepæler fra nå til avreise: -->
<!-- - Spesifikasjon ferdig: [dato] -->
<!-- - Første versjon av websiden: [dato] -->
<!-- - Rute og campingplasser booket: [dato] -->
<!-- - Innhold komplett: [dato] -->
<!-- - Avreise: [dato] -->

### 8.3 Vedlikehold underveis
<!-- Hvordan oppdateres websiden under ferien? -->
<!-- - Hvem oppdaterer? -->
<!-- - Hvor ofte? -->
<!-- - Hva slags endringer er typiske? -->

---

## 9. Fremtidige muligheter (utenfor scope)

<!-- Idéer som kan vurderes senere, men som ikke er del av første versjon: -->
<!-- - Bildegalleri / reisedagbok med bilder -->
<!-- - Integrasjon med værdata (API) -->
<!-- - GPS-sporing av ruten -->
<!-- - Deling med familie/venner -->
<!-- - Flerspråklig innhold -->

---

## Endringslogg

| Dato | Endring | Av |
|------|---------|-----|
| 2026-04-09 | Dokumentet opprettet — struktur og tomme seksjoner | Claude + Arne |
