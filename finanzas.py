
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import streamlit as st


base = pd.read_excel("base_prueba.xlsx")  # lectura de la base
# cambio de formato de fecha a 'YYYY-MM-DD'
base['FECHA'] = base['FECHA'].dt.strftime('%Y-%m-%d')
base["FECHA"] = pd.to_datetime(base["FECHA"])
base["FECHA"]=base["FECHA"].dt.date







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
        print(f"Error al obtener datos para {simbolo}: {str(e)}")
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

# simbolo="JEPQ"
# fecha_fin="2024-11-02"

# aaa=acumulado(simbolo, fecha_fin,base)



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
        

        
        print(todo["Monto"])
       
        
    return todo
    

def info_accion(simbolo,base):
    
    
    precio_actual=obtener_precios_periodo(simbolo, datetime.now().date(), datetime.now().date()+timedelta(days=1)).reset_index()["Close"][0]
    total_acciones=sum(base[(base["TICKER"]==simbolo)&((base["OPERACION"]=="COMPRA"))]["UNIDADES"])
    total_monto=sum(base[(base["TICKER"]==simbolo)&((base["OPERACION"]=="COMPRA"))]["MONTO"])
    total_dividendos=sum(base[(base["TICKER"]==simbolo)&((base["OPERACION"]=="DIVIDENDO"))]["UNIDADES"])
    precio_compra=total_monto/total_acciones
    rentabilidad=(precio_actual-precio_compra)/precio_compra
    
    
    
    return total_acciones,total_monto,total_dividendos,precio_compra,rentabilidad











simbolos=base["TICKER"].drop_duplicates()
fecha_fin="2024-11-06"
tiempos=["Mes","6 meses","1 año","1 semana"]

prueba=datos_conjunto(simbolos,base)


datetime.now().date()+timedelta(days=1)












# Ejemplo de uso en Streamlit
def main():
    

    
    
  
    st.title('Rentabilidad Conjunto')
    
    todo=datos_conjunto(simbolos,base)
    tiempo = st.selectbox('Selecciona una fecha',tiempos,key="conjunto")
    grafico_fecha("Conjunto",todo,tiempo)
    
    st.divider()
    
    
    
    st.title('Rentabilidad Individual')    
    simbolo = st.selectbox('Selecciona una función', simbolos)
    tiempo = st.selectbox('Selecciona una fecha',tiempos,key="individual")
    prueba = acumulado(simbolo, datetime.now().date()+timedelta(days=1),base)      
    grafico_fecha(simbolo,prueba,tiempo)
    total_acciones,total_monto,total_dividendos,precio_compra,rentabilidad=info_accion(simbolo, base)
    
    st.text(f"Total Acciones: {total_acciones}")
    st.text(f"Total Invertido: {total_monto}")
    st.text(f"Dividendos: {total_dividendos}")
    st.text(f"Precio compra: {precio_compra}")
    st.text(f"Rentabilidad: {rentabilidad*100} %")
    
    
  
    st.title('2. falta crear una funcion para el calculo de rentabilidades')
    st.title('3. crear una vista donde apareza el monto invertido, cantidad de acciones, valor actual, precio promedio de compra')
    st.title('4. crear una pestaña de dividendos')





if __name__ == '__main__':
    main()











