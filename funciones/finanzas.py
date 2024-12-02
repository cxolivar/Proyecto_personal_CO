

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import streamlit as st
from funciones import sql
import plotly.graph_objects as go


def obtener_precios_periodo(simbolo, fecha_inicio, fecha_fin):
    """
    Obtiene los precios históricos de una acción para un período específico

    Parameters:
    simbolo (str): Símbolo del ticker (ej: 'AAPL', 'GOOGL')
    fecha_inicio (str): Fecha inicial en formato 'YYYY-MM-DD'
    fecha_fin (str): Fecha final en formato 'YYYY-MM-DD'

    Returns:
    pandas.DataFrame: DataFrame con los precios históricos
    """
    try:
        ticker = yf.Ticker(simbolo)
        hist = ticker.history(start=fecha_inicio, end=fecha_fin)

        if not hist.empty:
            hist = hist.round(2)
            return hist
        return None

    except Exception as e:
        #print(f"Error al obtener datos para {simbolo}: {str(e)}")
        return None




def acumulado(simbolo, fecha_fin,base):
    base_s=base[base["TICKER"]==simbolo]
    inicio="2024-01-01"
    inicio = datetime.strptime(inicio, '%Y-%m-%d')
    inicio=inicio.date()    
    
    precios = obtener_precios_periodo(simbolo, inicio, fecha_fin)    
    rango_fecha=precios.reset_index()["Date"].dt.date
    
    

    acu_monto=[]
    acu_acciones=[]
    for fecha in rango_fecha:
        
        sum_monto = sum(base_s[(base_s["FECHA"] >= inicio) & (base_s["FECHA"] <= fecha) & (base_s["OPERACION"] == "COMPRA")]["MONTO"])
        sum_acciones = sum(base_s[(base_s["FECHA"] >= inicio) & (base_s["FECHA"] <= fecha) & (base_s["OPERACION"] == "COMPRA")]["UNIDADES"])
        acu_monto.append(sum_monto)
        acu_acciones.append(sum_acciones)    
    
    
    
    pd.to_datetime(base_s["FECHA"]).info()
    
    
    





    acumulado = pd.DataFrame({"Fecha": rango_fecha, "Monto": acu_monto, "Acciones": acu_acciones})
    acumulado["Precio_accion"]=precios.reset_index()["Close"]
    acumulado["Monto_invertido"] = acumulado["Acciones"] *precios.reset_index()["Close"]
    acumulado["Rentabilidad"] = (acumulado["Monto_invertido"]-acumulado["Monto"])/acumulado["Monto"]
    return acumulado


def grafico(simbolo, df):
    # Configuramos el estilo del gráfico
    plt.style.use('classic')
    
    # Creamos un solo gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Graficamos ambas líneas en el mismo eje
    ax.plot(df["Fecha"], df['Monto_invertido'],
            color='red', label='Valor Inversión', linewidth=2)
    ax.plot(df["Fecha"], df['Monto'], 
            color='blue', label='Invertido', linewidth=2)
    
    # Configuración del gráfico
    ax.set_title(f'Evolución del Monto para {simbolo}',
                fontsize=12, pad=15)
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precio ($)')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='center left', bbox_to_anchor=(0.0, 0.5))
    
    # Rotamos las fechas para mejor legibilidad
    plt.setp(ax.get_xticklabels(), rotation=45)
    
    # Ajustamos el espaciado
    plt.tight_layout()
    
    # Mostramos el gráfico
    plt.show()
    
    st.pyplot(fig)
    

def grafico_fecha(simbolo, df_aux,tiempo):
    
    if tiempo=="Mes":
        delta=30
    elif tiempo=="6 meses":
        delta=180
    elif tiempo=="1 año":
        delta=365
    elif tiempo=="1 semana":
        delta=7
        
        
    
    ahora = datetime.now().date()
    fecha_inicial=ahora-timedelta(days=delta)
    
    df=df_aux[(df_aux["Fecha"]>=fecha_inicial)&(df_aux["Fecha"]<=ahora)]
    
    
    # Configuramos el estilo del gráfico
    plt.style.use('classic')
    
    # Creamos un solo gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Graficamos ambas líneas en el mismo eje
    ax.plot(df["Fecha"], df['Monto_invertido'],
            color='red', label='Valor Inversión', linewidth=2)
    ax.plot(df["Fecha"], df['Monto'], 
            color='blue', label='Invertido', linewidth=2)
    
    # Configuración del gráfico
    ax.set_title(f'Evolución del Monto para {simbolo}',
                fontsize=12, pad=15)
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precio ($)')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='center left', bbox_to_anchor=(0.0, 0.5))
    
    # Rotamos las fechas para mejor legibilidad
    plt.setp(ax.get_xticklabels(), rotation=45)
    
    # Ajustamos el espaciado
    plt.tight_layout()
    
    # Mostramos el gráfico
    plt.show()
    
    st.pyplot(fig)    


