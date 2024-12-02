# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 09:17:27 2024

@author: Carmen
"""
import streamlit as st
from datetime import datetime, timedelta
from funciones import sql
from funciones import finanzas





st.title("")

base=sql.db_a_df("inversiones")
#base=base[base["INVERSOR"]=="Camilo"]
tail=base.tail(10).reset_index(drop=True)
seleccion=st.dataframe(tail,on_select="rerun",selection_mode=["single-row"],use_container_width=True)

operaciones=base["OPERACION"].unique()




c1,c2=st.columns(2)


with c1:
    with st.form("my_form"):
        st.header("Agregar Movimiento")
        inversor=st.selectbox("Seleccione inveror",["Camilo","Celeste"])
        
        
        ticker = st.selectbox("Ticker",["BITO","SCHD","JEPQ","NVDY","IDV","QQQ","IVV","MSTR"],key="camilo")
            
        operacion = st.selectbox('Selecciona una opción', operaciones)
        monto=st.number_input("monto")
        unidades=st.number_input("acciones")
        submitted = st.form_submit_button("Agregar")
    
        if submitted:
            sql.insertar_inversiones(ticker,inversor,operacion,monto,unidades)
            st.rerun()
            

with c2:

    try:
        selector=seleccion['selection']['rows'][0]
        # st.text(seleccion)
        # st.text(selector)
        
        
        
        with st.form("my_form2"):
            st.header("Elimnar movimiento")
            ID=tail["ID"][selector]
            ticker = base[base["ID"]==selector]["TICKER"]
            operacion = base[base["ID"]==selector]["OPERACION"]
            monto=base[base["ID"]==selector]["MONTO"]
            unidades=base[base["ID"]==selector]["UNIDADES"]
            submitted2 = st.form_submit_button("eliminar")
            st.text(ID)
        
        
            if submitted2:
                sql.borrar_por_id(ID)
                st.session_state.selected_rows = []  # Limpia la selección
                st.experimental_rerun()
            
    except:
        selector=1

