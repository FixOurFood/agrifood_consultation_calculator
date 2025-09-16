import streamlit as st
import numpy as np
import pandas as pd
import time


# Helper Functions

# Updates the value of the sliders by setting the session state
def update_slider(keys, values):
    """updates the value of the sliders by setting the session state"""
    if np.isscalar(values):
        for key in keys:
            st.session_state[key] = values
    else:
        for key, value in zip(keys, values):
            st.session_state[key] = value

default_widget_values = {
    # Scenario
    "scenario": "Baseline",

    # Scenario settings
    "pop_proj":"Medium",
    "yield_proj":0,
    "elasticity":0.5,

    # Consumer demand sliders and widgets
    "ruminant": 0,
    "dairy": 0,
    "pig_poultry": 0,
    "eggs": 0,
    "fish_seafood": 0,
    "pulses": 0,
    "fruit_veg": 0,
    "cereals": 0,
    "meat_alternatives": 0,
    "dairy_alternatives":0,
    "waste": 0,
    
    # Land use sliders and widgets
    "foresting_pasture": 13.17,
    "bdleaf_conif_ratio":75,
    "land_BECCS": 0,
    "land_BECCS_pasture": 0,
    "lowland_peatland": 0,
    "upland_peatland": 0,
    "horticulture":0,
    "pulse_production":0,
    "mixed_farming": 0,

    # Livestock farming sliders and widgets
    "silvopasture": 0,
    "stock_density": 0,
    "pasture_soil_carbon": 0,
    "methane_inhibitor": 0,
    "manure_management": 0,
    "animal_breeding": 0,
    "fossil_livestock": 0,
    "livestock_yield":100,

    # Arable farming sliders and widgets
    "agroforestry": 0,
    "arable_soil_carbon": 0,
    "fossil_arable": 0,
    "nitrogen": 0,
    "vertical_farming": 0,

    # Technology and innovation sliders and widgets
    "waste_BECCS": 0,
    "overseas_BECCS": 0,
    "DACCS": 0,
    "biochar":0
}

def reset_sliders(keys=None):
    """Resets the selected sliders to their default values"""
    st.query_params.clear()
    if keys is None:
        for key in default_widget_values.keys():
            update_slider(keys=[key], values=[default_widget_values[key]])
    else:
        keys = np.hstack(keys)
        update_slider(keys=keys, values=[default_widget_values[key] for key in keys])

def map_max(map, dim):
    """function to return the coordinate index of the maximum value along a
    dimension"""

    length_dim = len(map[dim].values)
    map_fixed = map.assign_coords({dim:np.arange(length_dim)})

    return map_fixed.idxmax(dim=dim, skipna=True)

def capitalize_first_character(s):
    """Capitalize the first character of a string"""
    if len(s) == 0:
        return s  # Return the empty string if input is empty
    return s[0].upper() + s[1:]


def help_str(help, sidebar_key, row_index, heading_key=None):
    """Returns a string with a link to the documentation given a header hash"""
    doc_str = st.secrets["modelling_doc_url"]
    help_string = help[sidebar_key][row_index]

    if heading_key is not None:
        help_string = f"[{help_string}]({doc_str}{heading_key})"

    return help_string

