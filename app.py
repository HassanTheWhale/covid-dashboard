#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

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

facilitiesDF.rename(columns={"ICU_Beds": "ICU Beds", "Medical_Staff": "Medical Staff"}, inplace=True)


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

    selected_country = st.selectbox('Select a country', countries_list)
    selected_year = st.selectbox('Select a year', year_list)

    newsDF_selected = newsDF[(newsDF['Country'] == selected_country) & (newsDF['Year'] == selected_year)]
    casesDF_selected = casesDF[(casesDF['Country'] == selected_country) & (casesDF['Year'] == selected_year)]
    facilitiesDF_selected = facilitiesDF[(facilitiesDF['Country'] == selected_country)]


#######################
# Plots

# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num}'

# Calculation year-over-year covid cases migrations
def calculate_covid_cases_difference(input_df, input_country, input_year):
  selected_casesDF_data = input_df[(input_df['Country'] == input_country) & (input_df['Year'] == input_year)]
  previous_year_data = input_df[(input_df['Country'] == input_country) & (input_df['Year'] == input_year-1)]

  selected_casesDF_data['COVID_Cases_Year'] = selected_casesDF_data['COVID_Cases'].sum()
  selected_casesDF_data['COVID_Cases_Diff'] = selected_casesDF_data['COVID_Cases'].sum() - previous_year_data['COVID_Cases'].sum()
  return selected_casesDF_data.sort_values(by="COVID_Cases", ascending=False)

def calculate_lung_cases_difference(input_df, input_country, input_year):
  selected_casesDF_data = input_df[(input_df['Country'] == input_country) & (input_df['Year'] == input_year)]
  previous_year_data = input_df[(input_df['Country'] == input_country) & (input_df['Year'] == input_year-1)]

  selected_casesDF_data['Lung_Cases_Year'] = selected_casesDF_data['Lung_Disease_Cases'].sum()
  selected_casesDF_data['Lung_Cases_Diff'] = selected_casesDF_data['Lung_Disease_Cases'].sum() - previous_year_data['Lung_Disease_Cases'].sum()
  return selected_casesDF_data.sort_values(by="Lung_Disease_Cases", ascending=False)

def calculate_death_cases_difference(input_df, input_country, input_year):
  selected_casesDF_data = input_df[(input_df['Country'] == input_country) & (input_df['Year'] == input_year)]
  previous_year_data = input_df[(input_df['Country'] == input_country) & (input_df['Year'] == input_year-1)]

  selected_casesDF_data['Death_Cases_Year'] = selected_casesDF_data['Deaths'].sum()
  selected_casesDF_data['Death_Cases_Diff'] = selected_casesDF_data['Deaths'].sum() - previous_year_data['Deaths'].sum()
  return selected_casesDF_data.sort_values(by="Deaths", ascending=False)


#######################
# Dashboard Main Panel
col = st.columns((0.5, 1.5, 1), gap='medium')

with col[0]:
    st.markdown(f'#### Total Numbers in {selected_country} - {selected_year}')
    
    df_covid_cases_difference_sorted = calculate_covid_cases_difference(casesDF, selected_country, selected_year)

    if selected_year > 2020:
        covid_Cases_year = format_number(df_covid_cases_difference_sorted["COVID_Cases_Year"].iloc[0])
        covid_Cases_delta = format_number(df_covid_cases_difference_sorted["COVID_Cases_Diff"].iloc[0])
    else:
        covid_Cases_year = casesDF_selected['COVID_Cases'].sum()
        covid_Cases_delta = ''
    st.metric(label="COVID Cases", value=covid_Cases_year, delta=covid_Cases_delta)

    df_lung_cases_difference_sorted = calculate_lung_cases_difference(casesDF, selected_country, selected_year)

    if selected_year > 2020:
        covid_Cases_year = format_number(df_lung_cases_difference_sorted["Lung_Cases_Year"].iloc[0])
        covid_Cases_delta = format_number(df_lung_cases_difference_sorted["Lung_Cases_Diff"].iloc[0])
    else:
        covid_Cases_year = casesDF_selected['Lung_Disease_Cases'].sum()
        covid_Cases_delta = ''
    st.metric(label="Lung Disease Cases", value=covid_Cases_year, delta=covid_Cases_delta)

    df_lung_cases_difference_sorted = calculate_death_cases_difference(casesDF, selected_country, selected_year)
    if selected_year > 2020:
        covid_Cases_year = format_number(df_lung_cases_difference_sorted["Death_Cases_Year"].iloc[0])
        covid_Cases_delta = format_number(df_lung_cases_difference_sorted["Death_Cases_Diff"].iloc[0])
    else:
        covid_Cases_year = casesDF_selected['Deaths'].sum()
        covid_Cases_delta = ''
    st.metric(label="Death Cases", value=covid_Cases_year, delta=covid_Cases_delta)

    with st.expander('About', expanded=True):
        st.write('''
            - :orange[**Course**]: CS-497
            - :orange[**Project**]: Dashboard
            - :orange[**Developed By**]: Hassan AlShammari
            - :orange[**Dataset**]: COVID-19
            ''')

