"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de obras
def initCatalog():
    catalog = model.newCatalog()
    return catalog
# Funciones para la carga de datos
def loadData(catalog):
    loadArtistas(catalog)
    loadObras(catalog)

def loadArtistas(catalog):
    """
    Carga todos los artistas del archivo y la agrega a la lista de obras en el catalogo general
    """
    Artistfile = cf.data_dir + 'Artists-utf8-small.csv'
    input_file = csv.DictReader(open(Artistfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)

def loadObras(catalog):
    """
    Carga todas las obras del archivo y la agrega a la lista de obras en el catalogo general
    """
    Obrasfile = cf.data_dir + 'Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(Obrasfile, encoding='utf-8'))
    for obra in input_file:
        model.addObra(catalog, obra)
# Funciones de ordenamiento
def sortArtworksandRange(lista,inicial,final):
    return model.sortArtworksandRange(lista,inicial,final)
def sortArtistInDateRange(catalog, date1,date2):
    return model.sortArtistInDateRange(catalog, date1,date2)
def sortArtworksByDate(lista):
    return model.sortArtworksByDate(lista)
def sortArtworksByPrice(lista):
    return model.sortArtworksByPrice(lista)
def OrdenarPorPrecio(lista):
    ListaOrdenada= model.OrdenarPorPrecio(lista)
    return ListaOrdenada    
def OrdenarDepartamentoAsignarPrecioyPeso(catalogo, departamento):
    ObrasPorDepartamento= model.OrdenarDepartamentoAsignarPrecioyPeso(catalogo, departamento)
    return ObrasPorDepartamento 
# Funciones de consulta sobre el catálogo
def RankingCountriesByArtworks(catalog,obras):
    return model.RankingCountriesByArtworks(catalog,obras)
def ObrasPorArtistaPorTecnica(catalogo,nombre):
    return model.ObrasPorArtistaPorTecnica(catalogo,nombre)
def buscarTecnicaMasRep(dicTecnicas):
    return model.buscarTecnicaMasRep(dicTecnicas)

