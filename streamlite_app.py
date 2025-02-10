import streamlit as st
import pandas as pd

from utils.altair_plots import *
from utils.helper_functions import *

from agrifoodpy.pipeline import Pipeline
from datablock_setup import datablock_setup
from pipeline_setup import pipeline_setup

from glossary import *
from consultation_utils import get_pathways, call_scenarios

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

# ------------------------
# Help and tooltip strings
# ------------------------
# GUI
st.set_page_config(layout='wide',
                   initial_sidebar_state='expanded',
                   page_title="Agrifood Calculator",
                   page_icon="images/fof_icon.png")

help = read_help()
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
    
        st.selectbox("Scenario", get_pathways(), index=None, placeholder=scenario,
                        help=help_str(help, "sidebar_consumer", 8),
                        on_change=call_scenarios, key="scenario")
    
        st.query_params.clear()
        
    else:
        if "ruminant" in st.query_params:
            values = [int(x) for x in st.query_params.values()]
            update_slider(list(st.query_params.keys()), values)
            st.query_params.clear()
        st.selectbox("Scenario", get_pathways(), index=None, placeholder="Select a scenario",
                        help=help_str(help, "sidebar_consumer", 8),
                        on_change=call_scenarios, key="scenario")
        

    # Consumer demand interventions

    with st.expander("**:spaghetti: Consumer demand**", expanded=False):

        consumer_slider_keys = ["ruminant", "dairy", "pig_poultry_eggs", "fruit_veg", "cereals", "waste", "meat_alternatives", "dairy_alternatives"]

        ruminant = st.slider('Reduce ruminant meat consumption',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="ruminant", help=help_str(help, "sidebar_consumer", 1, "pjtbcox0lw1k"))
        
        dairy = st.slider('Reduce dairy consumption',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="dairy", help=help_str(help, "sidebar_consumer", 2, "z0gjphyzstcl"))
        
        pig_poultry_eggs = st.slider('Reduce pig, poultry and eggs consumption',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="pig_poultry_eggs", help=help_str(help, "sidebar_consumer", 3, "6u16n1fg1w03"))
        
        fruit_veg = st.slider('Increase fruit and vegetable consumption',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="fruit_veg", help=help_str(help, "sidebar_consumer", 4, "okbabgaqb068"))
        
        if not st.session_state["cereal_scaling"]:
            cereals = st.slider('Increase cereal consumption',
                            min_value=-100, max_value=100, step=1, value=0,
                            key="cereals", help=help_str(help, "sidebar_consumer", 5, "p0a3p6fkxlzn"),
                            disabled=st.session_state["cereal_scaling"])

        meat_alternatives = st.slider('Increase meat alternatives uptake',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="meat_alternatives", help=help_str(help, "sidebar_consumer", 7, "ty2fxim28j6p"))     
        
        dairy_alternatives = st.slider('Increase dairy alternatives uptake',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="dairy_alternatives", help=help_str(help, "sidebar_consumer", 8, "ty2fxim28j6p"))
        
        waste = st.slider('Food waste and over-eating reduction',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="waste", help=help_str(help, "sidebar_consumer", 6, "jjk6fgg4t69m"))  

        st.button("Reset", on_click=reset_sliders, key='reset_consumer',
                  kwargs={"keys": [consumer_slider_keys, "consumer_bar"]})

    # Land use change

    with st.expander("**:earth_africa: Land use change**"):

        land_slider_keys = ["foresting_pasture", "land_BECCS", "lowland_peatland", "upland_peatland", "soil_carbon", "mixed_farming"]

        foresting_pasture = st.slider('Additional forested UK land area percentage',
                        min_value=-25, max_value=25, step=1, value=0,
                        key="foresting_pasture", help=help_str(help, "sidebar_land", 0, "oqoktlcczgw8"))        

        land_BECCS = st.slider('Percentage of farmland used for BECCS crops',
                        min_value=0, max_value=20, step=1,
                        key="land_BECCS", help=help_str(help, "sidebar_land", 1, "hjx1wpsuoy8u"))

        lowland_peatland = st.slider('Percentage of lowland peatland restored',
                             min_value=0, max_value=100, step=1,
                             key="lowland_peatland", help=help_str(help, "sidebar_land", 2, "eln33eildo1k"))
        
        upland_peatland = st.slider('Percentage of upland peatland restored',
                             min_value=0, max_value=100, step=1,
                             key="upland_peatland", help=help_str(help, "sidebar_land", 2, "rgtch9lm7i39"))

        soil_carbon = st.slider('Percentage of land managed for soil carbon management',
                                 min_value=0, max_value=100, step=1,
                                 key="soil_carbon", help=help_str(help, "sidebar_land", 3, "3a92auci0xj5"))
        
        mixed_farming = st.slider('Percentage of arable land converted to mixed farming',
                                  min_value=0, max_value=100, step=1,
                                  key="mixed_farming", help=help_str(help, "sidebar_land", 4, "7su0nj7wz5ct"))

        st.button("Reset", on_click=reset_sliders, key='reset_land',
                  kwargs={"keys":[land_slider_keys, "land_bar"]})
        
    # Livestock farming practices

    with st.expander("**:cow: Livestock farming practices**"):

        livestock_slider_keys = ["silvopasture",
                                 "methane_inhibitor",
                                 "manure_management",
                                 "animal_breeding",
                                 "fossil_livestock"]
        
        silvopasture = st.slider('Pasture land % converted to silvopasture',
                        min_value=0, max_value=100, step=1,
                        key='silvopasture', help=help_str(help, "sidebar_livestock", 0, "8r8po4kj9qqw"))        
        
        methane_inhibitor = st.slider('Methane inhibitor use in livestock feed',
                        min_value=0, max_value=100, step=1,
                        key='methane_inhibitor', help=help_str(help, "sidebar_livestock", 1, "tbok5jqrlrxb"))
        
        manure_management = st.slider('Manure management in livestock farming',
                        min_value=0, max_value=100, step=1,
                        key='manure_management', help=help_str(help, "sidebar_livestock", 2, "aqz9utt7u1x"))
        
        animal_breeding = st.slider('Livestock breeding',
                        min_value=0, max_value=100, step=1,
                        key='animal_breeding', help=help_str(help, "sidebar_livestock", 3, "u9p65u7y1vdc"))
        
        fossil_livestock = st.slider('Fossil fuel use for heating, machinery',
                        min_value=0, max_value=100, step=1,
                        key='fossil_livestock', help=help_str(help, "sidebar_livestock", 4, "qtazr4y5dfwi"))
        

        st.button("Reset", on_click=reset_sliders, key='reset_livestock',
            kwargs={"keys": [livestock_slider_keys, "livestock_bar"]})

    # Arable farming practices

    with st.expander("**:ear_of_rice: Arable farming practices**"):

        arable_slider_keys = ["agroforestry", "fossil_arable", "vertical_farming"]
        
        agroforestry = st.slider('Arable land % converted to agroforestry',
                        min_value=0, max_value=100, step=1,
                        key='agroforestry', help=help_str(help,"sidebar_land",4, "90swrlvdy6f8"))

        fossil_arable = st.slider('Fossil fuel use for machinery',
                        min_value=0, max_value=100, step=1,
                        key='fossil_arable', help=help_str(help,"sidebar_arable",1,"6j2golzh19zq"))
        
        vertical_farming = st.slider('Vertical and urban farming',
                        min_value=0, max_value=100, step=1,
                        key='vertical_farming', help=help_str(help,"sidebar_arable",2,"2w3tq0fbry5i"))
                        
        st.button("Reset", on_click=reset_sliders, key='reset_arable',
            kwargs={"keys": [arable_slider_keys, "arable_bar"]})        

    # Technology and innovation

    with st.expander("**:gear: Technology and innovation**"):
        
        technology_slider_keys = ["waste_BECCS", "overseas_BECCS", "DACCS"]

        waste_BECCS = st.slider('BECCS sequestration from waste \n [Mt CO2e / yr]',
                        min_value=0, max_value=100, step=1,
                        key='waste_BECCS', help=help["sidebar_innovation"][0])

        overseas_BECCS = st.slider('BECCS sequestration from overseas biomass \n [Mt CO2e / yr]',
                        min_value=0, max_value=100, step=1,
                        key='overseas_BECCS', help=help["sidebar_innovation"][1])

        DACCS = st.slider('DACCS sequestration \n [Mt CO2e / yr]',
                        min_value=0, max_value=20, step=1,
                        key='DACCS', help=help["sidebar_innovation"][3])

        st.button("Reset", on_click=reset_sliders, key='reset_technology',
                  kwargs={"keys": [technology_slider_keys, "innovation_bar"]})
        
    st.button("Reset all sliders", on_click=reset_sliders, key='reset_all')
    
    st.caption('''--- Developed with funding from [FixOurFood](https://fixourfood.org/).''')
    
    st.caption('''--- We would be grateful for your feedback - 
               [Fill in our Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSdnBp2Rmr-1fFYRQvEVcLLKchdlXZG4GakTBK5yy6jozUt8NQ/viewform?usp=sf_link).''')
    
    st.caption('''--- For a list of references to the datasets used, please
                visit our [reference document](https://docs.google.com/document/d/1A2J4BYIuXMgrj9tuLtIon8oJTuR1puK91bbUYCI8kHY/).''')
    
    if st.button("Help"):
        first_run_dialog()

# ----------------------------------------
#                  Main
# ----------------------------------------

food_system = Pipeline(datablock_setup())
food_system = pipeline_setup(food_system)
food_system.run()
datablock_result = food_system.datablock

# -------------------
# Execute plots block
# -------------------
from plots import plots
metric_yr = plots(datablock_result)
