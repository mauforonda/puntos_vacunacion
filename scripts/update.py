#!/usr/bin/env python3

from zipfile import ZipFile
import io
import os
import geopandas as gpd
import requests
import pandas as pd

def load_departamentos():
    return gpd.read_file('scripts/departamentos.geojson').set_index('departamento')

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

def update_tabla(tipo, gdf):
    url_base = 'https://umap.openstreetmap.fr/en/map/puntos-de-vacunacion-covid-19-bolivia_611476#18/{}/{}'
    gdf_copy = gdf.copy()
    gdf_copy = pd.concat([gpd.tools.sjoin(gdf_copy, departamentos.loc[[departamento]], how='left').dropna(subset=['index_right']) for departamento in departamentos.index]).rename(columns={'index_right':'departamento'})
    gdf_copy['url'] = gdf_copy.geometry.apply(lambda g: url_base.format(g.y, g.x))
    gdf_copy.drop(columns=['geometry']).sort_values('departamento').to_csv(tipo + '.csv', index=False)

def update(tipo):
    gdf = tipo()
    gdf.to_file(tipo.__name__ + '.geojson', driver='GeoJSON')
    update_tabla(tipo.__name__, gdf)

departamentos = load_departamentos()
update(gobierno)
update(comunidad)