with col[1]:
    st.markdown('#### Death vs Resources')
    scatter_casesDF = casesDF_selected.copy();
    scatter_casesDF = scatter_casesDF.groupby('Region')[['Deaths']].sum().reset_index();

    scatter_facilitiesDF = facilitiesDF.copy();
    scatter_facilitiesDF = scatter_facilitiesDF.groupby('Region')[['Medical Staff', 'ICU Beds', 'Ventilators']].mean().reset_index()
    casesFacilitiesMerged = pd.merge(scatter_casesDF, scatter_facilitiesDF, on='Region')

    df = px.data.iris()
    fig = px.scatter(casesFacilitiesMerged, x="Medical Staff", y="Ventilators", color="Deaths", color_continuous_scale="Reds", hover_data=['Deaths'])

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('#### Reports Count per Region per')
    casesDF_selected_area = casesDF_selected.copy();
    casesDF_selected_area["Month"] = casesDF_selected_area["Date"].dt.to_period("M").astype(str)

    casesDF_selected_area = casesDF_selected_area.groupby(["Month"])[["COVID_Cases", "Lung_Disease_Cases", "Deaths"]].sum().reset_index()

    casesDF_selected_area['Month'] = pd.to_datetime(casesDF_selected_area['Month'])

    months = casesDF_selected_area["Month"].unique()
    cases = ['COVID_Cases', "Lung_Disease_Cases", "Deaths"]

    data = {'Date': months}
    for case in cases:
        casesPerDate = []
        for date in months:
            df = casesDF_selected_area[(casesDF_selected_area["Month"] == date)]
            casesPerDate.append(df[case].sum())
        data[case] = casesPerDate
    
    df = pd.DataFrame(data)
    df = df.sort_values(by='Date')

    print(df[cases[0]])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df[cases[0]],
        name="COVID Cases",
        stackgroup='one' # define stack group
    ))

    fig.add_trace(go.Scatter(
        x=df['Date'], y=df[cases[1]],
        name="Lung Disease Cases",
        stackgroup='one' # define stack group
    ))

    fig.add_trace(go.Scatter(
        x=df['Date'], y=df[cases[2]],
        name="Death Cases",
        stackgroup='one' # define stack group
    ))
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

with col[2]:
    st.markdown('#### Regions vs COVID Cases')
    casesDF_selected_bar = casesDF_selected.copy();
    casesDF_selected_bar = casesDF_selected_bar.groupby('Region')["COVID_Cases"].sum().reset_index(name="COVID Cases")
    casesDF_selected_bar = casesDF_selected_bar.sort_values(by="COVID Cases", ascending=False)
    fig = px.bar(casesDF_selected_bar, x="Region", y="COVID Cases", color="Region")
    st.plotly_chart(fig, use_container_width=True)


    st.markdown('#### Country Health Resources')
    
    st.dataframe(facilitiesDF_selected[['Region', 'Hospitals', 'ICU Beds', 'Ventilators', 'Medical Staff']],
                 hide_index=True,
                 width=None,
                 )
