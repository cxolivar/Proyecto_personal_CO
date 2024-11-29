# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 20:35:01 2024

@author: Carmen
"""
import mysql.connector
import pandas as pd

base_a_subir=pd.read_excel("G:/Mi unidad/Camilo Olivares/Finanzas/Python/Proyecto Finanzas/base_prueba.xlsx")


# conexion con la bd
database=mysql.connector.connect(
    host="mysql-3a922659-camiloaod.j.aivencloud.com",
    user="avnadmin",
    passwd="AVNS_ppnx6jFf5FGTQwyEUjZ",
    database="Inversiones",
    port=11358
        )


# cursor que permite ejeutar las consultas
cursor=database.cursor(buffered=True)

# crea la base de datos
def crear_db(nombre):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre}")



#borrar base
def borrar_db(nombre):
    cursor.execute(f"DELETE FROM {nombre}")
    database.commit()
               
#ver las tablas que hay en la base de datos utilizando codigo
def ver_tablas():
    cursor.execute("SHOW TABLES")
    for table in cursor:
        print(table)               
               
# consultar los datos de la base de datos    
def ver_datos_tabla(nombre):    
    cursor.execute(f"SELECT * FROM {nombre}")
    result=cursor.fetchall()
    for coche in result:
        print(coche)



    
# insertar registros en una tabla
def insertar_inversiones(ticker,operacion,monto,unidades):

    sql = "INSERT INTO inversiones (ticker, operacion, monto, unidades, fecha) VALUES (%s, %s, %s, %s, CURRENT_DATE)"
    values = (ticker, operacion, monto, unidades, )
    cursor.execute(sql, values)    
    database.commit()


def borrar_por_id(id):
     cursor.execute(f"DELETE FROM inversiones WHERE ID={id}")
     database.commit()   





def df_to_list_of_tuples(df):

    return [tuple(row) for row in df.itertuples(index=False)]

aaa=df_to_list_of_tuples(base_a_subir)

              
#insertar registros de forma masiva

cursor.executemany("INSERT INTO inversiones VALUES(null,%s,%s,%s,%s,%s)",aaa)
database.commit()
 



def insertar_df_masico(df):
    aaa=[tuple(row) for row in df.itertuples(index=False)]
    cursor.executemany("INSERT INTO inversiones VALUES(null,%s,%s,%s,%s,%s)",aaa)
    database.commit()
    
    



               



#actualiza registros de la base de datos
cursor.execute("UPDATE vehiculos SET modelo='Leon' WHERE marca='Seat'")
database.commit()
               

query=("SELECT * FROM inversiones")
df=pd.read_sql(query,database)

############################################

ver_tablas()
ver_datos_tabla("inversiones")
insertar_inversiones("BITO", "compra", 123, 33)
borrar_por_id(344)
borrar_db("inversiones")
df=pd.read_excel("base_prueba.xlsx")
crear_db("prueba")
insertar_df_masico(df)






cursor.execute("INSERT INTO inversiones VALUES(null,BITO,COMPRA,100,10,CURRENT_DATE)")
database.commit()



len(df)
sum(df[df["TICKER"]=="BITO"]["MONTO"])/1
               