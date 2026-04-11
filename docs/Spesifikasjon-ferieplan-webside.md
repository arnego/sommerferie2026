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

#### Ruteoversikt

| # | Sted | Land | Ankomst | Avreise | Netter | Uke |
|---|------|------|---------|---------|--------|-----|
| 1 | Løkken Strand | DK | 4. juli | 8. juli | 4 | 28 |
| 2 | Billund (Legoland) | DK | 8. juli | 11. juli | 3 | 28 |
| 3 | Hamburg | DE | 11. juli | 14. juli | 3 | 28-29 |
| 4 | Berlin | DE | 14. juli | 19. juli | 5 | 29 |
| 5 | Bad Schandau (Saksisk Sveits) | DE | 19. juli | 22. juli | 3 | 30 |
| 6 | Warnemunde (transit) | DE | 22. juli | 23. juli | 1* | 30 |
| 7 | Kobenhavn | DK | 23. juli | 27. juli | 4 | 30 |
| 8 | Goteborg | SE | 27. juli | 30. juli | 3 | 31 |
| 9 | Kongsberg | NO | 30. juli | - | Hjemme | 31 |

*Transitstopp med stranddag -- unntak fra 3-netter-regelen.

**Totalt:** 26 overnattinger, ca. 2 455 km kjoring + 3 fergestrekninger. Hjemme 30. juli.

#### Kjoreetapper

| Fra | Til | Avstand | Kjoretid | Rute |
|-----|-----|---------|----------|------|
| Kongsberg | Larvik (ferge) | 85 km | 1 t 10 min | E18 sor |
| Larvik | Hirtshals (ferge) | - | 3 t 45 min | Color Line SuperSpeed |
| Hirtshals | Lokken | 55 km | 45 min | Rute 55 |
| Lokken | Billund | 185 km | 2 t 30 min | Via Viborg |
| Billund | Hamburg | 340 km | 4 t 30 min | E45/A7 |
| Hamburg | Berlin | 290 km | 3 t 45 min | A24 |
| Berlin | Bad Schandau | 250 km | 3 t 15 min | A13/A17 |
| Bad Schandau | Warnemunde | 400 km | 5 t 15 min | Via Dresden-Leipzig (A13/A14/A19) |
| Warnemunde | Gedser (ferge) | - | 2 t | Scandlines |
| Gedser | Kobenhavn | 170 km | 2 t 15 min | E47/E55 |
| Kobenhavn | Goteborg | 330 km | 4 t 30 min + 20 min ferge | Via Helsingor-Helsingborg (ForSea) |
| Goteborg | Kongsberg | 350 km | 4 t 30 min | E6/E18 |

Alle kjoretider er beregnet med campingvogn (ca. 80 km/t snitt).

#### Ferger

**Color Line SuperSpeed (Larvik-Hirtshals)**
- Overfartstid: ca. 3 t 45 min
- Avganger: 2-3 daglig i juli (typisk 07:30 og 15:30 fra Larvik)
- Estimert pris (bil + campingvogn + 2 voksne + 1 barn): 2 500 - 4 500 NOK en vei
- Nettside: https://www.colorline.no/larvik-hirtshals
- Lekerom ombord for barn

**Scandlines (Rostock-Gedser)**
- Overfartstid: ca. 2 timer
- Avganger: ca. hver 1,5-2 time
- Estimert pris (bil + campingvogn, passasjerer inkl.): 1 400 - 2 300 NOK en vei
- Nettside: https://www.scandlines.com/
- Lekeomrade og kafeteria ombord

**ForSea (Helsingor-Helsingborg)**
- Overfartstid: ca. 20 minutter
- Avganger: hvert 15-20 minutt, dognkontinuerlig
- Estimert pris (bil + campingvogn): 1 000 - 1 700 NOK en vei
- Nettside: https://www.forsea.se/

---

#### Stopp 1: Lokken Strand, Danmark (4 netter: 4.-8. juli)

**Campingplass: Lokken Klit Camping**
- Adresse: Furreby Kirkevej 97, 9480 Lokken, Danmark
- Nettside: https://www.loekkenklit.dk/
- Fasiliteter: Innendors svommebasseng med barnebasseng, stor lekeplass, trampoliner, minigolf, butikk, moderne sanitaeranlegg med familierom
- Ca. 800 meter til Lokken Strand
- Tar imot campingvogn med stromtilkobling (16A CEE)
- Booket: Nei
- Bookingref: -

