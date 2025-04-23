from agrifoodpy.pipeline import Pipeline
from datablock_setup import *
from model import *
import streamlit as st

def pipeline_setup(food_system):

    # Global parameters
    food_system.datablock_write(["global_parameters", "timescale"], st.session_state.n_scale)

    # Consumer demand
    food_system.add_node(project_future,
                            {"yield_change":st.session_state.yield_proj})
    
    food_system.add_node(item_scaling,
                            {"scale":1+st.session_state.ruminant/100,
                            "items":[2731, 2732],
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient,
                            "constant":st.session_state.cereal_scaling,
                            "non_sel_items":("Item_group", "Cereals - Excluding Beer")})

    food_system.add_node(item_scaling,
                            {"scale":1+st.session_state.pig_poultry/100,
                            "items":[2733, 2734],
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient,
                            "constant":st.session_state.cereal_scaling,
                            "non_sel_items":("Item_group", "Cereals - Excluding Beer")})

    food_system.add_node(item_scaling,
                            {"scale":1+st.session_state.fish_seafood/100,
                            "items":("Item_group", "Fish, Seafood"),
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient,
                            "constant":st.session_state.cereal_scaling,
                            "non_sel_items":("Item_group", "Cereals - Excluding Beer")})

    food_system.add_node(item_scaling,
                            {"scale":1+st.session_state.dairy/100,
                            "items":[2740, 2743, 2948],
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient,
                            "constant":st.session_state.cereal_scaling,
                            "non_sel_items":("Item_group", "Cereals - Excluding Beer")})

    food_system.add_node(item_scaling,
                            {"scale":1+st.session_state.eggs/100,
                            "items":[2949],
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient,
                            "constant":st.session_state.cereal_scaling,
                            "non_sel_items":("Item_group", "Cereals - Excluding Beer")})

    food_system.add_node(item_scaling,
                            {"scale":1+st.session_state.fruit_veg/100,
                            "items":("Item_group", ["Vegetables", "Fruits - Excluding Wine"]),
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient,
                            "constant":st.session_state.cereal_scaling,
                            "non_sel_items":("Item_group", "Cereals - Excluding Beer")})

    food_system.add_node(item_scaling,
                            {"scale":1+st.session_state.pulses/100,
                            "items":("Item_group", ["Pulses"]),
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient,
                            "constant":st.session_state.cereal_scaling,
                            "non_sel_items":("Item_group", "Cereals - Excluding Beer")})

    food_system.add_node(cultured_meat_model,
                            {"cultured_scale":st.session_state.meat_alternatives/100,
                            "labmeat_co2e":st.session_state.labmeat_co2e,
                            "items":[2731, 2732, 2733, 2734],
                            "copy_from":2731,
                            "new_items":5000,
                            "new_item_name":"Alternative meat",
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity]})

    food_system.add_node(cultured_meat_model,
                            {"cultured_scale":st.session_state.dairy_alternatives/100,
                            "labmeat_co2e":st.session_state.dairy_alternatives_co2e,
                            "items":[2948, 2743, 2740],
                            "copy_from":2948,
                            "new_items":5001,
                            "new_item_name":"Alternative dairy",
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity]})
    
    if not st.session_state.cereal_scaling:
        food_system.add_node(item_scaling,
                            {"scale":1+st.session_state.cereals/100,
                            "items":("Item_group", "Cereals - Excluding Beer"),
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity],
                            "scaling_nutrient":st.session_state.scaling_nutrient})


    food_system.add_node(food_waste_model,
                            {"waste_scale":st.session_state.waste,
                            "kcal_rda":st.session_state.rda_kcal,
                            "source":["production", "imports"],
                            "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity]})


    # Land management
    food_system.add_node(forest_land_model_new,
                            {"forest_fraction":st.session_state.foresting_pasture/100,
                            "bdleaf_conif_ratio":st.session_state.bdleaf_conif_ratio/100,
                            })

    food_system.add_node(BECCS_farm_land,
                        {"farm_percentage":st.session_state.land_BECCS/100,
                        })

    food_system.add_node(shift_production,
                         {"scale":st.session_state.horticulture/100,
                          "items":("Item_group", ["Vegetables",
                                                  "Fruits - Excluding Wine",
                                                  "Vegetables Oils",
                                                  "Spices",
                                                  "Starchy Roots",
                                                  "Sugar Crops",
                                                  "Oilcrops",
                                                  "Treenuts",
                                                  ]),
                          "items_target":("Item_group", ["Cereals - Excluding Beer",
                                                         "Pulses",
                                                         ]),
                          "land_area_ratio":0.08650301817
                          })
    
    food_system.add_node(shift_production,
                         {"scale":st.session_state.pulse_production/100,
                          "items":("Item_group", "Pulses"),
                          "items_target":("Item_group", ["Cereals - Excluding Beer",
                                                         "Vegetables",
                                                         "Fruits - Excluding Wine",
                                                         "Vegetables Oils",
                                                         "Spices",
                                                         "Starchy Roots",
                                                         "Sugar Crops",
                                                         "Oilcrops",
                                                         "Treenuts",                                                      
                                                         ]),
                          "land_area_ratio":0.03327492402
                          })

    food_system.add_node(peatland_restoration,
                        {"restore_fraction":0.0475*st.session_state.lowland_peatland/100,
                         "new_land_type":"Restored lowland peat",
                         "old_land_type":["Arable"],
                         "items":"Vegetal Products",
                         })
    
    food_system.add_node(peatland_restoration,
                        {"restore_fraction":0.0273*st.session_state.upland_peatland/100,
                         "new_land_type":"Restored upland peat",
                         "old_land_type":["Improved grassland", "Semi-natural grassland"],
                         "items":"Animal Products",
                         })
    
    food_system.add_node(managed_agricultural_land_carbon_model,
                        {"fraction":st.session_state.pasture_soil_carbon/100,
                         "managed_class":"Managed pasture",
                         "old_class":["Improved grassland", "Semi-natural grassland"]})
    
    food_system.add_node(managed_agricultural_land_carbon_model,
                        {"fraction":st.session_state.arable_soil_carbon/100,
                         "managed_class":"Managed arable",
                         "old_class":"Arable"})


    food_system.add_node(mixed_farming_model,
                        {"fraction":st.session_state.mixed_farming/100,
                         "prod_scale_factor":st.session_state.mixed_farming_production_scale,
                         "items":("Item_origin","Vegetal Products"),
                         "secondary_prod_scale_factor":st.session_state.mixed_farming_secondary_production_scale,
                         "secondary_items":("Item_origin","Animal Products")})

    # Livestock farming practices        
    
    food_system.add_node(agroecology_model,
                            {"land_percentage":st.session_state.silvopasture/100.,
                            "agroecology_class":"Silvopasture",
                            "land_type":["Improved grassland",
                                         "Semi-natural grassland",
                                         "Managed pasture"],
                            "tree_coverage":st.session_state.agroecology_tree_coverage,
                            "replaced_items":[2731, 2732],
                            "seq_ha_yr":st.session_state.agroecology_tree_coverage*(st.session_state.bdleaf_conif_ratio/100 * st.session_state.bdleaf_seq_ha_yr \
                                        + (1 - st.session_state.bdleaf_conif_ratio/100) * st.session_state.conif_seq_ha_yr) \
                                        + (1 - st.session_state.agroecology_tree_coverage) * st.session_state.managed_pasture_seq_ha_yr,
                            })
    
    food_system.add_node(scale_impact,
                         {"items":("Item_origin","Vegetal Products"),
                          "scale_factor":st.session_state.nitrogen_ghg_factor*st.session_state.nitrogen/100})

    food_system.add_node(scale_impact,
                            {"items":[2731, 2732],
                            "scale_factor":st.session_state.methane_ghg_factor*st.session_state.methane_inhibitor/100})
    
    food_system.add_node(scale_production,
                            {"scale_factor":1+st.session_state.stock_density/100,
                             "items":[2731, 2732, 2733, 2735, 2948, 2740, 2743],
                             "elasticity":[st.session_state.elasticity, 1-st.session_state.elasticity]})

    # food_system.add_node(scale_production,
    #                         {"scale_factor":1-st.session_state.methane_prod_factor*st.session_state.methane_inhibitor/100,
    #                         "items":[2731, 2732]})

    food_system.add_node(scale_impact,
                            {"items":[2731, 2732, 2733, 2735, 2948, 2740, 2743],
                            "scale_factor":st.session_state.manure_ghg_factor*st.session_state.manure_management/100})

    # food_system.add_node(scale_production,
    #                         {"scale_factor":1-st.session_state.manure_prod_factor*st.session_state.manure_management/100,
    #                         "items":[2731, 2732, 2733, 2735, 2948, 2740, 2743]})

    food_system.add_node(scale_impact,
                            {"items":[2731, 2732],
                            "scale_factor":st.session_state.breeding_ghg_factor*st.session_state.animal_breeding/100})

    # food_system.add_node(scale_production,
    #                         {"scale_factor":1-st.session_state.breeding_prod_factor*st.session_state.animal_breeding/100,
    #                         "items":[2731, 2732]})
    
    food_system.add_node(scale_impact,
                            {"items":("Item_origin","Animal Products"),
                            "scale_factor":st.session_state.fossil_livestock_ghg_factor*st.session_state.fossil_livestock/100})

    # food_system.add_node(scale_production,
    #                         {"scale_factor":1 - st.session_state.fossil_livestock_prod_factor*st.session_state.fossil_livestock/100,
    #                         "items":("Item_origin","Animal Products")})

    # Arable farming practices
    food_system.add_node(agroecology_model,
                            {"land_percentage":st.session_state.agroforestry/100.,
                            "agroecology_class":"Agroforestry",
                            "land_type":["Arable",
                                         "Managed arable"],
                            "tree_coverage":st.session_state.agroecology_tree_coverage,
                            "replaced_items":2511,
                            "seq_ha_yr":st.session_state.agroecology_tree_coverage*(st.session_state.bdleaf_conif_ratio/100 * st.session_state.bdleaf_seq_ha_yr \
                                        + (1 - st.session_state.bdleaf_conif_ratio/100) * st.session_state.conif_seq_ha_yr) \
                                        + (1 - st.session_state.agroecology_tree_coverage) * st.session_state.managed_pasture_seq_ha_yr,
                            
                            })
    
    # food_system.add_node(zero_land_farming_model,
    #                      {"fraction":st.session_state.vertical_farming/100,
    #                       "items":("Item_group", ["Vegetables", "Fruits - Excluding Wine"]),
    #                       "bdleaf_conif_ratio":st.session_state.bdleaf_conif_ratio/100})
    

    food_system.add_node(extra_urban_farming,
                         {"fraction":st.session_state.vertical_farming/100,
                          "items":("Item_group", ["Vegetables", "Fruits - Excluding Wine"])
                          })

    food_system.add_node(scale_impact,
                            {"items":("Item_origin", "Vegetal Products"),
                            "scale_factor":st.session_state.fossil_arable_ghg_factor*st.session_state.fossil_arable/100})

    # food_system.add_node(scale_production,
    #                         {"scale_factor":1 - st.session_state.fossil_arable_prod_factor*st.session_state.fossil_arable/100,
    #                         "items":("Item_origin", "Vegetal Products")})

    # Technology & Innovation    
    food_system.add_node(ccs_model,
                            {"waste_BECCS":st.session_state.waste_BECCS*1e6,
                            "overseas_BECCS":st.session_state.overseas_BECCS*1e6,
                            "DACCS":st.session_state.DACCS*1e6})


    # Compute emissions and sequestration
    food_system.add_node(forest_sequestration_model,
                            {"land_type":["Broadleaf woodland",
                                          "Coniferous woodland",
                                          "Restored upland peat",
                                          "Restored lowland peat",
                                          "Managed arable",
                                          "Managed pasture",
                                          "Mixed farming",
                                          ],
                            "seq":[st.session_state.bdleaf_seq_ha_yr,
                                   st.session_state.conif_seq_ha_yr,
                                   st.session_state.peatland_seq_ha_yr,
                                   st.session_state.peatland_seq_ha_yr,
                                   st.session_state.managed_arable_seq_ha_yr,
                                   st.session_state.managed_pasture_seq_ha_yr,
                                   st.session_state.mixed_farming_seq_ha_yr,
                                   ]})

    food_system.add_node(compute_emissions)

    return food_system
