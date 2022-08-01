# Daily-fire-hazard-index-herault

## Output

1 - Tiff géoréférencé avec valeur entre 0 et 1 dans ``./output/GeoTiff/{date}.tiff``

2 - Image RGB selon echelle de risque  dans ``./output/PNG/{date}.png``

## Instalation

1 - Télécharger répertoire

2 - Télecharger les dépendeances (dans l'invité de commandes) :

```bash
$ pip install -r ./requirements.txt
```

3 - Dans config.py (éditeur de texte ou idle python)  actualiser les token et id sentinelhub / meteo france :

https://donneespubliques.meteofrance.fr/?fond=creation_compte

https://services.sentinel-hub.com/
