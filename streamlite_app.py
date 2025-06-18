import streamlit as st
import pandas as pd

from utils.altair_plots import *
from utils.helper_functions import *
from utils.custom_widgets import text_plus_slider, text_plus_segment, selectbox_plus_icon
from utils.help_dialogs import *

from agrifoodpy.pipeline import Pipeline
from datablock_setup import datablock_setup
from pipeline_setup import pipeline_setup

from glossary import *
from consultation_utils import get_pathways, call_scenarios, submit_scenario

timer = Timer()

if "cereal_scaling" not in st.session_state:
    st.session_state["cereal_scaling"] = True

if "cereals" not in st.session_state:
    st.session_state["cereals"] = 0

if "first_run" not in st.session_state:
    st.session_state["first_run"] = True

if "show_afolu_only" not in st.session_state:
    st.session_state["show_afolu_only"] = False

if "ssr_metric" not in st.session_state:
    st.session_state["ssr_metric"] = "g/cap/day"

if "plot_key" not in st.session_state:
    st.session_state["plot_key"] = "Summary"

if "check_ID" not in st.session_state:
    st.session_state["check_ID"] = False

if "testing" not in st.session_state:
    st.session_state["testing"] = False

if "embedding" not in st.session_state:
    st.session_state["embedding"] = False

if "embedding" in st.query_params:
    st.session_state["embedding"] = True

# ------------------------
# Help and tooltip strings
# ------------------------
# GUI
st.set_page_config(layout='wide',
                   initial_sidebar_state='expanded',
                   page_title="Future Food Calculator",
                   page_icon="images/fof_icon.png")

set_advanced_settings()

