import streamlit as st
import pandas as pd
import plotly.express as px

co2_df = pd.read_csv("CO2_per_capita.csv", sep=";")
geo_df = pd.read_csv("geo_data.csv")

st.title("CO2 Emissions Dashboard")
st.header("Good morning, Good evening and Good night.")

df_clean = co2_df.dropna(subset=["CO2 Per Capita (metric tons)"])
df_clean = df_clean.sort_values("Year")

geo_clean = geo_df[["Three_Letter_Country_Code", "Continent_Name"]]

df_merged = df_clean.merge(
    geo_clean,
    left_on="Country Code",
    right_on="Three_Letter_Country_Code",
    how="left"
)

year = st.slider(
    "Select a year",
    min_value=int(df_merged["Year"].min()),
    max_value=int(df_merged["Year"].max()),
    value=2008
)

nb_displayed = st.selectbox(
    "Select number of countries",
    [3, 5, 10, 20, 30]
)



def top_n_emitters_v2(df, year, nb_displayed):
    df_filtered = df[df["Year"] == year]

    df_top = df_filtered.sort_values(
        "CO2 Per Capita (metric tons)",
        ascending=False
    ).head(nb_displayed)

    fig = px.bar(
        df_top,
        x="Country Name",
        y="CO2 Per Capita (metric tons)",
        color="Continent_Name",
        title=f"Top {nb_displayed} CO2 emitters per capita in {year}"
    )

    return fig


fig_bar = top_n_emitters_v2(df_merged, year, nb_displayed)
st.plotly_chart(fig_bar)


fig_scatter_map = px.scatter_geo(
    df_merged,
    locations="Country Code",
    size="CO2 Per Capita (metric tons)",
    color="Continent_Name",
    animation_frame="Year",
    hover_name="Country Name",
    projection="natural earth",
    title="CO2 emissions per capita by continent"
)

st.plotly_chart(fig_scatter_map)


fig_choropleth = px.choropleth(
    df_merged,
    locations="Country Code",
    color="CO2 Per Capita (metric tons)",
    animation_frame="Year",
    hover_name="Country Name",
    projection="natural earth",
    title="CO2 emissions per capita by country"
)

st.plotly_chart(fig_choropleth)

st.dataframe(co2_df)