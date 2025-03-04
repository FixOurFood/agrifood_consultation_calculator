import streamlit as st

# ------------------------------------------------------------------------------
#                                Consumer demand
# ------------------------------------------------------------------------------
@st.dialog("Reduce ruminant meat consumption", width="small")
def ruminant_help():
    st.markdown('''
        Meat production produces significantly higher greenhouse gas (GHG)
        emissions compared to other types of food. Ruminant meat, such as beef,
        goat and sheep, can produce 3 to 10 times more emissions than other meats
        (Poore & Nemecek 2018).

        This slider lets you reduce how much ruminant meat each person eats each day
        and replaces it with cereals, keeping the total calories the same.
        A value above 0 means some reduction in meat consumption,
        with 100% meaning no ruminant meat at all.''')

@st.dialog("Reduce dairy consumption", width="small")
def dairy_help():
    st.markdown("""
        Animal products, including dairy, produce significantly more greenhouse gas
        emissions than plant-based foods.  \n

        This slider lets you reduce the amount of dairy (milk, butter and cream) a
        person consumes each day. The dairy removed is replaced with alternative foods,
        keeping the total calorie intake the same. A value above 0 means some reduction
        in dairy consumption, with 100% meaning no dairy products at all.""")


@st.dialog("Reduce pig meat, poultry and eggs consumption", width="small")
def pig_pultry_eggs_help():
    st.markdown("""
        Animal products, including pork, poultry and eggs, produce significantly more
        greenhouse gas emissions than plant-based foods.  \n
                        
        This slider lets you reduce the amount of pork, poultry and eggs a person
        consumes each day. The animal products removed are replaced with alternative
        foods, keeping the total calorie intake the same. A value above 0 means some
        reduction in pork, poultry and eggs, with 100% meaning no consumption of these
        products at all.""")

@st.dialog("Increase fruit and vegetable consumption", width="small")
def fruits_veg_help():
    st.markdown("""
        Consumption of fruit and vegetables is currently below the recommended guidelines.  \n

        This slider lets you increase the quantities of fruit and vegetables eaten per
        person per day.  \n

        A value above 0 means some increase in fruit and vegetable consumption,
        with 100% meaning that each person is eating double the amount of fruit and
        vegetables.""")
    
@st.dialog("Increase fruit and vegetable consumption", width="small")
def pulses_help():
    st.markdown("""
        Pulses can be a good replacement for animal proteins, while having a
        smaller land and GHG footprint. \n

        This slider lets you increase the quantities of pulses eaten per
        person per day.  \n

        A value above 0 means some increase in pulses consumption,
        with 100% meaning that each person is eating double the amount of pulses.""")
    
@st.dialog("Food waste and overeating reduction", width="small")
def waste_help():
    st.markdown("""
        Globally, one third of food is lost or wasted, and overeating adds to this
        waste, by consuming more food than necessary. Currently the average daily
        calorie intake is above 3,300kcal, compared to the recommended level is
        2,250kcal.  \n
                        
        This slider allows you to reduce waste, including excess calories from
        overeating, as a percentage of total intake. A value above 0 indicates a
        reduction, with 100% meaning that calorie intake per person is lowered to the
        recommended 2,250kcal.""")
    
@st.dialog("Alternative products", width="small")
def alternative_products_help():
    st.markdown("""
        Producing beef produces significantly higher greenhouse gas (GHG) emissions than
        other foods. Replacing beef with alternatives that typically come from plants,
        helps reduce emissions from land use and animal processing. These alternative
        products include plant based food such as Quorn, vegetarian sausages, soy meat,
        as well as lab-grown (cultured) meat made from animal cells and grown in
        controlled environments. \n

        This slider allows you to replace beef in your diet with alternative meat
        products. A value of 0% means no change, while 100% means all beef is replaced.
        The model assumes that nutritional values remain the same.""")

