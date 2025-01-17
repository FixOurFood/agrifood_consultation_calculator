# FAIR wrapper, needed for caching
import streamlit as st
import numpy as np

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
    "scenario": "Business as Usual",

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
    "peatland": 0,
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

    # Advanced settings sliders and widgets
    "labmeat_slider": 25,
    "rda_slider": 2250,
    "timescale_slider": 20,
    "max_ghg_animal": 30,
    "max_ghg_plant": 30,
    "bdleaf_conif_ratio": 75,
    "bdleaf_seq_ha_yr": 3.5,
    "conif_seq_ha_yr": 6.5,
    "nutrient_constant": "kCal/cap/day",
    "domestic_use_source": "production"
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

def item_name_code(arr):
    if np.array_equal([2949],arr):
        return "Egg"
    elif np.array_equal([2761, 2762, 2763, 2764, 2765, 2766, 2767, 2768, 2769], arr):
        return "Fish/Seafood"
    elif np.array_equal([2740, 2743, 2948], arr):
        return "Dairy"
    elif np.array_equal([2734], arr):
        return "Poultry"
    elif np.array_equal([2733], arr):
        return "Pigmeat"
    
def update_progress(bar_values, bar_key):
    session_vals = [st.session_state[val] for val in bar_values]
    st.session_state[bar_key] = 4 * sum(session_vals) / 100 / len(session_vals)

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
    
    st.video("https://youtu.be/kx8j151hfLE")

    st.write("""We would be grateful for your feedback - Fill in our [Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSdnBp2Rmr-1fFYRQvEVcLLKchdlXZG4GakTBK5yy6jozUt8NQ/viewform?usp=sf_link)""")

    if st.button("Get Started"):
        st.rerun()

def change_to_afolu_only():
    st.session_state.show_afolu_only = st.session_state.show_afolu_only_checkbox

def update_SSR_metric():
    st.session_state.ssr_metric = st.session_state.update_ssr_metric

def update_plot_key():
    st.session_state.plot_key = st.session_state.update_plot_key