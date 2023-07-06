# DKLAT-SOM

Undersøgelse af sammenhængen mellem DVR90, DKLAT og DMIs LAT-værdier. Oprindeligt rapporteret
af Søopmålingen (SOM), der i forbindelse med en opmåling i Nordsøen har observeret at
forskellen mellem DVR90 og DKLAT omkring Hirtshals er omtrent 50 cm, hvilket ikke stemmer
overens med den forventede LAT-værdi på 23 cm.

Denne undersøgelse prøver at belyse problemstillingen ved at korrigere for kendte effekter, såsom
DVR90s afvigelse fra lokal middelvandstand (i 1990) og den relative uplift mellem land og hav.
Selv efter denne korrektion ses stadig en afvigelse på et par decimeter mellem DKLAT og DVR90-geoiden.

Årsagen til forskellen er endnu ikke fundet.

Koden i dette repository tilvejebringer et datagrundlag til videre analyse. Se følgende afsnit
for vejledning i opsætning af koden.

## Installation

**Forudsætninger for installation og kørsel af program**:

* Git
* En fungerende Conda eller Mamba installation

Start med lave en lokal kopi af kode og modelfiler:

```
git clone git@github.com:SDFIdk/DKLAT-SOM.git
```

Opret nyt conda miljø:

```
conda env create --file environment.yml
```

Aktiver det nye miljø:

```
conda activate dklat-som
```

Kør programmet:

```
python main.py
```

Ved kørsel af programmet udskrives diverse data, som også gemmes i en GeoJSON fil kaldet `LAT.geojson`.
Denne fil kan indlæses i et GIS-program med henblik på at skabe et bedre visuelt overblik over de
relevante parametre.