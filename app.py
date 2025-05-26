#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="COVID & Lung Disease Cases",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="collapsed")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


#######################
# Load data
newsDF = pd.read_csv('data/COVID-19_and_Lung_Disease_News_Headlines_Dataset.csv')
casesDF = pd.read_csv('data/COVID-19_and_Lung_Disease_Cases_Dataset.csv')
facilitiesDF = pd.read_csv('data/Healthcare_Facilities_Dataset.csv')

# Clean Data
newsDF = newsDF.drop_duplicates()
casesDF = casesDF.drop_duplicates()
facilitiesDF = facilitiesDF.drop_duplicates()

newsDF["Date"] = pd.to_datetime(newsDF["Date"])
newsDF["Year"] = newsDF['Date'].dt.year
newsDF = newsDF.sort_values(by="Year")
casesDF["Date"] = pd.to_datetime(casesDF["Date"])
casesDF["Year"] = casesDF['Date'].dt.year
casesDF = casesDF.sort_values(by="Year")

#######################
# Sidebar
with st.sidebar:
    st.title('🦠 COVID & Lung Disease Cases')
    
    year_list = list(casesDF['Year'].unique())
    countries_list = list(casesDF['Country'].unique())

    selected_year = st.selectbox('Select a year', year_list)
    newsDF_selected = newsDF[newsDF['Year'] == selected_year]
    casesDF_selected = casesDF[casesDF['Year'] == selected_year]

    selected_country = st.selectbox('Select a country', countries_list)
    newsDF_selected = newsDF[newsDF['Country'] == selected_country]
    casesDF_selected = casesDF[casesDF['Country'] == selected_country]

#######################
# Plots


#######################
# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='small')

with col[0]:
    st.markdown('#### Title')

with col[1]:
    st.markdown('#### Title')
    

with col[2]:
    st.markdown('#### Title')

    with st.expander('About', expanded=True):
        st.write('''
            - :orange[**Title**]: ...
            ''')
