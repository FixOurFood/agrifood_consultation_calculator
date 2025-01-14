import streamlit as st
import pandas as pd
import copy

from utils.altair_plots import *
from utils.helper_functions import *

from utils.pipeline import Pipeline
from datablock_setup import datablock
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
help = pd.read_csv(st.secrets["tooltips_url"], dtype='string')

# GUI
st.set_page_config(layout='wide',
                   initial_sidebar_state='expanded',
                   page_title="Agrifood Calculator",
                   page_icon="images/fof_icon.png")

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
                        key="dairy", help=help["sidebar_consumer"][2])
        
        pig_poultry_eggs = st.slider('Reduce pig, poultry and eggs consumption',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="pig_poultry_eggs", help=help["sidebar_consumer"][3])
        
        fruit_veg = st.slider('Increase fruit and vegetable consumption',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="fruit_veg", help=help["sidebar_consumer"][4])
        
        if not st.session_state["cereal_scaling"]:
            cereals = st.slider('Increase cereal consumption',
                            min_value=-100, max_value=100, step=1, value=0,
                            key="cereals", help=help["sidebar_consumer"][5],
                            disabled=st.session_state["cereal_scaling"])

        meat_alternatives = st.slider('Increase meat alternatives uptake',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="meat_alternatives", help=help["sidebar_consumer"][7])     
        
        dairy_alternatives = st.slider('Increase dairy alternatives uptake',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="dairy_alternatives", help=help["sidebar_consumer"][7])
        
        waste = st.slider('Food waste and over-eating reduction',
                        min_value=-100, max_value=100, step=1, value=0,
                        key="waste", help=help["sidebar_consumer"][6])  

        st.button("Reset", on_click=reset_sliders, key='reset_consumer',
                  kwargs={"keys": [consumer_slider_keys, "consumer_bar"]})

    # Land use change

    with st.expander("**:earth_africa: Land use change**"):

        land_slider_keys = ["foresting_pasture", "land_BECCS", "peatland", "soil_carbon", "mixed_farming"]

        foresting_pasture = st.slider('Forested pasture land fraction',
                        min_value=0, max_value=100, step=1,
                        key="foresting_pasture", help=help["sidebar_land"][0])        

        land_BECCS = st.slider('Percentage of farmland used for BECCS crops',
                        min_value=0, max_value=20, step=1,
                        key="land_BECCS", help=help["sidebar_innovation"][1])

        peatland = st.slider('Percentage of peatland restored',
                             min_value=0, max_value=100, step=1,
                             key="peatland", help=help["sidebar_land"][2])

        soil_carbon = st.slider('Percentage of managed land for soil carbon management',
                                 min_value=0, max_value=100, step=1,
                                 key="soil_carbon", help=help["sidebar_land"][3])
        
        mixed_farming = st.slider('Percentage of agricultural land converted to mixed farming',
                                  min_value=0, max_value=100, step=1,
                                  key="mixed_farming", help=help["sidebar_land"][4])

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
                        key='silvopasture', help=help["sidebar_land"][3])        
        
        methane_inhibitor = st.slider('Methane inhibitor use in livestock feed',
                        min_value=0, max_value=100, step=1,
                        key='methane_inhibitor', help=help["sidebar_livestock"][0])
        
        manure_management = st.slider('Manure management in livestock farming',
                        min_value=0, max_value=100, step=1,
                        key='manure_management', help=help["sidebar_livestock"][1])
        
        animal_breeding = st.slider('Livestock breeding',
                        min_value=0, max_value=100, step=1,
                        key='animal_breeding', help=help["sidebar_livestock"][2])
        
        fossil_livestock = st.slider('Fossil fuel use for heating, machinery',
                        min_value=0, max_value=100, step=1,
                        key='fossil_livestock', help=help["sidebar_livestock"][4])
        

        st.button("Reset", on_click=reset_sliders, key='reset_livestock',
            kwargs={"keys": [livestock_slider_keys, "livestock_bar"]})

    # Arable farming practices

    with st.expander("**:ear_of_rice: Arable farming practices**"):

        arable_slider_keys = ["agroforestry", "fossil_arable", "vertical_farming"]
        
        agroforestry = st.slider('Arable land % converted to agroforestry',
                        min_value=0, max_value=100, step=1,
                        key='agroforestry', help=help["sidebar_land"][4])

        fossil_arable = st.slider('Fossil fuel use for machinery',
                        min_value=0, max_value=100, step=1,
                        key='fossil_arable', help=help["sidebar_arable"][1])
        
        vertical_farming = st.slider('Vertical and urban farming',
                        min_value=0, max_value=100, step=1,
                        key='vertical_farming', help=help["sidebar_arable"][2])
                        
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
        
    # Advanced settings

    with st.expander("Advanced settings"):
        
        password = st.text_input("Enter the advanced settings password", type="password")
        if password == st.secrets["advanced_options_password"]:

            check_ID = st.checkbox('Check ID for submission', value=False, key='check_ID')
            emission_factors = st.selectbox('Emission factors', options=["NDC 2020", "PN18"], key='emission_factors')
            cereal_scaling = st.checkbox('Scale cereal production to meet nutrient demands', value=True, key='cereal_scaling')

            cc_production_decline = st.checkbox('Production decline caused by climate change', value=False, key='cc_production_decline')

            labmeat_co2e = st.slider('Cultured meat GHG emissions [g CO2e / g]', min_value=1., max_value=120., value=6.5, key='labmeat_slider')
            dairy_alternatives_co2e = st.slider('Dairy alternatives GHG emissions [g CO2e / g]', min_value=0.10, max_value=0.27, value=0.14, key='dairy_alternatives_slider')
            
            rda_kcal = st.slider('Recommended daily energy intake [kCal]', min_value=2000, max_value=2500, value=2250, key='rda_slider')
            n_scale = st.slider('Adoption timescale [years]', min_value=0, max_value=50, value=20, step=5, key='n_scale')
            max_ghge_animal = st.slider('Maximum animal production GHGE reduction due to innovation [%]', min_value=0, max_value=100, value=30, step=10, key = "max_ghg_animal", help = help["advanced_options"][3])
            max_ghge_plant = st.slider('Maximum plant production GHGE reduction due to innovation [%]', min_value=0, max_value=100, value=30, step=10, key = "max_ghg_plant", help = help["advanced_options"][4])
            bdleaf_conif_ratio = st.slider('Ratio of coniferous to broadleaved reforestation', min_value=0, max_value=100, value=75, step=10, key = "bdleaf_conif_ratio", help = help["advanced_options"][5])
            bdleaf_seq_ha_yr = st.slider('Broadleaved forest CO2 sequestration [t CO2 / ha / year]', min_value=1., max_value=15., value=3.5, step=0.5, key = "bdleaf_seq_ha_yr", help = help["advanced_options"][6])
            peatland_seq_ha_yr = st.slider('Peatland CO2 sequestration [t CO2 / ha / year]', min_value=1., max_value=15., value=5., step=0.5, key = "peatland_seq_ha_yr", help = help["advanced_options"][6])
            
            conif_seq_ha_yr = st.slider('Coniferous forest CO2 sequestration [t CO2 / ha / year]', min_value=1., max_value=30., value=6.5, step=0.5, key = "conif_seq_ha_yr", help = help["advanced_options"][7])
            elasticity = st.slider("Production / Imports elasticity ratio", min_value=0., max_value=1., value=0.5, step=0.1, key="elasticity", help = help["advanced_options"][9])
            agroecology_tree_coverage = st.slider("Tree coverage in agroecology", min_value=0., max_value=1., value=0.1, step=0.1, key="tree_coverage")
            
            # tillage_prod_factor = st.slider("Soil tillage production reduction", min_value=0., max_value=1., value=0.3, step=0.1, key="tillage_prod")
            # tillage_ghg_factor = st.slider("Soil tillage GHG reduction", min_value=0., max_value=1., value=0.3, step=0.1, key="tillage_ghg")

            manure_prod_factor = st.slider("Manure production reduction", min_value=0., max_value=1., value=0.3, step=0.1, key="manure_prod")
            manure_ghg_factor = st.slider("Manure GHG reduction", min_value=0., max_value=1., value=0.3, step=0.1, key="manure_ghg")

            breeding_prod_factor = st.slider("Breeding production reduction", min_value=0., max_value=1., value=0.3, step=0.1, key="breeding_prod")
            breeding_ghg_factor = st.slider("Breeding GHG reduction", min_value=0., max_value=1., value=0.3, step=0.1, key="breeding_ghg")

            methane_prod_factor = st.slider("Methane inhibitors production reduction", min_value=0., max_value=1., value=0.3, step=0.1, key="methane_prod")
            methane_ghg_factor = st.slider("Methane inhibitors GHG reduction", min_value=0., max_value=1., value=0.3, step=0.1, key="methane_ghg")

            # soil_management_ghg_factor = st.slider("Soil and carbon management GHG reduction", min_value=0., max_value=.2, value=0.05, step=0.01, key="soil_management_ghg")

            fossil_livestock_ghg_factor = st.slider("Livestock fossil fuel GHG reduction", min_value=0., max_value=.2, value=0.05, step=0.01, key="fossil_livestock_ghg_factor")
            fossil_arable_ghg_factor = st.slider("Arable fossil fuel GHG reduction", min_value=0., max_value=.2, value=0.05, step=0.01, key="fossil_arable_ghg_factor")

            fossil_livestock_prod_factor = st.slider("Livestock fossil fuel production reduction", min_value=0., max_value=1., value=0.05, step=0.01, key="fossil_livestock_prod_factor")
            fossil_arable_prod_factor = st.slider("Arable fossil fuel production reduction", min_value=0., max_value=1., value=0.05, step=0.01, key="fossil_arable_prod_factor")
            
            scaling_nutrient = st.radio("Which nutrient to keep constant when scaling food consumption",
                                        ('g/cap/day', 'g_prot/cap/day', 'g_fat/cap/day', 'kCal/cap/day'),
                                        horizontal=True,
                                        index=3,
                                        help=help["advanced_options"][9],
                                        key='nutrient_constant')
            
            st.button("Reset", on_click=update_slider,
                    kwargs={"values": [6.5, 0.14, 2250, 20, 30, 30, 50, 3.5, 6.5, 0.1, "kCal/cap/day"],
                            "keys": ['labmeat_slider',
                                     'dairy_alternatives_slider',
                                     'rda_slider',
                                     'timescale_slider',
                                     'max_ghg_animal',
                                     'max_ghg_plant',
                                     'bdleaf_conif_ratio',
                                     'bdleaf_seq_ha_yr',
                                     'conif_seq_ha_yr',
                                     'tree_coverage',
                                     'nutrient_constant']},
                    key='reset_a')

        else:
            if password != "":
                st.error("Incorrect password")

            st.session_state.cereal_scaling = True
            st.session_state.check_ID = False
            st.session_state.emission_factors = "NDC 2020"

            st.session_state.cc_production_decline = False

            st.session_state.labmeat_co2e = 6.5
            st.session_state.dairy_alternatives_co2e = 0.14
            st.session_state.rda_kcal = 2250

            st.session_state["n_scale"] = 20
            st.session_state.max_ghge_animal = 30
            st.session_state.max_ghge_plant = 30

            st.session_state.bdleaf_conif_ratio = 75
            st.session_state.bdleaf_seq_ha_yr = 3.5
            st.session_state.conif_seq_ha_yr = 6.5
            st.session_state.peatland_seq_ha_yr = 5.0

            st.session_state.elasticity = 0.5
            st.session_state.agroecology_tree_coverage = 0.1

            # tillage_prod_factor = 0.3
            # tillage_ghg_factor = 0.3

            st.session_state.manure_prod_factor = 0.3
            st.session_state.manure_ghg_factor = 0.3

            st.session_state.breeding_prod_factor = 0.3
            st.session_state.breeding_ghg_factor = 0.3

            st.session_state.methane_prod_factor = 0.3
            st.session_state.methane_ghg_factor = 0.3

            # soil_management_ghg_factor = 0.05

            st.session_state.fossil_livestock_ghg_factor = 0.05
            st.session_state.fossil_livestock_prod_factor = 0.05

            st.session_state.fossil_arable_ghg_factor = 0.05
            st.session_state.fossil_arable_prod_factor = 0.05
            
            st.session_state.scaling_nutrient = 'kCal/cap/day'              

    st.button("Reset all sliders", on_click=reset_sliders, key='reset_all')
    
    st.caption('''--- Developed with funding from [FixOurFood](https://fixourfood.org/).''')
    
    st.caption('''--- We would be grateful for your feedback - 
               [Fill in our Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSdnBp2Rmr-1fFYRQvEVcLLKchdlXZG4GakTBK5yy6jozUt8NQ/viewform?usp=sf_link).''')
    
    st.caption('''--- For a list of references to the datasets used, please
                visit our [reference document](https://docs.google.com/spreadsheets/d/1XkOELCFKHTAywUGoJU6Mb0TjXESOv5BbR67j9UCMEgw/edit?usp=sharing).''')
    
    if st.button("Help"):
        first_run_dialog()


# ----------------------------------------
#                  Main
# ----------------------------------------

food_system = Pipeline(copy.deepcopy(datablock))
food_system = pipeline_setup(food_system)
food_system.run()
datablock_result = food_system.datablock

# -------------------
# Execute plots block
# -------------------
from plots import plots
metric_yr = plots(datablock_result)
