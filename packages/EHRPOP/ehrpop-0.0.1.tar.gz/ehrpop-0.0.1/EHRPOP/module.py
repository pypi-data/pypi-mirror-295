import numpy as np
import plotly.graph_objects as go
import pandas as pd
import re
import json
import os
from datetime import date
from .utils import load_json_data

json_path = os.path.join(os.path.dirname(__file__), 'all_codes.json')

# Load the JSON data initially
data = load_json_data()



def cleanAllCodes():
    """
    Deletes all codes from the Surgery section of the JSON data.

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """
    # Iterate through each code type in the Surgery section
    for code_type in data['Treatment']['Surgery']:
        # Check if the entry is a list (which presumably holds codes)
        if isinstance(data['Treatment']['Surgery'][code_type], list):
            # Clear all codes from the list
            if(code_type in ['ATC','CCAM','ICD10']):
                data['Treatment']['Surgery'][code_type].clear()
                print(f"All codes removed from Surgery '{code_type}'.")

    # Iterate through each code type in the RT section
    for code_type in data['Treatment']['RT']:
        # Check if the entry is a list (which presumably holds codes)
        if isinstance(data['Treatment']['RT'][code_type], list):
            # Clear all codes from the list
            if(code_type in ['ATC','CCAM','ICD10']):
                data['Treatment']['RT'][code_type].clear()
                print(f"All codes removed from RT '{code_type}'.")

    # Iterate through each code type in the CT section
    for code_type in data['Treatment']['CT']:
        # Check if the entry is a list (which presumably holds codes)
        if isinstance(data['Treatment']['CT'][code_type], list):
            # Clear all codes from the list
            if(code_type in ['ATC','CCAM','ICD10']):
                data['Treatment']['CT'][code_type].clear()
                print(f"All codes removed from CT '{code_type}'.")

    # Iterate through each code type in the ET section
    for code_type in data['Treatment']['ET']:
        # Check if the entry is a list (which presumably holds codes)
        if isinstance(data['Treatment']['ET'][code_type], list):
            # Clear all codes from the list
            if(code_type in ['ATC','CCAM','ICD10']):
                data['Treatment']['ET'][code_type].clear()
                print(f"All codes removed from ET '{code_type}'.")


    # Iterate through each code type in the TT section
    for code_type in data['Treatment']['TT']:
        # Check if the entry is a list (which presumably holds codes)
        if isinstance(data['Treatment']['TT'][code_type], list):
            # Clear all codes from the list
            if(code_type in ['ATC','CCAM','ICD10']):
                data['Treatment']['TT'][code_type].clear()
                print(f"All codes removed from TT '{code_type}'.")

    # Iterate through each code type in the Other section
    for code_type in data['Treatment']['Other']:
        # Check if the entry is a list (which presumably holds codes)
        if isinstance(data['Treatment']['Other'][code_type], list):
            # Clear all codes from the list
            if(code_type in ['ATC','CCAM','ICD10']):
                data['Treatment']['Other'][code_type].clear()
                print(f"All codes removed from Other '{code_type}'.")



    # Save the updated JSON data back to the file
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("All codes have been deleted.")



def addCodeSurgery(code, code_type):
    """
    Adds a code to the Surgery section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be added.
    code_type : str
        The type of code (e.g., 'ATC', 'CCAM', 'ICD10').

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """

    if code_type not in data['Treatment']['Surgery']:
        print(f"Error: Invalid code type '{code_type}'")
        return
    
    if code not in data['Treatment']['Surgery'][code_type]:
        data['Treatment']['Surgery'][code_type].append(code)
        print(f"Code '{code}' added to Surgery '{code_type}'.")
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
    else:
        print(f"Code '{code}' already exists in Surgery '{code_type}'.")

def deleteCodeSurgery(code):
    """
    Deletes a code from the Surgery section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be deleted.

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """

    found = False
    for code_type in data['Treatment']['Surgery']:
        if isinstance(data['Treatment']['Surgery'][code_type], list) and code in data['Treatment']['Surgery'][code_type]:
            data['Treatment']['Surgery'][code_type].remove(code)
            found = True
            print(f"Code '{code}' removed from Surgery '{code_type}'.")
            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)


    
    if not found:
        print(f"Code '{code}' not found in Surgery section.")

def addCodeRT(code, code_type):
    """
    Adds a code to the Radiotherapy section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be added.
    code_type : str
        The type of code (e.g., 'ATC', 'CCAM', 'ICD10').

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """
    if code_type not in data['Treatment']['RT']:
        print(f"Error: Invalid code type '{code_type}'")
        return
    
    if code not in data['Treatment']['RT'][code_type]:
        data['Treatment']['RT'][code_type].append(code)
        print(f"Code '{code}' added to RT '{code_type}'.")
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
    else:
        print(f"Code '{code}' already exists in RT '{code_type}'.")

def deleteCodeRT(code):
    """
    Deletes a code from the Radiotherapy section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be deleted.

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """
    found = False
    for code_type in data['Treatment']['RT']:
        if isinstance(data['Treatment']['RT'][code_type], list) and code in data['Treatment']['RT'][code_type]:
            data['Treatment']['RT'][code_type].remove(code)
            found = True
            print(f"Code '{code}' removed from RT '{code_type}'.")
            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            

    if not found:
        print(f"Code '{code}' not found in RT section.")

def addCodeCT(code, code_type):
    """
    Adds a code to the Chemotherpay section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be added.
    code_type : str
        The type of code (e.g., 'ATC', 'CCAM', 'ICD10').

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """
    if code_type not in data['Treatment']['CT']:
        print(f"Error: Invalid code type '{code_type}'")
        return
    
    if code not in data['Treatment']['CT'][code_type]:
        data['Treatment']['CT'][code_type].append(code)
        print(f"Code '{code}' added to CT '{code_type}'.")
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
    else:
        print(f"Code '{code}' already exists in CT '{code_type}'.")

def deleteCodeCT(code):
    """
    Deletes a code from the Chemotherpay section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be deleted.

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """
    found = False
    for code_type in data['Treatment']['CT']:
        if isinstance(data['Treatment']['CT'][code_type], list) and code in data['Treatment']['CT'][code_type]:
            data['Treatment']['CT'][code_type].remove(code)
            found = True
            print(f"Code '{code}' removed from CT '{code_type}'.")
            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    if not found:
        print(f"Code '{code}' not found in CT section.")

def addCodeET(code, code_type):
    """
    Adds a code to the Endocrine therapy section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be added.
    code_type : str
        The type of code (e.g., 'ATC', 'CCAM', 'ICD10').

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """
    if code_type not in data['Treatment']['ET']:
        print(f"Error: Invalid code type '{code_type}'")
        return
    
    if code not in data['Treatment']['ET'][code_type]:
        data['Treatment']['ET'][code_type].append(code)
        print(f"Code '{code}' added to ET '{code_type}'.")
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    else:
        print(f"Code '{code}' already exists in ET '{code_type}'.")