**Aktiviteter:**

| Aktivitet | Type | Prioritet | Beskrivelse |
|-----------|------|-----------|-------------|
| Lokken Strand | Strand/bading | Must-do | En av Danmarks bredeste sandstrender. Sandslottbygging, lek i bolgene. Ikoniske hvite badehus. |
| Rubjerg Knude Fyr | Natur/severdighet | Must-do | Besomt fyrtarn omgitt av sandklitter. 15 min kjoring. Lett turvei opp. |
| Dagstur til Skagen / Grenen | Natur/severdighet | Must-do | 1 t 15 min kjoring. Grenen der to hav moetes -- William kan sta i to hav samtidig. Sandormen (traktor-buss) kjorer ut til spissen. |
| Faarup Sommerland | Forlystelsespark | Nice-to-have | Danmarks storste forlystelsespark med vannpark. 25 min kjoring. Barneland for de minste. |
| Nordsoen Oceanarium (Hirtshals) | Akvarium | Nice-to-have | Nordeuropas storste akvarium med havsaeler og haier. 40 min kjoring. |
| Raabjerg Mile | Natur | Nice-to-have | Danmarks storste vandresandklit. Unikt landskap som minner om en orken. |

**Tips:**
- Juli er hoysesong -- book campingplass tidlig
- CampingKey Europe anbefales for rabatter og innsjekk pa danske campingplasser
- Husk solkrem og vindjakke -- vestkysten kan vaere blaseende

---

#### Stopp 2: Billund, Danmark (3 netter: 8.-11. juli)

**Campingplass: Billund Camping**
- Adresse: Ellehammers Alle 2, 7190 Billund, Danmark
- Nettside: https://www.billund-camping.dk/
- Fasiliteter: Gangavstand til LEGOLAND (under 1 km), lekeplass, butikk, moderne sanitaeranlegg med familierom, Wi-Fi
- Tar imot campingvogn med stromtilkobling
- Booket: Nei
- Bookingref: -

**Aktiviteter:**

| Aktivitet | Type | Prioritet | Beskrivelse |
|-----------|------|-----------|-------------|
| LEGOLAND Billund | Forlystelsespark | Must-do | Hovedattraksjonen. DUPLO Land og LEGO City for 5-aringer. Miniland. Planlegg en hel dag. https://www.legoland.dk/ |
| LEGO House | Museum/opplevelse | Must-do | "Home of the Brick" i Billund sentrum. Interaktive byggesoner. 3-4 timer. https://www.legohouse.com/ |
| Givskud Zoo (LEGOLAND Wildlife Park) | Dyrepark/safari | Must-do | Safari-park med lover, giraffer, elefanter. 25 min kjoring. https://www.givskudzoo.dk/ |
| Lalandia Billund (Aquadome) | Badeland | Nice-to-have | Tropisk badeland med vannrutsjebaner. Dagsbillett mulig. Perfekt pa regnvaersdager. |
| Kongernes Jelling | UNESCO/historie | Nice-to-have | Vikinghistorie med interaktivt opplevelsessenter. 20 min kjoring. Gratis inngang. |

**Tips:**
- Vurder 2-dagers billett til LEGOLAND
- LEGOLAND apner vanligvis kl. 10:00 -- vaer tidlig for aa unnga koer

---

#### Stopp 3: Hamburg, Tyskland (3 netter: 11.-14. juli)

**Campingplass: Campingplatz Stover Strand International**
- Adresse: Stover Strand 10, 21423 Drage (Elbmarsch), Tyskland
- Nettside: https://www.stfreizeit.de/
- Fasiliteter: Stor lekeplass, sandstrand ved Elben med bademuligheter, innendors svommebasseng, minimarked, restaurant, sportsaktiviteter, Wi-Fi
- Ca. 35 km sorost for Hamburg sentrum (ca. 40 min med bil)
- Tar imot campingvogn med stromtilkobling (16A)
- Booket: Nei
- Bookingref: -

**Aktiviteter:**

