# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 15:08:32 2020

@author: sebde
"""

import csv

with open ("synergy_logistics_database.csv","r") as base_datos:
    lector=csv.DictReader(base_datos)
    
    """Haremos dos listas de diccionarios, en uno guardaremos 
    las importaciones y en otra lista las exportaciones
    para poder trabajar de manera separada
    """
    
    importaciones=[]
    exportaciones=[]
    for linea in lector:
        if linea["direction"]=="Exports":
            exportaciones.append(linea)
        else:
            importaciones.append(linea)
    
    
    # Código para mejores rutas
    
    """Vamos a crear una lista para tener todas las rutas posibles
    para importacion y exportacion, ademas de los paises que importan y
    exportan ,ademas de los montos totales
    """
    
    rutas_export=[]#Para alamcenar las diferentes rutas de exportaciones
    rutas_import=[]#PAra almacenar las distintas rutas de importacion
    paises_export=[]#Para alamcenar los paises que son exportadores
    paises_import=[]#Para almacenar los paises que importan
    productos=[]#Para tener la lista de los productos que se importan y exportan
    total_exp=0#Valor total de las exportaciones
    total_import=0#Valor total de las importaciones
    #Primero para las exportaciones
    for elemento in exportaciones:
        total_exp+=int(elemento["total_value"])
        agregar=[]
        agregar.append(elemento["origin"])
        agregar.append((elemento["destination"]))
        if agregar not in rutas_export:
            rutas_export.append(agregar)
        if agregar[0] not in paises_export:
            paises_export.append(agregar[0])
        if elemento["product"] not in productos:
            productos.append(elemento["product"])
    
    
    #Luego para las importaciones
    for elemento in importaciones:
        total_import+=int(elemento["total_value"])
        agregar=[]
        agregar.append(elemento["origin"])
        agregar.append((elemento["destination"]))
        if agregar not in rutas_import:
            rutas_import.append(agregar)
        if agregar[1] not in paises_import:
            paises_import.append(agregar[1])
     
    
    """ Ahora vamos a contar para cada ruta el total de esa ruta y el número 
    de viajes que han seguido esa ruta
    """
#Exportaciones
    datos_exportacion=[]
    for ruta in rutas_export:
        valor_tot=0
        cuenta_viajes=0
        for x in exportaciones:
            if ruta[0]==x["origin"] and ruta[1]==x["destination"]:
                valor_tot+=int(x["total_value"])
                cuenta_viajes+=1
        datos_ruta={"origen":ruta[0],"destino":ruta[1],"valor_total":valor_tot,"viajes":cuenta_viajes}
        datos_exportacion.append(datos_ruta) # Se alamcenan los diccionarios en esta lista

#Importaciones
    datos_importacion=[]
    for ruta in rutas_export:
        valor_tot=0
        cuenta_viajes=0
        for x in importaciones:
            if ruta[0]==x["origin"] and ruta[1]==x["destination"]:
                valor_tot+=int(x["total_value"])
                cuenta_viajes+=1
        datos_ruta={"origen":ruta[0],"destino":ruta[1],"valor_total":valor_tot,"viajes":cuenta_viajes}
        datos_importacion.append(datos_ruta)


#EXportaciones

    #Ordenamos primero de acuerdo a la ruta con mayores viajes
    mas_viajes_export=sorted(datos_exportacion,key=lambda k: k["viajes"],reverse=True)
    
    #Luego ordenamos de acuerdo a la ruta con mayor cantidad de dinero generada
    mas_valor_export=sorted(datos_exportacion,key=lambda k: k["valor_total"],reverse=True)
   
 #Importaciones   
 
    #Ordenamos primero de acuerdo a la ruta con mayores viajes
    mas_viajes_import=sorted(datos_importacion,key=lambda k: k["viajes"],reverse=True)
    
    #Luego ordenamos de acuerdo a la ruta con mayor cantidad de dinero generada
    mas_valor_import=sorted(datos_importacion,key=lambda k: k["valor_total"],reverse=True)
 
    def mostrar(lista=mas_viajes_export,M=10,topico="viajes",direccion="exportacion"):
        contador=1
        print("Las rutas de ",direccion, " con mas ",topico, "son:")
        for i in lista:
            if contador>M:
                break
            print(contador," .- ", i["origen"], " a ", i["destino"], "con:  ", i[topico])
            contador+=1
        
    #Ocuoamos la funcion para mostrar todos los resultados 
    print("")
    mostrar()
    print("""
          """)
    mostrar(mas_valor_export,topico="valor_total",direccion="exportacion")
    print("""
          """)
    mostrar(mas_viajes_import,topico="viajes",direccion="importacion")
    print("""
          """)
    mostrar(mas_valor_import,topico="valor_total",direccion="importacion")    
    #Código para medios mas utilizados  
    transportes=[]
    
    for elemento in exportaciones:
        if elemento["transport_mode"] not in transportes:
            transportes.append(elemento["transport_mode"])
        
        
    #Ahora vamos a contar el número de veces que se utilizo cada transporte 
    transportes_exp=[]
    transportes_imp=[]
    for i in transportes:
        contador_exp=0
        contador_imp=0
        valor_exp=0
        valor_imp=0
        for j in exportaciones:
            if i==j["transport_mode"]:
                contador_exp+=1
                valor_exp+=int(j["total_value"])
        transportes_exp.append([i,contador_exp,valor_exp])
        
        for h in importaciones:
            if i==h["transport_mode"]:
                contador_imp+=1
                valor_imp+=int(h["total_value"])
        transportes_imp.append([i,contador_imp,valor_imp])
       
    mas_utilizados_exp=sorted(transportes_exp,key=lambda k: k[1],reverse=True)   
    mas_utilizados_imp=sorted(transportes_imp,key=lambda k: k[1],reverse=True)

    contador=1
    print("""
          """)
    print("Los 3 medios de transporte mas usados para exportar son: ")
    for i in mas_utilizados_exp:
        if contador>3:
            break
        print(contador, ".- ", i[0],"con " , i[1]," viajes y ",i[2]," de valor total")
        contador+=1
    
    contador=1
    print("""
          """)
    print("Los 3 medios de transporte mas usados para importar son: ")
    for i in mas_utilizados_imp:
        if contador>3:
            break
        print(contador, ".- ", i[0],"con " , i[1]," viajes y ",i[2], " de valor total")
        contador+=1
    
    
#Ahora buscaremos que paises aportan el 80% de las exportaciones
    total_exp_pais=[]
    for i in paises_export:
        valor_pais=0
        for j in exportaciones:
            if i == j["origin"]:
                valor_pais+=int(j["total_value"])
        total_exp_pais.append([i,valor_pais])#Aqui almacenamos el aporte de cada pais
    #Posteriormente ordenamos de mayor a menor las aportaciones            
    orden_total_pais=sorted(total_exp_pais,key=lambda k: k[1],reverse=True)
    
    #Y mostramos al usuario
    porcentaje=0
    contador=1
    print("""
          """)
    print("Países que aportan el 80% del valor total de las exportaciones")
    for i in orden_total_pais:
        if porcentaje<=(total_exp*0.8):#Mostraremos hasta que se cubra el 80%
            print(contador, ".- ",i[0]," aporta",i[1], " que representa un ", (i[1]/total_exp)*100,"%")
            contador+=1
            porcentaje+=i[1]
        else:
            break
    
 # Ahora buscaremos que paises aportan el 80% de las importaciones   
    total_imp_pais=[]
    for i in paises_import:
        valor_pais=0
        for j in importaciones:
            if i == j["destination"]:
                valor_pais+=int(j["total_value"])
        total_imp_pais.append([i,valor_pais])#Aqui almacenamos el aporte de cada pais
    #Posteriormente ordenamos de mayor a menor las aportaciones            
    orden_total_pais=sorted(total_imp_pais,key=lambda k: k[1],reverse=True)
    
    #Y mostramos al usuario
    porcentaje=0
    contador=1
    print("""
          """)
    print("Países que aportan el 80% del valor total de las importaciones")
    for i in orden_total_pais:
        if porcentaje<=(total_import*0.8):#Mostraremos hasta que se cubra el 80%
            print(contador, ".- ",i[0]," aporta",i[1], " que representa un ", (i[1]/total_import)*100,"%")
            contador+=1
            porcentaje+=i[1]
        else:
            break

#Ahora vamos a cer cuales son los productos mas exportados
    productos_mas_exp=[]
    productos_mas_import=[]
    for i in productos:
        contador1=0
        for j in exportaciones:
            if i==j["product"]:
                contador1+=1
        productos_mas_exp.append([i,contador1])
        contador2=0
        for h in importaciones:
            if i==h["product"]:
                contador2+=1
        productos_mas_import.append([i,contador2])
    
    orden_produc_mas_exp=sorted(productos_mas_exp,key=lambda k: k[1],reverse=True)
    orden_produc_mas_import=sorted(productos_mas_import,key=lambda k: k[1],reverse=True)
    
    contador=1
    print("""
          """)
    print("Los 10 producots mas exportados son:")
    for i in orden_produc_mas_exp:
        if contador>10:
            break
        print(contador,".- ",i[0], "con: ",i[1],"exportaciones")
        contador+=1
    
    contador=1
    print("""
          """)
    print("Los 10 producots mas importados son:")
    for i in orden_produc_mas_import:
        if contador>10:
            break
        print(contador,".- ",i[0], "con: ",i[1],"importaciones")
        contador+=1
    