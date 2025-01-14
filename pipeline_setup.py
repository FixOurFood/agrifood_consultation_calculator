from utils.pipeline import Pipeline
from datablock_setup import *
from model import *
import streamlit as st

def pipeline_setup(food_system):

    # Global parameters
    food_system.datablock_write(["global_parameters", "timescale"], st.session_state.n_scale)

    # Consumer demand
    food_system.add_step(project_future,
                            {"scale":proj_pop,
                            "cc_decline":st.session_state.cc_production_decline})

    food_system.add_step(item_scaling,
                            {"scale":1-st.session_state.ruminant/100,
                            "items":[2731, 2732],
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient,
                            "constant":st.session_state.cereal_scaling,
                            "non_sel_items":cereal_items})

    food_system.add_step(item_scaling,
                            {"scale":1-st.session_state.pig_poultry_eggs/100,
                            "items":[2733, 2734, 2949],
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient,
                            "constant":st.session_state.cereal_scaling,
                            "non_sel_items":cereal_items})

    food_system.add_step(item_scaling,
                            {"scale":1-st.session_state.dairy/100,
                            "items":[2740, 2743, 2948],
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient,
                            "constant":st.session_state.cereal_scaling,
                            "non_sel_items":cereal_items})

    food_system.add_step(item_scaling,
                            {"scale":1+st.session_state.fruit_veg/100,
                            "item_group":["Vegetables", "Fruits - Excluding Wine"],
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient,
                            "constant":st.session_state.cereal_scaling,
                            "non_sel_items":cereal_items})

    if not st.session_state.cereal_scaling:
        food_system.add_step(item_scaling,
                            {"scale":1+st.session_state.cereals/100,
                            "item_group":["Cereals - Excluding Beer"],
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient})

    food_system.add_step(cultured_meat_model,
                            {"cultured_scale":st.session_state.meat_alternatives/100,
                            "labmeat_co2e":st.session_state.labmeat_co2e,
                            "items":[2731, 2732],
                            "copy_from":2731,
                            "new_items":5000,
                            "new_item_name":"Alternative meat",
                            "source":"production"})

    food_system.add_step(cultured_meat_model,
                            {"cultured_scale":st.session_state.dairy_alternatives/100,
                            "labmeat_co2e":st.session_state.dairy_alternatives_co2e,
                            "items":[2948],
                            "copy_from":2948,
                            "new_items":5001,
                            "new_item_name":"Alternative dairy",
                            "source":"production"})    

    food_system.add_step(food_waste_model,
                            {"waste_scale":st.session_state.waste,
                            "kcal_rda":st.session_state.rda_kcal,
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity]})


    # Land management
    food_system.add_step(spare_alc_model,
                            {"spare_fraction":st.session_state.foresting_pasture/100,
                            "land_type":["Improved grassland", "Semi-natural grassland"],
                            "items":"Animal Products"})
    

    food_system.add_step(foresting_spared_model,
                            {"forest_fraction":1,
                            "bdleaf_conif_ratio":st.session_state.bdleaf_conif_ratio/100})

    food_system.add_step(BECCS_farm_land,
                            {"farm_percentage":st.session_state.land_BECCS/100})

    food_system.add_step(peatland_restoration,
                        {"restore_fraction":st.session_state.peatland/100,
                         "land_type":["Improved grassland", "Semi-natural grassland", "Arable"],
                         "items":"Animal Products",
                         "peat_map_key":"peatland",
                         "mask_val":1})

    food_system.add_step(soil_carbon_sequestration,
                        {"fraction":st.session_state.soil_carbon/100})

    food_system.add_step(mixed_farming_model,
                        {"fraction":st.session_state.mixed_farming/100})



    # Livestock farming practices        
    food_system.add_step(agroecology_model,
                            {"land_percentage":st.session_state.silvopasture/100.,
                            "agroecology_class":"Silvopasture",
                            "land_type":["Improved grassland", "Semi-natural grassland"],
                            "tree_coverage":st.session_state.agroecology_tree_coverage,
                            "replaced_items":[2731, 2732],
                            "new_items":2617,
                            "item_yield":1e2})

    food_system.add_step(scale_impact,
                            {"items":[2731, 2732],
                            "scale_factor":1 - st.session_state.methane_ghg_factor*st.session_state.methane_inhibitor/100})

    food_system.add_step(scale_production,
                            {"scale_factor":1-st.session_state.methane_prod_factor*st.session_state.methane_inhibitor/100,
                            "items":[2731, 2732]})

    food_system.add_step(scale_impact,
                            {"items":[2731, 2732],
                            "scale_factor":1 - st.session_state.manure_ghg_factor*st.session_state.manure_management/100})

    food_system.add_step(scale_production,
                            {"scale_factor":1-st.session_state.manure_prod_factor*st.session_state.manure_management/100,
                            "items":[2731, 2732]})

    food_system.add_step(scale_impact,
                            {"items":[2731, 2732],
                            "scale_factor":1 - st.session_state.breeding_ghg_factor*st.session_state.animal_breeding/100})

    food_system.add_step(scale_production,
                            {"scale_factor":1-st.session_state.breeding_prod_factor*st.session_state.animal_breeding/100,
                            "items":[2731, 2732]})
    
    food_system.add_step(scale_impact,
                            {"items":[2731, 2732],
                            "scale_factor":1 - st.session_state.fossil_livestock_ghg_factor*st.session_state.fossil_livestock/100})

    food_system.add_step(scale_production,
                            {"scale_factor":1 - st.session_state.fossil_livestock_prod_factor*st.session_state.fossil_livestock/100,
                            "items":[2731, 2732]})

    # Arable farming practices
    food_system.add_step(agroecology_model,
                            {"land_percentage":st.session_state.agroforestry/100.,
                            "agroecology_class":"Agroforestry",
                            "land_type":["Arable"],
                            "tree_coverage":st.session_state.agroecology_tree_coverage,
                            "replaced_items":2511,
                            "new_items":2617,
                            "item_yield":1e2})
    
    food_system.add_step(zero_land_farming_model,
                         {"fraction":st.session_state.vertical_farming/100,
                          "items":("Item_group", ["Vegetables", "Fruits - Excluding Wine"]),
                          "bdleaf_conif_ratio":st.session_state.bdleaf_conif_ratio/100})

    food_system.add_step(scale_impact,
                            {"item_origin":"Vegetal Products",
                            "scale_factor":1 - st.session_state.fossil_arable_ghg_factor*st.session_state.fossil_arable/100})

    food_system.add_step(scale_production,
                            {"scale_factor":1 - st.session_state.fossil_arable_prod_factor*st.session_state.fossil_arable/100,
                            "item_origin":"Vegetal Products"})

    # Technology & Innovation    
    food_system.add_step(ccs_model,
                            {"waste_BECCS":st.session_state.waste_BECCS*1e6,
                            "overseas_BECCS":st.session_state.overseas_BECCS*1e6,
                            "DACCS":st.session_state.DACCS*1e6})


    # Compute emissions and sequestration
    food_system.add_step(forest_sequestration_model,
                            {"land_type":["Broadleaf woodland", "Coniferous woodland", "Peatland"],
                            "seq":[st.session_state.bdleaf_seq_ha_yr,
                                   st.session_state.conif_seq_ha_yr,
                                   st.session_state.peatland_seq_ha_yr]})

    food_system.add_step(compute_emissions)

    return food_system
