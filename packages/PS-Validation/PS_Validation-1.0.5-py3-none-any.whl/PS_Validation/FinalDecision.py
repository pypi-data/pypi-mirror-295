def finalDecision(df):
    # Initialize the 'Decision' column and the new columns with None
    df['Decision'] = None
    new_columns = ['New_Status', 'New_Comment', 'New_More_Details','New_Right PN', 'New_Right Supplier', 'New_Source']
    df[new_columns] = None

    # Apply conditions to update the DataFrame
    vishay_condition = df['VISHAY_PARTS'].notna()
    old_db_condition = df[['Status', 'Comment', 'More_Details', 'Right PN', 'Right Supplier', 'Source']].notna().any(axis=1)

    # Update based on Vishay Parts presence
    df.loc[vishay_condition, ['Decision', 'New_Status', 'New_Source']] = ['Valid', 'Valid', 'Vishay Quality']

    # Update based on old database values if 'Decision' is still None
    df.loc[df['Decision'].isna() & old_db_condition, 'Decision'] = 'OldDB'
    df.loc[df['Decision'] == 'OldDB', new_columns] = df.loc[df['Decision'] == 'OldDB', ['Status', 'Comment', 'More_Details','Right PN', 'Right Supplier', 'Source']].values


    df['Decision'][(df['Decision'].isna()) & (df['Arrow Price List'].notna())]= 'Valid_Need check supplier format'

    df['Decision'][(df['Decision'].isna()) & (df['DECISION_PCN_URL']=='EXACT')]= 'Valid_Need check supplier format'

    df['Decision'][(df['Decision'].isna()) & (df['DECISION_DATASHEET']=='EXACT')]= 'Valid_Need check supplier format'

    df.loc[df['Decision'].isna() , 'Decision']= 'Need Check'
    return df