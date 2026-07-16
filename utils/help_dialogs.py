import streamlit as st

def more_details_link(header):
    more_help_str = """ More details can be found in the [modelling document]""" + \
    f"""(https://docs.google.com/document/d/1A2J4BYIuXMgrj9tuLtIon8oJTuR1puK91bbUYCI8kHY/edit?tab=t.0#heading=h.{header})."""


    return more_help_str


# ------------------------------------------------------------------------------
#                                Consumer demand
# ------------------------------------------------------------------------------

@st.dialog("Reduce ruminant meat consumption", width="small")
def ruminant_help():
    st.markdown('''
                Meat production produces significantly higher greenhouse gas
                (GHG) emissions compared to other types of food. Ruminant meat,
                such as beef, goat and sheep, can produce 3 to 10 times more
                emissions than other meats [(Poore & Nemecek 2018)]\
                (https://www.science.org/doi/10.1126/science.aaq0216).

                This slider lets you reduce how much ruminant meat each person
                consumes each day. The meat removed is replaced with cereals,
                keeping the total calorie intake the same. A value below 0 means
                some reduction in ruminant meat consumption, with -100%
                meaning no ruminant meat at all.

                ''' + more_details_link("pjtbcox0lw1k"))

@st.dialog("Reduce dairy consumption", width="small")
def dairy_help():
    st.markdown("""
                Animal products, including dairy, produce significantly more
                greenhouse gas emissions (GHG) than plant-based foods 
                [(Poore & Nemecek 2018)](https://www.science.org/doi/10.1126/science.aaq0216).

                This slider lets you reduce the amount of dairy (milk, butter
                and cream) a person consumes each day. The dairy removed is
                replaced with cereals, keeping the total calorie
                intake the same. 
                A value below 0 means some reduction in dairy consumption, with
                -100% meaning no dairy products  at all

                """ + more_details_link("z0gjphyzstcl"))

@st.dialog("Reduce fish and seafood", width="small")
def fish_seafood_help():
    st.markdown("""
                Fish and seafood, while generally having a lower greenhouse gas
                footprint compared to other animal products, still contribute to
                environmental impacts, compared to plant-based foods.

                This slider lets you reduce the amount of fish and seafood a
                person consumes each day. The fish and seafood removed are
                replaced with alternative foods, keeping the total calorie
                intake the same.

                A value below 0 means some reduction in fish and seafood
                consumption, with -100% meaning no consumption of these products
                at all.

                """ + more_details_link("o0o7i5cuukc6"))

@st.dialog("Reduce eggs consumption", width="small")
def eggs_help():
    st.markdown("""
                Eggs, like other animal products, produce significantly more
                greenhouse gas emissions than plant-based foods.

                This slider lets you reduce the amount of eggs a person consumes
                each day. The eggs removed are replaced with alternative foods,
                keeping the total calorie intake the same.

                A value below 0 means some reduction in egg consumption, with
                -100% meaning no consumption of eggs at all.

                """ + more_details_link("6u16n1fg1w03"))

@st.dialog("Reduce pig meat and poultry", width="small")
def pig_poultry_help():
    st.markdown("""
                Other animal meat products, including pork and poultry, produce
                significantly more greenhouse gas emissions than plant-based
                foods.

                This slider lets you reduce the amount of pork and, poultry
                a person consumes each day. The animal products removed are
                replaced with alternative foods, keeping the total calorie
                intake the same. 

                A value below 0 means some reduction in pork and poultry,
                with -100% meaning no consumption of these products at all.

                """ + more_details_link("6u16n1fg1w03"))

@st.dialog("Increase fruit and vegetable consumption", width="small")
def fruits_veg_help():
    st.markdown("""
                Consumption of fruit and vegetables is currently below the
                recommended guidelines. 

                This slider lets you increase the quantities of fruit and
                vegetables eaten per person per day. 
                A value above 0 means some increase in fruit and vegetable
                consumption, with 100% meaning that each person is eating double
                the amount of fruit and vegetables.
                
                """ + more_details_link("qtof6gnbjli9"))
    
@st.dialog("Increase pulses consumption", width="small")
def pulses_help():
    st.markdown("""
                Pulses can be a good replacement for animal proteins, while
                having a smaller land and GHG footprint.

                This slider lets you increase the quantities of pulses eaten per
                person per day.

                A value above 0 means some increase in pulses consumption,
                with 100% meaning that each person is eating double the amount
                of pulses.
                
                """ + more_details_link("26acabtru2i"))
    
