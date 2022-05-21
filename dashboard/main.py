import streamlit as st
from dashboard_functions import get_data, line_plot, bar_char

def main(api_url):

    data = {"average_lap_time": None, 
            "average_pitstops_time": None,
            "constructor_lap_records": None,
            "constructor_wins": None,
            "driver_lap_records": None,
            "driver_wins": None}

    data = get_data(api_url, data)

    st.write("""
    ## Formula 1 results dashboard 1950 - 2017
    """)

    if st.button("Refresh"):
        st.experimental_singleton.clear()
        data = get_data(api_url, data)
        st.experimental_rerun()

    data_to_show = st.sidebar.radio(
        "Select data",
        ("Average lap time per circuit",
        "Average pit stops time",
        "Constructor lap records",
        "Constructor wins",
        "Driver lap records",
        "Driver wins"))
        
    st.write(f"""### {data_to_show}""")

    if data_to_show == "Average lap time per circuit":

        circuit_names = sorted(data["average_lap_time"]["name"].unique())
        circuit = st.sidebar.selectbox(
        "Select circuit",
        circuit_names)
        line_plot(data["average_lap_time"],
            "year",
            "time",
            "Average lap time",
            filter_column="name",
            filter_value=circuit)

    elif data_to_show == "Average pit stops time":

        line_plot(data["average_pitstops_time"],
            "year",
            "time",
            "Average pitsopts time")

    elif data_to_show == "Constructor lap records":

        bar_char(data["constructor_lap_records"],
            x="Fastest lap records",
            y="Constructor",
            to_drop=["constructorid", "nationality"],
            rename={"name": "Constructor", "fastestlaps": "Fastest lap records"},
            total_rows=10)

    elif data_to_show == "Constructor wins":

        bar_char(data["constructor_wins"],
            x="Wins",
            y="Constructor",
            to_drop=["constructorid"],
            rename={"name": "Constructor", "nationality": "Nationality", "wins": "Wins"},
            total_rows=12)

    elif data_to_show == "Driver lap records":

        bar_char(data["driver_lap_records"],
            x="Fastest lap records",
            y="Driver",
            to_drop=["driverid", "forename", "nationality"],
            rename={"surname": "Driver", "fastestlaps": "Fastest lap records"},
            total_rows=10)

    elif data_to_show == "Driver wins":

        bar_char(data["driver_wins"],
            x="Wins",
            y="Driver",
            to_drop=["driverid"],
            rename={"forename": "Name", "surname": "Driver", "nationality": "Nationality", "wins": "Wins"},
            total_rows=12)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("api_url", type=str)
    parsed_args = parser.parse_args()
    main(parsed_args.api_url)