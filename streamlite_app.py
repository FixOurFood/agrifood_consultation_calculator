import streamlit as st
import pandas as pd

from utils.altair_plots import *
from utils.helper_functions import *
from utils.custom_widgets import text_plus_slider, text_plus_segment
from utils.help_dialogs import *

from agrifoodpy.pipeline import Pipeline
from datablock_setup import datablock_setup
from pipeline_setup import pipeline_setup

from glossary import *
from consultation_utils import get_pathways, call_scenarios, submit_scenario

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

# ------------------------
# Help and tooltip strings
# ------------------------
# GUI
st.set_page_config(layout='wide',
                   initial_sidebar_state='expanded',
                   page_title="Agrifood Calculator",
                   page_icon="images/fof_icon.png")

set_advanced_settings()

with open('utils/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if st.session_state.first_run:
    st.session_state.first_run = False
    first_run_dialog()

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
                     on_change=call_scenarios, key="scenario")
    
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
                     on_change=call_scenarios, key="scenario")
        

    # Consumer demand interventions

    with st.expander("**:spaghetti: Consumer demand**", expanded=False):

        consumer_slider_keys = ["ruminant",
                                "dairy",
                                "pig_poultry_eggs",
                                "pulses",
                                "fruit_veg",
                                "cereals",
                                "waste",
                                "meat_alternatives",
                                "dairy_alternatives"]

        text_plus_slider("Reduce ruminant meat consumption",
                         key="ruminant", help_dialog=ruminant_help)
        
        text_plus_slider("Reduce dairy consumption",
                         key="dairy", help_dialog=dairy_help)
        
        text_plus_slider("Reduce pig, poultry and eggs consumption",
                         key="pig_poultry_eggs", help_dialog=pig_pultry_eggs_help)
        
        text_plus_slider("Increase pulses consumption", max_value=500,
                         key="pulses", help_dialog=pulses_help)
        
        text_plus_slider("Increase fruit and vegetable consumption", max_value=500,
                         key="fruit_veg", help_dialog=fruits_veg_help)
        
        text_plus_slider("Increase meat alternatives consumption", min_value=0,
                         key="meat_alternatives", help_dialog=alternative_products_help)
        
        text_plus_slider("Increase dairy alternatives consumption", min_value=0,
                         key="dairy_alternatives", help_dialog=alternative_products_help)
        
        text_plus_slider("Reduce food waste and overeating", min_value=0,
                         key="waste", help_dialog=waste_help)

        st.button("Reset", on_click=reset_sliders, key='reset_consumer',
                  kwargs={"keys": consumer_slider_keys})

    # Land use change

    with st.expander("**:earth_africa: Land use change**"):

        land_slider_keys = ["foresting_pasture",
                            "land_BECCS",
                            "lowland_peatland",
                            "upland_peatland",
                            "soil_carbon",
                            "mixed_farming",
                            "bdleaf_conif_ratio"]

        text_plus_slider("Additional forested UK land area percentage", min_value=-25, max_value=25,
                         key="foresting_pasture", help_dialog=afforestation_help)
        
        text_plus_slider("Percentage of new forested land that is broadleaf", min_value=0, max_value=100,
                         key="bdleaf_conif_ratio")

        text_plus_slider("Percentage of farmland used for BECCS crops", min_value=0, max_value=20,
                         key="land_BECCS", help_dialog=beccs_help)
        
        text_plus_slider("Percentage of lowland peatland restored", min_value=0, max_value=100,
                         key="lowland_peatland", help_dialog=peatland_restoration_help)
        
        text_plus_slider("Percentage of upland peatland restored", min_value=0, max_value=100,
                         key="upland_peatland", help_dialog=peatland_restoration_help)
        
        text_plus_slider("Percentage of land managed for soil carbon management", min_value=0, max_value=100,
                         key="soil_carbon", help_dialog=soil_management_help)
        
        text_plus_slider("Percentage of arable land converted to mixed farming", min_value=0, max_value=100,
                         key="mixed_farming", help_dialog=mixed_farming_help)

        st.button("Reset", on_click=reset_sliders, key='reset_land',
                  kwargs={"keys":land_slider_keys})
        
    # Livestock farming practices

    with st.expander("**:cow: Livestock farming practices**"):

        livestock_slider_keys = ["silvopasture",
                                 "stock_density",
                                 "methane_inhibitor",
                                 "manure_management",
                                 "animal_breeding",
                                 "fossil_livestock"]
        
        text_plus_slider('Pasture land % converted to silvopasture', min_value=0,
                         key="silvopasture", help_dialog=silvopasture_help)
        
        text_plus_slider('Reduce stocking density',
                         key="stock_density")
        
        text_plus_slider('Methane inhibitor use in livestock feed', min_value=0,
                         key="methane_inhibitor", help_dialog=methane_inhibitor_help)
        
        text_plus_slider('Manure management in livestock farming', min_value=0,
                         key="manure_management", help_dialog=manure_management_help)
        
        text_plus_slider('Animal breeding practices', min_value=0,
                         key="animal_breeding", help_dialog=breeding_help)
        
        text_plus_slider('Fossil fuel use in livestock farming', min_value=0,
                         key="fossil_livestock", help_dialog=fossil_livestock_help)

        st.button("Reset", on_click=reset_sliders, key='reset_livestock',
            kwargs={"keys": livestock_slider_keys})

    # Arable farming practices

    with st.expander("**:ear_of_rice: Arable farming practices**"):

        arable_slider_keys = ["agroforestry",
                              "fossil_arable",
                              "nitrogen",
                              "vertical_farming"]
        
        text_plus_slider('Arable land % converted to agroforestry', min_value=0,
                         key="agroforestry", help_dialog=agroforestry_help)
        
        text_plus_slider('Fossil fuel use for machinery in arable farms', min_value=0,
                         key="fossil_arable", help_dialog=fossil_arable_help)
        
        text_plus_slider('Increase Nitrogen efficiency', min_value=0,
                         key="nitrogen")
        
        text_plus_slider('Vertical and urban farming', min_value=0,
                         key="vertical_farming", help_dialog=urban_help)
        
        st.button("Reset", on_click=reset_sliders, key='reset_arable',
            kwargs={"keys": arable_slider_keys})        

    # Technology and innovation

    with st.expander("**:gear: Technology and innovation**"):
        
        technology_slider_keys = ["waste_BECCS",
                                  "overseas_BECCS",
                                  "DACCS"]

        text_plus_slider('BECCS sequestration from waste', min_value=0,
                         key="waste_BECCS", help_dialog=beccs_waste_help)

        text_plus_slider('BECCS sequestration from overseas biomass', min_value=0,
                         key="overseas_BECCS", help_dialog=beccs_overseas_help)
        
        text_plus_slider('DACCS sequestration', min_value=0, max_value=20, 
                         key="DACCS", help_dialog=daccs_help)

        st.button("Reset", on_click=reset_sliders, key='reset_technology',
                  kwargs={"keys": technology_slider_keys})
        
    with st.expander("**📈 Scenario settings**"):

        pop_projection = text_plus_segment("Population projection",
                                           ["Low", "Medium", "High", "Zero migration"],
                                           default="Medium",
                                           key="pop_proj",
                                           help_dialog=population_help)
        
        text_plus_segment("Yield projection",
                            [-0.27, 0.0, 0.34, 0.58],
                            default=0.0,
                            format_func=format_yield_proj,
                            key="yield_proj",
                            help_dialog=crop_yields_help)
        

        text_plus_segment("International trade projection",
                            [0, 0.5, 1],
                            default=0.5,
                            format_func=format_elasticity,
                            key="elasticity",
                            help_dialog=trade_help)

