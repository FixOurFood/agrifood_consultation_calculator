import streamlit as st
import numpy as np
from utils.altair_plots import *

def plot_self_sufficiency(datablock):

    metric_yr = 2050

    col1_ssr, col2_ssr, col3_ssr = st.columns([1,2,1])

    # Inputs
    with col3_ssr:
        ssr_metric = st.selectbox("Metric", ["g/cap/day", "kCal/cap/day", "g_prot/cap/day", "g_fat/cap/day"])
        dissagregation = st.selectbox("Disaggregation", ["Item_name", "Item_group", "Item_origin"])
        item_selection = {}
        item_list = st.multiselect("Food item", np.unique(datablock["food"][ssr_metric][dissagregation].values))
        if len(item_list) > 0:
            item_selection = {"Item":item_list}

        # Build fbs for plotting
        fbs = datablock["food"][ssr_metric].sel(Year=metric_yr).fillna(0)
        fbs = fbs.fbs.group_sum(coordinate=dissagregation, new_name="Item")
        fbs = fbs.sel(item_selection)
        SSR_metric_yr = fbs.fbs.SSR()
        SSR = datablock["food"][ssr_metric].fillna(0).fbs.SSR().sel(Year=slice(None, metric_yr)) * 100

        with st.container(border=True):
            st.metric("Self-sufficiency for your selection",
                    value="{:.2f} %".format(100*fbs.fbs.SSR()))

    with col1_ssr:
        st.markdown("""# Self-sufficiency""")
        st.markdown("""<div style="text-align: justify;">
                    The self-sufficiency ratio (SSR) is a measure of the proportion of a
                    country's food production that is consumed domestically. It is calculated
                    as the ratio of production to domestic consumption.
                    A higher SSR indicates that a country is more self-sufficient in food
                    production, while a lower SSR indicates that a country relies more on
                    imports to meet its food needs. </div>""", unsafe_allow_html=True)

    # plots
    with col2_ssr:
        
        f = plot_years_total(SSR, ylabel="Self-sufficiency ratio [%]", yrange=(40, 95)).configure_axis(
            labelFontSize=10,
            titleFontSize=15,
            labelAngle=-45,
            ).properties(height=300)        

        origin_color={"Animal Products": "red",
                    "Plant Products": "green",
                    "Alternative Food": "blue"}
    
        domestic_use = fbs["imports"]+fbs["production"]-fbs["exports"]
        domestic_use.name="domestic"
    
        production_bar = plot_single_bar_altair(fbs["production"],
                                                    show="Item",
                                                    vertical=False,
                                                    ax_ticks=True,
                                                    bar_width=100,
                                                    ax_min=0,
                                                    ax_max=np.max([fbs["production"].sum(), domestic_use.sum()]),
                                                    axis_title="Food production per capita",
                                                    unit=ssr_metric.replace("_"," "))

        imports_bar = plot_single_bar_altair(domestic_use,
                                                    show="Item",
                                                    vertical=False,
                                                    ax_ticks=True,
                                                    bar_width=100,
                                                    ax_min=0,
                                                    ax_max=np.max([fbs["production"].sum(), domestic_use.sum()]),
                                                    axis_title="Domestic use per capita",
                                                    unit=ssr_metric.replace("_"," "))    

        with st.container(border=True):
            st.altair_chart(f, use_container_width=True)
        with st.container(border=True):
            st.altair_chart(production_bar, use_container_width=True)
            st.altair_chart(imports_bar, use_container_width=True)