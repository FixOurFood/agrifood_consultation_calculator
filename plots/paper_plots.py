import streamlit as st
from utils.altair_plots import *
import matplotlib.pyplot as plt
from matplotlib import colors

from utils.consultation_utils import get_figure_captions

from streamlit_theme import st_theme

def paper_plots():

    datablock = st.session_state["datablock"]
    
    st.markdown("# Paper plots")
    if (st.button("Update figure captions")):
        get_figure_captions.clear()

    captions = get_figure_captions()
    figs = []

    # ---------
    # Figure 1
    # ---------
    # FAOSTAT plot 

    to_plot = datablock["food"]["g/cap/day"].sel(Year=2050).fillna(0)
    to_plot["Item_group"].values = np.array(to_plot["Item_group"].values, dtype=str)
    to_plot = to_plot.fbs.group_sum(coordinate="Item_group", new_name="Item")

    to_plot = to_plot.rename({"food": "Retail"})
    to_plot = to_plot.rename({"production": "Production"})
    to_plot = to_plot.rename({"imports": "Imports"})
    to_plot = to_plot.rename({"exports": "Exports"})
    to_plot = to_plot.rename({"stock": "Stock"})
    to_plot = to_plot.rename({"losses": "Losses"})
    to_plot = to_plot.rename({"processing": "Processing"})
    to_plot = to_plot.rename({"other": "Other"})
    to_plot = to_plot.rename({"feed": "Feed"})
    to_plot = to_plot.rename({"seed": "Seed"})

    f1 = plot_bars_altair(to_plot, show="Item", x_axis_title="g/cap/day")
    figs.append(f1)

    # ---------
    # Figure 2
    # ---------
    # Emissions balance as a function of time 

    from agrifoodpy.utils.scaling import logistic_scale

    removals = logistic_scale(
        y0=2020,
        y1=2020,
        y2=2035,
        y3=2050,
        c_init=-9,
        c_end=-52,
    )

    lu_sinks = logistic_scale(
        y0=2020,
        y1=2020,
        y2=2035,
        y3=2050,
        c_init=-17,
        c_end=-36,
    )

    lu_sources = logistic_scale(
        y0=2020,
        y1=2020,
        y2=2035,
        y3=2050,
        c_init=18.99,
        c_end=12.18,
    )

    balance = xr.Dataset({
        "Removals": removals,
        "LU Sinks": lu_sinks,
        "LU Sources": lu_sources,
    })

    balance_da = balance.to_dataarray(dim="Item")
    balance_da.name = "Emissions balance"

    f2 = plot_years_altair(
        balance_da,
        show="Item",
        ylabel="MtCO2e/year",
        ymin=-100,
        ymax=50,)

    figs.append(f2)


    # ---------
    # Figure 3
    # ---------
    # Land use plot

    theme = st_theme(key="paper_plots_theme")
    if theme is not None:
        background_color = theme["backgroundColor"]
    else:
        background_color = 'white'

    plt.rcParams['axes.facecolor'] = background_color

    from .land_use import map_max

    f3, axs = plt.subplots(1)
    f3.patch.set_facecolor(background_color)
    axs.set_facecolor(background_color)
    pctg = datablock["land"]["percentage_land_use"]
    LC_toplot = map_max(pctg, dim="aggregate_class")

    color_list = [land_color_dict[key] for key in pctg.aggregate_class.values]
    label_list = [land_label_dict[key] for key in pctg.aggregate_class.values]

    unique_index = np.unique(label_list, return_index=True)[1]

    cmap_tar = colors.ListedColormap(color_list)
    cmap_tar.set_bad(background_color)
    bounds_tar = np.linspace(-0.5, len(color_list)-0.5, len(color_list)+1)
    norm_tar = colors.BoundaryNorm(bounds_tar, cmap_tar.N)

    axs.imshow(LC_toplot, interpolation="none", origin="lower",
                    cmap=cmap_tar, norm=norm_tar)

    axs.axis("off")
    axs.set_xlim(left=-100)
    axs.set_ylim(top=980)

    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    axins = inset_axes(axs, width=1.0, height=1.0)

    land_pctg = pctg.sum(dim=["x", "y"])

    land_labels = land_pctg.aggregate_class.values
    land_values = land_pctg.values

    axins.set_facecolor(background_color)
    axins.pie(land_values, colors=color_list, startangle=140)
    axins.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    figs.append(f3)

    # ---------
    # Figure 4
    # ---------
    # FAOSTAT plot weighted by kCal/cap/day

    to_plot = datablock["food"]["kCal/cap/day"].sel(Year=2050).fillna(0)
    to_plot["Item_group"].values = np.array(to_plot["Item_group"].values, dtype=str)
    to_plot = to_plot.fbs.group_sum(coordinate="Item_group", new_name="Item")

    to_plot = to_plot.rename({"food": "Retail"})
    to_plot = to_plot.rename({"production": "Production"})
    to_plot = to_plot.rename({"imports": "Imports"})
    to_plot = to_plot.rename({"exports": "Exports"})
    to_plot = to_plot.rename({"stock": "Stock"})
    to_plot = to_plot.rename({"losses": "Losses"})
    to_plot = to_plot.rename({"processing": "Processing"})
    to_plot = to_plot.rename({"other": "Other"})
    to_plot = to_plot.rename({"feed": "Feed"})
    to_plot = to_plot.rename({"seed": "Seed"})

    f4 = plot_bars_altair(to_plot, show="Item", x_axis_title="kCal/cap/day")
    figs.append(f4)

    # ---------
    # Figure 5
    # ---------
    # FAOSTAT plot weighted by gCO2e/cap/day 

    to_plot = datablock["food"]["g_co2e/cap/day"].sel(Year=2050).fillna(0)
    to_plot["Item_group"].values = np.array(to_plot["Item_group"].values, dtype=str)
    to_plot = to_plot.fbs.group_sum(coordinate="Item_group", new_name="Item")

    to_plot = to_plot.rename({"food": "Retail"})
    to_plot = to_plot.rename({"production": "Production"})
    to_plot = to_plot.rename({"imports": "Imports"})
    to_plot = to_plot.rename({"exports": "Exports"})
    to_plot = to_plot.rename({"stock": "Stock"})
    to_plot = to_plot.rename({"losses": "Losses"})
    to_plot = to_plot.rename({"processing": "Processing"})
    to_plot = to_plot.rename({"other": "Other"})
    to_plot = to_plot.rename({"feed": "Feed"})
    to_plot = to_plot.rename({"seed": "Seed"})

    f5 = plot_bars_altair(to_plot, show="Item", x_axis_title="g_co2e/cap/day")
    figs.append(f5)

    # ---------
    # Figure 6
    # ---------
    # Scenarios contribution to net zero

    pctgs = xr.load_dataset("plots/data/attribution_results_ds.nc")
    print(pctgs)

    pctgs = 70.16 - pctgs

    scenarios = [
    "AFN+ - (a) Build Back Fast Again",
    "AFN+ - (b) Circular Worlds",
    "AFN+ - (c) Self- sufficiency for Security",
    "AFN+ - (d) The Right to Food",
    "CB7"
    ]


    f6 = plot_bars_altair2(
        pctgs,
        data_vars=scenarios,
        reversed_vars=[],
        show="Item",
        x_axis_title="Emissions reduction (MtCO2e/year)",
        stacked=False,
        horizontal=False,
    )

    figs.append(f6)

    # ---------
    # Figure 7
    # ---------
    # UK as farm

    figs.append("images/CB7_small.jpg")

    # --------------------
    # Place figures in app
    # --------------------
    
    cols = st.columns((1,3,1))

    while len(figs) < len(captions):
        figs.append(None)
    with cols[1]:
        for fig_id, (f, capt) in enumerate(zip(figs, captions)):
            with st.expander(f"Figure {fig_id+1}"):
                if f is None:
                    st.write("In preparation")
                elif isinstance(f, str):
                    st.image(f)
                elif isinstance(f, plt.Figure):
                    st.pyplot(f, use_container_width=True)
                else:
                    st.altair_chart(f, use_container_width=True)
                st.caption(capt)

# paper_plots()