| Aktivitet | Type | Prioritet | Beskrivelse |
|-----------|------|-----------|-------------|
| Miniatur Wunderland | Museum/attraksjon | Must-do | Verdens storste modelljernbaneutstilling i Speicherstadt. Bestill billetter online pa forhand! 3-4 timer. https://www.miniatur-wunderland.com/ |
| Tierpark Hagenbeck | Dyrepark | Must-do | Hamburgs dyrepark med tropisk akvarium, strykedyr-omrade for barn. Halv dag. https://www.hagenbeck.de/ |
| Hafenrundfahrt (havnecruise) | Batkjoring | Must-do | Barkas-tur i Hamburgs havn fra Landungsbrucken. Ca. 1 time. Store containerskip. |
| Planten un Blomen | Park/lek | Nice-to-have | Gratis bypark med stor lekeplass og vannlekeplass om sommeren. Vannlysspill om kvelden. |

**Tips:**
- Umweltplakette (gron miljuplakett) kreves for kjoring i Hamburg -- bestill fra umwelt-plakette.de (15-30 EUR)
- Miniatur Wunderland er alltid utsolgt i hoysesong -- bestill billetter i god tid!

---

#### Stopp 4: Berlin, Tyskland (5 netter: 14.-19. juli)

**Campingplass: DCC-Campingplatz Berlin-Gatow**
- Adresse: Kladower Damm 213-217, 14089 Berlin-Gatow, Tyskland
- Nettside: https://www.dccberlin.de/
- Fasiliteter: Stor lekeplass, sandstrand ved Havel med bademuligheter, kajakkutleie, kiosk, grillplasser, Wi-Fi
- Ca. 22 km fra Fischerinsel (ca. 40 min med kollektiv, 30-40 min med bil)
- Tar imot campingvogn med stromtilkobling (16A CEE)
- Booket: Nei
- Bookingref: -

**Familiebesok: Andre og Lucia**
- Adresse: Fischerinsel 9, 10179 Berlin
- Sentralt i Berlin Mitte, ved Spree-elven

**Aktiviteter:**

| Aktivitet | Type | Prioritet | Beskrivelse |
|-----------|------|-----------|-------------|
| Besok Andre og Lucia | Familiebesok | Must-do | Fischerinsel 9. Fine spaserturer langs Spree i naerheten. |
| Berlin Zoo | Dyrehage | Must-do | En av Europas mest artsrike. Akvarium inkludert. Halv til hel dag. https://www.zoo-berlin.de/ |
| LEGOLAND Discovery Centre | Innendors opplevelse | Must-do | LEGO-opplevelsessenter med byggeverksteder og 4D-kino. Bestill online. 2-3 timer. https://www.legolanddiscoverycentre.com/berlin/ |
| Tropical Islands | Badeland/tropisk | Must-do | Verdens storste innendors tropiske badeanlegg. Ca. 60 km sor for Berlin (dagstur). Hel dag. https://www.tropical-islands.de/ |
| Naturkundemuseum | Museum | Nice-to-have | Verdens storste monterte dinosaurskjelett. Barn elsker dinosauravdelingen. 2-3 timer. https://www.museumfuernaturkunde.berlin/ |
| Tempelhofer Feld | Park/friluft | Nice-to-have | Gammel flyplass omgjort til enorm bypark. Sykling, drageflying med William. Gratis. |

**Tips:**
- Umweltplakette kreves ogsa i Berlin
- Vurder Berlin WelcomeCard for 5 dager (dekker kollektivtransport + rabatter)
- Campingplassen ved Havel er fin for bading pa varme dager

---

#### Stopp 5: Bad Schandau / Saksisk Sveits, Tyskland (3 netter: 19.-22. juli)

**Campingplass: Campingplatz Ostrauer Muhle**
- Adresse: Ostrauer Muhle 15, 01814 Bad Schandau, Tyskland
- Nettside: https://www.ostrauer-muehle.de/
- Fasiliteter: Lekeplass, Elbe-elven i naerheten, felleskjokken, turstier direkte fra plassen, restauranter i gangavstand
- Ligger direkte i Bad Schandau ved foten av nasjonalparken
- Tar imot campingvogn med stromtilkobling
- Booket: Nei
- Bookingref: -

**Aktiviteter:**

