import streamlit as st
import pandas as pd
import numpy as np
def main():
    option = st.sidebar.text_input("I - Digite o separador do seu .CSV",',')
    
    uploaded_file = st.sidebar.file_uploader("II - Buscar arquivo CSV ", type="csv")
#função que carrega um arquivo .CSV e transforma num Dataframe
    def load_data(uploaded_file,option):
        try:
            data = pd.read_csv(uploaded_file,sep=option,thousands = '.', decimal = ',')
            data['Data'] = pd.to_datetime(data['Data'],format='%Y/%m/%d',errors='ignore')            
            return data
        except KeyError: 
            st.sidebar.error('Selecione o separador correto')
        except TypeError: 
            data = load_data(uploaded_file,option)
        except AttributeError:    
            st.error('Algo deu errado')
    
        
    if uploaded_file is not None:
        data = load_data(uploaded_file,option)
        df = data
        try:
            data.to_csv('data.csv',sep=option)
            #Ver dados brutos        
            #visualizar dados em branco
            st.write(df)         
                   
main()  

             
