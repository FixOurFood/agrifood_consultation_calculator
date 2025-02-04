import streamlit as st
import numpy as np
import pandas as pd

# Helper Functions

# Updates the value of the sliders by setting the session state
def update_slider(keys, values):
    if np.isscalar(values):
        for key in keys:
            st.session_state[key] = values
    else:
        for key, value in zip(keys, values):
            st.session_state[key] = value

default_widget_values = {
    # Scenario
    "scenario": "Baseline",

    # Consumer demand sliders and widgets
    "consumer_bar": 0,
    "ruminant": 0,
    "dairy": 0,
    "pig_poultry_eggs": 0,
    "fruit_veg": 0,
    "cereals": 0,
    "meat_alternatives": 0,
    "dairy_alternatives":0,
    "waste": 0,

    # Land use sliders and widgets
    "land_bar": 0,
    "foresting_pasture": 0,
    "land_BECCS": 0,
    "lowland_peatland": 0,
    "upland_peatland": 0,
    "soil_carbon": 0,
    "mixed_farming": 0,

    # Technology and innovation sliders and widgets
    "innovation_bar": 0,
    "waste_BECCS": 0,
    "overseas_BECCS": 0,
    "DACCS": 0,

    # Livestock farming sliders and widgets
    "livestock_bar": 0,
    "silvopasture": 0,
    "methane_inhibitor": 0,
    "manure_management": 0,
    "animal_breeding": 0,
    "fossil_livestock": 0,

    # Arable farming sliders and widgets
    "arable_bar": 0,
    "agroforestry": 0,
    "fossil_arable": 0,
    "vertical_farming": 0,

}

def reset_sliders(keys=None):
    if keys is None:
        for key in default_widget_values.keys():
            update_slider(keys=[key], values=[default_widget_values[key]])
    else:
        keys = np.hstack(keys)
        update_slider(keys=keys, values=[default_widget_values[key] for key in keys])

# function to return the coordinate index of the maximum value along a dimension
def map_max(map, dim):

    length_dim = len(map[dim].values)
    map_fixed = map.assign_coords({dim:np.arange(length_dim)})

    return map_fixed.idxmax(dim=dim, skipna=True)

def capitalize_first_character(s):
    if len(s) == 0:
        return s  # Return the empty string if input is empty
    return s[0].upper() + s[1:]


def help_str(help, sidebar_key, row_index, heading_key=None):
    doc_str = "https://docs.google.com/document/d/1A2J4BYIuXMgrj9tuLtIon8oJTuR1puK91bbUYCI8kHY/edit#heading=h."
    help_string = help[sidebar_key][row_index]

    if heading_key is not None:
        help_string = f"[{help_string}]({doc_str}{heading_key})"

    return help_string

@st.dialog("Agrifood Calculator", width="large")
def first_run_dialog():

    st.write("""The Agrifood Calculator provides a model of the UK agrifood
            system that allows you to explore pathways for how we might reduce
            the UK’s greenhouse gas emissions to net zero by 2050 through
            agriculture and food.""")
    
    st.write("""Choose your interventions for reducing emissions or increasing
            sequestration, set the level for where you want the intervention
            to be, and the calculator shows how your choices affect UK emissions,
            land use and UK self-sufficiency.""")
    
    st.write("""Once you have used the sliders to select your preferred levels
             of intervention, enter your email address in the field below and
             click the "Submit pathway" button. You can change your responses as
             many times as you want before the expert submission deadline on
             26th March 2025.
             """)
    
    _, col2, _ = st.columns([0.5, 1, 0.5])
    with col2:
        st.image("images/slider_gif_intro.gif")
                 
    st.write("""The Agrifood Calculator was developed with funding from [FixOurFood](https://fixourfood.org/).
            It was conceived as a tool to support evidence based policy making
            and to engage food system stakeholders in a conversation about
            pathways to net zero.""")
    
    st.video("https://youtu.be/xHbKmMsDegc")

    st.write("""We would be grateful for your feedback - Fill in our [Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSdnBp2Rmr-1fFYRQvEVcLLKchdlXZG4GakTBK5yy6jozUt8NQ/viewform?usp=sf_link)""")

    if st.button("Get Started"):
        st.rerun()

def change_to_afolu_only():
    st.session_state.show_afolu_only = st.session_state.show_afolu_only_checkbox

def update_SSR_metric():
    st.session_state.ssr_metric = st.session_state.update_ssr_metric

def update_plot_key():
    st.session_state.plot_key = st.session_state.update_plot_key

@st.cache_data(ttl=60*60*24)
def read_help():
    """Reads the tooltip text from tooltips URL"""
    return pd.read_csv(st.secrets["tooltips_url"], dtype='string')

@st.cache_data(ttl=60*60*24)
def read_advanced_settings():
    """Reads the advanced settings from the spreadsheet URL"""
    advanced_settings  = pd.read_csv(st.secrets["advanced_settings_url"], dtype='string')
    for index, row in advanced_settings.iterrows():
        if row["type"] == "float": 
            st.session_state[row["key"]] = float(row["value"])
        elif row["type"] == "string":
            st.session_state[row["key"]] = str(row["value"])
        elif row["type"] == "bool":
            st.session_state[row["key"]] = row["value"] == "TRUE"