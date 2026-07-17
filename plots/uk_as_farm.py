import streamlit as st
from millify import millify
from utils.altair_plots import *
from utils.helper_functions import aligned_markdown
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.patches as mpatches

from components.farm import farm_component


def change_to_afolu_only():
    """Helper to change the Agrifood Only checkbox to True"""
    st.session_state.show_afolu_only = st.session_state.show_afolu_only_checkbox


def update_SSR_metric():
    """Helper to update the SSR metric"""
    st.session_state.ssr_metric = st.session_state.update_ssr_metric


def map_max(map, dim):
    """function to return the coordinate index of the maximum value along a
    dimension"""

    length_dim = len(map[dim].values)
    map_fixed = map.assign_coords({dim: np.arange(length_dim)})

    return map_fixed.idxmax(dim=dim, skipna=True)


def plot_uk_as_farm():

    datablock = st.session_state["datablock"]

    col1_farm, col2_farm = st.columns((1, 3))

    with col1_farm:
        st.markdown("""# UK as a farm""")
        aligned_markdown("""The UK as a farm chart visualizes the entire country as a single farm,
            and allows us to understand the overall agricultural and food
            production system of the UK, including land use, livestock
            populations, crop areas, and other key metrics. 
            This holistic view helps in assessing the sustainability and
            efficiency of the UK's food system.""",
            alignment="justify")
        
        aligned_markdown("""Hover over the chart to see the values of each component""",
            alignment="justify")
        
    with col2_farm:

        with st.container(border=True):

            data = {
                "total_emissions": float(datablock["metrics"]["total_emissions"]),
                "self_sufficiency": float(
                    datablock["metrics"]["SSR_metric_yr"].values
                ),  #  TOOD check if right metric
                "dairy_herd": float(
                    datablock["metrics"]["new_dairy_herd"].isel(Year=-1).values
                )
                / 1e6,
                "beef_herd": float(
                    datablock["metrics"]["new_beef_herd"].isel(Year=-1).values
                )
                / 1e6,
                "pigs": float(datablock["metrics"]["new_pig_heads"].isel(Year=-1).values)
                / 1e6,
                "poultry": float(
                    datablock["metrics"]["new_poultry_heads"].isel(Year=-1).values
                )
                / 1e6,
                "sheep": float(datablock["metrics"]["new_sheep_flock"].isel(Year=-1).values)
                / 1e6,
                "potatoes": float(
                    datablock["metrics"]["new_potato_area"].isel(Year=-1).values
                ),
                "oilseeds": float(
                    datablock["metrics"]["new_oilseed_area"].isel(Year=-1).values
                ),
                "cereals": float(
                    datablock["metrics"]["new_cereal_area"].isel(Year=-1).values
                ),
                "horticulture": float(datablock["metrics"]["new_horticulture_area"]),
                "other_crops": float(
                    datablock["metrics"]["other_crops_area_mha"].isel(Year=-1).values
                ),
                "additional_forest": float(datablock["metrics"]["new_forest_land"]) / 1e6,
                "total_arable": float(datablock["metrics"]["total_arable"]) / 1e6,
                "total_pasture": float(datablock["metrics"]["total_pasture"]) / 1e6,
                "restored_peatland": float(datablock["metrics"]["total_restored_peatland"])
                / 1e6,
                "agroforestry": float(datablock["metrics"]["total_agroforestry"]) / 1e6,
                "silvopasture": float(datablock["metrics"]["total_silvopasture"]) / 1e6,
                "mixed_farming": float(datablock["metrics"]["total_mixed_farming"]) / 1e6,
                "beccs_on_arable": float(datablock["metrics"]["beccs_on_arable"]) / 1e6,
                "beccs_on_pasture": float(datablock["metrics"]["beccs_on_pasture"]) / 1e6,
                "total_beccs": float(datablock["metrics"]["total_beccs"]) / 1e6,
            }
            # print(data)
            farm_component(data)
    
# plot_uk_as_farm()
