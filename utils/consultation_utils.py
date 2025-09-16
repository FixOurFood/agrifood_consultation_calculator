import streamlit as st
import gspread
from google.oauth2 import service_account
from utils.helper_functions import update_slider, default_widget_values
import subprocess
import numpy as np
import xarray as xr

SCOPES = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = dict(st.secrets["gspread"]["gs_api_key"])

credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

if st.secrets["branch"] == "consultation":
    APP_BASE_URL = "https://agrifood-consultation.streamlit.app/"
    SCENARIOS_WORKSHEET = "Scenarios"

elif st.secrets["branch"] == "sarah_jp_hack":
    APP_BASE_URL = "https://sarahjp-hack.streamlit.app/"
    SCENARIOS_WORKSHEET = "sarahjp_scenarios"

gc = gspread.authorize(credentials)
sh = gc.open_by_key(st.secrets["scenarios_worksheet_key"])

pathways_worksheet = sh.worksheet(SCENARIOS_WORKSHEET)
enrolments_worksheet = sh.worksheet("Form responses 2")

@st.cache_data(ttl=60*60*24)
def get_user_list():
    """Get the list of user IDs from the spreadsheet URL"""

    user_list = enrolments_worksheet.col_values(5)
    user_list = user_list[1:]
    return user_list

@st.dialog("Submit scenario")
def submit_scenario(
    name,
    ambition_levels=False,
    check_users=True,
    datablock=None,
    user_id=None,
    worksheet=None,
    generate_url=False
    ):
    """Submit a pathway to the scenarios Google Sheet.

    Parameters:
    ----------
    name : str
        The name of the scenario
    ambition_levels : bool
        Whether to submit the ambition levels stored in the session state, or
        run a test submission with dummy data instead.
    check_users : bool
        Whether to check if the user is in the database before allowing a
        submissions
    datablock : dict
        A dictionary containing additional data to be submitted.
    user_id : str
        The user's ID to be checked in the users database
    worksheet : str
        Name of the worksheet to submit scenarios to.
    generate_url : bool
        Whether to print a code box with the submissions URL in the confirmation
        modal.
    """

    ws = sh.worksheet(worksheet)

    hash = get_latest_commit_hash()[:7]

    if not ambition_levels:
        row = [name, "test"]
        ws.append_row(row)
        return
    
    if check_users:
        if user_id not in get_user_list():
            st.error(f'User ID {user_id} not found in database', icon="🚨")
    
    if name is None or name == "":
        name = "Anonymous submission"

    if generate_url and datablock is not None:
        url = build_url()
        name_to_cell = f'=HYPERLINK("{url}", "{name}")'
    else:
        name_to_cell = name

    row = [name_to_cell]

    # Append slider values. Skip the scenario key
    for key in list(default_widget_values.keys())[1:]:
        row.append(st.session_state[key])

    # Append hash of the current commit 
    row.append(hash)        

    # Append additional data from the datablock
    if datablock is not None:
        extra_values = [
            datablock["metrics"]["SSR_metric_yr"],
            datablock["metrics"]["total_emissions"],
            datablock["metrics"]["new_herd"].isel(Year=-1),
            datablock["metrics"]["new_dairy_herd"].isel(Year=-1),
            datablock["metrics"]["new_dairy_herd_2y"].isel(Year=-1),
            datablock["metrics"]["new_beef_herd"].isel(Year=-1),
            datablock["metrics"]["new_pig_heads"].isel(Year=-1),
            datablock["metrics"]["new_poultry_heads"].isel(Year=-1),
            datablock["metrics"]["new_sheep_flock"].isel(Year=-1),
            datablock["metrics"]["new_potato_area"].isel(Year=-1),
            datablock["metrics"]["new_oilseed_area"].isel(Year=-1),
            datablock["metrics"]["new_cereal_area"].isel(Year=-1),
            datablock["metrics"]["new_horticulture_area"],
            datablock["metrics"]["other_crops_area_mha"].isel(Year=-1),
            datablock["metrics"]["reduction_emissions_pctg"],
            datablock["metrics"]["new_forest_land"]/1e6,
            datablock["metrics"]["forest_sequestration_MtCO2"],
            datablock["metrics"]["reduction_emissions_agricultural_pctg"],
            datablock["metrics"]["agricultural_emissions"],
            datablock["metrics"]["total_removals"],
            datablock["metrics"]["total_arable"]/1e6,
            datablock["metrics"]["new_arable_land_pctg"],
            datablock["metrics"]["total_pasture"]/1e6,                            
            datablock["metrics"]["new_pasture_land_pctg"],
            0,
            datablock["metrics"]["total_restored_peatland"]/1e6,
            datablock["metrics"]["total_agroforestry"]/1e6,
            datablock["metrics"]["total_silvopasture"]/1e6,
            datablock["metrics"]["total_mixed_farming"]/1e6,
            datablock["metrics"]["beccs_on_arable"]/1e6,
            datablock["metrics"]["beccs_on_pasture"]/1e6,
            datablock["metrics"]["total_beccs"]/1e6,
            ]
        
        if np.isscalar(extra_values):
            extra_values = [extra_values]
        for i, val in enumerate(extra_values):
            if isinstance(val, xr.DataArray):
                extra_values[i] = val.to_numpy().item()
        # values_formatted = ['{0:.3f}'.format(val) for val in extra_values]
        row.extend(extra_values)

    with st.spinner("Submitting scenario..."):
        ws.append_row(row)

        last_row = len(ws.col_values(1))
        ws.update_cell(last_row, 1, name_to_cell)

    st.success(f'Succesfully submitted scenario {name}', icon="✅")
    st.write("""Thank you four submission! If you would like to share your
             scenario with others, please copy the URL below.""")
    if generate_url:
        st.code(url, wrap_lines=True, language=None)

@st.cache_data(ttl=60*60*24)
def get_pathways():
    """Get the pathways names from the Google Sheet"""

    values = pathways_worksheet.col_values(1)
    return values[3:]

@st.cache_data(ttl=60*60*24)
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
    pathway_values = [str(x) if any(c.isalpha() for c in str(x)) 
                      else float(x) if x != ""
                      else 0
                      for x in pathway_values]

    # Get keys
    keys = pathways_worksheet.row_values(3)

    # Create dictionary
    pathway_dict = dict(zip(keys[1:], pathway_values))
    
    return pathway_dict

def call_scenarios(scenario=None):
    """Call the scenarios from the Google Sheet"""

    # Clear query parameters
    st.query_params.clear()

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

def build_url(base_url=APP_BASE_URL):
    """Builds a URL to access the current pathway."""

    url = base_url
    url += "?embedding=true&"

    # Skip first key, which is the scenario name
    for key in list(default_widget_values.keys())[1:]:
        url += f"{key}={st.session_state[key]}&"

    return url

@st.cache_data(ttl=60*60*24)
def get_worksheet_list():
    """Get the list of worksheets in the spreadsheet."""

    ws_list = sh.worksheets()
    ws_list_name = [ws.title for ws in ws_list]
    return ws_list_name