| Aktivitet | Type | Prioritet | Beskrivelse |
|-----------|------|-----------|-------------|
| Basteibroen (Basteibracke) | Natur/utsiktspunkt | Must-do | Ikonisk steinbro 194 meter over Elben. Kort sti fra parkering (15-20 min). Hold godt i William -- bratte stup! Ga tidlig. |
| Festung Konigstein | Festning/historie | Must-do | En av Europas storste fjellsfestninger. Kanoner, tunneler, utsikt. Halv dag. https://www.festung-koenigstein.de/ |
| Kirnitzschtalbahn | Historisk trikk | Must-do | Historisk sporvogn fra Bad Schandau til Lichtenhainer Wasserfall. William vil elske trikketuren! |
| Amselsee i Rathen | Natur/bat | Nice-to-have | Rolig innsjovandring med robatutleie. |
| Elbeskipsfart (hjuldampere) | Batkjoring | Nice-to-have | Historiske hjuldampere pa Elben. Fantastisk utsikt fra vannet. https://www.saechsische-dampfschiffahrt.de/ |
| Pirna gammelby | By/kultur | Nice-to-have | Sjarmerende gammelby med fargerike hus. 15 min kjoring. Is og spasertur. |

**Tips:**
- Ingen Umweltzone i Bad Schandau (men Dresden har -- unnga a kjore inn i sentrum)
- Ga til Bastei tidlig pa morgenen for a unnga folkemengder
- Bad Schandau har historisk personheis opp til utsiktspunkt

---

#### Stopp 6: Warnemunde, Tyskland (1 natt transit: 22.-23. juli)

**Campingplass: Campingpark Warnemunde**
- Adresse: Parkstrasse 1, 18119 Rostock-Warnemunde, Tyskland
- Nettside: https://www.campingpark-warnemuende.de/
- Fasiliteter: Gangavstand til sandstrand (ca. 800m), lekeplass, sanitaeranlegg, Wi-Fi
- Tar imot campingvogn med stromtilkobling (16A)
- Booket: Nei
- Bookingref: -

**Aktiviteter:**

| Aktivitet | Type | Prioritet | Beskrivelse |
|-----------|------|-----------|-------------|
| Warnemunde Strand | Strand/bading | Must-do | Bred sandstrand med grunt, barnevennlig vann. Strandkurver (Strandkorb) kan leies. |
| Warnemunde fyrtarn | Severdighet | Nice-to-have | Utsikt fra fyrtarnet. Like ved strand og havn. |
| Se pa ferger i havnen | Underholdning | Nice-to-have | Store Scandlines-ferger -- spennende for William. |

**Tips:**
- Ingen Umweltzone i Warnemunde/Rostock
- Scandlines-fergen til Gedser gar fra Rostock fergeterminal (ikke Warnemunde) -- ca. 20 min kjoring

---

#### Stopp 7: Kobenhavn, Danmark (4 netter: 23.-27. juli)

**Campingplass: DCU-Camping Charlottenlund Fort**
- Adresse: Strandvejen 144B, 2920 Charlottenlund, Danmark
- Nettside: https://www.dcu.dk/campingpladser/charlottenlund-fort
- Fasiliteter: Lekeplass, direkte strandtilgang (badestrand), minimarked, vaskerom, grillplasser, Wi-Fi
- Ca. 8 km nord for Kobenhavns sentrum, buss 14 til sentrum
- Historisk festningsomrade ved Oresund
- Tar imot campingvogn med stromtilkobling
- Booket: Nei
- Bookingref: -

**Aktiviteter:**

| Aktivitet | Type | Prioritet | Beskrivelse |
|-----------|------|-----------|-------------|
| Tivoli Gardens | Forlystelsespark | Must-do | Verdens nest eldste forlystelsespark (1843). Mange karuseller for sma barn. Barn under 8 gratis m/voksen. https://www.tivoli.dk/ |
| Bakken (Dyrehavsbakken) | Forlystelsespark | Must-do | Verdens eldste forlystelsespark, gratis inngang! Ligger i Dyrehaven med tamme hjorter. https://www.bakken.dk/ |
| Den Bla Planet | Akvarium | Must-do | Nordeuropas storste akvarium. Haier, havskildpadder, interaktive utstillinger. https://denblaaplanet.dk/ |
| Kobenhavns Zoo | Dyrehage | Nice-to-have | Elefanter, isbjorn, lover. Eget barne-zoo der William kan klappe dyr. https://www.zoo.dk/ |
| Amager Strandpark | Strand/bading | Nice-to-have | Kunstig sandstrand med grunt barnevennlig vann og lekeplasser. Gratis. |
| Nyhavn + kanalbat | By/sightseeing | Nice-to-have | Fargerike hus, is, batkjoring pa kanalene (ca. 30 min). |
| Experimentarium | Vitensenter | Nice-to-have | Interaktivt vitensenter med hands-on utstillinger for barn. https://www.experimentarium.dk/ |

