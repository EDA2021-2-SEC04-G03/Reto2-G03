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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.arraylist import  iterator, newList, size, subList
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import shellsort as sh
from DISClib.Algorithms.Sorting import mergesort as m
from datetime import datetime
import time
assert cf
import operator

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""


# Construccion de modelos
def newCatalog():
    estructura= "ARRAY_LIST"
    catalog = {'obras': None,
               'artistas': None,
               }

    catalog['artistas'] = {"mID":None,"mAnoNacimiento": None, "mNombre": None}
    catalog['artistas']["mID"]=mp.newMap(20000,maptype="CHAINING",loadfactor=4)
    catalog['artistas']["mNombre"]=mp.newMap(20000,maptype="CHAINING",loadfactor=4)
    catalog['artistas']["mAnoNacimiento"]=mp.newMap(20000,maptype="CHAINING",loadfactor=4)
    catalog['obras'] =  {"mMedio":None,"mDepartamento": None, "mFechaAd": None,"mNacionalidad": None}
    catalog['obras']["mDepartamento"]=mp.newMap(200000,maptype="CHAINING", loadfactor=4)
    catalog['obras']["mNacionalidad"]=mp.newMap(200000,maptype="CHAINING", loadfactor=4)
    catalog['obras']["mMedio"]=mp.newMap(200000,maptype="CHAINING", loadfactor=4)
    catalog['obras']["mFechaAd"]=mp.newMap(200000,maptype="CHAINING", loadfactor=4)
    return catalog


def addArtist(catalog, artista):
    """
    Adiciona un artista a lista de artistas, se hace un diccionario vacio y luego 
    se llena con los atributos que necesitamos en el reto, tambien se asigna un espacio
    para las obras con una lista vacia.
    """
    artist= {}
    artist["ConstituentID"]= artista["ConstituentID"]
    artist["DisplayName"]= artista["DisplayName"]
    artist["BeginDate"]= artista["BeginDate"]
    artist["EndDate"]= artista["EndDate"]
    artist["Nationality"]= artista["Nationality"]
    artist["Gender"]= artista["Gender"]
    artist["Artworks"]= lt.newList("ARRAY_LIST",cmpfunction= cmpObraId)
    artist["mArtworksTecnica"]= mp.newMap(200,maptype="CHAINING",loadfactor=4)
    mp.put(catalog["artistas"]["mID"],artist["ConstituentID"], artist)
    addOrCreateListInMap(catalog["artistas"]["mAnoNacimiento"],artist["BeginDate"],artist)
    addOrCreateListInMap(catalog["artistas"]["mNombre"],artist["DisplayName"],artist)

def addOrCreateListInMap(mapa, llave, elemento):
    if mp.contains(mapa,llave)==False:
        lista_nueva=lt.newList("ARRAY_LIST")
        lt.addLast(lista_nueva,elemento)
        mp.put(mapa,llave,lista_nueva)
    else:
        pareja=mp.get(mapa,llave)
        lista_existente=me.getValue(pareja)
        lt.addLast(lista_existente,elemento)
        mp.put(mapa,llave,lista_existente)

