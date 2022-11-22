# Pràctica 1 - Tipologia i Tipus de dades

## Descripció del repositori

### Membres del equip
Els membres que conformen l'equip són:

1. **Marc González Planes** - [@Magopla](https://github.com/Magopla)</li>
2. **Maria Sunyer** -[@MSunyerR](https://github.com/MSunyerR)</li>


## Context
Hem decidit realitzar scraping a la pàgina web del supermercat “Ulabox”. Ens hem decantat per fer scraping d’un supermercat perquè considerem que els últims mesos s’estan disparant alarmes socials en torn al preu de la cistella de compra, per tant, el fet de poder obtenir les dades d’un supermercat ens pot permetre aplicacions que cerquin ofertes, tendències de preus, etc.

A més a més, l'experiència obtinguda durant la realització de la pràctica és reutilitzable al fer scraping d’altres supermercats o pàgines basades amb productes.

En quant a supermercat, hem decidit fer servir Ulabox com a exemple degut a que la pàgina robots.txt, permeteix fer scraping de qualsevol element de la pàgina https://www.ulabox.com/robots.txt

L’adreça del supermercat és al següent:
https://www.ulabox.com/

## Títol del dataset
El dataset resultat s’ha anomenat:

**Nov-19-2022_productes_alimentacio_ulabox.csv**

## Descripció del dataset
Aquest dataset agrupa informació referent a tots els productes d’alimentació disponibles al supermercat Ulabox. Per cada producte, obtenim l’informació mostrada en la página web:  el seu nom, imatge, preu, informació nutricional i fabricant. A més a més, guardem l’enllaç a on es troba el producte i la categoria i subcategoria dins del supermercat.

Hem separat el dataset en dues parts, la primera conté les dades dels productes (descripció, preu…) i la segona, conté les imatges dels productes. Per tant el dataset conté de dues parts separades pero relacionades per el camp “ID”.

Les parts es troben al projecte:
- /csv/ : Conté el dataset normal.
- /img/ : Conté les imatges dels productes evaluats.


## Fitxers i estructura
En el nostre repositori es pot trobar la següent estructura:

- img/: Aquí es poden trobar les imatges dels productes, el nom de la imatge fa referència a l'ID del producte.
- pdf/: Document de la pràctica
- dataset/: dataset resultant de l'execució del codi.
- src/: codi Python.


## Configuració de l'entorn
Les llibreries poden revisar-se al fitxer **requirements.txt**:

- requests~=2.25.0
- pandas~=1.2.4
- selenium~=4.5.0
- beautifulsoup4~=4.11.1

## Execució del programa
Per executar el programa cal executar el fitxer **"Ulabox.py"**
El programa carregarà els enllaços i generara el dataset amb la data d'execució.

## Consideracions
L'objectiu d'aquesta activitat és la creació d'un dataset a partir de els dades obtingudes a un lloc web.
Forma part de les activitats referents a l'assignatura de **Tipologia i tipus de dades** del **Màster en Ciència de Dades** de la Universitat Oberta de Catalunya.
