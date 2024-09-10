from .read_file import read
from .Validation import ProcessingDecision as ps_pandas
from .FinalDecision import finalDecision
from .TablesData import RunTables
from .ConnectOracledb import QueryExecuter
from . import ParsePDF
import re
import time
import os
from pandas import read_csv
# Regex pattern to match illegal characters
ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

def remove_illegal_characters(value):
    """Removes illegal characters from a string."""
    if isinstance(value, str):
        return ILLEGAL_CHARACTERS_RE.sub("}", value)
    return value

def process_data(part_column_name, man_column_name, input_file):
    """Processes the input file, runs validation, and saves the cleaned data to an output file."""

    cc= read_csv(r'https://docs.google.com/spreadsheets/d/e/2PACX-1vSJnwTDdwXbCNZepA6r8XsQxBPuXm4h2-zAeg3e2ZnsaKB8Poe6ISWQVLIos5ZkFzWyRVpoWTa81xhQ/pub?gid=0&single=true&output=csv')
    if cc['Running'][cc['Tool_Name']== 'ps_validation'].astype(str).tolist()[0].lower() !='true':
        raise StopAsyncIteration
    start_time= time.time()
    # Read and clean input file
    df = read(input_file)
    df = df.drop_duplicates()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        config= read(r"Config.txt")
        print("ManualConfig")
    except:
        config_path = os.path.join(current_dir, 'Config.txt')
        config= read(config_path)
        print("PreConfig")
        
    auto_engine= config['local_server'][0]
    # Process Tables Data
    tb = RunTables(df, part_column_name, man_column_name,
                pathOldDB=rf"{auto_engine}\Full_Data\Importer_New_Design\Log_Files\Data_Services\Parametric Quality\A.Gamal\PS_Validation_Tool\Old DB.xlsx",
                pathEngName=rf"{auto_engine}\Full_Data\Importer_New_Design\Log_Files\Data_Services\Parametric Quality\A.Gamal\PS_Validation_Tool\Eng. Name.xlsx",
                top_path=rf"{auto_engine}\Full_Data\Importer_New_Design\Log_Files\Data_Services\Parametric Quality\A.Gamal\PS_Validation_Tool\Top_Suppliers.xlsx"
                )
    tb.runAll()
    df = tb.getUpdatedDF()

    # Extract PDF data
    pdf_data = ParsePDF.GetPDFText(df['DATASHEET'].dropna().unique())
    # Run PN Validation on Datasheet
    df[['DECISION_DATASHEET', 'EQUIVALENT_DATASHEET', 'SUFFIXS_DATASHEET', 'POSITIONS_DATASHEET']]= None
    df = df.apply(ps_pandas(part_column_name, 'DATASHEET', pdf_data).MakeDecision, axis=1)
    print('Part Validation Done.')
    # Run PN Validation on PCN
    pcn_data = ParsePDF.GetPDFText(df['PCN_URL'].dropna().unique())
    df[['DECISION_PCN_URL', 'EQUIVALENT_PCN_URL', 'SUFFIXS_PCN_URL', 'POSITIONS_PCN_URL']]= None
    df = df.apply(ps_pandas(part_column_name, 'PCN_URL', pcn_data).MakeDecision, axis=1)
    print('PCN Validation Done.')
    # Select required columns
    required_columns = [
        'COM_ID', part_column_name, man_column_name, 'DATASHEET', 'PL_NAME', 'DESCRIPTION', 'FLAG',
        'ISSUE_TYPE', 'MORE_DETAILS', 'CORRECT_PART', 'CORRECT_SUPPLIER', 'INSERTION_DATE',
        'DECISION_DATASHEET', 'EQUIVALENT_DATASHEET', 'SUFFIXS_DATASHEET', 'POSITIONS_DATASHEET',
        'LIFECYCLE_STATUS', 'LIFECYCLE_SOURCE', 'LC_SOURCE_TYPE', 'CONTACTING_SUPPLIER',
        'FAST_TABLE', 'FAST_COMMENT',
        'Arrow Price List',
        'VISHAY_PARTS',
        'PCN_URL',
        'DECISION_PCN_URL', 'EQUIVALENT_PCN_URL', 'SUFFIXS_PCN_URL', 'POSITIONS_PCN_URL',
        'Status', 'Comment', 'More_Details', 'Right PN', 'Right Supplier', 'Source', 'Eng. Name'
    ]
    # Clean illegal characters
    df_cleaned = df.applymap(remove_illegal_characters)

    # Final decision processing
    final_df = finalDecision(df_cleaned[required_columns])

    # Save the cleaned data to an Excel file
    final_df.to_excel(input_file.replace('.xlsx','_Ouput.xlsx'), index=False, engine='openpyxl')

    rows= final_df.shape[0]
    valid= final_df[final_df['Decision']!='Need Check'].shape[0]
    checks= final_df[final_df['Decision']=='Need Check'].shape[0]
    data= time.strftime('%Y-%m-%d %H.%M')

    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)

    connection= QueryExecuter().connection
    query=f"""INSERT INTO PS_VALIDATION(DATETIME, USER_ID, TOTAL_ROWS, NUM_VALID, NUM_CHECK, RUNTIME)
        VALUES ('{data}', '{os.getlogin()}', {rows}, {valid}, {checks}, '{hours:02}:{minutes:02}:{seconds:02}')"""
    connection.cursor().execute(query)
    connection.commit()
    print('The Output file exported.')