# Daily-fire-hazard-index-herault

![DHFI exemple](https://github.com/AGottardiSDIS/Daily-fire-hazard-index-herault/blob/main/_readme_data/dhfi%20avec%20barre.png)

DFHI est un algorithme calculant le risque incendie journalier de l'Hérault en fonction de données météo-france (vent, humidité, température), des données sur le type de végétation ainsi que des données sur la santé du couvert végétal via des observations satellite Sentinel 2. La zone d'étude correspond au département de l'Hérault (34) sensible aux riques incendie avec 500 feux répértoriés les 3 dernières années. 

## Fonctionnement 

![fonct](https://github.com/AGottardiSDIS/Daily-fire-hazard-index-herault/blob/main/_readme_data/schema.png)

## Output

1 - Tiff géoréférencé avec valeur entre 0 et 1 dans ``./output/GeoTiff/{date}.tiff``

2 - Image RGB selon echelle de risque  dans ``./output/PNG/{date}.png``

## Installation

1 - Télécharger répertoire

2 - Télecharger les dépendeances (dans l'invité de commandes) :

```bash
$ pip install -r ./requirements.txt
```

3 - Dans config.py (éditeur de texte ou idle python)  actualiser les token et id sentinelhub / meteo france :

https://partner-api.meteofrance.com/store/site/pages/list-apis.jag

https://services.sentinel-hub.com/

4 - Lancer __main__.py :

Si le code est lancé après 18h on obtient la carte du risque du lendemain 

Sinon la carte de risque de la journée

5 (optionnel) - Ouverture avec QGIS et echelle de risque nommée pour la colorimétrie :  ``./QGIS_Echelle.txt``
