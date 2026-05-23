import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

if "visibility" not in st.session_state:
    st.session_state.visibility = "hidden"


@st.cache_data
def load_data(file_name):
    return pd.read_parquet(file_name)

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
            label_visibility=st.session_state.visibility,
            value=df["DATE OCC"].max()
        )

        todate = st.datetime_input(
            "To",
            min_value=df["DATE OCC"].min(),
            max_value=df["DATE OCC"].max(),
            label_visibility=st.session_state.visibility,
            value=df["DATE OCC"].max()
        )

    if (flag):
        df = df[df["DATE OCC"] >= (datenow - datebfr)]
    else:
        df = df[ (df ["DATE OCC"] >= fromdate) & (df["DATE OCC"] <= todate)]




    fig = px.scatter_map(
        df,
        lat='LAT',
        lon='LON',
        center={
            "lat": df["LAT"].mean(),
            "lon": df["LON"].mean()
            },
        color="AREA NAME",
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
