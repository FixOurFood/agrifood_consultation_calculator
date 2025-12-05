import streamlit as st
from millify import millify
from utils.altair_plots import *
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


def plot_uk_as_farm(datablock, background_color):

    with st.container(height=820, border=True):

        data = {
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

    # Self-sufficiency ratio
    ssr_metric = st.session_state["ssr_metric"]
    with st.container(height=375, border=True):

        SSR_ref = datablock["metrics"]["SSR_ref"]
        SSR_metric_yr = datablock["metrics"]["SSR_metric_yr"]
        gcapday = datablock["metrics"]["gcapday_item_origin"]

        st.markdown("""**Self-sufficiency**""")

        st.metric(
            label="SSR",
            value="{:.2f} %".format(100 * SSR_metric_yr),
            delta="{:.2f} %".format(100 * (SSR_metric_yr - SSR_ref)),
            label_visibility="collapsed",
        )

    # Production
    with st.container(height=392 + 75, border=True):

        new_dairy_herd = datablock["metrics"]["new_dairy_herd"].isel(Year=-1)
        new_beef_herd = datablock["metrics"]["new_beef_herd"].isel(Year=-1)
        new_poultry_heads = datablock["metrics"]["new_poultry_heads"].isel(Year=-1)
        new_pig_heads = datablock["metrics"]["new_pig_heads"].isel(Year=-1)
        new_sheep_flock = datablock["metrics"]["new_sheep_flock"].isel(Year=-1)
        baseline_dairy_herd = datablock["metrics"]["baseline_dairy_herd"]
        baseline_beef_herd = datablock["metrics"]["baseline_beef_herd"]
        baseline_poultry_heads = datablock["metrics"]["baseline_poultry_heads"]
        baseline_pig_heads = datablock["metrics"]["baseline_pig_heads"]
        baseline_sheep_flock = datablock["metrics"]["baseline_sheep_flock"]

        st.markdown("""**Production and consumption**""")

        cols = st.columns(3)
        with cols[0]:
            st.metric(
                label="Herd size",
                value=f"{millify(new_dairy_herd+new_beef_herd, precision=2)}",
                delta=millify(
                    new_dairy_herd
                    + new_beef_herd
                    - baseline_dairy_herd
                    - baseline_beef_herd,
                    precision=2,
                ),
            )
        with cols[1]:
            st.metric(
                label="Dairy herd",
                value=f"{millify(new_dairy_herd, precision=2)}",
                delta=millify(new_dairy_herd - baseline_dairy_herd, precision=2),
            )
        with cols[2]:
            st.metric(
                label="Beef herd",
                value=f"{millify(new_beef_herd, precision=2)}",
                delta=millify(new_beef_herd - baseline_beef_herd, precision=2),
            )

        with cols[0]:
            st.metric(
                label="Poultry heads",
                value=f"{millify(new_poultry_heads, precision=2)}",
                delta=millify(new_poultry_heads - baseline_poultry_heads, precision=2),
            )
        with cols[1]:
            st.metric(
                label="Pig heads",
                value=f"{millify(new_pig_heads, precision=2)}",
                delta=millify(new_pig_heads - baseline_pig_heads, precision=2),
            )
        with cols[2]:
            st.metric(
                label="Sheep flock",
                value=f"{millify(new_sheep_flock, precision=2)}",
                delta=millify(new_sheep_flock - baseline_sheep_flock, precision=2),
            )

        st.markdown("""**Land use**""")
