import streamlit as st
import matplotlib.pyplot as plt
from utils.glossary import *
from utils.helper_functions import *
from streamlit_theme import st_theme

@st.fragment()
def plots(datablock):

    theme = st_theme()
    if theme is not None:
        background_color = theme["backgroundColor"]
    else:
        background_color = 'white'

    plt.rcParams['axes.facecolor'] = background_color

    # ----------------------------------------    
    #                  Plots
    # ----------------------------------------

    # if not st.session_state["embedding"] and plot_key=="Summary":
    #     with st.expander("**Future Food Calculator - The UK in 2050**", expanded=True):
    #         st.write("""Click on an aspect of the food system you would like to change - on
    #                 the left side of the page. Move the sliders to explore how different
    #                 interventions in the food system impact the UK emissions balance,
    #                 self-sufficiency, and land use. Alternatively, select a scenario
    #                 from the dropdown menu on the top of the sidebar to automatically
    #                 position sliders to pre-set values. Detailed charts describing the
    #                 effects of interventions on different aspects of the food system
    #                 can be found in the dropdown menu at the bottom of the page.""")
    #         st.write("""Challenge: can you move the sliders to get the UK to net zero
    #                 (diamond is at zero)? Are you happy with this solution? If so, submit
    #                 your proposed solution at the bottom of this page!
    #                 """)

    st.session_state["background_color"] = background_color
    st.session_state["datablock"] = datablock

    from .uk_as_farm import plot_uk_as_farm
    from .summary import plot_summary
    from .annual_quantities import plot_annual_quantities
    from .per_capita import plot_per_capita
    from .land_use import plot_land_use
    from .self_sufficiency import plot_self_sufficiency
    # from .paper_plots import paper_plots

    # pages = [
    #     st.Page("plots/summary.py", title="Summary"),
    #     st.Page("plots/annual_quantities.py", title="Annual quantities"),
    #     st.Page("plots/per_capita.py", title="Per capita daily values"),
    #     st.Page("plots/self_sufficiency.py", title="Self-sufficiency ratio"),
    #     st.Page("plots/land_use.py", title="Land"),
    #     st.Page("plots/uk_as_farm.py", title="UK as farm")
    # ]

    # if st.secrets["branch"] == "sarah_jp_hack":
    #     pages.append(st.Page("plots/paper_plots.py", title="Paper plots"))

    # pg = st.navigation(
    #     [
    #         *pages
    #     ],
    #     position="top",
    # )

    # pg.run()

    plot_key = st.segmented_control("Choose from the options below to explore a more detailed breakdown of your selected pathway", option_list, default="Summary")

    # UK as farm
    if plot_key == 'UK as farm':
        plot_uk_as_farm()

    # Summary
    if plot_key == "Summary":
        plot_summary()        

    # Emissions per food group or origin
    if plot_key == "Annual quantities":
        plot_annual_quantities()

    # FAOSTAT bar plot with per-capita daily values
    elif plot_key == "Per capita values":
        plot_per_capita()        
        
    # Self-sufficiency ratio as a function of time
    elif plot_key == "Self-sufficiency ratio":
        plot_self_sufficiency()

    # Various land plots, including Land use and ALC
    elif plot_key == "Land":
        plot_land_use()

    # elif plot_key == "Paper plots":
    #     paper_plots()
