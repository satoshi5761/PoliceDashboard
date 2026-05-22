import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

if "visibility" not in st.session_state:
    st.session_state.visibility = "hidden"


@st.cache_data
def load_data(file_name):
    return pd.read_parquet(file_name)

def heat_map():
    global df

    radius = st.slider(
        label="radius",
        min_value=1,
        max_value=10,
        value=1
    )
    fig = px.density_map(
        df,
        lat='LAT',
        lon='LON', 
        center={
        "lat": df["LAT"].mean(),
        "lon": df["LON"].mean()
        },
        radius=radius, 
        zoom=10,
        map_style="open"
        )
    
    st.plotly_chart(fig)



def main():

    st.title("Police")


    df = load_data("crime_sample_50k.parquet")

    all_area = sorted(np.unique(df["AREA NAME"]))
    area = st.sidebar.multiselect(
        "Select Area",
        all_area,
        default=all_area
    )
    
    df = df[df["AREA NAME"].isin(area)]

    last = st.radio(
        "Rentang Waktu",
        ["1 Hour", "24 Hour", "3 days", "7 days", "1 Month", "Select Arbitrary Date"],
        horizontal=True,
    )

    datenow = df["DATE OCC"].max()
    datebfr = None

    flag = 1
    if (last != "Select Arbitrary Date"):
        st.session_state.visibility = 'collapsed'
    else:
        st.session_state.visibility = "visible"


    if (last == "1 Hour"):
        datebfr = pd.Timedelta(hours=1)
    
    elif (last == "24 Hour"):
        datebfr = pd.Timedelta(hours=24)

    elif (last == "3 days"):
        datebfr = pd.Timedelta(days=3)
    
    elif (last == "7 days"):
        datebfr = pd.Timedelta(days=7)

    elif (last == "1 Month"):
        datebfr = pd.Timedelta(days=30)
    else:
        flag = 0
        fromdate = st.datetime_input(
            "From",
            min_value=df["DATE OCC"].min(),
            max_value=df["DATE OCC"].max(),
            label_visibility=st.session_state.visibility
        )

        todate = st.datetime_input(
            "To",
            min_value=df["DATE OCC"].min(),
            max_value=df["DATE OCC"].max(),
            label_visibility=st.session_state.visibility
        )

    if (flag):
        df = df[df["DATE OCC"] >= (datenow - datebfr)]




    fig = px.scatter_map(
        df,
        lat='LAT',
        lon='LON',
        center={
            "lat": df["LAT"].mean(),
            "lon": df["LON"].mean()
            },
        color="Crm Cd Desc",
        hover_data=[
            "AREA NAME",
            "Crm Cd Desc",
            "Vict Age",
            "Vict Sex",
            "Weapon Desc"
        ],
        map_style="carto-darkmatter"

    )
    
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)


    st.write(df)
    
    

main()