def datos_conjunto(simbolos,base):
    
    aux=acumulado(simbolos[0],datetime.now().date()+timedelta(days=1),base)
    todo=pd.DataFrame()
    todo["Fecha"]=aux["Fecha"]
    todo["Monto"]=0
    todo["Monto_invertido"]=0

    for simbolo in simbolos:
        
        aux=acumulado(simbolo,datetime.now().date(),base)
                
        todo["Monto"]=todo["Monto"]+aux["Monto"]
        todo["Monto_invertido"]=todo["Monto_invertido"]+aux["Monto_invertido"]
        

        
        # print(todo["Monto"])
       
        
    return todo
    


def info_accion(simbolo,base):

    stock = yf.Ticker(simbolo)
    todays_data = stock.history(period="1d")
    precio_actual = todays_data['Close'][0]
    
    #precio_actual=obtener_precios_periodo(simbolo, datetime.now().date(), datetime.now().date()+timedelta(days=1)).reset_index()["Close"][0]
    total_acciones=sum(base[(base["TICKER"]==simbolo)&((base["OPERACION"]=="COMPRA"))]["UNIDADES"])
    total_monto=sum(base[(base["TICKER"]==simbolo)&((base["OPERACION"]=="COMPRA"))]["MONTO"])
    total_dividendos=sum(base[(base["TICKER"]==simbolo)&((base["OPERACION"]=="DIVIDENDO"))]["MONTO"])
    precio_compra=total_monto/total_acciones
    rentabilidad=(precio_actual-precio_compra)/precio_compra
    
    
    
    return total_acciones,total_monto,total_dividendos,precio_compra,rentabilidad,precio_actual


def faltante(simbolo,base,meta,politica):
    total_acciones,total_monto,total_dividendos,precio_compra,rentabilidad,precio_actual=info_accion(simbolo, base)
    
    ticker = simbolo
    stock = yf.Ticker(ticker)
    todays_data = stock.history(period="1d")
    current_price = todays_data['Close'][0]
    fal=meta*politica-current_price*total_acciones
    return fal

def orden_inversion(meta,base):
    meta=meta
    politica=pd.DataFrame({"TICKER":["NVDY","BITO","IDV","SCHD","JEPQ"],
                           "POLITICA":[0.35,0.35,0.1,0.1,0.1]})   
    
    
    #faltante
    politica["FALTANTE"]=0
    aux=[]
    for ti in politica["TICKER"]:
        pol=politica[politica["TICKER"]==ti]["POLITICA"][politica.loc[politica["TICKER"]==ti].index[0]]          
        bi=faltante(ti, base, meta,pol)    
        aux.append(bi)
    
    politica["FALTANTE"]=aux
    
 
    #rendimiento    
    politica["RENTABILIDAD"]=0
    aux=[]
    for ti in politica["TICKER"]:
        pol=politica[politica["TICKER"]==ti]["POLITICA"][politica.loc[politica["TICKER"]==ti].index[0]]          
        total_acciones,total_monto,total_dividendos,precio_compra,rentabilidad,precio_actual=info_accion(ti,base) 
        aux.append(rentabilidad)
    
    politica["RENTABILIDAD"]=aux 
 
    df_ordenado = politica.sort_values(by='RENTABILIDAD')
    B=df_ordenado["TICKER"].to_list()
    
    df_ordenado_faltante=df_ordenado[df_ordenado["FALTANTE"]>5]
    invertir=df_ordenado_faltante.head(1)["TICKER"].to_list()
    
    invertir.extend(B)
    simbolos = []
    for elemento in invertir:
        if elemento not in simbolos:
            simbolos.append(elemento)
    return simbolos,politica
            