@st.dialog("Food waste and overeating reduction", width="small")
def waste_help():
    st.markdown("""
                Globally, one third of food is lost or wasted, and overeating
                adds to this waste, by consuming more food than needed.
                Currently the average daily calorie intake is above 3,300kcal
                (including wasted food), while the recommended intake is
                2,250kcal.

                This slider allows you to reduce food waste, including excess
                calories from overeating, as a percentage of total intake.

                A value above 0 indicates a reduction, with 100% meaning that
                calorie intake per person is lowered to the recommended
                2,250kcal per person.
                
                """ + more_details_link("jjk6fgg4t69m"))
    
@st.dialog("Alternative products", width="small")
def alternative_products_help():
    st.markdown("""
                Producing meat produces significantly higher greenhouse gas
                (GHG) emissions than other foods. Replacing animal products with
                alternatives that typically come from plants, helps reduce
                emissions from land use and animal processing. These alternative
                products include plant based food such as Quorn, vegetarian
                sausages, soy meat, as well as lab-grown (cultured) meat made
                from animal cells and grown in controlled environments.

                This slider allows you to replace meat in your diet with
                alternative meat products.

                A value above 0 means a reduction, with 100% meaning all meat is
                replaced. The model assumes that nutritional values remain the
                same.

                More detail can be found in the modelling document.
                
                """ + more_details_link("z0gjphyzstcl"))

# ------------------------------------------------------------------------------
#                           Land use change
# ------------------------------------------------------------------------------

@st.dialog("Forested spared land fraction", width="small")
def afforestation_help():
    st.markdown("""
                Taking pasture land out of production, creates more land
                available for activities that benefit carbon sequestration such
                as forestry or peatland restoration.

                This slider allows you to remove pasture land from food
                production and repurpose it for carbon sequestration.

                A value above 0 means some pasture land is taken out of
                production, with 100% meaning all pasture land is taken out of
                production.

                As pasture land for food production decreases, the model
                proportionally reduces production of animal-based products.
                To maintain balance in the food system, imports increase by the
                same amount as the reduction in domestic production.

                The model assumes that low and high quality land have the same
                productivity. It also assumes that all food production occurs on
                pasture land.

                """ + more_details_link("oqoktlcczgw8"))

@st.dialog("Percentage of arable land used for BECCS crops", width="small")
def beccs_help():
    st.markdown("""
                Species with deep root systems have a higher potential for
                carbon capture, helping to reduce the level of carbon dioxide in
                the atmosphere.Once saturated, these crops are renewed and
                either stored underground or repurposed in ways that do not 
                release carbon dioxide.

                This slider converts arable farm land into land available for
                carbon-capturing crops.

                However, this intervention may also have negative effects, such
                as reduced food availability and potential impacts on
                biodiversity.

                A value above 0 means some arable land is used for BECCS
                (bioenergy with carbon capture and storage) crops with 100%
                meaning all arable land is taken out of production.

                As the arable land for food production decreases, the model
                proportionally reduces production of plant-based products.
                To maintain balance in the food system, imports increase by the
                same amount as the reduction in domestic production.

                """ + more_details_link("hjx1wpsuoy8u"))

@st.dialog("Upland and low peat restoration", width="small")
def peatland_restoration_help():
    st.markdown("""
                Peatlands are one of the most effective ecosystems for capturing
                and storing carbon. They can store around twice as much carbon
                as forests and other biomes. Restoring peatland is crucial for
                ensuring that these naturally occurring carbon sinks are
                stabilised, and continue to capture and store carbon rather than
                releasing it into the atmosphere.

                This slider allows you to convert agricultural land back into
                peatland in areas that were historically peatland. In upland
                areas pastureland is converted, while in lowland areas, arable
                land is converted.

                A value of above 0 means some agricultural land is converted,
                with 100% meaning all agricultural land on peaty soil is
                converted back to peatland.
                
                """ + more_details_link("eln33eildo1k"))

@st.dialog("Improved land management for carbon sequestration", width="small")
def soil_management_help():
    st.markdown("""
                ‘Managed arable’ and ‘managed pasture’ systems, adopt techniques
                that benefit soil health and improve carbon sequestration.

                This slider allows you to shift  from traditional arable and
                pasture farming to ‘managed arable’ and ‘managed pasture’
                system, whilst maintaining the same level of food production.

                It relies on two key techniques, mob grazing and zero and min
                till.

                Mob grazing involves moving cows frequently, allowing pasture
                to rest and recover. This improves grass growth, strengthens
                roots and helps the soil hold more water and nutrients. Zero and
                min-till are techniques which reduce soil disturbance by
                avoiding ploughing, helping to keep nutrients in the soil and
                lowering the need for fertilisers.

                A value above 0 means some land shifts to improved land
                management, with 100% meaning all land is converted land managed
                for carbon sequestration.

                """ + more_details_link("3a92auci0xj5"))