def deleteCodeET(code):
    """
    Deletes a code from the Endocrine therapy section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be deleted.

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """
    found = False
    for code_type in data['Treatment']['ET']:
        if isinstance(data['Treatment']['ET'][code_type], list) and code in data['Treatment']['ET'][code_type]:
            data['Treatment']['ET'][code_type].remove(code)
            found = True
            print(f"Code '{code}' removed from ET '{code_type}'.")
            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    
    if not found:
        print(f"Code '{code}' not found in ET section.")

def addCodeTT(code, code_type):
    """
    Adds a code to the Targeted therapy section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be added.
    code_type : str
        The type of code (e.g., 'ATC', 'CCAM', 'ICD10').

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """
    if code_type not in data['Treatment']['TT']:
        print(f"Error: Invalid code type '{code_type}'")
        return
    
    if code not in data['Treatment']['TT'][code_type]:
        data['Treatment']['TT'][code_type].append(code)
        print(f"Code '{code}' added to TT '{code_type}'.")
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)


    else:
        print(f"Code '{code}' already exists in TT '{code_type}'.")

def deleteCodeTT(code):
    """
    Deletes a code from the Targeted therapy section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be deleted.

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """
    found = False
    for code_type in data['Treatment']['TT']:
        if isinstance(data['Treatment']['TT'][code_type], list) and code in data['Treatment']['TT'][code_type]:
            data['Treatment']['TT'][code_type].remove(code)
            found = True
            print(f"Code '{code}' removed from TT '{code_type}'.")
            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)            

    if not found:
        print(f"Code '{code}' not found in TT section.")

def addCodeOther(code, code_type):
    """
    Adds a code to the Other section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be added.
    code_type : str
        The type of code (e.g., 'ATC', 'CCAM', 'ICD10').

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """
    if code_type not in data['Treatment']['Other']:
        print(f"Error: Invalid code type '{code_type}'")
        return
    
    if code not in data['Treatment']['Other'][code_type]:
        data['Treatment']['Other'][code_type].append(code)
        print(f"Code '{code}' added to Other '{code_type}'.")
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)


    else:
        print(f"Code '{code}' already exists in Other '{code_type}'.")

def deleteCodeOther(code):
    """
    Deletes a code from the Other section of the JSON data.

    Parameters
    ----------
    code : str
        The code to be deleted.

    Returns
    -------
    None
        It updates the JSON data and saves it to a file.
    """
    found = False
    for code_type in data['Treatment']['Other']:
        if isinstance(data['Treatment']['Other'][code_type], list) and code in data['Treatment']['Other'][code_type]:
            data['Treatment']['Other'][code_type].remove(code)
            found = True
            print(f"Code '{code}' removed from Other '{code_type}'.")
            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)            

    if not found:
        print(f"Code '{code}' not found in Other section.")

def readJSON(input_filepath):
    """
    Read a JSON file and ensure it starts with 'Treatment'.
    Concatenate its data with another JSON file.
    """

    def load_json_data(filepath):
        """Utility function to load JSON data from a given file path."""
        with open(filepath, 'r') as file:
            data = json.load(file)
        return data



    input_data = load_json_data(input_filepath)
    
    # Check if the JSON structure starts with "Treatment"
    if "Treatment" not in input_data:
        raise ValueError("The JSON structure must start with 'Treatment'.")
    
    
    # Concatenate the input data with the output data
    if "Treatment" not in data:
        data["Treatment"] = {}
    
    for treatment_type, treatment_data in input_data["Treatment"].items():
        if treatment_type not in data["Treatment"]:
            data["Treatment"][treatment_type] = treatment_data
        else:
            for category, codes in treatment_data.items():
                if category not in data["Treatment"][treatment_type]:
                    data["Treatment"][treatment_type][category] = codes
                else:
                    data["Treatment"][treatment_type][category].extend(codes)
                    # Remove duplicates if needed
                    data["Treatment"][treatment_type][category] = list(set(data["Treatment"][treatment_type][category]))
    
    # Save the updated data back to the output JSON file
    with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

