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
    map_fixed = map.assign_coords({dim:np.arange(length_dim)})

    return map_fixed.idxmax(dim=dim, skipna=True)

def plot_summary():

    datablock = st.session_state["datablock"]
    background_color = st.session_state["background_color"]

    reference_emissions_baseline = st.secrets["baseline_total_emissions"]

    col_comp_1, col_comp_2, col_comp_3 = st.columns([1,1,1])

    with col_comp_1:

        # Emissions and removals balance
        with st.container(height=850, border=True):

            emissions_balance = datablock["metrics"]["emissions_balance"]
            total_seq = datablock["metrics"]["total_sequestration"]
            total_removals = datablock["metrics"]["total_removals"]
            total_emissions = datablock["metrics"]["total_emissions"]
            agricultural_emissions = datablock["metrics"]["agricultural_emissions"]
            reference_afolu_emissions = st.secrets["baseline_afolu_emissions"]
            
            st.markdown('''**UK Emissions balance**''')
                
            if st.session_state["show_afolu_only"]:
                emissions_balance = emissions_balance.sel(Sector=["Agriculture", "LU sinks", "Removals"])
                reference_emissions_baseline = reference_afolu_emissions

            c = plot_single_bar_altair(emissions_balance, show="Sector", color=sector_emissions_colors,
                axis_title="Mt CO2e / year", unit="Mt CO2e / year", vertical=True,
                mark_total=True, show_zero=True, ax_ticks=True, legend=True,
                ax_min=-80, ax_max=120, reference=reference_emissions_baseline)
                
            c = c.properties(height=450)
            # c = c.configure(background='white').configure_axisLeft(labelColor='black', titleColor='black').configure_legend(labelColor='black', titleColor='black')

            st.altair_chart(c, use_container_width=True)
            st.checkbox("Show agriculture and land use only", value=False, on_change=change_to_afolu_only, key="show_afolu_only_checkbox")
            st.metric(label="Total emissions", value="{:.2f} Mt CO2e / year".format(emissions_balance.sum().values),
                delta="{:.2f} Mt CO2e / year".format(emissions_balance.sum().values - reference_emissions_baseline),
                delta_color="inverse")
            
            st.metric(label="Sequestration and removals", value="{:.2f} Mt CO2e / year".format(total_seq + total_removals))
            st.metric(label="Agricultural emissions", value="{:.2f} Mt CO2e / year".format(agricultural_emissions))

            # st.markdown(f"Total emissions: **{emissions_balance.sum().to_numpy():.2f} Mt CO2e / year**")
            # st.caption('''<div style="text-align: justify;">
            #            The diagram above visualises the balance between total
            #            emissions produced in the UK, and carbon storage.
            #            The red diamond shows the net balance, the red dot is
            #            at zero and your goal is to move the sliders to get
            #            them to line up.</div>''', unsafe_allow_html=True)
            # st.write("\n")
            # st.caption('''<div style="text-align: justify;">
            #            It assumes other (non agrifood) sectors reduce their
            #            emissions according to the CCC balanced pathway.
            #            The black line shows the situation in 2050 if the
            #            agrifood system stays the same as it is today. 
            #            </div>''', unsafe_allow_html=True)

    with col_comp_2:

        # Self-sufficiency ratio
        ssr_metric = st.session_state["ssr_metric"]
        with st.container(height=375, border=True):

            SSR_ref = datablock["metrics"]["SSR_ref"]
            SSR_metric_yr = datablock["metrics"]["SSR_metric_yr"]
            gcapday = datablock["metrics"]["gcapday_item_origin"]

            st.markdown('''**Self-sufficiency**''')

            st.metric(label="SSR", value="{:.2f} %".format(100*SSR_metric_yr),
                delta="{:.2f} %".format(100*(SSR_metric_yr-SSR_ref)), label_visibility="collapsed")

            origin_color={"Animal Products": "red",
                            "Plant Products": "green",
                            "Alternative Food": "blue"}
            
            domestic_use = gcapday["imports"]+gcapday["production"]-gcapday["exports"]
            domestic_use.name="domestic"

            production_bar = plot_single_bar_altair(gcapday["production"],
                                                    show="Item",
                                                    legend=True,
                                                    vertical=False,
                                                    ax_ticks=True,
                                                    bar_width=100,
                                                    ax_min=0,
                                                    ax_max=np.max([gcapday["production"].sum(), domestic_use.sum()]),
                                                    axis_title="Food production per capita",
                                                    unit=ssr_metric.replace("_"," "),
                                                    color=origin_color)

            imports_bar = plot_single_bar_altair(domestic_use,
                                                    show="Item",
                                                    legend=True,
                                                    vertical=False,
                                                    ax_ticks=True,
                                                    bar_width=100,
                                                    ax_min=0,
                                                    ax_max=np.max([gcapday["production"].sum(), domestic_use.sum()]),
                                                    axis_title="Domestic use per capita",
                                                    unit=ssr_metric.replace("_"," "),
                                                    color=origin_color)

            if SSR_metric_yr < SSR_ref:
                st.markdown(f'''
                <span style="color:red">
                <b>The UK is more dependent on imports than today</b>
                </span>
                ''', unsafe_allow_html=True)

            elif SSR_metric_yr > SSR_ref and SSR_metric_yr < 1:
                st.markdown(f'''
                <span style="color:orange">
                <b>The UK is more self-sufficient</b>
                </span>
                ''', unsafe_allow_html=True)

            elif SSR_metric_yr > 1:
                st.markdown(f'''
                <span style="color:green">
                <b>The UK is completely self-sufficient</b>
                </span>
                ''', unsafe_allow_html=True)

            st.write("")

            st.altair_chart(production_bar, use_container_width=True)
            st.altair_chart(imports_bar, use_container_width=True)
            # st.selectbox("Select metric",
                            
            #                 ["g/cap/day",
            #                 "g_prot/cap/day",
            #                 "g_fat/cap/day",
            #                 "g_co2e/cap/day",
            #                 "kCal/cap/day",],

            #                 key="update_ssr_metric",
            #                 on_change=update_SSR_metric,
            #                 label_visibility="collapsed",
            #                 placeholder="Select metric")
            
            # st.caption('''<div style="text-align: justify;">
            # This panel calculates how much the UK relies on food imports, by
            # comparing the amount we produce in the UK to the amount we use.
            # The UK currently produces 73% of what it uses, and a lower value
            # would mean we depend more on imports.</div>''', unsafe_allow_html=True)
            # st.write("\n")
            # st.caption('''<div style="text-align: justify;">
            # This percentage can be calculated by weight (tonnes produced /
            # tonnes used) or other metrics e.g. kcal produced / kcal used or
            # nutrients such as protein.
            # </div>''', unsafe_allow_html=True)

        
        # Production
        with st.container(height=392+75, border=True):

            st.markdown('''**UK as farm**''')

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

            # new_dairy_herd = datablock["metrics"]["new_dairy_herd"].isel(Year=-1)
            # new_beef_herd = datablock["metrics"]["new_beef_herd"].isel(Year=-1)
            # new_poultry_heads = datablock["metrics"]["new_poultry_heads"].isel(Year=-1)
            # new_pig_heads = datablock["metrics"]["new_pig_heads"].isel(Year=-1)
            # new_sheep_flock = datablock["metrics"]["new_sheep_flock"].isel(Year=-1)
            # baseline_dairy_herd = datablock["metrics"]["baseline_dairy_herd"]
            # baseline_beef_herd = datablock["metrics"]["baseline_beef_herd"]
            # baseline_poultry_heads = datablock["metrics"]["baseline_poultry_heads"]
            # baseline_pig_heads = datablock["metrics"]["baseline_pig_heads"]
            # baseline_sheep_flock = datablock["metrics"]["baseline_sheep_flock"]

            # st.markdown('''**Production and consumption**''')

            # cols = st.columns(3)
            # with cols[0]:
            #     st.metric(label="Herd size", value=f"{millify(new_dairy_herd+new_beef_herd, precision=2)}",
            #             delta=millify(new_dairy_herd+new_beef_herd - baseline_dairy_herd - baseline_beef_herd, precision=2))
            # with cols[1]:
            #     st.metric(label="Dairy herd", value=f"{millify(new_dairy_herd, precision=2)}",
            #             delta=millify(new_dairy_herd - baseline_dairy_herd, precision=2))
            # with cols[2]:
            #     st.metric(label="Beef herd", value=f"{millify(new_beef_herd, precision=2)}",
            #             delta=millify(new_beef_herd - baseline_beef_herd, precision=2))
                
            # with cols[0]:
            #     st.metric(label="Poultry heads", value=f"{millify(new_poultry_heads, precision=2)}",
            #             delta=millify(new_poultry_heads - baseline_poultry_heads, precision=2))
            # with cols[1]:
            #     st.metric(label="Pig heads", value=f"{millify(new_pig_heads, precision=2)}",
            #             delta=millify(new_pig_heads - baseline_pig_heads, precision=2))
            # with cols[2]:
            #     st.metric(label="Sheep flock", value=f"{millify(new_sheep_flock, precision=2)}",
            #             delta=millify(new_sheep_flock - baseline_sheep_flock, precision=2))


    with col_comp_3:
        
        # Land use
        with st.container(height=850, border=True):

            total_pasture = datablock["metrics"]["total_pasture"]
            total_forest = datablock["metrics"]["total_forest"]
            total_arable = datablock["metrics"]["total_arable"]
            baseline_pasture = datablock["metrics"]["baseline_pasture"]
            baseline_forest = datablock["metrics"]["baseline_forest"]
            baseline_arable = datablock["metrics"]["baseline_arable"]
            pctg = datablock["land"]["percentage_land_use"]

            st.markdown('''**Land use**''')

            f, plot1 = plt.subplots(1, figsize=(6, 6))
            f.patch.set_facecolor(background_color)
            LC_toplot = map_max(pctg, dim="aggregate_class")

            color_list = [land_color_dict[key] for key in pctg.aggregate_class.values]
            label_list = [land_label_dict[key] for key in pctg.aggregate_class.values]

            unique_index = np.unique(label_list, return_index=True)[1]

            cmap_tar = colors.ListedColormap(color_list)
            cmap_tar.set_bad(background_color)
            bounds_tar = np.linspace(-0.5, len(color_list)-0.5, len(color_list)+1)
            norm_tar = colors.BoundaryNorm(bounds_tar, cmap_tar.N)

            plot1.imshow(LC_toplot, interpolation="none", origin="lower",
                            cmap=cmap_tar, norm=norm_tar)
            patches = [mpatches.Patch(color=color_list[i],
                                        label=label_list[i]) for i in unique_index]

            plot1.axis("off")
            plot1.set_xlim(left=-100)
            plot1.set_ylim(top=1000)

            totals = pctg.sum(dim=["x", "y"])
            bar_land_use = plot_single_bar_altair(totals, show="aggregate_class",
                axis_title="Land use [ha]", unit="Hectares", vertical=False,
                color=land_color_dict, ax_ticks=True, bar_width=100)
            
            st.pyplot(f)
            st.altair_chart(bar_land_use, use_container_width=True)

            cols_metrics_land = st.columns(3)
            with cols_metrics_land[0]:

                st.metric(label="Pasture area", value=f"{millify(total_pasture, precision=2)} ha",
                        delta=f"{millify(total_pasture-baseline_pasture, precision=2)} ha")
                
            with cols_metrics_land[1]:

                st.metric(label="Forested area", value=f"{millify(total_forest, precision=2)} ha",
                        delta=f"{millify(total_forest-baseline_forest, precision=2)} ha")

            with cols_metrics_land[2]:
                
                st.metric(label="Arable area", value=f"{millify(total_arable, precision=2)} ha",
                        delta=f"{millify(total_arable-baseline_arable, precision=2)} ha")                    

            # st.caption('''<div style="text-align: justify;">
            # The map above shows the distribution of land use types in the UK.
            # Land use types are associated with different processes,
            # including food production, forests and hybrid productive systems
            # such as silvoarable (trees mixed with crops) and silvopasture
            # (animals mixed with crops).
            # </div>''', unsafe_allow_html=True)

# plot_summary()