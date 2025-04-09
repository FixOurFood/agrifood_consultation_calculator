import streamlit as st
import gspread
from google.oauth2 import service_account
from utils.helper_functions import update_slider, reset_sliders
import subprocess
import numpy as np

SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = dict(st.secrets["gspread"]["gs_api_key"])
APP_BASE_URL = "https://sarahjp-hack.streamlit.app/"

credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# SUBMISSION_WORKSHEET = "Stakeholder submissions - roadmap workshop Jan 23"
# SUBMISSION_WORKSHEET = "Stage I submissions"
SUBMISSION_WORKSHEET = "submissions_8apr25"

gc = gspread.authorize(credentials)
sh = gc.open_by_key("1ZEb7PzEi6aKv303t7ypFriIt89FPzXTySGt_vmY60_Y")
stage_I_worksheet = sh.worksheet(SUBMISSION_WORKSHEET)
pathways_worksheet = sh.worksheet("Sensitivity Analysis")
enrolments_worksheet = sh.worksheet("Form responses 2")

stage_I_deadline = 'December 31, 2024'

keys=[

    "pop_proj",
    "yield_proj",
    "elasticity",

    "ruminant",
    "dairy",
    "pig_poultry_eggs",
    "pulses",
    "fruit_veg",
    "cereals",
    "meat_alternatives",
    "dairy_alternatives",
    "waste",

    "foresting_pasture",
    "bdleaf_conif_ratio", 
    "land_BECCS",
    "lowland_peatland",
    "upland_peatland",
    "soil_carbon",
    "mixed_farming",
    
    "silvopasture",
    "stock_density",
    "methane_inhibitor",
    "manure_management",
    "animal_breeding",
    "fossil_livestock",
    
    "agroforestry",
    "fossil_arable",
    "nitrogen",
    "vertical_farming",
    
    "waste_BECCS",
    "overseas_BECCS",
    "DACCS",
]

def get_user_list():
    """Get the list of user IDs from the spreadsheet URL"""

    user_list = enrolments_worksheet.col_values(5)
    user_list = user_list[1:]
    return user_list

@st.dialog("Submit scenario")
def submit_scenario(user_id, ambition_levels=False, check_users=True, name=None, extra_values=None):
    """Submit the pathway to the Google Sheet.

    Parameters:
    ----------

    user_id : str
        The user's ID.
        
    ambition_levels : bool
        Whether to submit the ambition levels stored in the session state, or
        run a test submission with dummy data instead.

    Returns:
    -------
        None
    """

    hash = get_latest_commit_hash()[:7]

    if not ambition_levels:
        row = [user_id, "test"]
        stage_I_worksheet.append_row(row)
        return
    
    if check_users:
        if user_id not in get_user_list():
            st.error(f'User ID {user_id} not found in database', icon="🚨")
    
    if name is None:
        name = " "
    
    else:
        row = [name,

            st.session_state["pop_proj"],
            st.session_state["yield_proj"],
            st.session_state["elasticity"],

            st.session_state["ruminant"],
            st.session_state["dairy"],
            st.session_state["pig_poultry"],
            st.session_state["eggs"],            
            st.session_state["pulses"],
            st.session_state["fruit_veg"],
            st.session_state["cereals"],
            st.session_state["meat_alternatives"],
            st.session_state["dairy_alternatives"],
            st.session_state["waste"],
            
            st.session_state["foresting_pasture"],
            st.session_state["bdleaf_conif_ratio"],
            st.session_state["land_BECCS"],
            st.session_state["lowland_peatland"],
            st.session_state["upland_peatland"],
            st.session_state["horticulture"],
            st.session_state["pulse_production"],
            st.session_state["mixed_farming"],

            st.session_state["silvopasture"],
            st.session_state["stock_density"],
            st.session_state["pasture_soil_carbon"],
            st.session_state["methane_inhibitor"],
            st.session_state["manure_management"],
            st.session_state["animal_breeding"],
            st.session_state["fossil_livestock"],

            st.session_state["agroforestry"],
            st.session_state["arable_soil_carbon"],
            st.session_state["fossil_arable"],
            st.session_state["nitrogen"],
            st.session_state["vertical_farming"],

            st.session_state["waste_BECCS"],
            st.session_state["overseas_BECCS"],
            st.session_state["DACCS"],
            
            hash
        ]

        if extra_values is not None:
            if np.isscalar(extra_values):
                extra_values = [extra_values]
            values_formatted = ['{0:.2f}'.format(val) for val in extra_values]
            row.extend(values_formatted)

        stage_I_worksheet.append_row(row)
        st.success(f'Succesfully submitted scenario {name}', icon="✅")
        st.write("""If you want to modify your submission, please use the same
                 scenario name as before.""")

# @st.cache_data(ttl=60*60*24)
def get_pathways():
    """Get the pathways names from the Google Sheet"""

    values = pathways_worksheet.col_values(1)
    return values[3:]

# @st.cache_data(ttl=60*60*24)
def get_pathway_data(pathway_name):
    """Get the scenario data from the Google Sheet"""

    # pathways_names
    pathway_names = pathways_worksheet.col_values(1)

    # Index of row with the corresponding pathway name
    idx = pathway_names.index(pathway_name)

    # Get values
    pathway_values = pathways_worksheet.row_values(idx + 1)
    pathway_values = pathway_values[1:]
    
    # Convert string values to numbers, replacing empty strings with 0
    pathway_values = [str(x) if any(c.isalpha() for c in str(x)) else float(x) if x != "" else 0 for x in pathway_values]

    # Get keys
    keys = pathways_worksheet.row_values(3)

    # Create dictionary
    pathway_dict = dict(zip(keys[1:], pathway_values))
    
    return pathway_dict

def call_scenarios(scenario=None):
    """Call the scenarios from the Google Sheet"""

    if scenario is None:
        scenario = st.session_state["scenario"]
        if scenario is None:
            return
    
    # Get the scenario data
    pathway_data = get_pathway_data(scenario)

    # Update the session state
    update_slider(list(pathway_data.keys()), list(pathway_data.values()))

def get_latest_commit_hash():
    """Returns the hash of the latest commit in the repository.
    """
    try:
        # Run 'git rev-parse HEAD' to get the last commit hash
        commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')
        return commit_hash
    except Exception as e:
        return f"Error retrieving commit hash: {e}"
    
if __name__ == "__main__":
    # submit_scenario("TEST")

    pathway_names = get_pathways()
    print(get_pathway_data(pathway_names[0]))

    print(get_user_list())

def build_url():

    url = APP_BASE_URL

    for key in keys:
        url += f"{key}={st.session_state[key]}&"

    return url