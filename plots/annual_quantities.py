import streamlit as st
from utils.altair_plots import *
from utils.helper_functions import aligned_markdown

def plot_annual_quantities():

    col1_annual, col2_annual = st.columns([1,3])

    with col1_annual:
        st.markdown("""# Annual quantities""")
        aligned_markdown("""This chart shows the annual quantities of food, feed, and
                    other elements in the food system, for different food items
                    or groups, measured by the equivalent quantity of food
                    produced, imported, exported, or consumed. The chart can be
                    adjusted to show different quantities associated with food,
                    including weight, nutrients, and even CO2-equivalent emissions
                    associated with food production.""", alignment="justify")
        
    with col2_annual:
        col_element, col_opt, col_y, col_sel = st.columns([1,1,1,1])

        datablock = st.session_state["datablock"]

        with col_element:
            element_key = st.selectbox(
                "Food Supply Element",
                ["Livestock", "production", "food", "imports", "exports", "feed"],
                index=1,
                format_func=lambda x: x.title())

        if element_key != "Livestock":

            with col_opt:
                dissagregation = st.selectbox(
                    "Plot options",
                    ["Item_group", "Item_origin", "Item_name"],
                    format_func=lambda x: x.replace("_"," "))
                
            with col_y:
                qty_key = st.selectbox(
                    "Quantity",
                    ["g_co2e/cap/day", "kCal/cap/day", "g/cap/day", "g_prot/cap/day", "g_fat/cap/day", "kton/year"],
                    index=5)

            with col_sel:
                item_list = st.multiselect(
                    "Item",
                    np.unique(datablock["food"][qty_key][dissagregation].values))
            
            
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

        else:
            to_plot = datablock["metrics"]["livestock"]

            with col_opt:
                dissagregation = st.multiselect("Type", to_plot["Item"].values)
            sel = {}
            if len(dissagregation) > 0:
                sel = {"Item": dissagregation}

            to_plot = to_plot.sel(sel)

            f = plot_years_altair(to_plot, show="Item")
            f=f.configure_axis(
                labelFontSize=15,
                titleFontSize=15)
            st.altair_chart(f, use_container_width=True)

# plot_annual_quantities()

        