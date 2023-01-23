import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots

#pujada d'arxiu de dades
df = pd.read_pickle("df_final.pkl")
st.set_page_config(layout="wide")
# Creació de la distribució del dashboard

#sidebar
# Object notation
sidebar = st.sidebar
fila1 = st.container()
columna1,columna2 = st.container().columns(2)


with sidebar:
    st.header("Panell de variables")
    ""
    selected_establiment  = st.multiselect(label="Tipo d'Establiment",
                                        options=df.TipoEstablecimiento.unique(), default="A - AUTOSERVICIO")
                                        
    all_options = st.checkbox("Tots els establiments")
    if all_options:
        selected_establiment = df.TipoEstablecimiento.unique()


    # Selecció de mesos 
    selected_month  = st.multiselect(label="Mes a escollir",
                                        options=df.Mes.unique(), default=3)
                                        
    all_options2 = st.checkbox("Tots els Mesos")
    if all_options2:
        selected_month = df.Mes.unique()




with fila1:
    st.header("Evolució Ventes vs Morts de covid")
    df_filtrat = df[df.TipoEstablecimiento.isin(list(selected_establiment))]
    df_filtrat = df_filtrat.pivot_table(index="Mes",
                                        values=["Importe Venta","casos"],
                                        aggfunc={"Importe Venta":"sum","casos":"mean"}).reset_index()
    # Es crea un subplot per poder fer dos eixos y i fer un plot alhora de dos px.lines
    subfig = make_subplots(specs=[[{"secondary_y": True}]])

    # Creem dos figures independents
    fig = px.line(df_filtrat,y="Importe Venta",x="Mes")
    fig2 = px.line(df_filtrat,y="casos",x="Mes")

    fig2.update_traces(yaxis="y2")

    subfig.add_traces(fig.data + fig2.data)
    subfig.layout.xaxis.title="Mesos"
    subfig.layout.yaxis.title="Importe Venta"
    subfig.layout.yaxis2.title="Morts Covid"

    # Recoloring
    subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
    st.plotly_chart(subfig,use_container_width=True)

with columna1:
    st.header("Top 10 Families de productes")
    df_filtrat2 = df[(df.TipoEstablecimiento.isin(list(selected_establiment))) &
                     (df.Mes.isin(list(selected_month)))]
    df_filtrat2 = df_filtrat2.pivot_table(index="Familia",values="Importe Venta",aggfunc="sum")
    to_plot2 = df_filtrat2.nlargest(10,columns="Importe Venta").reset_index()
    fig3 = px.bar(to_plot2,x="Familia",y="Importe Venta")
    st.plotly_chart(fig3,use_container_width=True)


with columna2:
    st.header("Bottom 10 Families de productes")
    to_plot3 = df_filtrat2.nsmallest(10,columns="Importe Venta").reset_index()
    fig4 = px.bar(to_plot3,x="Familia",y="Importe Venta")
    st.plotly_chart(fig4,use_container_width=True)