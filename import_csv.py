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


            
            def estatistica(df):
                try:
                    import matplotlib.pylab as plt    
                    st.title('Estatística básica')
                    st.write(df.describe())
                    #Histograma
                    colunas = df.columns
                    st.title(' Verificação individual das variáveis')
                    variavel = st.selectbox('Selecione uma variável do seu conjunto de dados',colunas )
                    media = df[variavel].mean()
                    media = round(media,2)
                    mediana = df[variavel].median()
                    from scipy.stats import mode
                    moda = mode(df[variavel]).mode[0]
                    moda = round(moda,2)
                    #st.markdown(f'### Verificação individual das variáveis')
                    st.markdown(f' _________\n ')
                    st.markdown(f'### Medidas de tendência central para __ {variavel} __')
                    st.markdown(f'Média  **{media}**')
                    st.markdown(f'Mediana **{mediana}**')
                    st.markdown(f'Moda **{moda}**\n ________________')
                    
                    st.markdown(f'# Disperção dos dados\n ### Amplitude e Desvio Padrão ')
                
                    mim = df[variavel].min()
                    mim = round(mim,2)
                    maxxi = df[variavel].max()
                    import statistics
                    
                    desvio = df[variavel].std()
                    desvio = round(desvio,2)
                    
                    st.markdown(f'Mínimo  **{mim}**')
                    st.markdown(f' Máximo  **{maxxi}**')
                    
                    st.markdown(f'Desvio padrão  **{desvio}**\n ________________')
                    
                    st.markdown('A próxima visualização apresenta Histograma e diagrama de caixa para melhor verificação de distribuição dos dados.' )
                    
                    st.set_option('deprecation.showPyplotGlobalUse', False)#desativando função de codigo de grafico errado
                    #grafico histograma e boxplot
                    with st.spinner('Plotando Gráfico...aguarde'):
                        plt.title(f'Histograma de {variavel}')
                        plt.xlabel(f'{variavel}')                      
                        plt.title(f'Histograma de {variavel}',fontsize=15)
                        plt.xlabel(f'{variavel}',fontsize=15)
                        plt.ylabel('Frequencia',fontsize=15)
                        df[variavel].plot(kind='hist')                                                    
                        st.pyplot(fig=None)
                        plt.title(f'Diagrama de caixa para {variavel}',fontsize=15)
                        df[variavel].plot(kind='box')
                        st.pyplot(fig=None)
                except TypeError:   
                    st.warning("Selecione uma variável diferente de Data") 
                       
            
            
            #configuração
            def configuracao(df):
                try:
                    st.title("Preparação dados")                
                    variavel = st.selectbox("Selecione a variável que deseja filtrar:", df.columns)
                    minimo, maximo = st.slider("Selecione o intervalo de valores que deseja manter:", float(df[variavel].min()), float(df[variavel].max()), (float(df[variavel].min()), float(df[variavel].max())))
                    df_filtrado = df[(df[variavel] >= minimo) & (df[variavel] <= maximo)]
                    df_fora = df[(df[variavel] < minimo) | (df[variavel] > maximo)]
                    
                    
                    st.write(f'Dados dora do interval __{minimo} -  {maximo} ','Total de ', df_fora[variavel].count(),df_fora)
                                    
                    if st.button("Eliminar valores anormais"):
                        df[variavel] = np.where((df[variavel] < minimo) | (df[variavel] > maximo), np.nan, df[variavel]) 
                        st.info("""
                            ### Instruções

                            1- Para encontrar valores fora dos padrões em outras variáveis é necessário fazer o dowload clicando no botão abaixo

                            2- Carregue o arquivo novamente e repita o procedimento nº1,
                                até que todas as variáveis estejam salvas

                            """)      
                        st.download_button(
                                label="Download .csv",
                                data=df.to_csv(index=False),
                                file_name="data.csv",
                                mime="text/csv")
                except ValueError: 
                        st.info('selecione uma variável diferente de Data')
                
            def excluir_alterar(df):
                   # Exibe as colunas do arquivo .csv
                    colunas_selecionadas = st.multiselect("Selecione as colunas", df.columns)                                  
                    # Permite que o usuário exclua as colunas selecionadas
                    if st.button("Excluir colunas"):
                        df = df.drop(columns=colunas_selecionadas)  
                        st.info(""" Para salvar as alterações é necessário baixar os dados e carrega-los novamente
                    """)                     
                    # Exibe o arquivo .csv atualizado
                    #df = df.set_index('Data')
                    
                    st.write(df)
                    #df = df.apply(pd.to_numeric, errors='coerce').astype(float)
                    #st.write(df)
                    st.download_button(
                                        label="Download .csv",
                                        data=df.to_csv(index='Data'),
                                        file_name="data.csv",
                                        mime="text/csv")

            #ImPUTAR AUSENTES       
            #@st.cache(allow_output_mutation=True)
            def imputar(df): 
                try:   
                    st.markdown( """ 
            ### Imputação de dados ausentes 
                    
            - Dados inexistentes serão preenchidos através do método ** K-vizinho mais próximo** [(KNNImputer)]\
                        (https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html)                 
                    """ )
                    st.write(df.style.highlight_null())
                    with st.spinner('Aguarde...Imputando dados ausentes...isso pode demorar'):                
                        import time
                        #IMPUTAR AUSENTES
                        import numpy as np
                        from sklearn.impute import KNNImputer
                        #marcador de tempo
                        
                        df = df.set_index('Data')
                        X = df
                        imputer = KNNImputer(n_neighbors=30, weights="distance",)
                        t1 = time.time()
                        
                        matrix = imputer.fit_transform(X)
                        tempoExec = time.time() - t1
                        #st.write(f' "Tempo de execução: {format(tempoExec)} segundos"')
                        
                        
                        copia = pd.DataFrame(matrix, columns=df.columns)
                       
                        copia.index = df.index
                        st.write('#### Novo conjunto com dados imputados',copia, )
                        aviso = st.success('Parabens ...Esta operação foi concluida com sucesso')
                        st.download_button(
                                label="Download .csv",
                                data=df.to_csv(index=False),
                                file_name="data.csv",
                                mime="text/csv")
                except AttributeError:
                   st.warning('Infelismente houve um erro na operação, mande um email relatando o problema para \
                (walingson.costa@unemat.br)')
                except KeyError:
                    st.warning('Verifique as colunas do seu dataset, se necessário exclua colunas vazias')
                    excluir_alterar(df)
                    st.info('Carregue novamente os dados alterados')
                        
            st.sidebar.subheader("Preparação dados")
            page = st.sidebar.selectbox(
                "III - Navegar para", ["🏠Homepage", "🔎Inspecionar dados brutos", "💹Estatistica básica dos dados",
                "⚒️Identificação de possíveis erros","✍️Preencher dados ausentes"])
            
            if page == "🏠Homepage":
                    st.warning('Para carregar o arquivo corretamente digite o tipo de separador do arquivo.CSV')           
            if page == "🔎Inspecionar dados brutos": 
                opcao = st.sidebar.radio('⬇',('Ver dados', 'Excluir dados'))
                if opcao == 'Ver dados':
                    st.write('### Dados brutos', df)
                else:
                    excluir_alterar(df)
                          
                    
            if page == '💹Estatistica básica dos dados':   
                estatistica(df)
            if page == "⚒️Identificação de possíveis erros":
                configuracao(df)   
            if page == '✍️Preencher dados ausentes':
                imputar(df)

                
        except TypeError:
            st.error('Algo deu errado')
            st.sidebar.error('Selecione o separador correto')
  
    


           
main()               
