from turtle import title
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import yfinance as yf 
import streamlit as st 
import base64

st.title('Stock Price 500 App')

st.markdown("""This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""") 

st.sidebar.header("User input Features")

@st.cache 
def load_data():
    url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html=pd.read_html(url,header=0)
    df=html[0]
    return df

df=load_data()
sector=df.groupby('GICS Sector')

sector_unique= sorted(df['GICS Sector'].unique())
selected_sector= st.sidebar.multiselect('Sector',sector_unique,sector_unique)

df_selected_sector= df[ (df['GICS Sector'].isin(selected_sector))]

st.header('Companies in the selected sector')
st.write('Data Dimension:'+str(df_selected_sector.shape[0])+'rows and'+str(df_selected_sector.shape[1])+'columns.')
st.dataframe(df_selected_sector)

#for downloading
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

def price_plot(symb):
    df= pd.DataFrame(data[symb].Close)
    df['Date']=df.index
    
    plt.plot(df.Date, df.Close,color="green",alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.xticks(rotation=90)
    plt.fill_between(df.Date, df.Close,color="green",alpha=0.3)
    plt.title(symb, fontweight='bold')
    return st.pyplot() #new 

st.set_option('deprecation.showPyplotGlobalUse', False)
 
no_company = st.sidebar.slider('Number of companies',1,5)
 
if st.button('Show plots'):
    
    st.header('Stock Closing Prices')
    for i in list(df_selected_sector.Symbol)[:no_company]:
        price_plot(i)
    

 
 
        
        


