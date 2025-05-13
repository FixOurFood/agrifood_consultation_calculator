import streamlit as st
from utils.altair_plots import *

def plot_annual_quantities(datablock):
    col_element, col_opt, col_y, col_sel = st.columns([1,1,1,1])
    with col_opt:
        dissagregation = st.selectbox("Plot options", ["Item_group", "Item_origin", "Item_name"], format_func=lambda x: x.replace("_"," "))
    with col_element:
        element_key = st.selectbox("Food Supply Element", ["production", "food", "imports", "exports", "feed"])
    with col_y:
        qty_key = st.selectbox("Quantity", ["g_co2e/year", "kCal/cap/day", "g/cap/day", "g_prot/cap/day", "g_fat/cap/day"])

    with col_sel:
        item_list = st.multiselect("Item", np.unique(datablock["food"][qty_key][dissagregation].values))
    item_selection = {}
    if len(item_list) > 0:
        item_selection = {"Item":item_list}

    if qty_key == "g_co2e/year":
        to_plot = datablock["impact"][qty_key][element_key].fillna(0)/1e6
    else:
        to_plot = datablock["food"][qty_key][element_key].fillna(0)
    to_plot[dissagregation].values = np.array(to_plot[dissagregation].values, dtype=str)
    to_plot = to_plot.fbs.group_sum(coordinate=dissagregation, new_name="Item")
    to_plot = to_plot.sel(item_selection)

    f = plot_years_altair(to_plot, show="Item", ylabel=qty_key)

    f=f.configure_axis(
        labelFontSize=15,
        titleFontSize=15)
    
    st.altair_chart(f, use_container_width=True)