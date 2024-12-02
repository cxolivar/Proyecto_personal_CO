# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 15:11:04 2024

@author: Carmen
"""
import streamlit as st
from datetime import datetime, timedelta
from funciones import sql
from funciones import finanzas
import pandas as pd
import math

#sql.borrar_datos_db("inversiones")
#sql.insertar_df_masico()
#sql.crear_tabla()
#base=sql.db_a_df("inversiones")


simbolos=["IVV","QQQ","MSTR"]
tiempos=["Mes","6 meses","1 año","1 semana"]







# Ejemplo de uso en Streamlit
def main():
    st.set_page_config(layout="wide")    

    base=sql.db_a_df("inversiones")
    base=base[base["INVERSOR"]=="Celeste"]
    aaaaa=base[base["TICKER"]=="IVV"]
    
    precio_dolar,precio_promedio_compra=finanzas.valor_dolar(base)
  
    # st.title("2.Tablero Tipo Racional")
    
    meta=10340
    simbolos,politica=finanzas.orden_inversion_cele(meta,base)
    columnas=math.ceil(len(simbolos)/2)
    faltante=sum(politica[politica["FALTANTE"]>0]["FALTANTE"])
    dias_habiles=finanzas.dias_habiles_hasta_fin_ano()
    
    c1,c2=st.columns(2)
    
    
    with c1:
        
        
        st.text(f"Invertir: {faltante/dias_habiles:.0f}    Meta: {meta}")
        st.text(f"Precio Dolar: {precio_dolar*1.0049:.0f}")
        st.text(f"Precio compra Dolar: {precio_promedio_compra:.0f}")
        

        
        
        columna=st.columns(columnas)
        cont=0
        for i in simbolos[:columnas]:
            
            with columna[cont]:            
                cont=1+cont
                # st.write(f"**TICKER: {i}**")
                total_acciones,total_monto,total_dividendos,precio_compra,rentabilidad,precio_actual=finanzas.info_accion(i,base)
                # st.text(f"Total Acciones: {total_acciones:.2f}")
                # st.text(f"Total Invertido: {total_monto:.0f}")
                # st.text(f"Dividendos: {total_dividendos:.2f}")
                # st.text(f"Precio compra: {precio_compra:.2f}")
                # st.text(f"Rentabilidad: {rentabilidad*100:.2f} %") 
                
                pol=politica[politica["TICKER"]==i]["POLITICA"][politica.loc[politica["TICKER"]==i].index[0]]          
                bi=finanzas.faltante(i, base, meta,pol)    
                # st.text(f"Faltante: {bi:.0f} ")              
                
                if bi > 5:
                    st.markdown(f"""
                    <div style="background-color: #AED6F1; padding: 8px;border:2px solid black;border-radius:10px;width:170px;height:200px;text-align:left">
                      <strong> TICKER: {i} </strong>  <br> 
                      Acciones {total_acciones:.2f}<br>
                      Invertido: {total_monto:.0f}<br>
                      Dividendos: {total_dividendos:.2f}<br>
                      Precio compra: {precio_compra:.2f}<br>
                      Rentabilidad: {rentabilidad*100:.2f} %<br>
                      Faltante: {bi:.0f}
                      
                    </div>
                    """, unsafe_allow_html=True)            
        
                
                else:
                    st.markdown(f"""
                    <div style="background-color: #2E86C1; padding: 8px;border:2px solid black;border-radius:10px;width:170px;height:200px;text-align:left">
                      <strong> TICKER: {i} </strong>  <br> 
                      Acciones {total_acciones:.2f}<br>
                      Invertido: {total_monto:.0f}<br>
                      Dividendos: {total_dividendos:.2f}<br>
                      Precio compra: {precio_compra:.2f}<br>
                      Rentabilidad: {rentabilidad*100:.2f} %<br>
                      Faltante: {bi:.0f}
                      
                    </div>
                    """, unsafe_allow_html=True)      
        
        
        st.text("")
        
        columna=st.columns(columnas)
        cont=0
        for i in simbolos[columnas:]:
            
            with columna[cont]:            
                cont=1+cont
                # st.write(f"**TICKER: {i}**") 
                total_acciones,total_monto,total_dividendos,precio_compra,rentabilidad,precio_actual=finanzas.info_accion(i,base)
                # st.text(f"Total Acciones: {total_acciones:.2f}")
                # st.text(f"Total Invertido: {total_monto:.2f}")
                # st.text(f"Dividendos: {total_dividendos:.2f}")
                # st.text(f"Precio compra: {precio_compra:.2f}")
                # st.text(f"Rentabilidad: {rentabilidad*100:.2f} %") 
                
                pol=politica[politica["TICKER"]==i]["POLITICA"][politica.loc[politica["TICKER"]==i].index[0]]          
                bi=finanzas.faltante(i, base, meta,pol)    
                # st.text(f"Faltante: {bi:.0f} ")      
            
                if bi > 5:
                    st.markdown(f"""
                    <div style="background-color: #AED6F1; padding: 8px;border:2px solid black;border-radius:10px;width:170px;height:200px;text-align:left">
                      <strong> TICKER: {i} </strong>  <br> 
                      Acciones {total_acciones:.2f}<br>
                      Invertido: {total_monto:.0f}<br>
                      Dividendos: {total_dividendos:.2f}<br>
                      Precio compra: {precio_compra:.2f}<br>
                      Rentabilidad: {rentabilidad*100:.2f} %<br>
                      Faltante: {bi:.0f}
                      
                    </div>
                    """, unsafe_allow_html=True)            
        
                
                else:
                    st.markdown(f"""
                    <div style="background-color: #2E86C1; padding: 8px;border:2px solid black;border-radius:10px;width:170px;height:200px;text-align:left">
                      <strong> TICKER: {i} </strong>  <br> 
                      Acciones {total_acciones:.2f}<br>
                      Invertido: {total_monto:.0f}<br>
                      Dividendos: {total_dividendos:.2f}<br>
                      Precio compra: {precio_compra:.2f}<br>
                      Rentabilidad: {rentabilidad*100:.2f} %<br>
                      Faltante: {bi:.0f}
                      
                    </div>
                    """, unsafe_allow_html=True)    
    
  
    with c2:
        st.plotly_chart(finanzas.grafico_torta(simbolos,base))


    
  
    
  

    
  
    
  
    simbolos=["QQQ","IVV","MSTR"]   
  
    st.title('Rentabilidad Conjunto')
    
    todo=finanzas.datos_conjunto(simbolos,base)
    tiempo = st.selectbox('Selecciona una fecha',tiempos,key="conjunto")
    finanzas.grafico_fecha("Conjunto",todo,tiempo)
    
    st.divider()
    
    
    
    st.title('Rentabilidad Individual')    
    simbolo = st.selectbox('Selecciona una función', simbolos)
    tiempo = st.selectbox('Selecciona una fecha',tiempos,key="individual")
    prueba = finanzas.acumulado(simbolo, datetime.now().date()+timedelta(days=1),base)      
    finanzas.grafico_fecha(simbolo,prueba,tiempo)
    total_acciones,total_monto,total_dividendos,precio_compra,rentabilidad,precio_actual=finanzas.info_accion(simbolo, base)
    
    st.text(f"Total Acciones: {total_acciones}")
    st.text(f"Total Invertido: {total_monto}")
    st.text(f"Dividendos: {total_dividendos}")
    st.text(f"Precio compra: {precio_compra}")
    st.text(f"Rentabilidad: {rentabilidad*100} %")
    
    
    
    
    
    
  

    



if __name__ == '__main__':
    main()



