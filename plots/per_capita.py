import streamlit as st
from utils.altair_plots import *
from utils.helper_functions import remove_underscore, aligned_markdown

def plot_per_capita():

    datablock = st.session_state["datablock"]

    metric_yr = 2050

    per_cap_options = {"g/cap/day": 5000,
                   "g_prot/cap/day": 250,
                   "g_fat/cap/day": 275,
                   "g_co2e/cap/day": 9000,
                   "kCal/cap/day": 7000}
    
    col1_percap, col2_percap = st.columns([1,3])

    with col2_percap:
        col_cap1, col_cap2, col_cap3, col_cap4 = st.columns(4)  
    
    with col_cap1:
        option_key = st.selectbox(
            "Quantity",
            list(per_cap_options.keys())
            )
    
    with col_cap2:
        dissagregation = st.selectbox(
            "Disaggregation",
            [
                "Item_origin",
                "Item_group",
                "Item_name",
                "Item_origin - list",
                "Item_group - list"
                ],
            format_func=remove_underscore
            )

    # If the item selected is a list 
    show_list = False
    if dissagregation in ["Item_origin - list", "Item_group - list"]:
        dissagregation = dissagregation.split(" - ")[0]
        show_list = True

    with col_cap3:
        item_list = st.multiselect(
            "Item",
            np.unique(datablock["food"][option_key][dissagregation].values)
            )
    
    item_selection = {}
    if len(item_list) > 0:
        item_selection = {"Item":item_list}

    to_plot = datablock["food"][option_key].sel(Year=metric_yr).fillna(0)
    to_plot[dissagregation].values = np.array(to_plot[dissagregation].values, dtype=str)

    if show_list:
        if len(item_list) > 0:
            to_plot = to_plot.sel(Item=np.isin(to_plot[dissagregation].values, item_list))

        to_plot = to_plot.fbs.group_sum(coordinate="Item_name", new_name="Item")

    else:
        to_plot = to_plot.fbs.group_sum(coordinate=dissagregation, new_name="Item")
        to_plot = to_plot.sel(item_selection)

    to_plot = to_plot.rename({"food": "Retail"})
    to_plot = to_plot.rename({"production": "Production"})
    to_plot = to_plot.rename({"imports": "Imports"})
    to_plot = to_plot.rename({"exports": "Exports"})
    to_plot = to_plot.rename({"stock": "Stock"})
    to_plot = to_plot.rename({"losses": "Losses"})
    to_plot = to_plot.rename({"processing": "Processing"})
    to_plot = to_plot.rename({"other": "Other"})
    to_plot = to_plot.rename({"feed": "Feed"})
    to_plot = to_plot.rename({"seed": "Seed"})

    with col1_percap:
        st.markdown("""# Per-capita food flows""")
        aligned_markdown("""
                    This chart shows the flow of quantities through the food
                    system, from production to consumption, for different food
                    items or groups, measured by the equivalent quantity of food
                    per person per day. The first two horizontal bars represent
                    the production and imports of food, which represent the main
                    ingresses of food into the system. The subsequent bars
                    represent the various uses of food, such as exports, 
                    feed for animals and seed for planting new crops.""",
                    alignment="justify")
        aligned_markdown("""
                    Retail represents the amount of food available for
                    consumption by the population.
                    """, alignment="justify")
        aligned_markdown("""
                    The chart can be adjusted to show different quantities
                    associated with food, including weight, nutrients, and even
                    CO2-equivalent emissions associated with food production.
                    """, alignment="justify")

    with col2_percap:

        adjust_scale = st.checkbox("Fix horizontal scale", value=True)
        if adjust_scale:
            f = plot_bars_altair2(
                to_plot,
                data_vars = ["Production", "Imports"],
                reversed_vars = ["Exports", "Stock", "Losses", "Processing", "Other", "Feed", "Seed", "Retail"],
                show="Item",
                x_axis_title=option_key,
                xlimit=per_cap_options[option_key])
        else:
            f = plot_bars_altair2(
                to_plot,
                data_vars = ["Production", "Imports"],
                reversed_vars = ["Exports", "Stock", "Losses", "Processing", "Other", "Feed", "Seed", "Retail"],
                show="Item",
                x_axis_title=option_key)

        if option_key == "kCal/cap/day":
            f += alt.Chart(pd.DataFrame({
            'Energy': [datablock["food"]["rda_kcal"]],
            'color': ['red']
            })).mark_rule().encode(
            x='Energy:Q',
            color=alt.Color('color:N', scale=None)
            )

        st.altair_chart(f, use_container_width=True)

# plot_per_capita()