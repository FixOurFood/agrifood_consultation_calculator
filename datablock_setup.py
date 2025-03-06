import numpy as np
import xarray as xr
import streamlit as st
import copy
import base64
from io import BytesIO
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from agrifoodpy.impact.model import fbs_impacts, fair_co2_only
from agrifoodpy.pipeline import Pipeline

@st.cache_data(ttl=60*60*24)
def datablock_setup(population_projection="Medium"):

    """
    This function sets up the datablock for the Agrifood Calculator.

    It loads the data from the agrifoodpy_data package and returns a datablock
    type dictionary with all the necessary data. This function is cached to
    improve performance and avoid re-running the function if the data has not
    changed. It takes a single argument, population_projection, which is a
    string that specifies the population projection to use.
    """

    from agrifoodpy_data.food import FAOSTAT, Nutrients_FAOSTAT
    from agrifoodpy_data.impact import PN18_FAOSTAT, UKNDC_FAOSTAT
    from agrifoodpy_data.population import UN
    from agrifoodpy_data.land import NaturalEngland_ALC_1000 as ALC

    datablock = {}
    datablock["food"] = {}
    datablock["land"] = {}
    datablock["impact"] = {}
    datablock["population"] = {}

    # ----------------------
    # Regional configuration
    # ----------------------

    area_pop = 826 #UK
    # area_pop = 900 # WORLD
    area_pop_world = 900 #WORLD

    area_fao = 229 #UK
    # area_fao = 5000 # WORLD
    years = np.arange(2020, 2051)

    # ------------------------------
    # Select population data from UN
    # ------------------------------

    pop = UN.Medium.sel(Region=[area_pop, area_pop_world], Year=years, Datatype="Total")*1000
    # pop_proj = UN[st.session_state["population_projection"]].sel(Region=[area_pop, area_pop_world], Year=years, Datatype="Total")*1000
    pop_proj = UN[population_projection].sel(Region=[area_pop, area_pop_world], Year=years, Datatype="Total")*1000

    years_with_data = pop_proj.where(np.isfinite(pop_proj), drop=True).Year.values
    years_to_fill = np.setdiff1d(years, years_with_data)
    
    pop_proj.loc[{"Year":years_to_fill}] = pop.sel(Year=years_to_fill)

    datablock["population"]["population"] = pop_proj

    # -----------------------------------------
    # Select food consumption data from FAOSTAT
    # -----------------------------------------

    FAOSTAT *= 1
    # 1000 T / year
    food_uk = FAOSTAT.sel(Region=229, Year=2020).expand_dims("Year")

    # Delete summary items
    food_uk = food_uk.drop_sel(Item=[2905, 2943, 2924,
                                    2946, 2961, 2960,
                                    2919, 2945, 2913,
                                    2911, 2923, 2907,
                                    2918, 2914, 2912,
                                    2908, 2909, 2922,
                                    2941, 2903])

    datablock["food"]["1000 T/year"] = food_uk


    # ----------------
    # Emission factors
    # ----------------
    scale_ones = xr.DataArray(data = np.ones_like(food_uk.Year.values),
                            coords = {"Year":food_uk.Year.values})
    extended_impact = PN18_FAOSTAT["GHG Emissions (IPCC 2013)"].drop_vars(["Item_name", "Item_group", "Item_origin"]) * scale_ones

    datablock["impact"]["gco2e/gfood"] = extended_impact

    cereal_items = food_uk.sel(Item=food_uk["Item_group"]=="Cereals - Excluding Beer").Item.values

    # --------------------------
    # UK Per capita daily values
    # --------------------------

    # g_food / cap / day
    pop_past_uk = pop.sel(Year=2020, Region=area_pop)
    food_cap_day_baseline = food_uk*1e9/pop_past_uk/365.25

    datablock["food"]["g/cap/day"] = food_cap_day_baseline

    # kCal, g_prot, g_fat / g_food
    qty_g = Nutrients_FAOSTAT[["kcal", "protein", "fat"]].sel(Region=area_fao, Year=2020)
    qty_g = qty_g.where(np.isfinite(qty_g), other=0)

    datablock["food"]["kCal/g_food"] = qty_g["kcal"]
    datablock["food"]["g_prot/g_food"] = qty_g["protein"]
    datablock["food"]["g_fat/g_food"] = qty_g["fat"]

    # kCal, g_prot, g_fat, g_co2e / cap / day
    kcal_cap_day_baseline = food_cap_day_baseline * datablock["food"]["kCal/g_food"]
    prot_cap_day_baseline = food_cap_day_baseline * datablock["food"]["g_prot/g_food"]
    fats_cap_day_baseline = food_cap_day_baseline * datablock["food"]["g_fat/g_food"]
    co2e_cap_day_baseline = food_cap_day_baseline * datablock["impact"]["gco2e/gfood"]

    datablock["food"]["kCal/cap/day"] = kcal_cap_day_baseline
    datablock["food"]["g_prot/cap/day"] = prot_cap_day_baseline
    datablock["food"]["g_fat/cap/day"] = fats_cap_day_baseline
    datablock["food"]["g_co2e/cap/day"] = co2e_cap_day_baseline

    # g_co2e / year

    # These are UK values for the entire population and year
    if "emission_factors" not in st.session_state:
        st.session_state.emission_factors = "NDC 2020"

    if st.session_state['emission_factors'] == "NDC 2020":
        scale_ones = xr.DataArray(data = np.ones_like(food_uk.Year.values),
                            coords = {"Year":food_uk.Year.values})

        extended_impact = UKNDC_FAOSTAT["GHG Emissions (IPCC 2013)"].drop_vars(["Item_name", "Item_group", "Item_origin"]) * scale_ones

        datablock["impact"]["gco2e/gfood"] = extended_impact

    datablock["impact"]["g_co2e/year"] = fbs_impacts(food_uk, datablock["impact"]["gco2e/gfood"])

    per_cap_day = {"Weight":food_cap_day_baseline,
                "Energy":kcal_cap_day_baseline,
                "Proteins":prot_cap_day_baseline,
                "Fat":fats_cap_day_baseline,
                "Emissions":co2e_cap_day_baseline}

    # ------------------
    # UK Per year values
    # ------------------

    # g_food, kCal, g_prot, g_fat, g_co2e / Year
    food_year_baseline = food_cap_day_baseline * pop_past_uk * 365.25
    kcal_year_baseline = kcal_cap_day_baseline * pop_past_uk * 365.25
    prot_year_baseline = prot_cap_day_baseline * pop_past_uk * 365.25
    fats_year_baseline = fats_cap_day_baseline * pop_past_uk * 365.25
    co2e_year_baseline = co2e_cap_day_baseline * pop_past_uk * 365.25

    datablock["food"]["g/year"] = food_year_baseline
    datablock["food"]["kCal/year"] = kcal_year_baseline
    datablock["food"]["g_prot/year"] = prot_year_baseline
    datablock["food"]["g_fat/year"] = fats_year_baseline
    datablock["food"]["g_co2e/year"] = co2e_year_baseline

    per_year = {"Weight":food_year_baseline,
                "Energy":kcal_year_baseline,
                "Fat":fats_year_baseline,
                "Proteins":prot_year_baseline,
                "Emissions":co2e_year_baseline}

    # -------------------------------
    # Land use data
    # -------------------------------

    # Get AES key & IV from secrets
    AES_KEY = base64.b64decode(st.secrets["AES_KEY"])
    AES_IV = base64.b64decode(st.secrets["AES_IV"])
    with open("UKCEH_LC_target_percentage.bin", "rb") as f:
        encrypted_data = f.read()

    # Decrypt the dataset
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    LC = xr.open_dataarray(BytesIO(decrypted_data))

    # Make sure the land use data and ALC data have the same coordinate base
    ALC, LC = xr.align(ALC, LC, join="outer")
    peatland = xr.open_dataarray("images/peatland_binary_mask.nc")

    # datablock["land"]["percentage_land_use"] = LC.where(np.isfinite(ALC.grade))
    datablock["land"]["percentage_land_use"] = LC
    datablock["land"]["dominant_classification"] = ALC.grade
    datablock["land"]["peatland"] = peatland

    # -------------------------------
    # Baseline data for comparison
    # -------------------------------

    datablock["land"]["baseline"] = copy.deepcopy(datablock["land"]["percentage_land_use"])
    datablock["food"]["baseline"] = copy.deepcopy(datablock["food"]["g/cap/day"])

    return datablock