# ----------------------------------------
#                  Main
# ----------------------------------------

food_system = Pipeline(datablock_setup(pop_projection))
food_system = pipeline_setup(food_system)
food_system.run()
datablock_result = food_system.datablock

with st.sidebar:
    with st.expander("**:arrow_right: Submit slider positions**"):
        st.markdown("""<div style="text-align: justify;">
            Once you have used the sliders to select your preferred levels of
            intervention, enter your email address in the field below and click
            the "Submit pathway" button. You can change your responses as many
            times as you want before the expert submission deadline on 26th
            March 2025.</div>""", unsafe_allow_html=True)
        
        submission_name = st.text_input("Enter the name of your submission", placeholder="Enter the name of your submission", label_visibility="hidden")
        
        allow_to_public_database = st.checkbox("Allow your pathway to be publicly available in the submissions database", value=True)
        st.caption("""By clicking ‘Submit’ you are agreeing to our Data Protection Policy [Data Protection Policy](https://docs.google.com/document/d/1E24m5bvY2g-LbHpyN2Y44A_GzYtMmNUKRFJ_Wc-JTP0/edit?tab=t.0)""")
        submit_state = st.button("Submit")
        if submit_state:
            submit_scenario(" ", ambition_levels=True, check_users=st.session_state.check_ID, name=submission_name)

    st.button("Reset all sliders", on_click=reset_sliders, key='reset_all')
    
    st.caption('''--- Developed with funding from [FixOurFood](https://fixourfood.org/).''')
    
    st.caption('''--- We would be grateful for your feedback - 
               [Fill in our Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSdnBp2Rmr-1fFYRQvEVcLLKchdlXZG4GakTBK5yy6jozUt8NQ/viewform?usp=sf_link).''')
    
    st.caption('''--- For a list of references to the datasets used, please
                visit our [reference document](https://docs.google.com/document/d/1A2J4BYIuXMgrj9tuLtIon8oJTuR1puK91bbUYCI8kHY/).''')
    
    if st.button("Help"):
        first_run_dialog()

# -------------------
# Execute plots block
# -------------------
from plots import plots
metric_yr = plots(datablock_result)