@st.dialog("Future Food Calculator", width="large")
def first_run_dialog():
    """Dialog that appears when the app is first run. If the 'Get started'
    button is pressed, the app is run again and the dialog is closed, while the
    'X' button closes the dialog without a rerun"""

    st.write("""The Future Food Calculator provides a model of the UK agrifood
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
                 
    st.write("""The Future Food Calculator was developed with funding from [FixOurFood](https://fixourfood.org/).
            It was conceived as a tool to support evidence based policy making
            and to engage food system stakeholders in a conversation about
            pathways to net zero.""")
    
    st.video("https://youtu.be/xHbKmMsDegc")

    st.write("""We would be grateful for your feedback - Fill in our [Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSdnBp2Rmr-1fFYRQvEVcLLKchdlXZG4GakTBK5yy6jozUt8NQ/viewform?usp=sf_link)""")

    if st.button("Get Started"):
        st.rerun()

def change_to_afolu_only():
    """Helper to change the Agrifood Only checkbox to True"""
    st.session_state.show_afolu_only = st.session_state.show_afolu_only_checkbox

def update_SSR_metric():
    """Helper to update the SSR metric"""
    st.session_state.ssr_metric = st.session_state.update_ssr_metric

def update_plot_key():
    """Helper to update the plot key"""
    st.session_state.plot_key = st.session_state.update_plot_key

@st.cache_data(ttl=60*60*24)
def read_help():
    """Reads the tooltip text from tooltips URL"""
    return pd.read_csv(st.secrets["tooltips_url"], dtype='string')

@st.cache_data(ttl=60*60*24)
def read_advanced_settings():
    """Reads the advanced settings from the spreadsheet URL"""
    advanced_settings  = pd.read_csv(st.secrets["advanced_settings_url"], dtype='string')
    advanced_settings_dict = {}

    for index, row in advanced_settings.iterrows():
        if row["type"] == "float": 
            advanced_settings_dict[row["key"]] = float(row["value"])
        elif row["type"] == "string":
            advanced_settings_dict[row["key"]] = str(row["value"])
        elif row["type"] == "bool":
            advanced_settings_dict[row["key"]] = row["value"] == "TRUE"
    
    return advanced_settings_dict

def set_advanced_settings():
    """Sets the advanced settings from the spreadsheet URL"""
    default_settings = read_advanced_settings()
    st.session_state.update(default_settings)

@st.cache_data(ttl=60*60*24)
def read_slider_ranges():
    """Reads the advanced settings from the spreadsheet URL"""
    slider_ranges  = pd.read_csv(st.secrets["slider_ranges_url"], dtype='string')
    for index, row in slider_ranges.iterrows():
        if row["type"] == "float": 
            st.session_state[row["key"]] = float(row["value"])
        elif row["type"] == "string":
            st.session_state[row["key"]] = str(row["value"])
        elif row["type"] == "bool":
            st.session_state[row["key"]] = row["value"] == "TRUE"

def format_elasticity(x):
    """Formats the elasticity values to a string """
    if x == 0:
        return "Imports"
    elif x == 0.5:
        return "Mixed"
    elif x == 1:
        return "Production"

def format_yield_proj(x):
    """Formats the yield projection values to a string """
    if x == -0.27:
        return "Climate sensitivity"
    elif x == 0.0:
        return "Baseline"
    elif x == 0.16:
        return "Medium"
    elif x == 0.34:
        return "High"
    
class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.last_ping_time = self.start_time

    def ping(self, message="Timer since last ping: "):
        current_time = time.time()
        elapsed_since_last_ping = current_time - self.last_ping_time
        self.last_ping_time = current_time
        print(f"{message} {elapsed_since_last_ping:.2f} seconds")

    def total(self, message="Total time elapsed: "):
        total_elapsed_time = time.time() - self.start_time
        print(f"{message} {total_elapsed_time:.2f} seconds")

def set_run_params_dict():

    params = {k:st.session_state[k] for k in list(default_widget_values.keys())}

    adv_set_dict = read_advanced_settings() 

    # Read query parameters and extract those that are advanced settings keys
    query_advanced_settings = np.intersect1d(list(st.query_params.keys()), list(adv_set_dict.keys()))
    if len(query_advanced_settings) > 0:
        for k in query_advanced_settings:
            if k in adv_set_dict:
                adv_set_dict[k] = float(st.query_params[k])


    params.update(adv_set_dict)
    params["cereal_scaling"] = True
    return params

@st.cache_data(ttl=60*60*24)
def cached_datablock_setup(
    AES_KEY,
    AES_IV,
    advanced_settings
    ):

    from future_food.datablock_setup import datablock_setup

    return datablock_setup(
        AES_KEY,
        AES_IV,
        advanced_settings)