def addObra(catalog, obra):
    artwork={}
    artwork["ObjectID"]= obra["ObjectID"]
    artwork["Title"]= obra["Title"]
    artwork["Medium"]= obra["Medium"]
    artwork["Date"]= obra["Date"]
    artwork["DateAcquired"]= obra["DateAcquired"]
    artwork["Department"]= obra["Department"]
    artwork["CreditLine"]= obra["CreditLine"]
    artwork["Dimensions"]= obra["Dimensions"]
    artwork["Depth (cm)"]= obra["Depth (cm)"]
    artwork["Diameter (cm)"]= obra["Diameter (cm)"]
    artwork["Height (cm)"]= obra["Height (cm)"]
    artwork["Length (cm)"]= obra["Length (cm)"]
    artwork["Weight (kg)"]= obra["Weight (kg)"]
    artwork["Circumference (cm)"]= obra["Circumference (cm)"]
    artwork["Width (cm)"]= obra["Width (cm)"]
    artwork["Classification"]= obra["Classification"]
    artwork["Seat Height (cm)"]= obra["Seat Height (cm)"]
    artwork["Artists"]= lt.newList("ARRAY_LIST",cmpfunction=cmpArtistId)
    codigosArtistas= obra['ConstituentID']
    codigosArtistas= codigosArtistas.replace("[","")
    codigosArtistas= codigosArtistas.replace("]","")
    codigosArtistas= codigosArtistas.replace(" ","")
    codigosArtistas= codigosArtistas.split(",")
    artwork["ConstituentID"]= codigosArtistas
    """
    vamos a hacer la conexión de referencias entre obras y artistas
    al artista se le adiciona la info de la obra a la lista artworks
     y viceversa con los artistas a la obra
    """
    for ID in codigosArtistas:
        par= mp.get(catalog["artistas"]["mID"], ID)
        if par:
            infoArtistaID= me.getValue(par)
            nombre = infoArtistaID["DisplayName"]
            lt.addLast(infoArtistaID["Artworks"],artwork)
            addOrCreateListInMap(infoArtistaID["mArtworksTecnica"], artwork["Medium"],artwork)
            lt.addLast(artwork["Artists"],infoArtistaID)
            mp.put(catalog["artistas"]["mNombre"],nombre, infoArtistaID)
    "tanto el mapa que tienE ID de artista como key  como el de nombre van a quedar también con la referencia de las obras"            
    artwork["Nacionalidad"]= lt.newList("ARRAY_LIST")
    for artista in lt.iterator(artwork["Artists"]):
        nacionalidad= artista["Nationality"]
        if nacionalidad=="":
            nacionalidad="Nationality Unkwonw"
        if lt.size(artwork["Nacionalidad"])==0 or lt.isPresent(artwork["Nacionalidad"], nacionalidad) !=0:
            lt.addLast(artwork["Nacionalidad"],nacionalidad)

    addOrCreateListInMap(catalog['obras']["mMedio"], artwork["Medium"],artwork)
    addOrCreateListInMap(catalog['obras']["mDepartamento"], artwork["Department"],artwork)
    addOrCreateListInMap(catalog['obras']["mFechaAd"], artwork["DateAcquired"],artwork)
    for nacionalidad in lt.iterator(artwork["Nacionalidad"]):
        addOrCreateListInMap(catalog['obras']["mNacionalidad"],nacionalidad,artwork)

#Funcione Comparacion Mapa#
def compareMap(nuevo, tag):
    entry = me.getKey(tag)
    if (nuevo == entry):
        return 0
    elif (nuevo > entry):
        return 1
    else:
        return 0
#REQ 1#
def sortArtistInDateRange(catalog, date1,date2):
    date1 = int(date1)
    date2 = int(date2)
    ListaAnosGen= mp.keySet(catalog["artistas"]["mAnoNacimiento"])
    listaEnRango = lt.newList("ARRAY_LIST") #porque luego se accede por pos#s
    lista_artistas_año= lt.newList("ARRAY_LIST")
    for i in lt.iterator(ListaAnosGen):
        AnoKey= int(i)
        if AnoKey != 0 and AnoKey >= date1 and AnoKey<=date2:
            lista_artistas_año= mp.get(catalog["artistas"]["mAnoNacimiento"],i)["value"]
            for artista in lt.iterator(lista_artistas_año):
                lt.addLast(listaEnRango, artista)
    listaOrdenada= listaEnRango.copy()
    listaOrdenada= m.sort(listaOrdenada,cmpArtistByDate)
    return (listaOrdenada)
def cmpArtistByDate(artist1, artist2):
    fecha1= (artist1['BeginDate'])
    fecha2=(artist2['BeginDate'])
    temp=False
    if fecha1=="":
        fecha1=0 
    if fecha2=="":
        fecha2=0
    temp= int(fecha1)<int(fecha2)
    return temp
#RETO 1 VERSIÓN SIN MAPA
# def sortArtistInDateRange(catalog, date1,date2):
#     # req1
#     date1 = int(date1)
#     date2 = int(date2)
#     listaEnRango = lt.newList("ARRAY_LIST") 
#     for i in lt.iterator(catalog['artistas']):
#         date= int(i['BeginDate'])
#         if date != 0 and date >= date1 and date<=date2:
#             lt.addLast(listaEnRango, i)
#     listaOrdenada= m.sort(ListaEnRango,cmpArtistByDate)
#     return (listaEnRango)
#REQ 2#
def sortArtworksandRange(catalog,inicial,final):
    inicial=datetime.strptime(str(inicial),"%Y-%m-%d")
    final=datetime.strptime(str(final),"%Y-%m-%d")
    listaAnhosAd=mp.keySet(catalog["obras"]["mFechaAd"])
    listaEnRango= lt.newList("ARRAY_LIST")
    listaInfo=lt.newList("ARRAY_LIST")
    purchased=0
    for i in lt.iterator(listaAnhosAd):
         date=i
         if date=="":
           date="0001-01-01"
         date_format=datetime.strptime(str(date),"%Y-%m-%d")
         if date_format<= final and date_format>=inicial:
               listaInfo=mp.get(catalog["obras"]["mFechaAd"],date)["value"]
               for info in lt.iterator(listaInfo):
                   lt.addLast(listaEnRango,info)
               creditLine=catalog["obras"]["mFechaAd"]["CreditLine"]
               if creditLine in ("Purchase").lower or ("Purchased").lower() in creditLine:
                   purchased+=1
    lista_ordenada= m.sort(listaEnRango,cmpArtworkByDateAcquired)
    dictRta={"lista":lista_ordenada,"numPurchase":purchased}
    return (dictRta)
