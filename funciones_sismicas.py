gistfile1.txt
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 11:50:37 2017

@author: carlos ramirez
"""
import math
import os

""" construye un lista con los pares de coordenadas del poligono que forma la ciudad
    como argumento recibe a path, la direccion de la carpeta donde estan los archivos
    csv que contiene los puntos, y el nombre de la ciudad tal como esta en la carpeta
    los puntos pueden tener la dos sigts sintaxis ['-xxxxxxx,xxxxxxx'] o 
    
    ['-xxxxxxxxx xxxxxxxxx']"""
def hacer_poligono(path,ciudad):
    
    path+='/'+ciudad
    archivo = open(path)
    s = archivo.readlines()
    l = []
    for n in s:
        if ',' in n:
            y = n.split(',')
            l.append([float(y[0]),float(y[1])])
        else:
            y = n.split()
            l.append([float(y[0]),float(y[1])])
    return l

#print(hacer_poligono(entrada,'Independencia.csv'))


#funcion hacer_poligonos acepta una lista con los nombres de las carpetas
#donde estan las ubicaciones de cada provincia ['Azua.csv','Barahona.csv',...]
#devuelve una lista con las ciudades y sus respectivas listas de de ubicaciones
#que forma el poligono [['Azua',[[-xxxx, xxxxx],....],['Barahona',[-xxxx, xxxx],[],....]]
def hacer_poligonos(files,path_provincias):
    poligonos = []
    for n in files:
        #print n
    
        poligonos.append([n,hacer_poligono(path_provincias,n)])
    return poligonos


def punto_en_poligono(x, y, poligono):
    #este codigo fue extraido de la pagina:https://sakseiw.wordpress.com
    """Comprueba si un punto se encuentra dentro de un polígono
        
       poligono - Lista de tuplas con los puntos que forman los vértices [(x1, x2), (x2, y2), ..., (xn, yn)]
    """
    i = 0
    j = len(poligono) - 1
    salida = False
    for i in range(len(poligono)):
        if (poligono[i][1] < y and poligono[j][1] >= y) or (poligono[j][1] < y and poligono[i][1] >= y):
            if poligono[i][0] + (y - poligono[i][1]) / (poligono[j][1] - poligono[i][1]) * (poligono[j][0] - poligono[i][0]) < x:
                salida = not salida
                #print salida
                
        j = i
    return salida
#recibe la locacion del evento x,y y devuelve el nombre de la provincia donde esta el evento
#o False sino esta en ninguna de las provincias de la lista
def de_que_provincia_es(x,y,files,path_provincias):
    
    poligonos = hacer_poligonos(files,path_provincias)
    for n in poligonos:
        if punto_en_poligono(x,y,n[1])==True:
            
            return n[0][:-4]
    return False
#poligonos = hacer_poligonos(files)

# la funcion "haversine" recibe dos coordenadas(lat1,lon1) y (lat2 y lon2)
# devuelve la distancia ortodromica entre los puntos  

def haversine(lat1,lon1,lat2,lon2):
  R = 6370
  dlat = lat2 - lat1
  dlon = lon2 - lon1
  D= 2*R*math.asin(math.sqrt(math.sin(math.radians(dlat/2))**2+
                             math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*
                     math.sin(math.radians(dlon/2))**2))
  
  return D
# la funcion calcular_ciudad calcula la ciudad importante mas cercana al sismo
# acepta 3 parametros el archivo con las ciudades y sus cordenadas, generado por
# la funcion formatear_lineas y la latitud y longitud del sismo sentido
def calcular_ciudad(ciudades,prov,lat,lon):
    
  l = [ciudades[prov]['ciudades'],ciudades[prov]['locacion']]
  dmin = 1000000
  ciudad = ''
  salida = []

  for i in range(len(l[1])):
    la = float(l[1][i][0])
    lo = float(l[1][i][1])
    d = haversine(lat,lon,la,lo)
    
    if d < dmin:
      dmin = d
      ciudad = l[0][i]
      salida = [la,lo,round(dmin,1),ciudad]
  return salida
# la funcion generar_comentario es la funcion que devuelve el comentario asociado
# con el sismo analizado con el siguiente formato: "3.0 Km al ONO de El Penon, Barahona."

def generar_comentario(ciudades,lat,lon,file_provincias):
  files = os.listdir(file_provincias)#tira el listado de las provincias(poligonos)
  prov_pol = de_que_provincia_es( lon,lat,files,file_provincias)#dice en que provincia esta el sismo,false si no esta en ningun poligono
  if prov_pol == False:
    return "Distante."
  v = calcular_ciudad(ciudades,prov_pol,lat,lon)#calcula la ciudad mas cercana dentro del poligono/provincia
 
  if v == False:
      return 'Fuera de la Region'
  direcciones = ['Este','ENE','NE','NNE','Norte','NNO','NO','ONO','Oeste','OSO','SO',
                 'SSO','Sur','SSE','SE','ESE']
  direccion =''
  cuadrante = 0
  dlat = lat -v[0] 
  dlon = lon -v[1]
  if dlat > 0:
    if dlon >0:
      cuadrante = 1
    if dlon <0:
      cuadrante = 2
  else:
    if dlon > 0:
      cuadrante = 4
    if dlon < 0:
      cuadrante = 3
  c = 11.25 #grado de la rosa
  q = 22.5 #grados correspondientes a cada punto y subpuntos cardinales

  t = math.atan(dlat/dlon)
  
  t = math.degrees(t)
  
  if cuadrante == 2:
    t = 180 + t 
  if cuadrante == 3:
    t = t + 180
  if cuadrante == 4:
    t = 360 +t
  #print t,cuadrante
  #condiciones para las direcciones
  if t < c:
    direccion = direcciones[0]
  if t >= c and t < c+q:
    direccion = direcciones[1]
  if t >= c+q and t < c+2*q:
    direccion = direcciones[2]
  if t >= c+2*q and t < c+3*q:
    direccion = direcciones[3]
  if t >= c+3*q and t < c+4*q:
    direccion = direcciones[4]
  if t >= c+4*q and t < c+5*q:
    direccion = direcciones[5]
  if t >= c+5*q and t < c+6*q:
    direccion = direcciones[6]
  if t >= c+6*q and t < c+7*q:
    direccion = direcciones[7]
  if t >= c+7*q and t < c+8*q:
    direccion = direcciones[8]
  if t >= c+8*q and t < c+9*q:
    direccion = direcciones[9]
  if t >= c+9*q and t < c+10*q:
    direccion = direcciones[10]
  if t >= c+10*q and t < c+11*q:
    direccion = direcciones[11]
  if t >= c+11*q and t < c+12*q:
    direccion = direcciones[12]
  if t >= c+12*q and t < c+13*q:
    direccion = direcciones[13]
  if t >= c+13*q and t < c+14*q:
    direccion = direcciones[14]
  if t >= c+14*q and t < c+15*q:
    direccion = direcciones[15]
  if t >= c+15*q and t < c+16*q:
    direccion = direcciones[0]
    #if n[0]== 'Elias Pina.csv':
             #   return 'Elias Piña'
            #if n[0]== 'Monsenor Nouel.cvs':
            #    return 'Monseñor Nouel'
    
  if prov_pol == 'Monsenor Nouel':
    prov_pol = 'Monseñor Nouel'
  if prov_pol ==  'Elias Pina':
    prov_pol ==  'Elias Piña'
  comentario = str(v[2])+" Km al " + direccion+ " de " + v[3]+', '+prov_pol+'.'
  return comentario

#prov = de_que_provincia_es(,get_lat(lat))
#prov = de_que_provincia_es( -71.529452,19.430041)

def get_ciudades(path_ciudades):
    
    archivo = open(path_ciudades)
    lista = archivo.readlines()
    l_final = []
    for e in lista:
        n = e.find('.')
        a =[e[:n].split(','),e[n+1:].split()]
        l_final.append(a)
    l_final.remove(l_final[0])
    ciudades = {}
    for e in l_final:
        ciudad = e[0][1][1:]
        #print ciudad
        if ciudad not in ciudades:
            ciudades[ciudad]={'ciudades':[e[0][0]],'locacion':[e[1]]}
        else:
            ciudades[ciudad]['ciudades'].append(e[0][0])
            ciudades[ciudad]['locacion'].append(e[1])
            #se genero un diccionario de ciudades con la sigt sintaxis:
            # ciudades['Valverde']={'ciudades':['Mao','Esperanza',...],'locacion':[['latitud','longitud'],...]}

    return ciudades

    



#comentario = generar_comentario(ciudades,  get_lat(lat), get_lon(lon), path_provincias)
#comentario = generar_comentario(ciudades, 19.3490, -68.4890, path_provincias)
def get_select(lineas,start,end):#devuelve un select de la lista lineas
                                #desde start hasta end
    return lineas[start:end]

def get_indices(lineas):#crea un arreglo con los indices iniciales de 
                        #cada select
    indices = []
    i = 0
    while i < len(lineas):
        if lineas[i][-2]=='1':
            ind = lineas.index(lineas[i])
            indices.append(ind)
        i+=1
    indices.append(lineas.index(lineas[-2]))
    return indices


def formatear(select,ciudades,path_provincias):
    
    l1 = ''
    l2 = ''
    for n in select:
        if n[-2] == '1':
            l1 = n
        if n[-2] == 'E':
            l2 = n
    #crear fecha
    anio = l1[1:5]
    mes = l1[6:8]
    #aqui se le da formato de dos digitos al mes
    if mes[0]==' ':
        mes = '0'+mes[1]
    dia = l1[8:10]
    #aqui se completa el campo dia con dos digitos
    if dia[0]==' ':
        dia = '0'+dia[1]
    #aqui se completa la fecha
    fecha = anio+'-'+mes+'-'+dia
    
    #---------------------------------------------
    #aqui se formatea la hora
    h = l1[11:15]
    sec = l1[16:18]
    #se completan los segundos a dos digitios de ser necesario
    if sec[0]==' ':
        sec = '0'+sec[1]
    hora = h[:2]+':'+h[2:]+':'+sec
    
    #--------------------------------------------
    #las demas variables importantes de la primera linea
    lat = l1[24:30]
    lon = l1[31:38]
    prof = l1[38:43]
    gap = l2[5:8]
    eprof = l2[38:43]
    rms = l1[52:55]
    #----------------------------------------------------
    #aqui se seleccionan las magnitudes
    l = l1[56:].split()
    ml ='---'
    mc ='---'
    mw ='---'
    for n in l:
        if 'L' in n:
            ml = n[:3]
        if 'C' in n:
            mc = n[:3]
        if 'W' in n:
            mw = n[:3]
    salida = fecha +' '+hora+' '+lat+' '+lon+' '+prof+ \
    '  '+eprof+'  '+gap+'  '+rms+'  '+ml+'  '+mc+'  '+mw+ ' '
    comentario = generar_comentario(ciudades,float(lat),float(lon),path_provincias)
    return salida + comentario
#--------------------------------------------------------
def crear_header():#crea la cabecera o titulo de la base de datos
    return 'fecha      hora     lat    lon      dep    edep  gap  rms  ml   mc   mw  comentario\n'

#-----------------------------------------------------------------
def anadir_registro(lineas,ciudades,select,path_provincias,out):#abre el archivo para anadir un nuevo registro
    salida = open(out,'a')
    salida.write(formatear(select,ciudades,path_provincias)+'\n')
    salida.close()
    
#------------------------------------------------------------------
def crear_dbd(lineas,ciudades,path_provincias,out):#crea la base de datos
#ciudades es un diccionario con
    salida = open(out,'w')
    header = crear_header()
    salida.write(header)
    salida.close()
    v = get_indices(lineas)
    
    #bucle para extraer los datos y anadirlos a la base de datos
    i = 0
    while i+1 < len(v):
        select = get_select(lineas,v[i],v[i+1])
        anadir_registro(lineas,ciudades,select,path_provincias,out)
        i+=1
def ordenar(arr):
    for i in range(len(arr)-1):
        for j in range(len(arr)-1):
            if arr[j].split()[0] > arr[j+1].split()[0]:
                temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1]=temp
    return arr