@st.dialog("Mixed farming", width="small")
def mixed_farming_help():
    st.markdown("""
                Mixed farming systems combine livestock and crops on the same
                farm. These systems can include a variety of crops and animals,
                offering benefits such as improved soil health and increased
                carbon sequestration.

                This slider converts a portion of the arable land available into
                a mixed system, that produces both animal and plant based
                products.

                A value above 0 means some land is converted, with 100% meaning
                all arable land is converted to a mixed farming system.

                """ + more_details_link("7su0nj7wz5ct"))

# ------------------------------------------------------------------------------
#                          Livestock farming
# ------------------------------------------------------------------------------

@st.dialog("Farmland % converted to Silvopasture", width="small")
def silvopasture_help():
    st.markdown("""
                Silvopasture (grazed woodland) is a system which combines tree
                crops, forage and livestock. When properly managed it can
                increase productivity and provide long term income by producing
                tree crops alongside forage and livestock.

                This slider converts a portion of pasture land into
                silovpasture, creating a mix of trees and grazing areas.

                A value above 0 means some land is converted, with 100% meaning
                all pasture land is converted to silvopasture.
                
                """ + more_details_link("8r8po4kj9qqw"))

@st.dialog("Methane inhibitor use in livestock feed", width="small")
def methane_inhibitor_help():
    st.markdown("""
                A significant proportion of emissions from livestock farming
                come from methane, which is released during digestion by
                ruminant animals, such as cattle, sheep and goats. Adjusting
                livestock feed can help  reduce these emissions. Interventions
                could include feeding livestock grasses with a higher sugar
                content, providing dairy cows with a high starch diet, precision
                feeding or using feed additives such as 3NOP or nitrate to
                inhibit methane production.

                This slider reduces methane emissions by improving livestock
                feed and adding inhibitors.

                A value above 0 means some farms adopt these practices, with
                100% meaning all farms implement them.

                """ + more_details_link("tbok5jqrlrxb"))


@st.dialog("Manure management in livestock farming", width="small")
def manure_management_help():
    st.markdown("""
                Manure is a major source of greenhouse gas emissions, including
                methane and nitrous oxide.Various practices can be used to
                reduce these emissions at the different stages including
                storage, transportation and disposal. Examples include anaerobic
                digestion which converts much of the organic carbon into biogas,
                methane capture and combustion, covering slurry to prevent
                methane escaping and slurry acidification to lower emissions
                during storage.

                This slider reduces methane emissions from manure by improving
                management practices.

                A value of 0% means no farms adopt these practices, while 100%
                means all farms implement them.

                """ + more_details_link("aqz9utt7u1x"))

@st.dialog("Manure management in livestock farming", width="small")
def breeding_help():
    st.markdown("""
                A significant proportion of emissions from livestock farming
                come from methane, which is released during digestion by
                ruminant animals, such as cattle, sheep, and goats.

                This slider reduces methane emissions by using selective
                breeding techniques. Genetic testing helps identify and breed
                animals with traits that naturally produce lower levels of
                greenhouse gas emissions.

                A value above 0 means some farms adopt this practice, with 100%
                meaning all farms implement it.

                """ + more_details_link("u9p65u7y1vdc"))

@st.dialog("Reducing fossil fuel use in livestock farming", width="small")
def fossil_livestock_help():
    st.markdown("""
                Farms produce significant greenhouse gas emissions by using
                fossil fuels to power machinery and heating systems.

                This slider reduces emissions by switching to low emission
                machinery and processes, including electronic vehicles,
                electricity powered machinery and low scale wind farms etc.

                A value above 0 means some farms adopt these measures, with 100%
                meaning all farms completely eliminate the use of fossil fuels
                for heating and machinery.

                """ + more_details_link("qtazr4y5dfwi"))

# ------------------------------------------------------------------------------
#                            Arable farming
# ------------------------------------------------------------------------------

@st.dialog("Farmland % converted to Agroforestry", width="small")
def agroforestry_help():
    st.markdown("""
                Agroforestry is a land management system where trees and
                hedgerows are planted on arable land, alongside crops. Benefits
                include improved soil health, increased  productivity from fruit
                trees, better resilience to extreme weather, and greater
                biodiversity, along with enhanced carbon sequestration. 

                This slider converts arable land into agroforestry.

                A value above 0 means some arable land is converted, with 100%
                meaning all arable land is converted to agroforestry.

                """ + more_details_link("90swrlvdy6f8"))