def SnakeyDiagram(df):
    """
    Generates a Sankey diagram of patient treatment sequences from a DataFrame of medical records.

    Parameters
    ----------
    df : DataFrame
        DataFrame containing patient ID, date, and medical codes in columns 'ID_PATIENT', 'DATE', 
        'CODE_CCAM', 'CODE_ATC', and 'CODE_ICD10'.

    Returns
    -------
    None
        It processes the DataFrame and displays a Sankey diagram showing the sequences of treatments.
    """
    def map_code(code):
        #All surgery codes (CCAM):
        surgeyCodes = data["Treatment"]['Surgery']['CCAM'] +  data["Treatment"]['Surgery']['ICD10'] +  data["Treatment"]['Surgery']['ATC']

        #All Chemotherapy codes (ICD10,CCAM,ATC):
        chemoCodes = data["Treatment"]['CT']['CCAM'] +  data["Treatment"]['CT']['ICD10'] +  data["Treatment"]['CT']['ATC']

        #Codes Targeted therapy
        TT_codes = data["Treatment"]['TT']['CCAM'] +  data["Treatment"]['TT']['ICD10'] +  data["Treatment"]['TT']['ATC']

        #Codes Radio therapy
        RtCodes = data["Treatment"]['RT']['CCAM'] +  data["Treatment"]['RT']['ICD10'] +  data["Treatment"]['RT']['ATC']

        #ET Codes
        ET_codes = data["Treatment"]['ET']['CCAM'] +  data["Treatment"]['ET']['ICD10'] +  data["Treatment"]['ET']['ATC']

        #Other codes
        Other_codes = data["Treatment"]['Other']['CCAM'] +  data["Treatment"]['Other']['ICD10'] +  data["Treatment"]['Other']['ATC']
        
        if code in RtCodes:
            return 'RT'
        elif code in TT_codes:
            return 'TT'
        elif code in chemoCodes:
            return 'Chemo'
        elif code in surgeyCodes:
            return 'Surgery'
        elif code in ET_codes:
            return 'ET'
        elif code in Other_codes:
            return 'OTHER'
        else:
            return np.nan
    
    df['CODE_ACT'] = df['CODE_CCAM'].combine_first(df['CODE_ATC']).combine_first(df['CODE_ICD10'])

    df = df.drop(columns=['CODE_ICD10', 'CODE_CCAM','CODE_ATC'])

    df = df.dropna(subset=['CODE_ACT'])
    
    # Apply the function to CODE_ACT column
    df['CODE_ACT'] = df['CODE_ACT'].apply(map_code)

    df = df.dropna(subset=['CODE_ACT'])

    df = df.sort_values(by='DATE', ascending=True)
    
    df['DATE'] = pd.to_numeric(df['DATE'], errors='coerce').fillna(999999)

    # Sort the DataFrame by ID_PATIENT and DATE
    df = df.sort_values(by=['ID_PATIENT', 'DATE'])
    
    def remove_consecutive_duplicates(treatments):
        return '->'.join([treatments[i] for i in range(len(treatments)) if i == 0 or treatments[i] != treatments[i-1]])

    # Group by ID_PATIENT and concatenate the CODE_ACT values without consecutive duplicates
    result = df.groupby('ID_PATIENT')['CODE_ACT'].apply(lambda x: remove_consecutive_duplicates(list(x))).reset_index()

    # Rename columns for clarity
    result.columns = ['ID_PATIENT', 'Traitements']
        
    treatment_counts = result['Traitements'].value_counts()
        
    # Filter out sequences that appear fewer than 10 times
    frequent_treatments = treatment_counts[treatment_counts >= 10].index

    # Filter the original DataFrame to keep only the frequent treatment sequences
    filtered_df = result[result['Traitements'].isin(frequent_treatments)]

    # Function to split treatments and label them uniquely
    def label_treatments(treatment_string):
        treatments = treatment_string.split('->')
        labeled_treatments = [f"{treatments[i]}{i+1}" for i in range(len(treatments))]
        return labeled_treatments
    
    sequence_counter = {}

    for treatments in filtered_df['Traitements']:
        sequence_list = label_treatments(treatments)
        for i in range(len(sequence_list) - 1):
            pair = (sequence_list[i], sequence_list[i + 1])
            if pair in sequence_counter:
                sequence_counter[pair] += 1
            else:
                sequence_counter[pair] = 1
                
    
    # Create source and target lists and values
    source = []
    target = []
    value = []

    for (src, tgt), val in sequence_counter.items():
        source.append(src)
        target.append(tgt)
        value.append(val)

    # Create a list of unique nodes
    all_nodes = list(set(source + target))
    
    node_indices = {node: idx for idx, node in enumerate(all_nodes)}

    # Map source and target to their indices
    source_indices = [node_indices[src] for src in source]
    target_indices = [node_indices[tgt] for tgt in target]
    
    # Create Sankey diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=value,
        )
    ))

    # Add annotations for the legend
    fig.update_layout(
        title_text="Sankey Diagram of Patient Treatment Sequences",
        font_size=10,
        annotations=[
            dict(x=1.1, y=0.85, text="RT: Radiotherapy", showarrow=False, font=dict(size=12)),
            dict(x=1.1, y=0.80, text="TT: Targeted Therapy", showarrow=False, font=dict(size=12)),
            dict(x=1.1, y=0.75, text="ET: Endocrine Therapy", showarrow=False, font=dict(size=12)),
            dict(x=1.1, y=0.70, text="Chemo: Chemotherapy", showarrow=False, font=dict(size=12)),
            dict(x=1.1, y=0.65, text="Surgery: Surgery", showarrow=False, font=dict(size=12)),
        ],
        margin=dict(l=50, r=200, t=50, b=50)  # Add margin on the right for the legend
    )
    fig.show()

def starts_with_any(code, codes_list):
    if pd.isnull(code):  # Checks for NaN or None
        return False
    return any(code.startswith(prefix) for prefix in codes_list)

def yesOrNo(df,CCAM_codes,ATC_codes,ICD_Codes,columnName,daysBefore,daysAfter,indexDate="DATE"
            ,indexCodeCCAM="CODE_CCAM",indexCodeATC="CODE_ATC",indexCodeICD="CODE_ICD10",
            indexID="ID_PATIENT",BC_index_surgery="BC_index_surgery"):
    '''
    Evaluates whether patients have received treatments encoded by CCAM, ATC, or ICD codes within a specified timeframe relative to their breast cancer surgery date. Outputs a DataFrame indicating whether each patient meets the specified criteria.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records, including columns for patient ID (ID_PATIENT), treatment codes (CODE_CCAM, CODE_ATC, CODE_ICD10), and treatment dates (DATE).
    CCAM_codes : list
        A list of CCAM codes. The function checks whether patients have received treatments coded with any of these CCAM codes.
    ATC_codes : list
        A list of ATC codes. Similar to CCAM_codes, this parameter specifies the ATC codes of interest for identifying relevant treatments.
    ICD_Codes : list
        A list of ICD codes used to identify relevant treatments based on these codes.
    columnName : str
        A string specifying the name of the output column in the result DataFrame that indicates whether each patient meets the criteria. This column will contain boolean values (True/False).
    daysBefore : int
        An integer specifying the number of days before breast cancer surgery within which treatments are considered relevant.
    daysAfter : int
        An integer specifying the number of days after breast cancer surgery within which treatments are considered relevant.
    indexDate : str, optional
        The column name for treatment dates in df (default is "DATE").
    indexCodeCCAM : str, optional
        The column name for CCAM codes in df (default is "CODE_CCAM").
    indexCodeATC : str, optional
        The column name for ATC codes in df (default is "CODE_ATC").
    indexCodeICD : str, optional
        The column name for ICD codes in df (default is "CODE_ICD10").
    indexID : str, optional
        The column name for patient ID in df (default is "ID_PATIENT").
    BC_index_surgery : str, optional
        The column name for breast cancer surgery dates in df (default is "BC_index_surgery").

    Returns
    -------
    DataFrame
        A DataFrame indicating, for each patient, whether they meet the specified criteria with a boolean value in the column specified by columnName.
    '''
    
    df['DATE_DIFF'] = df[indexDate] - df[BC_index_surgery]

    matches = ((df[indexCodeCCAM].isin(CCAM_codes) |
           df[indexCodeATC].isin(ATC_codes) |
           df[indexCodeICD].isin(ICD_Codes))& (df['DATE_DIFF'] >= -daysBefore) & (df['DATE_DIFF'] <= daysAfter) )
    
    result = matches.groupby(df[indexID]).any().reset_index()
    
    result = result.rename(columns={0: columnName})

    return result

def isTreatedByIt(df,CCAM_codes,ATC_codes,ICD_Codes,columnName
            ,indexCodeCCAM="CODE_CCAM",indexCodeATC="CODE_ATC",indexCodeICD="CODE_ICD10",
            indexID="ID_PATIENT"):
    
    '''
    Assesses treatment records in a DataFrame to determine if each patient has received a treatment corresponding to any of the provided CCAM, ATC, or ICD codes. Generates a summary DataFrame that includes each patient's ID and a boolean indicator of whether they have received any of the specified treatments.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records. This DataFrame should include columns for patient ID (ID_PATIENT), treatment codes (CODE_CCAM, CODE_ATC, CODE_ICD10), and treatment dates (DATE). It also includes an alternate date column (DATE_ENTREE) for use when the DATE is missing.
    CCAM_codes : list
        A list of CCAM codes used to identify relevant treatments.
    ATC_codes : list
        A list of ATC codes used to identify relevant treatments.
    ICD_Codes : list
        A list of ICD codes used to identify relevant treatments.
    columnName : str
        A string specifying the name for the output column in the resulting DataFrame. This column will contain boolean values indicating whether each patient has received any treatment matching the specified codes.
    indexCodeCCAM : str, optional
        The column name for CCAM codes in df (default is "CODE_CCAM").
    indexCodeATC : str, optional
        The column name for ATC codes in df (default is "CODE_ATC").
    indexCodeICD : str, optional
        The column name for ICD codes in df (default is "CODE_ICD10").
    indexID : str, optional
        The column name for patient ID in df (default is "ID_PATIENT").

    Returns
    -------
    DataFrame
        A DataFrame indicating, for each patient, whether they have received any treatment matching the specified codes with a boolean value in the column specified by columnName.
    '''

    matches = (df[indexCodeCCAM].isin(CCAM_codes) |
           df[indexCodeATC].isin(ATC_codes) |
           df[indexCodeICD].isin(ICD_Codes))
    
    result = matches.groupby(df[indexID]).any().reset_index()
    
    result = result.rename(columns={0: columnName})

    return result