def dias_habiles_hasta_fin_ano():
  """Calcula los días hábiles entre la fecha actual y fin de año, considerando solo fines de semana.

  Returns:
    Un entero representando la cantidad de días hábiles.
  """

  # Obtener la fecha actual y la de fin de año
  hoy = pd.to_datetime('today')

  fin_ano=datetime(hoy.year, 12, 31)
  # Crear un rango de fechas
  fechas = pd.date_range(start=hoy, end=fin_ano)

  # Crear un DataFrame con las fechas y un indicador de día hábil
  df = pd.DataFrame({'fecha': fechas})
  df['dia_semana'] = df['fecha'].dt.dayofweek
  df['dia_habil'] = ~(df['dia_semana'].isin([5, 6]))  # Solo consideramos fines de semana

  # Contar los días hábiles
  dias_habiles = df['dia_habil'].sum()

  return dias_habiles

def grafico_torta(simbolos,base):


    labels=simbolos
    values=[]
     
    for sim in labels:
        
        total_acciones,total_monto,total_dividendos,precio_compra,rentabilidad,precio_actual=info_accion(sim,base)
        values.append(total_acciones*precio_actual)
        

        n = len(labels)
        parents = ["Portfolio"] * n

     

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
        # title={
        #     'text': "Distribución de los dividendos",
        #     'y':0.95,
        #     'x':0.5,
        #     'xanchor': 'center',
        #     'yanchor': 'top',
        #     'font': dict(size=20)
        # },
        width=800,
        height=600,
        margin=dict(t=100, l=25, r=25, b=25)
    )
    
    #fig.show()
    return fig

def valor_dolar(base):
    dolares=sum(base[base["OPERACION"]=="AUMENTO FONDO"]["MONTO"])
    pesos=sum(base[base["OPERACION"]=="AUMENTO FONDO"]["UNIDADES"])
    
    precio_promedio_compra=pesos/dolares
    
    
    # Definimos el par de divisas: USDCLP (Dólar estadounidense / Peso chileno)
    ticker = "USDCLP=X"
    # Obtenemos los datos del ticker
    data = yf.download(tickers=ticker, period="1d", interval="1m")
    # Extraemos el último precio de cierre
    precio_dolar = data['Close'].iloc[-1]
    a=precio_dolar[0]
    return a,precio_promedio_compra



def orden_inversion_cele(meta,base):
    meta=meta
    politica=pd.DataFrame({"TICKER":["IVV","QQQ","MSTR"],
                           "POLITICA":[0.45,0.45,0.1]})   
    
    
    #faltante
    politica["FALTANTE"]=0
    aux=[]
    for ti in politica["TICKER"]:
        pol=politica[politica["TICKER"]==ti]["POLITICA"][politica.loc[politica["TICKER"]==ti].index[0]]          
        bi=faltante(ti, base, meta,pol)    
        aux.append(bi)
    
    politica["FALTANTE"]=aux
    
 
    #rendimiento    
    politica["RENTABILIDAD"]=0
    aux=[]
    for ti in politica["TICKER"]:
        pol=politica[politica["TICKER"]==ti]["POLITICA"][politica.loc[politica["TICKER"]==ti].index[0]]          
        total_acciones,total_monto,total_dividendos,precio_compra,rentabilidad,precio_actual=info_accion(ti,base) 
        aux.append(rentabilidad)
    
    politica["RENTABILIDAD"]=aux 
 
    df_ordenado = politica.sort_values(by='RENTABILIDAD')
    B=df_ordenado["TICKER"].to_list()
    
    df_ordenado_faltante=df_ordenado[df_ordenado["FALTANTE"]>5]
    invertir=df_ordenado_faltante.head(1)["TICKER"].to_list()
    
    invertir.extend(B)
    simbolos = []
    for elemento in invertir:
        if elemento not in simbolos:
            simbolos.append(elemento)
    return simbolos,politica

def caja_camilo(base):
    
    filtro=["DIVIDENDO","AUMENTO FONOD","VENTA","INTERESES"]
    suma=sum(base[base["OPERACION"].isin(filtro)]["MONTO"])
    
    
    filtro=["COMPRA"]
    resta=sum(base[base["OPERACION"].isin(filtro)]["MONTO"])   
    
    return suma-resta+9680.71999324500000

def caja_celeste(base):
    
    filtro=["DIVIDENDO","AUMENTO FONDO","VENTA","INTERESES"]
    suma=sum(base[base["OPERACION"].isin(filtro)]["MONTO"])
    
    
    filtro=["COMPRA"]
    resta=sum(base[base["OPERACION"].isin(filtro)]["MONTO"])   
    
    return suma-resta










