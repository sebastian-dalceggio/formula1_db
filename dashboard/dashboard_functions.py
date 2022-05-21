import streamlit as st
import requests
import pandas as pd
import altair as alt
from classes.decorators import retry

@retry(tries=100, time_sleep=2)
@st.experimental_singleton
def get_data(api_url, data):
    for k in data.keys():
        data[k] = pd.read_json(requests.get(api_url + k).json()["data"])
    return data

def line_plot(df, x, y, title, filter_column=None, filter_value=None):
    df = df.copy()
    if filter_column != None and filter_value != None:
        df = df.loc[df[filter_column] == filter_value]
        title = title + " in " + str(filter_value)
    chart = (
        alt.Chart(
            data=df,
            title=title,
        )
        .mark_line()
        .encode(
            x=alt.X(x, type="ordinal", axis=alt.Axis(title='Year')),
            y=alt.Y(y, axis=alt.Axis(title='Average time'), sort="descending")
        )
    ).properties(
    width=500,
    height=300)
    st.altair_chart(chart)
    return 0

def bar_char(df, x, y, to_drop=None, rename=None, total_rows=None):
    df = df.copy()
    df.index = df.index + 1 
    if to_drop != None:
        for column in to_drop:
            df.drop(column, axis=1, inplace=True)
    if rename != None:
        df.rename(rename, axis=1, inplace=True)
    if total_rows != None:
        df.drop(df.index[total_rows:], inplace=True)
    chart = alt.Chart(df).mark_bar().encode(
        alt.X(x),
        alt.Y(y, sort="-x")
    ).properties(
    width=500,
    height=300)
    
    text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text=x
        )
    st.write(chart + text)
    return 0