@st.dialog("Low Carbon Technology on Farm", width="small")
def fossil_arable_help():
    st.markdown("""
                Farms produce significant greenhouse gas emissions by using
                fossil fuels to power machinery and heating systems.

                This slider reduces emissions by switching to low emission
                machinery and processes, including converting farm equipment to
                run on renewable energy.

                A value above 0 means some farms adopt this practice, with 100%
                meaning all farms implement it.

                """ +  more_details_link("6j2golzh19zq"))

@st.dialog("Urban agriculture and vertical farming", width="small")
def urban_help():
    st.markdown("""
                Urban and vertical agriculture provide a method for food
                production that has a smaller environmental footprint compared
                to traditional agriculture, while also freeing up land for other
                uses. Significant improvements are improving yields and energy
                efficiency.

                This slider reduces the use of arable land while maintaining the
                same level of production by shifting some of it to urban and
                vertical farming systems.

                A value of above 0 means some production is moved away from
                arable land, with 100% meaning all production is moved from
                arable land.

                """ + more_details_link("2w3tq0fbry5i"))


@st.dialog("Nitrogen use efficiency", width="small")
def nitrogen_help():
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

@st.dialog("Enhanced weathering and biochar", width="small")
def biochar_help():
    pass


# ------------------------------------------------------------------------------
#                                Projection baseline
# ------------------------------------------------------------------------------

@st.dialog("Population projection", width="small")
def population_help():
    st.markdown("""
                The population projection describes the expected population
                growth rate until 2050. The options presented here correspond to
                the UN's  population prospects models, which are assuming
                various rates of fertility, mortality, and migration.

                For further details, [see the World Population Prospects 2024 report]\
                (https://population.un.org/wpp/assets/Files/WPP2024_Methodology.pdf).
                """)

@st.dialog("Crop yields", width="small")
def crop_yields_help():
    st.markdown("""
                The crop yield projection describes the expected change in crop
                yields by 2050. The values presented here represent a steady
                change in yield from 2025-2050, which can be affected by
                factors, including climate stress, technological improvements,
                and changes in agricultural practices.

                4 scenarios are available, which match the crop yield
                assumptions from the [6th Carbon Budget]\
                (https://www.theccc.org.uk/wp-content/uploads/2020/12/Sector-summary-Agriculture-land-use-land-use-change-forestry.pdf).
                - **Baseline**: The baseline scenario assumes no change in crop
                yields, staying constant at around 8.2 of wheat tonnes per
                hectare.
                - **Climate sensitivity**: Climate risks dominate future yield,
                resulting in a reduction of 27% in crop yields.
                - **Medium**: Assumes a 34% increase in crop yields, to 11
                tonnes per hectare. Primarily driven by the increased CO2
                fertilization effect, longer growing seasons, and improved
                agricultural practices.
                - **High**: Assumes a 58% increase in crop yields, to 13 tonnes
                of wheat per hectare. Driven  by the increased CO2 fertilization
                effect, longer growing seasons, and improved agricultural
                practices, as well as reduced risks from climate change.
                """)

@st.dialog("Trade elasticity", width="small")
def trade_help():
    st.markdown("""
                When the amount of food used in the UK changes, it must either
                come from domestic production or from imports. This setting lets
                you decide whether changes to UK food use are met through
                changes to imports, changes to production or an equal mixture of
                both. If one of the two gets to zero for a particular commodity
                any further changes will affect the other.

                In reality, trade adjustment will vary for each commodity and
                change over time with economic conditions. For further
                discussion, click [here](https://docs.google.com/document/d/1A2J4BYIuXMgrj9tuLtIon8oJTuR1puK91bbUYCI8kHY/edit?tab=t.0#heading=h.5wokskh532mj).
                """)
    
@st.dialog("Forest mode", width="small")
def forest_mode_help():
    st.markdown("""
                This setting lets you choose how forest area is determined in
                the model. 

                - **Input slider**: Forest area is determined by the
                'Forest' slider in the Land Use Change section.
                Resulting woodland area matches the value set in this slider,
                and can be controlled by the user.

                - **Driven by production**: Forest area is determined by the
                relative change of pasture and arable land due to production
                shifts. Forest percentage becomes an output of the model, rather
                than an input. If pasture land decreases more than arable land,
                forest area increases, and vice versa.
                """)
    
@st.dialog("Feed mode", width="small")
def feed_mode_help():
    st.markdown("""
                This setting lets you choose how feed for animals and other
                production dependent quantities are managed in the model.

                - **Re-export**: Feed, seed and processing quantities no longer
                used for animal and vegetal production are exported to other
                countries. This means that feed, seed and processing quantities
                are not reduced, and the model assumes that other countries will
                use the feed, seed and processing quantities that are no longer
                needed in the UK.

                - **Scale**: Production and imports of feed, seed and processing
                quantities are scaled according to changes in domestic
                production.
                """)