#Versión sin mapa
#def sortArtworksandRange(lista,inicial,final):
#   inicial=datetime.strptime(str(inicial),"%Y-%m-%d")
#   final=datetime.strptime(str(final),"%Y-%m-%d")
#   listaEnRango= lt.newList("ARRAY_LIST")
#   purchased=0
#   for i in lt.iterator(lista):
#        date=i['DateAcquired']
#       if date=="":
#           date="0001-01-01"
#       date_format=datetime.strptime(str(date),"%Y-%m-%d")
#       if date_format<= final and date_format>=inicial:
#               lt.addLast(listaEnRango,i)
#               credit_line= str(i["CreditLine"]).lower()
#               if ("Purchase").lower() in credit_line or ("Purchased").lower() in credit_line :
#                   purchased+=1
#     lista_ordenada= ins.sort(listaEnRango,cmpArtworkByDateAcquired)
#     return (lista_ordenada,purchased)
def sortArtworksByDate(lista):
    lista_ordenada= lista.copy()
    lista_ordenada= m.sort(lista_ordenada,cmpArtworkByDate)
    return lista_ordenada
def sortArtworksByPrice(listaog):
    lista= listaog.copy()
    m.sort(lista,cmpArtworktByPrice)
    return lista

#REQ 3#
def ObrasPorArtistaPorTecnica(catalogo,nombre):
    mapaTecnicas=mp.newMap(200,maptype="CHAINING", loadfactor=4)
    par= mp.get(catalogo["artistas"]["mNombre"], nombre)
    if par:
        artista= me.getValue(par)
        mapaTecnicas= artista["mArtworksTecnica"]
        TecnicaMasRep= buscarTecnicaMasRep(mapaTecnicas)
        lista= me.getValue(mp.get(mapaTecnicas,TecnicaMasRep))
        listaObrasTecnica= lista.copy()
    numeroObras= lt.size(artista["Artworks"])
    m.sort(listaObrasTecnica,cmpArtworkByDate)
    return(mapaTecnicas,TecnicaMasRep, numeroObras,listaObrasTecnica)

def buscarTecnicaMasRep(Tecnicas):
    size_mayor=0
    for tecnica in lt.iterator(mp.keySet(Tecnicas)):
        size= lt.size(me.getValue(mp.get(Tecnicas,tecnica)))
        if size>size_mayor:
            size_mayor= size
            TecnicaMas= tecnica
    return TecnicaMas
#REQ 4#
def RankingCountriesByArtworks (catalog,obras):
    nacionalidades=catalog["obras"]["mNacionalidad"]
    keyNacionalidades=mp.keySet(nacionalidades)
    mayor=0
    listaNumObras=lt.newList("ARRAY_LIST")
    for i in lt.iterator(keyNacionalidades):
        listaElement=lt.newList("ARRAY_LIST")
        element=mp.get(nacionalidades,i)["value"]
        tam=int(mp.size(element)) #num de obras
        if tam>mayor:
            mayor=element
        lt.addLast(listaElement,i)
        lt.addLast(listaElement,tam)
        lt.addLast(listaNumObras,listaElement)
    m.sort(listaNumObras,cmpNumObras)
    return(listaNumObras)

def cmpNumObras (num1,num2):
    
    temp=False
    temp= int(num1)<int(num2)
    return temp
#RETO 1 VERSIÓN 
#def RankingCountriesByArtworks (catalog,obras):
    #lista_artistas=catalog["artistas"]
    #dict_nacionalidades= {}
    #for i in obras:
        #for n in lt.iterator(lista_artistas):
            #if i in n["Artworks"]:
                #nacionalidad= n["Nationality"]
                #if nacionalidad not in dict_nacionalidades:
                    #dict_nacionalidades[nacionalidad]=1
                #else:
                    #dict_nacionalidades[nacionalidad]+=1
    #return (dict_nacionalidades)

