# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 20:35:01 2024

@author: Carmen
"""
import mysql.connector
import pandas as pd

#base_a_subir=pd.read_excel("G:/Mi unidad/Camilo Olivares/Finanzas/Python/Proyecto Finanzas/base_prueba.xlsx")


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
def borrar_datos_db(nombre):
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
def insertar_inversiones(ticker,inversor,operacion,monto,unidades):

    sql = "INSERT INTO inversiones (ticker,inversor, operacion, monto, unidades, fecha) VALUES (%s,%s, %s, %s, %s, CURRENT_DATE)"
    values = (ticker,inversor, operacion, monto, unidades, )
    cursor.execute(sql, values)    
    database.commit()


def borrar_por_id(ID):
     cursor.execute(f"DELETE FROM inversiones WHERE ID={ID}")
     database.commit()   





def df_to_list_of_tuples(df):

    return [tuple(row) for row in df.itertuples(index=False)]




def insertar_df_masico():
    df=pd.read_excel("G:/Mi unidad/Camilo Olivares/Finanzas/Python/Proyecto Finanzas/base_prueba2.xlsx")
    aaa=[tuple(row) for row in df.itertuples(index=False)]
    cursor.executemany("INSERT INTO inversiones VALUES(null,%s,%s,%s,%s,%s,%s)",aaa)
    database.commit()
    
    
def borrar_tabla(nombre):
    cursor.execute(f"DROP TABLE {nombre}")
    database.commit()    

def crear_tabla():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inversiones(      
        ID int(10) auto_increment not null,        
        TICKER varchar(40) not null,
        INVERSOR varchar(40),
        OPERACION varchar(40) not null,
        MONTO float(20,10) not null,
        UNIDADES float(20,10) not null,
        FECHA DATE not null,
        CONSTRAINT pk_inversiones PRIMARY KEY(id)
        )
                   """)    
    
               

def db_a_df(nombre):
    query=(f"SELECT * FROM {nombre}")
    df=pd.read_sql(query,database)
    return df


# insertar registros en una tabla
def insertar_politica(ticker,meta):

    sql = "INSERT INTO politica (ticker,meta) VALUES (%s,%s)"
    values = (ticker,meta, )
    cursor.execute(sql, values)    
    database.commit()
