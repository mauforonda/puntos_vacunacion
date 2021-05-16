#!/usr/bin/env python3

from zipfile import ZipFile
import io
import os
import geopandas as gpd
import requests

def gobierno():
    url = 'https://www.google.com/maps/d/u/0/kml?mid=1MnsO6uh8ZGZJmY4NhtwKfzgXwvxYsPCi'
    kml = 'doc.kml'
    response = requests.get(url)
    kmz = ZipFile(io.BytesIO(response.content), 'r')
    kmz.extract(kml)
    gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    gdf = gpd.read_file(kml, driver='KMZ')
    os.remove(kml)
    return gdf

def comunidad():
    return gpd.read_file('http://umap.openstreetmap.fr/en/datalayer/1752252/')

def update(tipo, location):
    gdf = tipo()
    gdf.to_file(location, driver='GeoJSON')

update(gobierno, 'gobierno.geojson')
update(comunidad, 'comunidad.geojson')
