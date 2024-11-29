# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 19:54:47 2024

@author: Carmen
"""

import streamlit as st
from datetime import datetime, timedelta
from funciones import sql
from funciones import finanzas
import pandas as pd
import plotly.graph_objects as go




st.title("")

base=sql.db_a_df("inversiones")
base=base[base["INVERSOR"]=="Camilo"]

def dividendos_ordenados(base):
    dividendos=base[base["OPERACION"]=="DIVIDENDO"]
    
    dividendo_conjunto=pd.pivot_table(dividendos,
                                          values="MONTO",
                                          index=["TICKER"], 
                                          aggfunc="sum")
    dividendo_conjunto=dividendo_conjunto.reset_index()  #TOTAL HORAS POR RUT-CARRERA-SEDE-JORNADA
    dividendo_conjunto=dividendo_conjunto[dividendo_conjunto["MONTO"]>0].sort_values(by='MONTO', ascending=False)
    return dividendo_conjunto

# st.dataframe(dividendos_ordenados(base))


def grafico_jerarquia(base):

    # Organizar los datos
    labels = dividendos_ordenados(base)["TICKER"].to_list()  # ETFs
    
    
    
    n = len(labels)
    parents = ["Portfolio"] * n
    
    
    values =dividendos_ordenados(base)["MONTO"].to_list()
    
    # Crear el gráfico
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        textinfo="label+value+percent parent",
        texttemplate="<b>%{label}</b><br>$%{value:.2f}",
        hovertemplate="<b>%{label}</b><br>Valor: $%{value:.2f}<br>% del Portfolio: %{percentParent:.1%}<extra></extra>",
        marker=dict(
            colors=['#E8F4F8',  # Color más claro para el portfolio
                    '#2E86C1', '#85C1E9', '#AED6F1', '#D6EAF8',
                    '#FAD7A0', '#F8C471']
        )
    ))
    
    # Personalizar el diseño
    fig.update_layout(
        title={
            'text': "Distribución de los dividendos",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        },
        width=800,
        height=600,
        margin=dict(t=100, l=25, r=25, b=25)
    )
    
    #fig.show()
    return fig


def grafico_columnas_agrupadas(base):

    df=base[base["OPERACION"].isin(["DIVIDENDO","INTERESES"])]
    df['Fecha'] = pd.to_datetime(df['FECHA'],format='%Y-%m-%d')
    df["MES"]=df['Fecha'].dt.month
    # Agrupar por año y mes, y calcular la suma
    df_grouped = df.groupby([df['Fecha'].dt.year, df['Fecha'].dt.month])['MONTO'].sum()
    # Renombrar el índice para que muestre el año y el mes
    df_grouped.index = df_grouped.index.set_names(['Año', 'Mes'])    
    df_grouped=df_grouped.reset_index()
    df=df_grouped
    
    
    
    # Crear el gráfico de barras apiladas
    fig = go.Figure()
    for col in df.columns[1:-1]:
        fig.add_trace(go.Bar(x=df['Mes'], y=df["MONTO"], name=col))
    
    # Personalizar el gráfico
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=df['Mes'],
            ticktext=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],
            #title='Mes'
        ),
        yaxis=dict(
            title='Monto',
            tickformat='$'
        ),
        barmode='group'
    )
    
    # Mostrar el gráfico en Streamlit
    return fig  







st.plotly_chart(grafico_jerarquia(base))     
 
    
st.plotly_chart(grafico_columnas_agrupadas(base))   