def isTreatedByItWithDate(df, CCAM_codes, ATC_codes, ICD_Codes, columnName,daysBefore,daysAfter
                         ,indexDate="DATE"
                    ,indexCodeCCAM="CODE_CCAM",indexCodeATC="CODE_ATC",indexCodeICD="CODE_ICD10",
                    indexID="ID_PATIENT",BC_index_surgery="BC_index_surgery"):
    
    '''
    Assesses treatment records in a DataFrame to determine if each patient has received a treatment corresponding to any of the provided CCAM, ATC, or ICD codes within a specified timeframe relative to their breast cancer surgery date. Generates a summary DataFrame that includes each patient's ID, a boolean indicator of whether they have received any of the specified treatments, and the date of the first treatment.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records. This DataFrame should include columns for patient ID (ID_PATIENT), treatment codes (CODE_CCAM, CODE_ATC, CODE_ICD10), and treatment dates (DATE). It also includes an alternate date column (DATE_ENTREE) for use when the DATE is missing.
    CCAM_codes : list
        A list of CCAM codes used to identify relevant treatments.
    ATC_codes : list
        A list of ATC codes used to identify relevant treatments.
    ICD_Codes : list
        A list of ICD codes used to identify relevant treatments.
    columnName : str
        A string specifying the name for the output column in the resulting DataFrame. This column will contain boolean values indicating whether each patient has received any treatment matching the specified codes.
    daysBefore : int
        The number of days before surgery within which treatments are considered relevant.
    daysAfter : int
        The number of days after surgery within which treatments are considered relevant.
    indexDate : str, optional
        The column name for treatment dates in df (default is "DATE").
    indexCodeCCAM : str, optional
        The column name for CCAM codes in df (default is "CODE_CCAM").
    indexCodeATC : str, optional
        The column name for ATC codes in df (default is "CODE_ATC").
    indexCodeICD : str, optional
        The column name for ICD codes in df (default is "CODE_ICD10").
    indexID : str, optional
        The column name for patient ID in df (default is "ID_PATIENT").
    BC_index_surgery : str, optional
        The column name for the breast cancer surgery date in df (default is "BC_index_surgery").

    Returns
    -------
    DataFrame
        A DataFrame indicating, for each patient, whether they have received any treatment matching the specified codes with a boolean value in the column specified by columnName, and the date of the first such treatment.
    '''

    df['DATE_DIFF'] = df[indexDate] - df[BC_index_surgery]
    
    df = df[(df['DATE_DIFF'] >= -daysBefore) & (df['DATE_DIFF'] <= daysAfter)]

    # Identify rows that match the specified treatment codes
    matches = df[indexCodeCCAM].isin(CCAM_codes) | df[indexCodeATC].isin(ATC_codes) | df[indexCodeICD].isin(ICD_Codes)
    
    # Filter the DataFrame to include only matching rows
    df_matches = df[matches]
    
    # Group by 'ID_PATIENT' and aggregate to find the minimum 'DATE' (i.e., the first treatment date) for each patient
    first_treatment_date = df_matches.groupby(indexID)[indexDate].min().reset_index(name=columnName+' First_Treatment_Date')
    
    # Determine if each patient received any treatment by checking if they appear in the aggregated results
    result = df[indexDate].drop_duplicates().reset_index(drop=True).to_frame()
    result = pd.merge(result, first_treatment_date, on=indexDate, how='left')
    
    # Add a column indicating True if the patient received treatment (i.e., has a 'First_Treatment_Date') and False otherwise
    result[columnName] = result[columnName+' First_Treatment_Date'].notna()
    
    # Reorder and rename columns as needed
    result = result[[indexDate, columnName,columnName+ ' First_Treatment_Date']]
    
    # Fill NaN dates for patients without treatments
    result[columnName+' First_Treatment_Date'] = result[columnName+' First_Treatment_Date'].fillna('No Treatment')
        
    return result

def isTreatedByItWithQte(df,CCAM_codes,ATC_codes,ICD_Codes,columnName):
    
    '''
    Determines if each patient in the DataFrame has received a treatment corresponding to any of the provided CCAM, ATC, or ICD codes and counts the number of relevant treatment sessions. Generates a summary DataFrame that includes each patient's ID and the number of treatment sessions.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records. This DataFrame should include columns for patient ID (ID_PATIENT), treatment codes (CODE_CCAM, CODE_ATC, CODE_ICD10), and treatment dates (DATE). It also includes an alternate date column (DATE_ENTREE) for use when the DATE is missing.
    CCAM_codes : list
        A list of CCAM codes used to identify relevant treatments.
    ATC_codes : list
        A list of ATC codes used to identify relevant treatments.
    ICD_Codes : list
        A list of ICD codes used to identify relevant treatments.
    columnName : str
        A string specifying the name for the output column in the resulting DataFrame. This column will contain the number of treatment sessions for each patient.

    Returns
    -------
    DataFrame
        A DataFrame indicating the number of relevant treatment sessions for each patient.
    '''

    
    #df['DATE'] = df['DATE'].fillna(df['DATE_ENTREE'])
    df['QUANTITE'] = df['QUANTITE'].fillna(1.0)
    df['SESSION'] = 1

    
    
    df['Is_Relevant'] = df['CODE_CCAM'].apply(starts_with_any, codes_list=CCAM_codes) | \
                    df['CODE_ATC'].apply(starts_with_any, codes_list=ATC_codes) | \
                    df['CODE_ICD10'].apply(starts_with_any, codes_list=ICD_Codes)

    #df['Is_Relevant'] = df['CODE_CCAM'].isin(CCAM_codes) | \
    #                df['CODE_ATC'].isin(ATC_codes) | \
    #                df['CODE_ICD10'].isin(ICD_Codes)
    
    patient_classification = {}
    
    
    for patient_id in df['ID_PATIENT'].unique():
        # Filter the patient's relevant treatments
        patient_df = df[(df['ID_PATIENT'] == patient_id) & df['Is_Relevant']]

        # Skip patients with no relevant treatments
        if patient_df.empty:
            patient_classification[patient_id] = 0
            continue
        
        
        patient_classification[patient_id] = sum(patient_df['SESSION'])
            

    result = pd.DataFrame(list(patient_classification.items()), columns=['ID_PATIENT', columnName])

    return result