**Tips:**
- Charlottenlund Fort er ekstremt populaer i juli -- book sa tidlig som mulig!
- Kombiner Bakken med tur i Dyrehaven (tamme hjorter)
- Pa vei fra Kobenhavn til Goteborg: stopp ved Kronborg slott i Helsingor (Hamlets slott) for fergen til Helsingborg

---

#### Stopp 8: Goteborg, Sverige (3 netter: 27.-30. juli)

**Campingplass: Lisebergs Camping & Stugby -- Karralund**
- Adresse: Olbersgatan 11, 416 55 Goteborg, Sverige
- Nettside: https://www.liseberg.se/boende/karralund/
- Fasiliteter: Lekeplass, utendors svommebasseng (sommer), minigolf, sykkelutleie, vaskerom, butikk, Wi-Fi
- Ca. 3 km fra sentrum, 15 min gang/sykkel til Liseberg
- Tar imot campingvogn med stromtilkobling
- Booket: Nei
- Bookingref: -

**Aktiviteter:**

| Aktivitet | Type | Prioritet | Beskrivelse |
|-----------|------|-----------|-------------|
| Liseberg | Forlystelsespark | Must-do | Skandinavias storste forlystelsespark. Kaniner-omradet for sma barn (fra 90 cm). https://www.liseberg.se/ |
| Universeum | Vitensenter/akvarium | Must-do | Nordeuropas storste vitensenter. Regnskogavdeling, haier, vannlek. https://www.universeum.se/ |
| Slottsskogen | Park/dyrepark | Must-do | Stor bypark med gratis dyrepark (seler, pingviner, elger). Lekeplasser. Gratis. |
| Maritiman | Skipsmuseum | Nice-to-have | Verdens storste flytende skipsmuseum. Utforsk u-bater og destroyere. https://www.maritiman.se/ |
| Paddan-batene | Batkjoring | Nice-to-have | Sightseeing gjennom kanalene. Lav brohoyde -- barn synes det er morsomt! Ca. 50 min. |

**Tips:**
- Siste stopp for ferien -- ta det rolig og nyt byen
- 30. juli: Kjor hjem til Kongsberg via E6/E18 (ca. 350 km, 4,5 timer)

---

#### Ukeoversikt

**Uke 28 (4.-11. juli): Danmark -- strand og Legoland**
Lokken Strand (4 netter) + Billund/Legoland (3 netter). Strandliv pa den danske vestkysten, dagstur til Skagen, deretter tre dager med LEGOLAND, LEGO House og Givskud Zoo.

**Uke 29 (11.-19. juli): Tyskland -- Hamburg og Berlin**
Hamburg (3 netter) + Berlin (5 netter). Miniatur Wunderland og Hagenbeck i Hamburg, deretter Berlin med familiebesok hos Andre og Lucia, Berlin Zoo, LEGOLAND Discovery Centre og Tropical Islands.

**Uke 30 (19.-27. juli): Saksisk Sveits og Kobenhavn**
Bad Schandau (3 netter) + Warnemunde transit (1 natt) + Kobenhavn (4 netter). Basteibroen, Konigstein festning og naturopplevelser i nasjonalparken, deretter stranddag i Warnemunde og ferge til Danmark. Kobenhavn med Tivoli, Bakken og Den Bla Planet.

**Uke 31 (27.-30. juli): Goteborg og hjemreise**
Goteborg (3 netter). Liseberg, Universeum og Slottsskogen. Hjemkjoring 30. juli via E6/E18.

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
| 2026-04-11 | Seksjon 2.3 oppdatert med komplett ruteforslag: 8 stopp, 26 netter, campingplasser, aktiviteter, kjoreetapper og ferger | Claude |
| 2026-04-11 | Fullstendig implementasjon av index.html: kart (Leaflet), reiseplan med ukekort, pakkelister med localStorage, budsjett og praktisk info. Responsiv testing (375/768/1280px), kontrastforbedring (muted #95A5A6 darknet til #607080 for WCAG AA). Fase 1-7 gjennomfort. | Claude |
