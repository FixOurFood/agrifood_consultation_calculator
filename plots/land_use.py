import streamlit as st
from utils.altair_plots import *
import matplotlib.pyplot as plt
from matplotlib import colors

def map_max(map, dim):
    """function to return the coordinate index of the maximum value along a
    dimension"""

    length_dim = len(map[dim].values)
    map_fixed = map.assign_coords({dim:np.arange(length_dim)})

    return map_fixed.idxmax(dim=dim, skipna=True)    

def plot_land_use(datablock, background_color):
    f, plot1 = plt.subplots(1, figsize=(8,8))
    f.patch.set_facecolor(background_color)
    plot1.set_facecolor(background_color)
    pctg = datablock["land"]["percentage_land_use"]
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
        with st.container(border=True, height=450):
            land_pctg = pctg.sum(dim=["x", "y"])
            pie = pie_chart_altair(land_pctg, show="aggregate_class", unit="ha")
            st.altair_chart(pie)

        total_area = land_pctg.sum().values
        baseline_forest_fraction = 100*datablock["land"]["baseline"].sel(aggregate_class=["Broadleaf woodland", "Coniferous woodland"]).sum().values/total_area
        forest_fraction = 100*land_pctg.sel(aggregate_class=["Broadleaf woodland", "Coniferous woodland"]).sum().values/total_area
        mixed_farming_fraction = land_pctg.sel(aggregate_class="Mixed farming").sum().values/total_area

        st.metric("Forested % of UK land", value=f"{forest_fraction:.2f}% ", delta=f"{forest_fraction-baseline_forest_fraction:.2f}%")
        st.metric("Mixed farming % of UK land", value=f"{100*mixed_farming_fraction:.2f}% ")

    