def tableValues(df, listColumns,dateStart=None,dateEnd=None):
    '''
    Generates a merged DataFrame of patient treatments based on specified columns.

    The function checks the presence of specified columns in the DataFrame,
    counts the occurrences of unique values in each column.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    listColumns : list of str
        A list of column names to process and merge based on their unique values.

    Returns
    -------
    DataFrame
        A merged DataFrame containing patient IDs and treatment information
        based on the specified columns.

    Raises
    ------
    ValueError
        If listColumns is empty or if any specified column is missing in the DataFrame.
    '''

        
    # Check if listColumns is empty
    if not listColumns:
        raise ValueError("listColumns cannot be empty.")
    
    # Check if all strings in listColumns are in df.columns
    missing_columns = [col for col in listColumns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following columns are missing in the DataFrame: {missing_columns}")
    
    if(dateStart!= None):
        base_date = pd.Timestamp(date(1960, 1, 1))
        dateStart = (pd.to_datetime(dateStart) - base_date)
        dateStart = dateStart.days
    
    if(dateEnd!= None):
        base_date = pd.Timestamp(date(1960, 1, 1))
        dateEnd = (pd.to_datetime(dateEnd) - base_date)
        dateEnd = dateEnd.days
    
    results = None  # Initialize results as None
    
    for coln in listColumns:
        count = 0
        for i in df[coln].value_counts().index.tolist():
            if count == 0:
                results = isTreatedByItWithQte(df, i, i, i, i)
            else:
                r = isTreatedByItWithQte(df, i, i, i, i)
                results = pd.merge(results, r, on='ID_PATIENT')
            count += 1

    return results

def tableSequances(df,listColumns):
    '''
    Generates a DataFrame with sequences of acts and dates for each patient based on specified columns.

    The function checks the presence of specified columns in the DataFrame,
    combines the codes from these columns into a single column, groups by patient ID,
    and sorts the acts by date.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    listColumns : list of str
        A list of column names to process and combine into a sequence of acts.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and sequences of acts and dates.

    Raises
    ------
    ValueError
        If listColumns is empty or if any specified column is missing in the DataFrame.
    '''

        
    # Check if listColumns is empty
    if not listColumns:
        raise ValueError("listColumns cannot be empty.")
    
    # Check if all strings in listColumns are in df.columns
    missing_columns = [col for col in listColumns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following columns are missing in the DataFrame: {missing_columns}")
        
        
    def combine_codes(row):
        codes = ""
        for col in listColumns:
            if pd.notnull(row[col]):
                    codes = row[col]
        return codes

    # Apply the function to create CODE_ACTS
    df['CODE_ACTS'] = df.apply(combine_codes, axis=1)
    df = df[df['CODE_ACTS']!=""]
    df = df[['ID_PATIENT', 'DATE', 'CODE_ACTS']]

    df = df.sort_values(by=['ID_PATIENT', 'DATE'])

    
    grouped = df.groupby('ID_PATIENT').agg({'DATE': list, 'CODE_ACTS': list}).reset_index()

    # Sort acts by date within each group
    grouped['ACTES'] = grouped.apply(lambda row: [act for _, act in sorted(zip(row['DATE'], row['CODE_ACTS']))], axis=1)

    # Create the final DataFrame with ID_PATIENT, DATES, and ACTES columns
    final_df = grouped[['ID_PATIENT', 'DATE', 'ACTES']]
    final_df.columns = ['ID_PATIENT', 'DATES', 'ACTES']
    
    return final_df

def tableSequancesTwo(df,listColumns):
    '''
    Generates a DataFrame with sequences of acts and dates for each patient based on specified columns.

    The function checks the presence of specified columns in the DataFrame, combines the codes from these columns
    into a single column, groups by patient ID, sorts the acts by date, and creates sequences of [interval, CODE_ACTS].

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    listColumns : list of str
        A list of column names to process and combine into a sequence of acts.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and sequences of acts and dates.

    Raises
    ------
    ValueError
        If listColumns is empty or if any specified column is missing in the DataFrame.
    '''    
    # Check if listColumns is empty
    if not listColumns:
        raise ValueError("listColumns cannot be empty.")
    
    # Check if all strings in listColumns are in df.columns
    missing_columns = [col for col in listColumns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following columns are missing in the DataFrame: {missing_columns}")
        
        
    def combine_codes(row):
        codes = ""
        for col in listColumns:
            if pd.notnull(row[col]):
                    codes = row[col]
        return codes

    # Apply the function to create CODE_ACTS
    df['CODE_ACTS'] = df.apply(combine_codes, axis=1)
    df = df[df['CODE_ACTS']!=""]
    df = df[['ID_PATIENT', 'DATE', 'CODE_ACTS']]
    
    # Sort the DataFrame by ID_PATIENT and DATE
    df = df.sort_values(by=['ID_PATIENT', 'DATE'])

    # Function to create the sequence for each patient
    def create_sequence(group):
        sequence = []
        prev_date = None
        for index, row in group.iterrows():
            if prev_date is None:
                prev_date = row['DATE']
                sequence.append(f"[0,{row['CODE_ACTS']}]")
            else:
                interval = row['DATE'] - prev_date
                sequence.append(f"[{interval},{row['CODE_ACTS']}]")
                prev_date = row['DATE']
        return sequence

    # Group by ID_PATIENT and apply the function
    result = df.groupby('ID_PATIENT').apply(create_sequence).reset_index()

    # Rename the columns
    result.columns = ['ID_PATIENT', 'Sequence']
    
    return result

def neoadjuvantOrAdjuvantOrBoth(df,CCAM_codes,ATC_codes,ICD_Codes,columnName,daysBefore,daysAfter
                               ,indexDate="DATE"
                    ,indexCodeCCAM="CODE_CCAM",indexCodeATC="CODE_ATC",indexCodeICD="CODE_ICD10",
                    indexID="ID_PATIENT",BC_index_surgery="BC_index_surgery"):
    
    '''
    Evaluates patient treatment records to classify each patient's treatment as neoadjuvant, adjuvant, both, or not applicable.
    This classification is determined based on whether the treatments, identified by specific CCAM, ATC, or ICD codes,
    occurred within specified days before or after breast cancer surgery.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records, including columns for patient ID (ID_PATIENT), treatment codes 
        (CODE_CCAM, CODE_ATC, CODE_ICD10), treatment dates (DATE), and an alternate date column (DATE_ENTREE) for use when the primary date is missing.
    CCAM_codes : list
        A list of CCAM codes identifying relevant treatments.
    ATC_codes : list
        A list of ATC codes identifying relevant treatments.
    ICD_Codes : list
        A list of ICD codes identifying relevant treatments.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating the classification of each patient's treatment relative to their surgery date.
    daysBefore : int
        The number of days before surgery within which treatments are considered neoadjuvant.
    daysAfter : int
        The number of days after surgery within which treatments are considered adjuvant.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and their treatment classification ('Neoadjuvant', 'Adjuvant', 'Both', or 'False').
    '''
    
    df['DATE_DIFF'] = df[indexDate] - df[BC_index_surgery]
    
    df = df[(df['DATE_DIFF'] >= -daysBefore) & (df['DATE_DIFF'] <= daysAfter)]

    df['Is_Relevant'] = df[indexCodeCCAM].isin(CCAM_codes) | df[indexCodeATC].isin(ATC_codes) | df[indexCodeICD].isin(ICD_Codes)
    
    patient_classification = {}
    
    for patient_id in df[indexID].unique():
        # Filter the patient's relevant treatments
        patient_df = df[(df[indexID] == patient_id) & df['Is_Relevant']]

        # Skip patients with no relevant treatments
        if patient_df.empty:
            patient_classification[patient_id] = 'False'
            continue

        # Count positive and negative DATE_DIFF values
        positive_count = sum(patient_df['DATE_DIFF'] > 0)
        negative_count = sum(patient_df['DATE_DIFF'] < 0)
        
        # Classify based on the counts
        if positive_count > 0 and negative_count > 0:
            patient_classification[patient_id] = 'Both'
        elif positive_count > 0:
            patient_classification[patient_id] = 'Adjuvant'
        elif negative_count > 0:
            patient_classification[patient_id] = 'Neoadjuvant'
        else:
            patient_classification[patient_id] = 'False'
            

    result = pd.DataFrame(list(patient_classification.items()), columns=[indexID, columnName])

    return result

def chemotherapyIntervals(df,CCAM_codes,ATC_codes,ICD_Codes,columnName,daysBefore,daysAfter
                          ,indexDate="DATE"
                    ,indexCodeCCAM="CODE_CCAM",indexCodeATC="CODE_ATC",indexCodeICD="CODE_ICD10",
                    indexID="ID_PATIENT",BC_index_surgery="BC_index_surgery"):
    
    df['DATE_DIFF'] = df[indexDate] - df[BC_index_surgery]
    
    df = df[(df['DATE_DIFF'] >= -daysBefore) & (df['DATE_DIFF'] <= daysAfter)]
    
    df.sort_values(by=[indexID, indexDate], inplace=True)
    
    df['Is_Relevant'] = df[indexCodeCCAM].isin(CCAM_codes) | df[indexCodeATC].isin(ATC_codes) | df[indexCodeICD].isin(ICD_Codes)
    
    patient_classification = {}
    
    
    for patient_id in df[indexID].unique():

        patient_df = df[(df[indexID] == patient_id) & df['Is_Relevant']]
        
        if patient_df.empty:
            patient_classification[patient_id] = 'False'
            continue
        
        Text = ""
        temp = 0
        c = 0
        for i ,data in patient_df.iterrows():
            if(c==0):
                Text = "0"
                temp = data[indexDate]
            else:
                Text += " -> " + str(data[indexDate]-temp)
                temp = data[indexDate]
                
            c+=1
            
        patient_classification[patient_id] = Text
        
        
    result = pd.DataFrame(list(patient_classification.items()), columns=[indexID, columnName])


    return result

def classify_regimen_chemo(text):

    #Never done a chemotherapy
    if(text=="False"):
        return "False"
    
    numbers = [float(num) for num in re.findall(r'\b\d+\.?\d*\b', text) if float(num) != 0]
    
    #They done only one chemotherapy session
    if(len(numbers)==0):
        return "ONE TREATMENT"
    
    numbers = [21 if num in [20, 22] else num for num in numbers] #To verify 
    numbers = [7 if num in [6, 8] else num for num in numbers] #To verify 
    numbers = [14 if num in [13, 15] else num for num in numbers] #To verify 

    
    def is_paclitaxel(seq): return all(num == 7 for num in seq)
    
    def is_anthracyclines_docetaxel(seq):
        return len(seq) >= 4 and all(num == 14 for num in seq[:3]) and all(num == 21 for num in seq[3:])
    
    def is_anthracyclines_paclitaxel(seq):
        return len(seq) >= 4 and all(num == 14 for num in seq[:3]) and all(num == 7 for num in seq[3:])
    
    def is_anthracyclines_paclitaxel2(seq):

        try:
            transition_index = next(i for i, num in enumerate(seq) if num == 7)
        except StopIteration:
            return False  # No 7-day interval found

        # Check if all intervals before transition are 21-day and after are 7-day
        before_transition = all(num == 21 for num in seq[:transition_index])
        after_transition = all(num == 7 for num in seq[transition_index:])

        return before_transition and after_transition

    def is_anthracyclines(seq): return all(num == 21 for num in seq) #Unknown after March 2012
    
    
    if is_paclitaxel(numbers): return 'Paclitaxel'
    if is_anthracyclines_docetaxel(numbers): return 'Anthracyclines/docetaxel'
    if is_anthracyclines_paclitaxel(numbers): return 'Anthracyclines/paclitaxel'
    if is_anthracyclines_paclitaxel2(numbers): return 'Anthracyclines/paclitaxel'
    if is_anthracyclines(numbers): return 'Anthracyclines'
    return 'Other'

def isDementia(df,columnName):
    
    '''
    Identifies all persons with dementia based on at least one of three criteria:
    1. Anti-Alzheimer drugs claims: At least 2 reimbursements over a 1-year period for anti-Alzheimer drugs 
       (ATC codes: N06DA02, N06DA0, N06DA04, N06DX01).
    2. Hospitalization with the International Classification of Diseases-10th Revision (ICD-10) dementia codes 
       (F00, F01, F02, F03, G30, G31.0, G31.1, F05.1).
    3. At least one hospitalization with a DP, DR, or DA diagnosis of dementia (same ICD-10 codes as above).

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has dementia.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have dementia.
    '''

    
    def determine_dementia(row):
        if row['IS Dementia']:
            return True
        elif not row['Qte Dementia']:
            return False

        elif row['Qte Dementia']>2:
            return True
        else:
            return False
    
    DementiaATC = isTreatedByItWithQte(df,[],data['Disease']['Dementia']['ATC'],[],'Qte Dementia')
    DementiaICD10 = isTreatedByIt(df,[],data['Disease']['Dementia']['ICD10'],[],'IS Dementia')
    
    
    Dementia = pd.merge(DementiaATC,DementiaICD10,on='ID_PATIENT')
    
    
    Dementia[columnName] = Dementia.apply(determine_dementia, axis=1)
    Dementia.drop(['Qte Dementia', 'IS Dementia'], axis=1, inplace=True)
    
    return Dementia
    
def isCOPD(df,columnName):
    '''
    Identifies patients with Chronic Obstructive Pulmonary Disease (COPD) based on specified ICD-10 and ATC codes.

    Criteria:
    - ICD-10 codes: "I278", "I279", "J40", "J41", "J42", "J43", "J44", "J45", "J46", "J47", "J60", "J61", "J62", "J63", "J64", "J65", "J66", "J67", "J684", "J701", "J703", "R03"

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has COPD.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have COPD.
    '''

    
    
    COPD = isTreatedByIt(df,[],data['Disease']['COPD']['ATC'],data['Disease']['COPD']['ICD10'],columnName)
    
    return COPD

def isHypertension(df,columnName):
    '''
    Identifies patients with hypertension based on antihypertensive drug dispensation criteria.

    Criteria:
    - Antihypertensive drugs dispensed at least 3 times during the previous 12 months.

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has hypertension.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have hypertension.
    '''

    
    def determine_hypertension(row):

        if not row['Qte Hypertension']:
            return False

        elif row['Qte Hypertension']>2:
            return True
        else:
            return False
    
    Hypertension = isTreatedByItWithQte(df,[],data['Disease']['Hypertension'],[],'Qte Hypertension')
    Hypertension[columnName] = Hypertension.apply(determine_hypertension, axis=1)
    Hypertension.drop(['Qte Hypertension'], axis=1, inplace=True)
    
    
    return Hypertension
       
def isDiabetes(df,columnName):
    '''
    Identifies patients with diabetes based on specified ICD-10 and ATC codes.

    Criteria:
    - Diabetes mellitus: "E10", "E11", "E12", "E13", "E14", "A10A", "A10B"
    - Complications of diabetes mellitus: "G590", "G632", "G730", "G990", "H280", "H360", "I792", "L97", "M142", "M146", "N083"

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has diabetes.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have diabetes.
    '''

    
    Diabetes = isTreatedByIt(df,[],data['Disease']['Diabetes']['ATC'],data['Disease']['Diabetes']['ICD10'],columnName)
    
    
    return Diabetes

def isCerebrovascular(df,columnName):
    '''
    Identifies patients with cerebrovascular disease based on ICD-10 codes.

    Criteria:
    - Cerebrovascular disease (ICD-10): G45, G46, H340, I60, I61, I62, I63, I64, I65, I66, I67, I68, I69

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has cerebrovascular disease.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have cerebrovascular disease.
    '''
    Cerebrovascular = isTreatedByIt(df,[],[],data['Disease']['Cerebrovascular Disease']['ICD10'],columnName)
    
    
    return Cerebrovascular

def isHeart_failure(df,columnName):
    '''
    Identifies patients with heart failure based on ICD-10 codes.

    Criteria:
    - Heart failure (ICD-10): I50, I11.0, I13.0, I13.2, I13.9, K76.1, J81

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has heart failure.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have heart failure.
    '''
    
    
    Heart_failure = isTreatedByIt(df,[],[],data['Disease']['Heart Failure']['ICD10'],columnName)
    
    
    return Heart_failure

def isMyocardial_infarction(df,columnName):
    '''
    Identifies patients with myocardial infarction based on ICD-10 codes.

    Criteria:
    - Myocardial infarction (ICD-10): I21, I22, I252, I255

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has myocardial infarction.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have myocardial infarction.
    '''

    
    
    Myocardial_infarction = isTreatedByIt(df,[],[],data['Disease']['Myocardial_infarction']['ICD10'],columnName)
    
    
    return Myocardial_infarction

def isChronic_ischaemic(df,columnName):
    '''
    Identifies patients with chronic ischaemic heart disease based on ICD-10 codes, excluding specific codes.

    Criteria:
    - Chronic ischaemic heart disease (ICD-10): I20, I21, I22, I23, I24, I25
    - Excludes I21 and I24 during the year n

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has chronic ischaemic heart disease.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have chronic ischaemic heart disease.
    '''
    
    def determine_chronic_ischaemic(row):

        if row['Without_chronic']:
            return False
        elif row['Chronic Ischaemic Heart Disease']:
            return True
        else:
            return False
    
    Without_chronic = ['I21','I24']
    Chronic_ischaemic = isTreatedByIt(df,[],[],data['Disease']['Chronic Ischaemic Heart Disease']['ICD10'],'Chronic Ischaemic Heart Disease')
    Without_chronic = isTreatedByIt(df,[],[],Without_chronic,'Without_chronic')
    Chronic_ischaemic = pd.merge(Chronic_ischaemic,Without_chronic,on='ID_PATIENT')
    
    Chronic_ischaemic[columnName] = Chronic_ischaemic.apply(determine_chronic_ischaemic,axis=1)
    
    Chronic_ischaemic.drop(['Chronic Ischaemic Heart Disease','Without_chronic'], axis=1, inplace=True)
    
    return Chronic_ischaemic

def isStroke(df,columnName):
    '''
    Identifies patients with acute stroke based on specific ICD-10 codes.

    Criteria:
    - Acute stroke (ICD-10): I60, I61, I62, I63, I64

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has acute stroke.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have acute stroke.
    '''


    Acute_stroke = isTreatedByIt(df,[],[],data['Disease']['Acute Stroke']['ICD10'],columnName)
    
    return Acute_stroke

def isRenal_disease(df,columnName):
    '''
    Identifies patients with renal disease based on specific ICD-10 codes.

    Criteria:
    - Renal disease (ICD-10): I120, I131, N032-N037, N052-N057, N18, N19, N250, Z490, Z491, Z492, Z940, Z992, JAEA003, HNEA002, JVJB001, JVJF004, JVJF008, JVRP004, JVRP007, JVRP008, YYYY007, 2121-2129, 2131, 2132, 2134-2140, 2142-2146, 2334

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has renal disease.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have renal disease.
    '''
    
    
    Renal_disease = isTreatedByIt(df,data['Disease']['Renal Disease']['CCAM'],[],data['Disease']['Renal Disease']['ICD10'],columnName)
    
    return Renal_disease

def isLiver_and_Pancreas(df,columnName):
    
    '''
    Identifies patients with liver and pancreas diseases based on specific ICD-10 codes.

    Criteria:
    - ICD-10 codes: B18, I85, K70-K76, K85, K86, Z94.4

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has liver and pancreas diseases.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have liver and pancreas diseases.
    '''

    
    Liver_and_Pancreas = isTreatedByIt(df,[],[],data['Disease']['Liver and Pancreas']['ICD10'],columnName)
    
    return Liver_and_Pancreas

def isUndernutrition(df,columnName):
    '''
    Identifies patients with undernutrition based on specific ICD-10 codes.

    Criteria:
    - ICD-10 codes: E12, E40, E41, E42, E43, E44, E46, R63, R630, R633, R634, R636, R64

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has undernutrition.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have undernutrition.
    '''

    
    Undernutrition = isTreatedByIt(df,[],[],data['Disease']['Undernutrition']['ICD10'],columnName)

    
    return Undernutrition

def isParkinson(df,columnName):
    
    '''
    Identifies patients with Parkinson's disease based on specific ICD-10 codes.

    Criteria:
    - ICD-10 codes: F02.3, G20

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has Parkinson's disease.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have Parkinson's disease.
    '''
    
    Parkinson = isTreatedByIt(df,[],[],data['Parkinson']['ICD10'],columnName)
    
    return Parkinson

def isEpilepsy(df,columnName):
    
    '''
    Identifies patients with epilepsy based on specific ICD-10 codes.

    Criteria:
    - ICD-10 codes: G40, G41

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has epilepsy.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have epilepsy.
    '''

    
    Epilepsy = isTreatedByIt(df,[],[],data['Disease']['Epilepsy']['ICD10'],columnName)
    
    return Epilepsy

def isPsychiatric_Disease(df,columnName):
    '''
    Identifies patients with psychiatric diseases based on specific ICD-10 criteria.

    Criteria:
    - Schizophrenia and delusional diseases: F20-F25, F28-F29
    - Depression and mood diseases: F30-F34, F38-F45, F48
    - Mental deficiency: F70-F73, F78, F79
    - Substance abuse disorders (drug, alcohol, cannabis): F10-F19
    - Disorders of psychological development: F80-F84, F88-F95, F98

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has a psychiatric disease.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have a psychiatric disease.
    '''

    
    Psychiatric_Disease_ICD10 = data['Disease']['Psychiatric Disease']['Schizophrenia and Delusional Diseases'] +data['Disease']['Psychiatric Disease']['Depression and Mood Diseases']+data['Disease']['Psychiatric Disease']['Mental Deficiency']+data['Disease']['Psychiatric Disease']['Substance Abuse Disorders']+data['Disease']['Psychiatric Disease']['Disorders of Psychological Development']
    
    Psychiatric_Disease = isTreatedByIt(df,[],[],Psychiatric_Disease_ICD10,columnName)
    
    return Psychiatric_Disease

def isPeripheral_vascular(df,columnName):
    '''
    Identifies patients with peripheral vascular diseases based on specific ICD-10 codes.

    Criteria:
    - ICD-10 codes: I70.x, I71.x, I73.1, I73.8, I73.9, I77.1, I79.0, I79.2, K55.1, K55.8, K55.9, Z95.8, Z95.9

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has peripheral vascular disease.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have peripheral vascular disease.
    '''
    
    Peripheral_vascular = isTreatedByIt(df,[],[],data['Disease']['Peripheral Vascular Disease']['ICD10'],columnName)
    
    return Peripheral_vascular

def isDyslipidemia(df,columnName):
    '''
    Identifies patients with dyslipidemia based on specific treatment criteria and absence of associated pathologies.

    Criteria:
    - Delivery on at least 3 occasions in the year:
      - Statins: C10AA, C10BA, C10BX
      - Fibrates: C10AB
      - Other lipid-lowering agents: C10AC, C10AD, C10AX

    Without associated pathology:
    - No code for coronary heart disease (I20, I21, I22, I23, I24, I25)
    - No code for stroke (I60, I61, I62, I63, I64)
    - No code for heart failure (I50, I11.0, I13.0, I13.2, I13.9, K76.1, J81)
    - No code for atherosclerosis of arteries of extremities (I70.2)
    - No code for chronic endstage kidney failure (N184, N185)
    - No code for diabetes mellitus ("E10", "E11", "E12", "E13", "E14", "A10A", "A10B") or complications

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient has dyslipidemia.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they have dyslipidemia.
    '''

    
    def determine_dyslipidemia(row):

        if row['Chronic ischaemic'] or row['Acute stroke'] or row['Heart failure'] or row['AOAOE'] or row['EKF']:
            return False
        elif not row['Qte Dyslipidemia']:
            return False

        elif row['Qte Dyslipidemia']>2:
            return True
        else:
            return False
    
    Dyslipidemia_ATC = data['Disease']['Dyslipidemia']['Statins'] + data['Disease']['Dyslipidemia']['Fibrates'] +data['Disease']['Dyslipidemia']['Other Lipid Lowering Agents']
    
    Dyslipidemia = isTreatedByItWithQte(df,[],Dyslipidemia_ATC,[],'Qte Dyslipidemia')
    
    atherosclerosis_of_arteries_of_extremities = isTreatedByIt(df,[],['I702'],[],'AOAOE')
    
    endstage_kidney_failure = isTreatedByIt(df,[],['N184','N185'],[],'EKF')
    
    
    Chronic_ischaemic = isChronic_ischaemic(df,'Chronic ischaemic')
    Acute_stroke = isStroke(df,'Acute stroke')
    Heart_failure = isHeart_failure(df,'Heart failure')
    
        
    Dyslipidemia = pd.merge(Dyslipidemia,Chronic_ischaemic[['ID_PATIENT','Chronic ischaemic']],on=['ID_PATIENT'])
    Dyslipidemia = pd.merge(Dyslipidemia,Acute_stroke,on=['ID_PATIENT'])
    Dyslipidemia = pd.merge(Dyslipidemia,Heart_failure,on=['ID_PATIENT'])
    Dyslipidemia = pd.merge(Dyslipidemia,atherosclerosis_of_arteries_of_extremities,on=['ID_PATIENT'])
    Dyslipidemia = pd.merge(Dyslipidemia,endstage_kidney_failure,on=['ID_PATIENT'])
    
    Dyslipidemia[columnName] = Dyslipidemia.apply(determine_dyslipidemia, axis=1)
    
    return Dyslipidemia[['ID_PATIENT',columnName]]

def isTobacco(df,columnName):
    '''
    Identifies patients with tobacco use based on specified ICD-10 and ATC codes.

    Criteria:
    - ICD-10 codes: [List of ICD-10 codes for tobacco use]
    - ATC codes: [List of ATC codes for tobacco use treatment]

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient uses tobacco.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they use tobacco.
    '''

    
    Tobacco = isTreatedByIt(df,[],data['Disease']['Tobacco']['ATC'],data['Disease']['Tobacco']['ICD10'],columnName)
    
    return Tobacco

def isAlcohol(df,columnName):
    '''
    Identifies patients with alcohol use based on specified ICD-10 and ATC codes.

    Criteria
    --------
    - ICD-10 codes: [List of ICD-10 codes for alcohol use]
    - ATC codes: [List of ATC codes for alcohol use treatment]

    Parameters
    ----------
    df : DataFrame
        The input DataFrame containing patient treatment records.
    columnName : str
        The name for the output column in the resulting DataFrame, indicating whether each patient uses alcohol.

    Returns
    -------
    DataFrame
        A DataFrame with patient IDs and a boolean indicator of whether they use alcohol.
    '''

    Alcohol = isTreatedByIt(df,[],data['Disease']['Alcohol']['ATC'],data['Disease']['Alcohol']['ICD10'],columnName)
    
    return Alcohol