# ------------------------------------------------------------------------------
#                           Land use change
# ------------------------------------------------------------------------------

@st.dialog("Percentage of arable land used for BECCS crops", width="small")
def beccs_help():
    pass

@st.dialog("Forested spared land fraction", width="small")
def afforestation_help():
    pass

@st.dialog("Upland and low peat restoration", width="small")
def peatland_restoration_help():
    pass

@st.dialog("Improved land management for increased sequestration", width="small")
def soil_management_help():
    pass

@st.dialog("Improved land management for increased sequestration", width="small")
def mixed_farming_help():
    pass

# ------------------------------------------------------------------------------
#                          Livestock farming
# ------------------------------------------------------------------------------

@st.dialog("Farmland % converted to Silvopasture", width="small")
def silvopasture_help():
    pass

@st.dialog("Methane inhibitor use in livestock feed", width="small")
def methane_inhibitor_help():
    pass

@st.dialog("Manure management in livestock farming", width="small")
def manure_management_help():
    pass

@st.dialog("Manure management in livestock farming", width="small")
def breeding_help():
    pass

@st.dialog("Reducing fossil fuel use in livestock farming", width="small")
def fossil_livestock_help():
    pass

# ------------------------------------------------------------------------------
#                            Arable farming
# ------------------------------------------------------------------------------

@st.dialog("Farmland % converted to Agroforestry", width="small")
def agroforestry_help():
    pass

@st.dialog("Low Carbon Technology on Farm", width="small")
def fossil_arable_help():
    pass

@st.dialog("Urban agriculture and vertical farming", width="small")
def urban_help():
    pass

# ------------------------------------------------------------------------------
#                          Techonology and innovation
# ------------------------------------------------------------------------------

@st.dialog("BECCS sequestration from waste", width="small")
def beccs_waste_help():
    pass

@st.dialog("BECCS sequestration from overseas biomass", width="small")
def beccs_overseas_help():
    pass

@st.dialog("DACCS sequestration", width="small")
def daccs_help():
    pass


# ------------------------------------------------------------------------------
#                                Projection baseline
# ------------------------------------------------------------------------------

@st.dialog("Population projection", width="small")
def population_help():
    st.markdown("""
                The population projection describes the expected population
                growth rate until 2050. The options presented here correspond
                to the UN's population prospects models, which are modelled 
                assumming various rates of fertility, mortality, and migration.

                For further details, [see the World Population Prospects 2024 report](https://population.un.org/wpp/assets/Files/WPP2024_Methodology.pdf).
                """)

@st.dialog("Crop yields", width="small")
def crop_yields_help():
    st.markdown("""
                The crop yield projection describes the expected change in crop
                yields until 2050. The values presented here describe a linear change  
                in yield over the 2025-2050 period, which can be caused by a
                variety of factors, including climate, technological improvements,
                and changes in agricultural practices.

                4 scenarios are available, which match the crop yield assumptions from
                the 6th Carbon Budget:
                - **Baseline**: The baseline scenario assumes no change in crop yields,
                staying constant at around 8.2 of wheat tonnes per hectare.
                - **Climate sensitivity**: Climate risks dominate future yield,
                resulting in a reduction of 27% in crop yields.
                - **Medium**: Assumes a 34% increase in crop yields, to 11 tonnes per hectare.
                Primarily driven by the increased CO2 fertilization effect, longer growing seasons,
                and improved agricultural practices.
                - **High**: Assumes a 58% increase in crop yields, to 13 tonnes of wheat per hectare.
                Driven  by the increased CO2 fertilization effect, longer growing seasons,
                and improved agricultural practices, as well as reduced risks from climate change.
                """)

@st.dialog("Trade elasticity", width="small")
def trade_help():
    st.markdown("""
                The trade model projection describes how the changes  
                in domestic use of agricultural products are supplied  
                from production and imports, with changes being fully  
                supplied from imports, from production, or from a  
                combination of both.
                """)