with open('utils/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if st.session_state.first_run and not st.session_state["embedding"]:
    st.session_state.first_run = False
    first_run_dialog()

timer.ping("Page setup")

with st.sidebar:

# ------------------------
#        Sidebar
# ------------------------

    col1, col2 = st.columns([7.5,2.5])

    if "scenario" in st.query_params:
        scenario = st.query_params["scenario"]
        call_scenarios(scenario)
    
        st.selectbox("Scenario",
                     get_pathways(),
                     index=None,
                     placeholder=scenario,
                     on_change=call_scenarios,
                     key="scenario",
                     label_visibility="collapsed")
    
        st.query_params.clear()
        
    else:
        if "ruminant" in st.query_params:
            values = [int(x) for x in st.query_params.values()]
            update_slider(list(st.query_params.keys()), values)
            st.query_params.clear()

        st.selectbox("Scenario",
                     get_pathways(),
                     index=None,
                     placeholder="Select a scenario",
                     on_change=call_scenarios,
                     key="scenario",
                     label_visibility="collapsed")
        
    # Consumer demand interventions

    with st.expander("**:spaghetti: Consumption**", expanded=False):

        text_plus_slider("Ruminant", "ruminant",
                         help_dialog=ruminant_help)
        
        text_plus_slider("Pig, poultry", "pig_poultry",
                         help_dialog=pig_poultry_help)
        
        text_plus_slider("Fish, seafood", "fish_seafood",
                         help_dialog=fish_seafood_help)

        text_plus_slider("Dairy", "dairy",
                         help_dialog=dairy_help)
        
        text_plus_slider("Eggs", "eggs",
                         help_dialog=eggs_help)

        text_plus_slider("Fruits, vegetables", "fruit_veg",max_value=500,
                         help_dialog=fruits_veg_help)
        
        text_plus_slider("Pulses", "pulses", max_value=500,
                         help_dialog=pulses_help)

        text_plus_slider("Alternative meat", "meat_alternatives", min_value=0,
                         help_dialog=alternative_products_help)

        text_plus_slider("Alternative dairy", "dairy_alternatives", min_value=0,
                         help_dialog=alternative_products_help)
        
        text_plus_slider("Food waste", "waste", min_value=0,
                         help_dialog=waste_help)


    # Land use change

    with st.expander("**:earth_africa: Land use**"):

        text_plus_slider("Forest", "foresting_pasture", value=13.17, min_value=0., max_value=50., step=0.1,
                         help_dialog=afforestation_help, sign=False)

        text_plus_slider("Broadleaf %", "bdleaf_conif_ratio", min_value=0, value=75)

        text_plus_slider("Arable to BECCS crops", "land_BECCS", min_value=0,
                         help_dialog=beccs_help)
        
        text_plus_slider("Pasture to BECCS crops", "land_BECCS_pasture", min_value=0,
                         help_dialog=beccs_help)

        text_plus_slider("Lowland peat", "lowland_peatland", min_value=0,
                         help_dialog=waste_help)
        
        text_plus_slider("Upland peat", "upland_peatland", min_value=0,
                         help_dialog=peatland_restoration_help)

        text_plus_slider("Horticulture", "horticulture", min_value=-100, max_value=500,
                         help_dialog=waste_help)
        
        text_plus_slider("Pulse production", "pulse_production", min_value=-100, max_value=500,
                         help_dialog=peatland_restoration_help)

        text_plus_slider("Mixed farming", "mixed_farming", min_value=0,
                         help_dialog=mixed_farming_help)

      
    # Livestock farming practices

    with st.expander("**:cow: Livestock**"):

        text_plus_slider("Silvopasture", "silvopasture", min_value=0,
                       help_dialog=silvopasture_help)
        
        text_plus_slider("Stocking density", "stock_density")

        text_plus_slider("Soil carbon", "pasture_soil_carbon", min_value=0,
                          help_dialog=soil_management_help)

        text_plus_slider("Methane inhibitors", "methane_inhibitor", min_value=0, max_value=100,
                         help_dialog=peatland_restoration_help)
        
        text_plus_slider("Manure management", "manure_management", min_value=0, max_value=100,
                        help_dialog=peatland_restoration_help)
        
        text_plus_slider("Animal breeding", "animal_breeding", min_value=0, max_value=100,
                        help_dialog=peatland_restoration_help)
        
        text_plus_slider("Fossil fuel use", "fossil_livestock", min_value=0, max_value=100,
                     help_dialog=peatland_restoration_help)
        
        text_plus_slider("Livestock productivity", "livestock_yield", min_value=50, value=100, max_value=150, sign=False)

    # Arable farming practices

    with st.expander("**:ear_of_rice: Arable**"):

        text_plus_slider("Agroforestry", "agroforestry", min_value=0,
                            help_dialog=agroforestry_help)
        
        text_plus_slider("Soil carbon", "arable_soil_carbon", min_value=0,
                            help_dialog=soil_management_help)
        
        text_plus_slider("Urban and CEA", "vertical_farming", min_value=0,
                            help_dialog=urban_help)

        text_plus_slider("Fossil fuel use", "fossil_arable", min_value=0, max_value=100,
                        help_dialog=peatland_restoration_help)
        
        text_plus_slider("Nitrogen efficiency", "nitrogen", min_value=0, max_value=100,
                     help_dialog=peatland_restoration_help)

    # Technology and innovation

    with st.expander("**:gear: Technology and innovation**"):
        
        text_plus_slider("Waste BECCS", "waste_BECCS", min_value=0,
                         help_dialog=waste_help, sign=False, percentage=False, 
                         suffix=" Mt CO2e/yr")
                        
        text_plus_slider("Overseas BECCS", "overseas_BECCS", min_value=0,
                         help_dialog=beccs_overseas_help, sign=False, percentage=False,
                         suffix=" Mt CO2e/yr")
        
        text_plus_slider("DACCS", "DACCS", min_value=0, max_value=20,
                         help_dialog=daccs_help, sign=False, percentage=False,
                         suffix=" Mt CO2e/yr")
        
        text_plus_slider("Biochar", "biochar", min_value=0, max_value=10,
                         help_dialog=biochar_help, sign=False, percentage=False,
                         suffix=" Mt CO2e/yr")

        
    with st.expander("**📈 Scenario settings**"):

        pop_projection = selectbox_plus_icon("Population projection",
                                        ["Low", "Medium", "High", "Zero migration"],
                                        default="Medium",
                                        key="pop_proj",
                                        help_dialog=population_help)

        selectbox_plus_icon("Crops yield projection",
                            [-0.27, 0.0, 0.16, 0.34],
                            default=0.0,
                            format_func=format_yield_proj,
                            key="yield_proj",
                            help_dialog=crop_yields_help)
        
        selectbox_plus_icon("International trade model",
                            [0, 0.5, 1],
                            default=0.5,
                            format_func=format_elasticity,
                            key="elasticity",
                            help_dialog=trade_help)
        
    timer.ping("Sidebar setup")

# ----------------------------------------
#                  Main
# ----------------------------------------

run_params = set_run_params_dict()
# print(run_params)
food_system = Pipeline(datablock_setup(pop_projection))
food_system = pipeline_setup(food_system, run_params)
food_system.run()
datablock_result = food_system.datablock

timer.ping("Pipeline run")

# -------------------
# Execute plots block
# -------------------
from plots.plots import plots
extra_values = plots(datablock_result)

timer.ping("Plots executed")

with st.sidebar:
    with st.expander("**:arrow_right: Submit slider positions**"):
        st.markdown("""<div style="text-align: justify;">
            Once you have used the sliders to select your preferred levels of
            intervention, enter your scenario name in the field below and click
            the "Submit pathway" button. You can change your responses as many
            times as you want before the expert submission deadline on 
            23rd May 2025..</div>""", unsafe_allow_html=True)
        
        submission_name = st.text_input("Enter the name of your submission", placeholder="Enter the name of your submission", label_visibility="hidden", key="submission_name")
        
        allow_to_public_database = st.checkbox("Allow your pathway to be publicly available in the submissions database", value=True)
        st.caption("""By clicking ‘Submit’ you are agreeing to our [Data Protection Policy](https://docs.google.com/document/d/1E24m5bvY2g-LbHpyN2Y44A_GzYtMmNUKRFJ_Wc-JTP0/edit?tab=t.0)""")
        submit_state = st.button("Submit", key="submit_scenario")
        if submit_state:
            submit_scenario(" ", ambition_levels=True, check_users=st.session_state.check_ID, name=submission_name, datablock=datablock_result)

    cols_buttons = st.columns(2)

    with cols_buttons[0]:
        st.button("Reset all sliders", on_click=reset_sliders, key='reset_all')

    with cols_buttons[1]:
        if st.button("Clear cache", help="Clear the cache to read advanced settings and scenarios list"):
            st.cache_data.clear()
            st.rerun()
    
    st.caption('''--- Developed with funding from [FixOurFood](https://fixourfood.org/).''')
    
    st.caption('''--- We would be grateful for your feedback - 
               [Fill in our Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSdnBp2Rmr-1fFYRQvEVcLLKchdlXZG4GakTBK5yy6jozUt8NQ/viewform?usp=sf_link).''')
    
    st.caption('''--- For a list of references to the datasets used, please
                visit our [reference document](https://docs.google.com/document/d/1A2J4BYIuXMgrj9tuLtIon8oJTuR1puK91bbUYCI8kHY/).''')
    
    if st.button("Help"):
        first_run_dialog()

timer.total("Total time taken")

# -----------------------------
#  Testing
# -----------------------------

if st.session_state["testing"]:
    
    st.session_state["ssr"] = float(extra_values[0])
    st.session_state["emissions_balance"] = float(extra_values[1])