#REQ 5#
def AsignarPrecio(object):
    #considerar datos vacios revisar reglas#
    m3=-1
    if object["Width (cm)"]!="" and object["Height (cm)"]!="" and object["Depth (cm)"]!="":
        m3= ((float(object["Width (cm)"]))*(float(object["Height (cm)"]))*(float(object["Depth (cm)"])))
        m3= m3/1000000
    m2=-1
    if object["Width (cm)"]!="" and object["Height (cm)"]!="":
        m2=(float(object["Width (cm)"]))*(float(object["Height (cm)"]))
        m2=m2/10000
    elif object["Circumference (cm)"]!="" and object["Diameter (cm)"]!="":
        m2=(float(object["Circumference (cm)"]))*(float(object["Circumference (cm)"]))
        m2=m2/1000
    precio=-1
    preciom3= 0
    preciom2= 0
    precioKg= 0
    if object["Weight (kg)"] != "":
        precioKg= 72* float(object["Weight (kg)"])
    if m3>0:
        preciom3= 72* float(m3)
    if m2>0:
        preciom2= 72* float(m2)
    if preciom3 ==0 and preciom2==0 and precioKg==0:
        precio=48
    elif preciom2> preciom3 and preciom2> precioKg:
        precio= preciom2
    elif preciom3> preciom2 and preciom3> precioKg:
        precio= preciom3
    elif precioKg> preciom2 and precioKg> preciom3:
        precio= precioKg 
    return (precio)

def OrdenarDepartamentoAsignarPrecioyPeso(catalogo, departamento):
    obrasPorDepartamento= mp.get(catalogo['obras']["mDepartamento"],departamento)["value"]
    listaR = lt.newList("ARRAY_LIST") #la lista R va a tener peso,precio,listaobras#
    precio=0
    peso=0
    for obra in lt.iterator (obrasPorDepartamento):
        obra["precio"]=AsignarPrecio(obra)
        precio+=float(obra["precio"])
        if obra["Weight (kg)"] != "":
            peso+=float(obra["Weight (kg)"])
    lt.addLast(listaR, peso)
    lt.addLast(listaR, round(precio,3))
    lt.addLast(listaR, obrasPorDepartamento)
    return listaR

# Funciones utilizadas para comparar elementos dentro de una lista
def cmpArtistId(artist1, artist2):
    if artist1["ConstituentID"] < artist2["ConstituentID"]:
        return -1 
    elif artist1["ConstituentID"] == artist2["ConstituentID"]:
        return 0
    else: 
        return 1
def cmpObraId(obra1, obra2):
    if obra1["ObjectID"] < obra2["ObjectID"]:
        return -1 
    elif obra1["ObjectID"] == obra2["ObjectID"]:
        return 0
    else: 
        return 1
def cmpArtworkByDateAcquired(artwork1, artwork2):
    fecha1= str(artwork1['DateAcquired'])
    fecha2=str(artwork2['DateAcquired'])
    if fecha1=="":
        fecha1="0001-01-01"
    if fecha2=="":
        fecha2="0001-01-01"
    date1 = datetime.strptime(fecha1, "%Y-%m-%d")
    date2 = datetime.strptime(fecha2, "%Y-%m-%d")
    if  int(date1)<int(date2):
        return -1 
    elif int(date1)==int(date2):
        return 0
    else: 
        return 1

def cmpArtworkByDate(artwork1, artwork2):
    fecha1= (artwork1['Date'])
    fecha2=(artwork2['Date'])
    temp=False
    if fecha1=="" and fecha2 =="":
        temp= False
    elif fecha1=="" and fecha2 !="":
        temp= False
    elif fecha2=="" and fecha1 !="":
        temp= True
    else:
        temp= int(fecha1)<int(fecha2)
    return temp
def cmpArtworktByPrice(obra1, obra2):
    precio1= float(obra1["precio"])
    precio2=float(obra2["precio"])
    return precio1<precio2
def compareNacionalidades (name,tag):
    tagentry = me.getKey(tag)
    if (name == tagentry):
        return 0
    elif (name > tagentry):
        return 1
    else:
        return -1
def cmpArtworkPorPrecio(Artwork1,Artwork2):
    precio1=Artwork1["precio"]
    precio2=Artwork2["precio"]
    return precio1< precio2