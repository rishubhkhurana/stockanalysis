# This is a sample Python script.

import streamlit as st
from data.datadownloader import *
from data.namemapping import *
import mplfinance as mfin
import matplotlib.pyplot as plt

st.title("Let'strategy make money")
st.header('Probabilistic Trading Dashboard')
st.subheader('')
ticker = st.sidebar.selectbox("Ticker select", tickerlist)
volume = st.sidebar.radio('Volume', ['True', 'False'])
# get the selected ticker data
df = get_data(tickernames[ticker])
st.write(df.head(5))
# plotting the stock
fig, ax = plt.subplots(1,1)
ax = mfin.plot(df, type='candle', style='charles', ax=ax, mav=(12, 21))
st.pyplot(fig)





