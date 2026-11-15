# bumlebusiness
Dette er vores Github project, hvor vi skal bruge SCRUM og indlæse, vise, analysere og visualisere logs


## Kom i gang

Kræver Python 3. Kør følgende i projektets rodmappe:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

På Windows aktiveres miljøet med `.venv\Scripts\activate` i stedet for `source .venv/bin/activate`.


# Data Loader – Udvikling og implementering

Denne sektion beskriver udviklingen af `data_loader.py`-modulet, inklusive implementeringsvalg, parsingmetoder, fejlhåndtering og udførte tests.

## 1. Indledende opsætning og fillæsning

Oprettede `data_loader.py`-modulet til at håndtere læsningen og processeringen af de rå VPN-sikkerhedslogs.

- Tilføjede filen `cyber_security_log_sample.txt` til projektets data-mappe.
- Implementerede funktionen `load_logs()`.
- Brugte den indbyggede funktion i Python til at tilgå `.txt`-filen.
- `readlines()` blev brugt til at hente de individuelle loglinjer ind i en liste.
- Tilføjede UTF-8 encoding til at sikre korrekt teksthåndtering.
- Brugte oprindeligt `pathlib` til filhåndtering. Dette blev der stillet spørgsmål til i gruppen, da koden var længere end ved brug af Pythons indbyggede `open()`-funktion.

De indledende tests bekræftede, at filen indeholdt 541 loglinjer.

## 2. Log parsing og dataudtræk

Udviklede `parse_log()`-funktionen til at konvertere de rå loglinjer til en struktureret Python dictionary.

### Den indledende opsætning med `split()`:

Oprindeligt blev der eksperimenteret med Pythons indbyggede `split()`-funktion til at separere en loglinje i de individuelle felter.

Under tests viste det sig dog, at der var problemer med `msg`-sektionen i loglinjerne, da disse indeholder anførselstegn og mellemrum.

For eksempel:

`msg="User authenticated successfully"`

Ved at bruge `split()` ville denne besked blive opdelt i flere forskellige dele og derved gøre dataanalyse og opdelingen uholdbar i længden.

### Implementeringen af `shlex`:

For at løse problemstillingen med `msg`-delen af loglinjerne blev `shlex`, som er et standardbibliotek, implementeret.

- Importerede `shlex`.
- Erstattede `split()` med `shlex.split()`.
- Verificering blev udført og bekræftede, at beskeden med anførselstegn og mellemrum nu blev bevaret som et enkelt element.

### Strukturen af dictionary

Efter opdelingen af de individuelle logdele:

- Oprettede et tomt dictionary til at indeholde hver logpost.
- Tidsstemplet opbevares separat under `timestamp`-key.
- `for`-loop bruges til at processere de resterende felter.
- `split("=", 1)` blev brugt til at separere key og values.

Tidsstemplet blev håndteret separat, da det ikke følger den samme procedure for key og value-struktur som de resterende logdele.

## 3. Håndtering af flere loglinjer samtidig

Efter at have opnået en succesfuld parsing af individuelle loglinjer implementerede jeg processen til at håndtere hele filen.

- Oprindeligt brugte jeg list comprehension til parsing af logdele.
- Opbevarede de resulterende dictionaries i en liste kaldet `parsed_logs`.
- Verificerede, at alle 541 loglinjer blev parsed korrekt.

List comprehension blev senere erstattet af et regulært `for`-loop med brugen af `enumerate()`.

Denne ændring gjorde, at programmet kunne holde styr på individuelle linjenumre, som gjorde det muligt at identificere og rapportere logindtastninger, der var misdannede.

Nummereringen med `enumerate()` starter med 1 for at matche linjenumrene i logfilen i stedet for Pythons default 0-baserede indeksering.

## 4. Exception-håndtering og fejlvalidering

Den oprindelige implementering blev udvidet til at håndtere manglende filer og misdannede logindtastninger.

### 4.1 Filindlæsning og exception-håndtering

Tilføjede `try/except`-håndtering til `load_logs()`.

- Implementerede `FileNotFoundError`-håndtering via `except`.
- Tilføjede en fejlbesked, når TXT-filen ikke kunne findes.
- Returnerer `None`, hvis indlæsning fejler.
- Tilføjede et check i hovedprogrammet til at forhindre videre processering, når ingen logs blev indlæst.

Testet ved midlertidigt at fejltaste filnavnet til en ikke-eksisterende fil.

**Resultat:** Fejlen blev fanget, en passende besked blev vist, og programmet afsluttede uden nogen fejl.

### 4.2 Tomme logindtastninger

Tilføjede verificering ved at bruge:

`if not parts:`

Det checker, om `shlex.split()` returnerer en tom liste.

- Tomme indtastninger genererer en fejlbesked.
- Parseren returnerer `None`.
- Hovedprocesseringsloopet identificerer en ugyldig indtastning og fortsætter med de resterende linjer.

Dette er blevet testet ved midlertidigt at indsætte en tom linje i loglisten.

**Resultat:** Den tomme linje blev identificeret ved (som eksempel) linje 3, og de resterende linjer blev processeret korrekt og med succes.

### 4.3 Tidsstempelvalidering

Oprindeligt blev tidsstempelverificeringen udført ved brug af et check på de første 4 værdier ved hjælp af `.isdigit()`.

Denne tilgang blev forbedret ved brug af Pythons `datetime`-modul (tak til Klaus for denne idé).

Implementeringen:

`datetime.strptime(parts[0], "%Y-%m-%dT%H:%M:%S")`

Dette validerer det komplette tidsstempel imod det forventede format.

- Ugyldige tidsstempler genererer en fejlbesked.
- Det berørte linjenummer og tidsstemplet identificeres og vises i udskriften.
- Ugyldige indtastninger afvises ved at returnere `None`.

Testet ved brug af en ugyldig datoindtastning.

**Resultat:** Det ugyldige tidsstempel blev korrekt identificeret og afvist.

### 4.4 Key-Value-validering

Tilføjede validering for at sikre, at hver del efter tidsstemplet indeholder et `=`-tegn.

- Checker hver del af loglinjen fra indeks `[1]` (efter tidsstemplet) individuelt ved brug af `"=" in part`.
- Valide dele bliver splittet op i keys og values.
- Ugyldige dele genererer en fejlbesked, som indeholder linjenummer og den misdannede del fra linjen i logfilen.

Testet ved brug af en misdannet del (`level INFO`) uden `=`-tegn.

**Resultat:** Den ugyldige del blev identificeret og afvist uden at afbryde processeringen af de resterende logindtastninger.















