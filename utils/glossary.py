glossary_dict = {
    "CO2e concentration": """Atmospheric CO2 concentration
    measured in parts per million (PPM)""",

    "CO2e emission per food item": """Fossil CO2 emissions to the atmosphere
    measured in billion tons per year""",

    "CO2e emission per food group": """Fossil CO2 emissions to the atmosphere
    measured in billion tons per year""",

    "Radiative forcing": """Balance between total energy
    absorved by Earth's atmosphere and total
    radiated energy back to space
    measured in Watts per square meter""",

    "Temperature anomaly": """Difference in Celcius degrees
    between projected atmospheric temperature
    and baseline expected from stable emissions""",

    "Nutrients": """ Daily protein and energy intake per capita,
    in grams and kCal, respectively""",

    "Land Use": """ Distribution of land use accross the UK """,

    "Omnivorous diet": """ Omnivorous diets include the consumption of both
    plant and animal origin food items.""",

    "Semi-vegetarian diet": """ While not uniquely defined, semi-vegetarian
    diets normally include the consumption of animal origin products, typically
    meat, but limited to only certain species, or certain ocassions.""",

    "Pescetarian diet": """ Pescetarian diet limits the consumption of animal
    meat to only that coming from seafood and fish meat.""",

    "Lacto-ovo-vegetarian diet": """ Lacto-ovo-vegetarian diets limits the
    consumption of animal products to only dairy products and eggs,
    supressing any kind of meat consumption.""",

    "Vegan diet": """ Full vegetarian or vegan diets do not include any
    product of animal origin, thus eliminating the consumption of meat, dairy
    products and eggs.""",

    "FAOSTAT Elements":  """ List of FAOSTAT food system elements """
}

vegetarian_diet_dict = {
    0: """Omnivorous diet:  Consumption of all types
    of food, including red (beef and goat) and white
    (pig, poultry) meat, fish and seafood, dairy
    products and eggs.""",

    1: """Semi-vegetarian diet:  Moderated consumption
    of meat, typically limited to white (pig, poultry)
    meat and seafood. Includes dairy products and
    eggs.""",

    2: """Pescetarian diet:  No red (beef, goat) or
    white (pig, poultry) meat consumption, processed
    animal protein only from fish and seafood.
    Includes dairy products and eggs.""",

    3: """Vegetarian diet:  No processed animal
    protein, including red (beef and goat), white
    (pig and poultry) meat or fish and seafood.
    Dairy products and eggs are consumed.""",

    4: """Vegan diet:  No products of animal origin
    are consumed. This includes red (beef and goat),
    white (pig and poultry) meat, fish and seafood
    or Dairy products and eggs"""
}

option_list = [
    "Summary",
    "Annual quantities",
    "Per capita daily values",
    "Land",
    "Self-sufficiency ratio"
    ]

FAOSTAT_percapita_items = [
    "Weight",
    "Energy",
    "Fat",
    "Proteins",
    "Emissions"
    ]

x_axis_title = {
    "Weight": "g / cap / day",
    "Energy": "kcal / cap / day",
    "Fat": "g fat / cap / day",
    "Proteins": "g protein / cap / day",
    "Emissions": "g CO2e / cap / day"
    }

land_color_dict = {
    'Broadleaf woodland':  "green",
    'Coniferous woodland':  "green",
    'New Broadleaf woodland':  "green",
    'New Coniferous woodland':  "green",
    'Arable':  "yellow",
    'Managed arable':  "lightyellow",
    'Managed pasture':  "gold",
    'Mixed farming':  "thistle",
    'Improved grassland':  "orange",
    'Semi-natural grassland':  "orange",
    'Mountain, heath and bog':  "gray",
    'Saltwater':  "gray",
    'Freshwater':  "gray",
    'Coastal':  "gray",
    'Built-up areas and gardens':  "gray",
    'Spared':  "purple",
    'Bioenergy crops (pasture)':  "red",
    'Bioenergy crops (arable)':  "red",
    'Silvopasture':  "lightgreen",
    'Agroforestry':  "lightblue",
    'Restored upland peat':  "darkred",
    'Restored lowland peat':  "darkred",
}

land_label_dict = {
    'Broadleaf woodland':  "Forest",
    'Coniferous woodland':  "Forest",
    'New Broadleaf woodland':  "Forest",
    'New Coniferous woodland':  "Forest",
    'Arable':  "Arable",
    'Managed arable':  "Managed arable",
    'Managed pasture':  "Managed pasture",
    'Mixed farming':  "Mixed farming",
    'Improved grassland':  "Pasture",
    'Semi-natural grassland':  "Pasture",
    'Mountain, heath and bog':  "Mountain",
    'Saltwater':  "Water",
    'Freshwater':  "Water",
    'Coastal':  "Water",
    'Built-up areas and gardens':  "Non-agricultural",
    'Spared':  "Spared",
    'Bioenergy crops (pasture)':  "BECCS",
    'Bioenergy crops (arable)':  "BECCS",
    'Silvopasture':  "Silvopasture",
    'Agroforestry':  "Agroforestry",
    'Restored lowland peat':  "Restored peatland",
    'Restored upland peat':  "Restored peatland",
}

# These are the sectoral emissions predicted by the CCC under its "Balanced
# Pathway" scenario. From the 6th carbon budget report (2020).
sector_emissions_dict = {
    "F-gases": 1.60,
    "Waste": 5.11,
    "Shipping": 0.51,
    "Aviation": 22.67,
    "LU sources": 6.08,  # Sum of 2050 land use sources
    "Agriculture": 0,  # Set to be calculated by the model
    "Fuel supply": 1.57,
    "Electricity": 1.00,
    "Manufacturing": 3.57,
    "Buildings": 1.11,  # Sum of residential and non-residential
    "Transport": 1.07,
    "LU sinks": 0,  # Set to be calculated by the model
    "Removals": -9.82,  # Baseline removals total to be calculated by the model
}

sector_emissions_colors = {
    "F-gases": "#280049",
    "Waste": "#96e9ff",
    "Shipping": "#ca7880",
    "Aviation": "#ab6b99",
    "LU sources": "#cde7b0",
    "Agriculture": "#a1d800",
    "Fuel supply": "#369993",
    "Electricity": "#ffff4b",
    "Manufacturing": "#aec5eb",
    "Buildings": "#ffac00",
    "Transport": "#7142ff",
    "LU sinks": "#1a5f31",
    "Removals": "#1a73e8",
}
