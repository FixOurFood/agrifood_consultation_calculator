import streamlit as st
import matplotlib.pyplot as plt
from glossary import *
from utils.helper_functions import *
from streamlit_theme import st_theme

from .summary import plot_summary
from .annual_quantities import plot_annual_quantities
from .per_capita import plot_per_capita
from .land_use import plot_land_use
from .self_sufficiency import plot_self_sufficiency

@st.fragment()
def plots(datablock):

    theme = st_theme()
    if theme is not None:
        background_color = theme["backgroundColor"]
    else:
        background_color = 'white'

    plt.rcParams['axes.facecolor'] = background_color

    # ----------------------------------------    
    #                  Plots
    # ----------------------------------------
    plot_key = st.session_state["plot_key"]

    # Summary
    if plot_key == "Summary":
        plot_summary(datablock, background_color)        

    # Emissions per food group or origin
    if plot_key == "Annual quantities":
        plot_annual_quantities(datablock)

    # FAOSTAT bar plot with per-capita daily values
    elif plot_key == "Per capita daily values":
        plot_per_capita(datablock)        
        
    # Self-sufficiency ratio as a function of time
    elif plot_key == "Self-sufficiency ratio":
        plot_self_sufficiency(datablock)

    # Various land plots, including Land use and ALC
    elif plot_key == "Land":
        plot_land_use(datablock, background_color)

    st.selectbox("Choose from the options below to explore a more detailed breakdown of your selected pathway", option_list, on_change=update_plot_key, key="update_plot_key")
