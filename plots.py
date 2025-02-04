import streamlit as st
from streamlit_extras.bottom_container import bottom
from streamlit_extras.add_vertical_space import add_vertical_space
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.patches as mpatches
from utils.altair_plots import *
from agrifoodpy.food.food import FoodBalanceSheet
from glossary import *
from utils.helper_functions import *
from consultation_utils import submit_scenario, get_user_list, stage_I_deadline

@st.fragment()
def plots(datablock):
    reference_emissions_baseline = 97.09
    reference_emissions_baseline_agriculture = 52.08

    # ----------------------------------------    
    #                  Plots
    # ----------------------------------------

    # Summary
    # -------
    metric_yr = 2050
    plot_key = st.session_state["plot_key"]

    if plot_key == "Summary":

        st.markdown("# Agrifood Calculator - The UK in 2050")
        st.write("""Click on an aspect of the food system you would like to change - on
                the left side of the page. Move the sliders to explore how different
                interventions in the food system impact the UK emissions balance,
                self-sufficiency, and land use. Alternatively, select a scenario
                from the dropdown menu on the top of the sidebar to automatically
                position sliders to pre-set values. Detailed charts describing the
                effects of interventions on different aspects of the food system
                can be found in the dropdown menu at the bottom of the page.""")
        st.write("""Challenge: can you move the sliders to get the UK to net zero
                (diamond is at zero)? Are you happy with this solution? If so, submit
                your proposed solution at the bottom of this page!
                """)
                
        col_comp_1, col_comp_2, col_comp_3 = st.columns([1,1,1])

        # Emissions and removals balance
        with col_comp_1:

            with st.container(height=800, border=True):
                
                st.markdown('''**UK Emissions balance**''')
                if st.session_state.emission_factors == "NDC 2020":
                    
                    seq_da = datablock["impact"]["co2e_sequestration"].sel(Year=metric_yr)
                    emissions = datablock["impact"]["g_co2e/year"]["production"].sel(Year=metric_yr)/1e6
                    total_emissions = emissions.sum(dim="Item").values/1e6
                    total_seq = seq_da.sel(Item=["Broadleaf woodland",
                                                 "Coniferous woodland",
                                                 "Peatland",
                                                 "Managed pasture",
                                                 "Managed arable",
                                                 "Mixed farming",
                                                 "Silvopasture",
                                                 "Agroforestry"]).sum(dim="Item").values/1e6
                    total_removals = seq_da.sel(Item=["BECCS from waste", "BECCS from overseas biomass", "BECCS from land", "DACCS"]).sum(dim="Item").values/1e6

                    emissions_balance = xr.DataArray(data = list(sector_emissions_dict.values()),
                                          name="Sectoral emissions",
                                          coords={"Sector": list(sector_emissions_dict.keys())})
                    
                    emissions_balance.loc[{"Sector": "Agriculture"}] = total_emissions
                    emissions_balance.loc[{"Sector": "Land use sinks"}] = -total_seq
                    emissions_balance.loc[{"Sector": "Removals"}] = -total_removals
                    
                    if st.session_state["show_afolu_only"]:
                        reference_emissions_baseline = 31.61
                        emissions_balance = emissions_balance.sel(Sector=["Agriculture", "Land use sinks", "Removals"])

                    c = plot_single_bar_altair(emissions_balance, show="Sector", color=sector_emissions_colors,
                        axis_title="Mt CO2e / year", unit="Mt CO2e / year", vertical=True,
                        mark_total=True, show_zero=True, ax_ticks=True, legend=True,
                        ax_min=-90, ax_max=120, reference=reference_emissions_baseline)
                    
                elif st.session_state.emission_factors == "PN18":

                    emissions = datablock["impact"]["g_co2e/year"]["production"].sel(Year=metric_yr)/1e6
                    emissions = emissions.fbs.group_sum(coordinate="Item_origin", new_name="Item")
                    seq_da = datablock["impact"]["co2e_sequestration"].sel(Year=metric_yr)

                    emissions_balance = xr.concat([emissions/1e6, -seq_da/1e6], dim="Item")
                    
                    c = plot_single_bar_altair(emissions_balance, show="Item",
                                                    axis_title="Sequestration / Production emissions [M tCO2e]",
                                                    ax_min=-3e2, ax_max=3e2, unit="M tCO2e", vertical=True,
                                                    mark_total=True, show_zero=True, ax_ticks=True)
                    
                c = c.properties(height=500)
                st.altair_chart(c, use_container_width=True)
                st.checkbox("Show agriculture and land use only", value=False, on_change=change_to_afolu_only, key="show_afolu_only_checkbox")
                st.markdown(f"Total emissions: **{emissions_balance.sum().to_numpy():.2f} Mt CO2e / year**")
                st.caption('''<div style="text-align: justify;">
                           The diagram above visualises the balance between total
                           emissions produced in the UK, and carbon storage.
                           The red diamond shows the net balance, the red dot is
                           at zero and your goal is to move the sliders to get
                           them to line up.</div>''', unsafe_allow_html=True)
                st.write("\n")
                st.caption('''<div style="text-align: justify;">
                           It assumes other (non agrifood) sectors reduce their
                           emissions according to the CCC balanced pathway.
                           The black line shows the situation in 2050 if the
                           agrifood system stays the same as it is today. 
                           </div>''', unsafe_allow_html=True)

        # Self-sufficiency ratio
        with col_comp_2:
            with st.container(height=800, border=True):

                st.markdown('''**Self-sufficiency**''')

                ssr_metric = st.session_state["ssr_metric"]
                gcapday = datablock["food"][ssr_metric].sel(Year=metric_yr).fillna(0)
                gcapday = gcapday.fbs.group_sum(coordinate="Item_origin", new_name="Item")
                gcapday_ref = datablock["food"][ssr_metric].sel(Year=2020).fillna(0)
                gcapday_ref = gcapday_ref.fbs.group_sum(coordinate="Item_origin", new_name="Item")

                SSR_ref = gcapday_ref.fbs.SSR()
                SSR_metric_yr = gcapday.fbs.SSR()

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


                st.altair_chart(production_bar, use_container_width=True)
                st.altair_chart(imports_bar, use_container_width=True)

                st.selectbox("Select metric", ["g/cap/day",
                                               "g_prot/cap/day",
                                               "g_fat/cap/day",
                                               "g_co2e/cap/day",
                                               "kCal/cap/day",],
                                               key="update_ssr_metric",
                                               on_change=update_SSR_metric)

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
                st.caption('''<div style="text-align: justify;">
                This panel calculates how much the UK relies on food imports, by
                comparing the amount we produce in the UK to the amount we use.
                The UK currently produces 73% of what it uses, and a lower value
                would mean we depend more on imports.</div>''', unsafe_allow_html=True)
                st.write("\n")
                st.caption('''<div style="text-align: justify;">
                This percentage can be calculated by weight (tonnes produced /
                tonnes used) or other metrics e.g. kcal produced / kcal used or
                nutrients such as protein.
                </div>''', unsafe_allow_html=True)
               
        # Land use
        with col_comp_3:
            with st.container(height=800, border=True):

                st.markdown('''**Land use**''')


                f, plot1 = plt.subplots(1, figsize=(6, 6))
                pctg = datablock["land"]["percentage_land_use"]
                LC_toplot = map_max(pctg, dim="aggregate_class")

                color_list = [land_color_dict[key] for key in pctg.aggregate_class.values]
                label_list = [land_label_dict[key] for key in pctg.aggregate_class.values]

                unique_index = np.unique(label_list, return_index=True)[1]

                cmap_tar = colors.ListedColormap(color_list)
                bounds_tar = np.linspace(-0.5, len(color_list)-0.5, len(color_list)+1)
                norm_tar = colors.BoundaryNorm(bounds_tar, cmap_tar.N)

                plot1.imshow(LC_toplot, interpolation="none", origin="lower",
                                cmap=cmap_tar, norm=norm_tar)
                patches = [mpatches.Patch(color=color_list[i],
                                            label=label_list[i]) for i in unique_index]

                plot1.axis("off")
                plot1.set_xlim(left=-100)
                plot1.set_ylim(top=1000)

                _, col_plot, _ = st.columns((0.1, 0.7, 0.1))
                with col_plot:
                    st.pyplot(f)

                pctg = datablock["land"]["percentage_land_use"]
                totals = pctg.sum(dim=["x", "y"])
                bar_land_use = plot_single_bar_altair(totals, show="aggregate_class",
                    axis_title="Land use [ha]", unit="Hectares", vertical=False,
                    color=land_color_dict, ax_ticks=True, bar_width=100)
                
                st.altair_chart(bar_land_use, use_container_width=True)

                st.caption('''<div style="text-align: justify;">
                The map above shows the distribution of land use types in the UK.
                Land use types are associated with different processes,
                including food production, forests and hybrid productive systems
                such as silvoarable (trees mixed with crops) and silvopasture
                (animals mixed with crops).
                </div>''', unsafe_allow_html=True)

    # Emissions per food group or origin
    # ----------------------------------
    if plot_key == "CO2e emission per food group":
        col_opt, col_element, col_y = st.columns([1,1,1])
        with col_opt:
            option_key = st.selectbox("Plot options", ["Food group", "Food origin"])
        with col_element:
            element_key = st.selectbox("Food Supply Element", ["production", "food", "imports", "exports", "feed"])
        with col_y:
            y_key = st.selectbox("Quantity", ["Emissions", "kCal/cap/day", "g/cap/day"])

        if y_key == "Emissions":
            emissions = datablock["impact"]["g_co2e/year"].sel(Year=slice(None, metric_yr))
            seq_da = datablock["impact"]["co2e_sequestration"].sel(Year=slice(None, metric_yr))

            if option_key == "Food origin":
                f = plot_years_altair(emissions[element_key]/1e6, show="Item_origin", ylabel="t CO2e / Year")

            elif option_key == "Food group":
                f = plot_years_altair(emissions[element_key]/1e6, show="Item_group", ylabel="t CO2e / Year")

            if element_key == "production":
                # Plot sequestration
                f += plot_years_altair(-seq_da, show="Item", ylabel="t CO2e / Year")
                emissions_sum = emissions[element_key].sum(dim="Item")
                seqestration_sum = seq_da.sum(dim="Item")

                f += plot_years_total((emissions_sum/1e6 - seqestration_sum),
                                    ylabel="t CO2e / Year",
                                    color="black")
        else:
            emissions = datablock["food"][y_key].sel(Year=slice(None, metric_yr))

            if option_key == "Food origin":
                f = plot_years_altair(emissions[element_key], show="Item_origin", ylabel=y_key)

            elif option_key == "Food group":
                f = plot_years_altair(emissions[element_key], show="Item_group", ylabel=y_key)

        f=f.configure_axis(
            labelFontSize=15,
            titleFontSize=15)
        
        st.altair_chart(f, use_container_width=True)

    # Emissions per food item from each group
    # ---------------------------------------
    elif plot_key == "CO2e emission per food item":
        col_opt, col_element, col_y = st.columns(3)
        with col_opt:
            option_key = st.selectbox("Plot options", np.unique(datablock["impact"]["g_co2e/year"].Item_group.values))
        with col_element:
            element_key = st.selectbox("Food Supply Element", ["production", "food", "imports", "exports", "feed"])
        with col_y:
            y_key = st.selectbox("Quantity", ["Emissions", "kCal/cap/day", "g/cap/day"])

        if y_key == "Emissions":
            to_plot = datablock["impact"]["g_co2e/year"].sel(Year=slice(None, metric_yr))
            to_plot = to_plot[element_key].sel(Item=to_plot["Item_group"] == option_key)/1e6

        else:
            to_plot = datablock["food"][y_key].sel(Year=slice(None, metric_yr))
            to_plot = to_plot[element_key].sel(Item=to_plot["Item_group"] == option_key)
        
        f = plot_years_altair(to_plot, show="Item_group", ylabel="t CO2e / Year")
        f = f.configure_axis(
                labelFontSize=15,
                titleFontSize=15)
            
        st.altair_chart(f, use_container_width=True)

    # FAOSTAT bar plot with per-capita daily values
    # ---------------------------------------------
    elif plot_key == "Per capita daily values":
        per_cap_options = {"g/cap/day": 5000,
                   "g_prot/cap/day": 250,
                   "g_fat/cap/day": 275,
                   "g_co2e/cap/day": 9000,
                   "kCal/cap/day": 7000}
        col_cap1, col_cap2, col_cap3 = st.columns(3)
        with col_cap1:
            option_key = st.selectbox("Plot options", list(per_cap_options.keys()))
        with col_cap2:
            dissagregation = st.selectbox("Disaggregation", ["Item_origin", "Item_group", "Item_name"])
        with col_cap3:
            item_list = st.multiselect("Item", np.unique(datablock["food"][option_key][dissagregation].values))
        item_selection = {}
        if len(item_list) > 0:
            item_selection = {"Item":item_list}
        adjust_scale = st.checkbox("Adjust scale", value=True)

        to_plot = datablock["food"][option_key].sel(Year=metric_yr).fillna(0)
        to_plot[dissagregation].values = np.array(to_plot[dissagregation].values, dtype=str)
        to_plot = to_plot.fbs.group_sum(coordinate=dissagregation, new_name="Item")
        to_plot = to_plot.sel(item_selection)

        if adjust_scale:
            f = plot_bars_altair(to_plot, show="Item", x_axis_title=option_key, xlimit=per_cap_options[option_key])
        else:
            f = plot_bars_altair(to_plot, show="Item", x_axis_title=option_key)

        if option_key == "kCal/cap/day":
            f += alt.Chart(pd.DataFrame({
            'Energy': [datablock["food"]["rda_kcal"]],
            'color': ['red']
            })).mark_rule().encode(
            x='Energy:Q',
            color=alt.Color('color:N', scale=None)
            )

        st.altair_chart(f, use_container_width=True)
        
    # Self-sufficiency ratio as a function of time
    # --------------------------------------------
    elif plot_key == "Self-sufficiency ratio":

        col1_ssr, col2_ssr, col3_ssr = st.columns([1,2,1])

        # Inputs
        with col3_ssr:
            ssr_metric = st.selectbox("Metric", ["g/cap/day", "kCal/cap/day", "g_prot/cap/day", "g_fat/cap/day"])
            dissagregation = st.selectbox("Disaggregation", ["Item_name", "Item_group", "Item_origin"])
            item_selection = {}
            item_list = st.multiselect("Food item", np.unique(datablock["food"][ssr_metric][dissagregation].values))
            if len(item_list) > 0:
                item_selection = {"Item":item_list}

            # Build fbs for plotting
            fbs = datablock["food"][ssr_metric].sel(Year=metric_yr).fillna(0)
            fbs = fbs.fbs.group_sum(coordinate=dissagregation, new_name="Item")
            fbs = fbs.sel(item_selection)
            SSR_metric_yr = fbs.fbs.SSR()
            SSR = datablock["food"][ssr_metric].fillna(0).fbs.SSR().sel(Year=slice(None, metric_yr)) * 100

            with st.container(border=True):
                st.metric("Self-sufficiency for your selection",
                        value="{:.2f} %".format(100*fbs.fbs.SSR()))


        with col1_ssr:
            st.markdown("""# Self-sufficiency""")
            st.markdown("""<div style="text-align: justify;">
                        The self-sufficiency ratio (SSR) is a measure of the proportion of a
                        country's food production that is consumed domestically. It is calculated
                        as the ratio of production to domestic consumption.
                        A higher SSR indicates that a country is more self-sufficient in food
                        production, while a lower SSR indicates that a country relies more on
                        imports to meet its food needs. </div>""", unsafe_allow_html=True)


        # plots
        with col2_ssr:
            
            f = plot_years_total(SSR, ylabel="Self-sufficiency ratio [%]", yrange=(40, 95)).configure_axis(
                labelFontSize=10,
                titleFontSize=15,
                labelAngle=-45,
                ).properties(height=300)        

            origin_color={"Animal Products": "red",
                        "Plant Products": "green",
                        "Alternative Food": "blue"}
        
            domestic_use = fbs["imports"]+fbs["production"]-fbs["exports"]
            domestic_use.name="domestic"
        
            production_bar = plot_single_bar_altair(fbs["production"],
                                                        show="Item",
                                                        vertical=False,
                                                        ax_ticks=True,
                                                        bar_width=100,
                                                        ax_min=0,
                                                        ax_max=np.max([fbs["production"].sum(), domestic_use.sum()]),
                                                        axis_title="Food production per capita",
                                                        unit=ssr_metric.replace("_"," "))

            imports_bar = plot_single_bar_altair(domestic_use,
                                                     show="Item",
                                                     vertical=False,
                                                     ax_ticks=True,
                                                     bar_width=100,
                                                     ax_min=0,
                                                     ax_max=np.max([fbs["production"].sum(), domestic_use.sum()]),
                                                     axis_title="Domestic use per capita",
                                                     unit=ssr_metric.replace("_"," "))
        

            with st.container(border=True):
                st.altair_chart(f, use_container_width=True)
            with st.container(border=True):
                st.altair_chart(production_bar, use_container_width=True)
                st.altair_chart(imports_bar, use_container_width=True)

    # Various land plots, including Land use and ALC
    # ----------------------------------------------
    elif plot_key == "Land":

        f, plot1 = plt.subplots(1, figsize=(8,8))
        pctg = datablock["land"]["percentage_land_use"]
        LC_toplot = map_max(pctg, dim="aggregate_class")

        color_list = [land_color_dict[key] for key in pctg.aggregate_class.values]
        label_list = [land_label_dict[key] for key in pctg.aggregate_class.values]

        unique_index = np.unique(label_list, return_index=True)[1]

        cmap_tar = colors.ListedColormap(color_list)
        bounds_tar = np.linspace(-0.5, len(color_list)-0.5, len(color_list)+1)
        norm_tar = colors.BoundaryNorm(bounds_tar, cmap_tar.N)

        plot1.imshow(LC_toplot, interpolation="none", origin="lower",
                        cmap=cmap_tar, norm=norm_tar)
        # patches = [mpatches.Patch(color=color_list[i],
                                    # label=label_list[i]) for i in unique_index]
        # plot1.legend(handles=patches, loc="upper left")

        plot1.axis("off")
        plot1.set_xlim(left=-100)
        plot1.set_ylim(top=980)

        col2_1, col2_2, col2_3 = st.columns((1,1.4,1))
        with col2_1:
            st.markdown("""# Land use""")
            st.markdown("""Land is fundamental for all human activities, including
                        food production. But it also plays a crucial role in the
                        dynamics of greenhouse gases in the atmosphere. Forests,
                        peatland and even agricultural soils are capable of storing
                        CO2, as long as we are able to find an adequate balance
                        between all land uses, are we are careful when using the soil
                        for food production.""")
        with col2_2:
            with st.container(border=True):
                st.pyplot(fig=f)
        with col2_3:
            with st.container(border=True):
                land_pctg = pctg.sum(dim=["x", "y"])
                pie = pie_chart_altair(land_pctg, show="aggregate_class", unit="ha")
                st.altair_chart(pie)

            total_area = land_pctg.sum().values
            baseline_forest_fraction = 100*datablock["land"]["baseline"].sel(aggregate_class=["Broadleaf woodland", "Coniferous woodland"]).sum().values/total_area
            forest_fraction = 100*land_pctg.sel(aggregate_class=["Broadleaf woodland", "Coniferous woodland"]).sum().values/total_area
            mixed_farming_fraction = land_pctg.sel(aggregate_class="Mixed farming").sum().values/total_area

            st.metric("Forested % of UK land", value=f"{forest_fraction:.2f}% ", delta=f"{forest_fraction-baseline_forest_fraction:.2f}%")
            st.metric("Mixed farming % of UK land", value=f"{100*mixed_farming_fraction:.2f}% ")
    
    st.selectbox("Choose from the options below to explore a more detailed breakdown of your selected pathway", option_list, on_change=update_plot_key, key="update_plot_key")

    if plot_key == "Summary":
        with st.container():
            st.markdown("""<div style="text-align: justify;">
            Once you have used the sliders to select your preferred levels of
            intervention, enter your email address in the field below and click
            the "Submit pathway" button. You can change your responses as many
            times as you want before the expert submission deadline on 26th
            March 2025.</div>""", unsafe_allow_html=True)

            col1_submit, col2_submit, col3_submit = st.columns(3)
                
            with col1_submit:
                submission_name = st.text_input("Enter the name of your submission", placeholder="Enter the name of your submission", label_visibility="hidden")
            with col2_submit:
                user_id = st.text_input("Enter your email", placeholder="Enter your email", label_visibility="hidden")
            with col3_submit:
                st.file_uploader("Optionally, add a narrative (PDF format) to go with your submission", accept_multiple_files=False)

            
            allow_to_public_database = st.checkbox("Allow your pathway to be publicly available in the submissions database", value=True)
            st.caption("""By clicking ‘Submit’ you are agreeing to our Data Protection Policy [Data Protection Policy](https://docs.google.com/document/d/1E24m5bvY2g-LbHpyN2Y44A_GzYtMmNUKRFJ_Wc-JTP0/edit?tab=t.0)""")
            submit_state = st.button("Submit")

            # submit scenario
            if submit_state:
                total_emissions = emissions_balance.sum()
                reducion_emissions_pctg = (total_emissions - reference_emissions_baseline) / reference_emissions_baseline * 100
                forest_land_ha = datablock["land"]["percentage_land_use"].sel(aggregate_class=["Broadleaf woodland", "Coniferous woodland"]).sum().values
                total_area = datablock["land"]["percentage_land_use"].sum().values
                new_forest_land_Mha = (forest_land_ha - datablock["land"]["baseline"].sel(aggregate_class=["Broadleaf woodland", "Coniferous woodland"]).sum().values)/1e6
                agricultural_emissions = emissions_balance.sel(Sector="Agriculture").sum().values
                reduction_emissions_agricultural_pctg = (agricultural_emissions - reference_emissions_baseline_agriculture) / reference_emissions_baseline_agriculture * 100

                arable_land = datablock["land"]["percentage_land_use"].sel(aggregate_class=["Arable", "Managed arable", "Mixed farming", "Agroforestry"]).sum().values / 1e6
                baseline_arable = datablock["land"]["baseline"].sel(aggregate_class=["Arable"]).sum().values / 1e6
                new_arable_land_pctg = (arable_land - baseline_arable) / baseline_arable * 100

                pasture_land = datablock["land"]["percentage_land_use"].sel(aggregate_class=["Improved grassland",
                                                                                             "Semi-natural grassland",
                                                                                             "Managed pasture",
                                                                                             "Silvopasture"]).sum().values / 1e6

                baseline_pasture = datablock["land"]["baseline"].sel(aggregate_class=["Improved grassland",
                                                                                      "Semi-natural grassland"]).sum().values / 1e6
                
                new_pasture_land_pctg = (pasture_land - baseline_pasture) / baseline_pasture * 100

                forest_sequestration_MtCO2 = seq_da.sel(Item=["Broadleaf woodland", "Coniferous woodland"]).sum(dim="Item").values/1e6
                total_removals = seq_da.sel(Item=["BECCS from waste", "BECCS from overseas biomass", "BECCS from land", "DACCS"]).sum(dim="Item").values/1e6

                extra_values = [SSR_metric_yr,
                                total_emissions,
                                reducion_emissions_pctg,
                                new_forest_land_Mha,
                                forest_sequestration_MtCO2,
                                reduction_emissions_agricultural_pctg,
                                agricultural_emissions,
                                total_removals,
                                arable_land,
                                new_arable_land_pctg,
                                pasture_land,
                                new_pasture_land_pctg,
                                ]

                submit_scenario(user_id, ambition_levels=True, check_users=st.session_state.check_ID, name=submission_name, extra_values=extra_values)

    if plot_key != "Summary":
        with bottom():
            from bottom import bottom_panel
            bottom_panel(datablock, metric_yr)


