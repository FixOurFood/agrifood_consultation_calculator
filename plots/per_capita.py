import streamlit as st
from utils.altair_plots import *

def plot_per_capita(datablock):

    metric_yr = 2050

    per_cap_options = {"g/cap/day": 5000,
                   "g_prot/cap/day": 250,
                   "g_fat/cap/day": 275,
                   "g_co2e/cap/day": 9000,
                   "kCal/cap/day": 7000}
    
    col_cap1, col_cap2, col_cap3 = st.columns(3)
    with col_cap1:
        option_key = st.selectbox("Plot options", list(per_cap_options.keys()))
    with col_cap2:
        dissagregation = st.selectbox("Disaggregation", ["Item_origin", "Item_group", "Item_name"])
    with col_cap3:
        item_list = st.multiselect("Item", np.unique(datablock["food"][option_key][dissagregation].values))
    item_selection = {}
    if len(item_list) > 0:
        item_selection = {"Item":item_list}
    adjust_scale = st.checkbox("Adjust scale", value=True)

    to_plot = datablock["food"][option_key].sel(Year=metric_yr).fillna(0)
    to_plot[dissagregation].values = np.array(to_plot[dissagregation].values, dtype=str)
    to_plot = to_plot.fbs.group_sum(coordinate=dissagregation, new_name="Item")
    to_plot = to_plot.sel(item_selection)

    if adjust_scale:
        f = plot_bars_altair(to_plot, show="Item", x_axis_title=option_key, xlimit=per_cap_options[option_key])
    else:
        f = plot_bars_altair(to_plot, show="Item", x_axis_title=option_key)

    if option_key == "kCal/cap/day":
        f += alt.Chart(pd.DataFrame({
        'Energy': [datablock["food"]["rda_kcal"]],
        'color': ['red']
        })).mark_rule().encode(
        x='Energy:Q',
        color=alt.Color('color:N', scale=None)
        )

    st.altair_chart(f, use_container_width=True)