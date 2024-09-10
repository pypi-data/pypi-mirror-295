from .ConnectOracledb import QueryExecuter
from . import TablesQuery
import pandas as pd
from . import read_file
from concurrent.futures import ThreadPoolExecutor

class RunTables():

    def __init__(self, df, parts_column= 'SE_PN',
                man_columns= 'SE_MAN',
                pathOldDB=r"\\10.199.104.106\Full_Data\Importer_New_Design\Log_Files\Data_Services\Parametric Quality\A.Gamal\PS_Validation_Tool\Old DB.xlsx",
                pathEngName=r"\\10.199.104.106\Full_Data\Importer_New_Design\Log_Files\Data_Services\Parametric Quality\A.Gamal\PS_Validation_Tool\Eng. Name.xlsx",
                top_path=r"\\10.199.104.106\Full_Data\Importer_New_Design\Log_Files\Data_Services\Parametric Quality\A.Gamal\PS_Validation_Tool\Top_Suppliers.xlsx"
                ):    
        self.df= df
        self.parts_column= parts_column
        self.man_columns= man_columns
        self.df[f"{self.parts_column}_lower"]= self.df[self.parts_column].str.lower()
        self.df[f"{self.parts_column}_lower"]= self.df[self.parts_column].str.lower()
        self.pathOldDB= pathOldDB
        self.pathEngName= pathEngName
        self.top_path= top_path
        self.db= QueryExecuter()

    def runVishayTable(self):
        # with ThreadPoolExecutor() as executor:
        #     result = pd.concat(executor.map(lambda hp: self.db.execute_query(TablesQuery.vishayTable(hp[0]), hp[1]), zip(self.placeholders, self.params)), ignore_index=True).drop_duplicates()
        self.placeholders, self.params = self.db.generateParamsPlaceholders(self.df[self.parts_column].dropna().str.lower().unique())
        vis_data= pd.concat([self.db.execute_query(TablesQuery.vishayTable(holder), param ) for holder, param in zip(self.placeholders, self.params)], ignore_index=True).drop_duplicates()
        #merge VishayTable
        self.df= pd.merge(self.df, vis_data, how='left', left_on=[f"{self.parts_column}_lower", self.man_columns], right_on=['LOWER_PART', 'VISHAY_MAN'])
        print('Vishay Table Done.')

    def runDeleteTable(self):
        self.placeholders, self.params = self.db.generateParamsPlaceholders(self.df[f"{self.parts_column}_lower"].dropna().unique())
        with ThreadPoolExecutor() as executor:
            result = pd.concat(executor.map(lambda hp: self.db.execute_query(TablesQuery.deleteTable(hp[0]), hp[1]), zip(self.placeholders, self.params)), ignore_index=True).drop_duplicates()
            result['PART_NUMBER_lower']= result['PART_NUMBER'].str.lower()
        #merge DeleteTable
        self.df= pd.merge(self.df, result, how='left', left_on=[f"{self.parts_column}_lower", self.man_columns], right_on=['PART_NUMBER_lower', 'SUPPLIER'])
        print('Delete Table Done.')

    def flagDeleteTopSupplier(self):
        #read top supplier file and add flags
        top_df=read_file.read(self.top_path)
        self.df['FLAG']= None
        self.df['FLAG'][self.df[self.man_columns].isin(top_df['Supplier'].values)]='TOP SUPPLIER'
        self.df['FLAG'][self.df['PART_NUMBER'].notna()]= 'Delete Table'
        self.df= self.df[self.df['FLAG'].notna()]
        print('TopSupplier Done.')

    def runComponentTable(self):
        self.placeholders, self.params = self.db.generateParamsPlaceholders(self.df[self.parts_column].dropna().unique())
        with ThreadPoolExecutor() as executor:
            result = pd.concat(executor.map(lambda hp: self.db.execute_query(TablesQuery.componentTable(hp[0]), hp[1]), zip(self.placeholders, self.params)), ignore_index=True).drop_duplicates()
            result['COM_PARTNUM_lower']= result['COM_PARTNUM'].str.lower()
        #merge ComponentTable
        self.df= pd.merge(self.df, result, how='left', left_on=[f"{self.parts_column}_lower", self.man_columns], right_on=['COM_PARTNUM_lower', 'MAN_NAME'])
        print('Component Table Done.')
    
    def runPCNTable(self):
        with ThreadPoolExecutor() as executor:
            result = pd.concat(executor.map(lambda hp: self.db.execute_query(TablesQuery.pcnTable(hp[0]), hp[1]), zip(self.placeholders, self.params)), ignore_index=True)
            latest_idx = result.groupby(['PCN_PART', 'PCN_MAN_NAME'])['NOTIFICATION_DATE'].idxmax()
            # Select rows using the indices of the latest dates
            latest_pcns = result.loc[latest_idx].reset_index(drop=True).drop_duplicates()
            latest_pcns['PCN_PART_lower']= latest_pcns['PCN_PART'].str.lower()
        #merge PCNTable
        self.df= pd.merge(self.df, latest_pcns, how='left', left_on=[f"{self.parts_column}_lower", self.man_columns], right_on=['PCN_PART_lower', 'PCN_MAN_NAME'])
        print('PCN Table Done.')

    def runArrowTable(self):
        # to get all rgiht parts from cm then pcn then delete then input part column
        # cause i can run LOWER in the query fo all these table, except arrow table cause it take huge time, 
        partsToRunOnArrow = self.df.apply(  
                                    lambda x: 
                                        x['VISHAY_PARTS'] if pd.notna(x['VISHAY_PARTS'])
                                        else x[self.parts_column], 
                                    axis=1)
        partsToRunOnArrow= pd.concat([partsToRunOnArrow, self.df[self.parts_column].dropna().str.upper(), self.df[self.parts_column].dropna().str.lower()]).dropna().unique()  
        self.placeholders, self.params = self.db.generateParamsPlaceholders(partsToRunOnArrow )
        with ThreadPoolExecutor() as executor:
            result = pd.concat(executor.map(
                lambda hp: self.db.execute_query(TablesQuery.arrowTable(hp[0]), hp[1]), zip(self.placeholders, self.params) 
                ), ignore_index=True).drop_duplicates()
            result['Arrow Price List_lower']= result['Arrow Price List'].str.lower()
            result= result.drop_duplicates(subset=['Arrow Price List_lower', 'ARROW_MAN_NAME'])
        #merge ArrowTable
        self.df= pd.merge(self.df, result, how='left', left_on=[f"{self.parts_column}_lower", self.man_columns], right_on=['Arrow Price List_lower', 'ARROW_MAN_NAME'])
        print('Arrow Table Done.')
   
    def runFastTable(self):
        self.placeholders, self.params = self.db.generateParamsPlaceholders( self.df['COM_ID'].dropna().astype(str).unique() )
        with ThreadPoolExecutor() as executor:
            result = pd.concat(executor.map(lambda hp: self.db.execute_query(TablesQuery.fastTable(hp[0]), hp[1]), zip(self.placeholders, self.params)), ignore_index=True).drop_duplicates()
        self.df= pd.merge(self.df, result, how='left', left_on=['COM_ID'], right_on=['FAST_TABLE'])
        self.df['FAST_TABLE'][self.df['FAST_TABLE'].notna()]= 'YES'
        print('Fast Table Done.')
    
    def runLifecycleTable(self):
        with ThreadPoolExecutor() as executor:
            result = pd.concat(executor.map(lambda hp: self.db.execute_query(TablesQuery.lifecycleTable(hp[0]), hp[1]), zip(self.placeholders, self.params)), ignore_index=True).drop_duplicates()
        grouped_data_concat =result.groupby('LC_COM_ID').apply(
            lambda x: x[x['LATEST']==1] if any(x['LATEST']==1) else x[x['LIFECYCLE_SOURCE'].notna()].drop_duplicates(subset='LC_COM_ID', keep='last')
            ).reset_index(drop=True)
        self.df= pd.merge(self.df, grouped_data_concat, how='left', left_on=['COM_ID', self.man_columns], right_on=['LC_COM_ID', 'LC_MAN_NAME'])
        print('Lifecycle Table Done.')

    def flagOldDB(self):
        old= read_file.read(self.pathOldDB)
        old= old.drop_duplicates(subset=['Part','Vendor'], keep='last')
        old_columns_target= ['Status','Comment','More_Details','Right PN','Right Supplier','Source']
        self.df[old_columns_target]= pd.merge(self.df, old, how='left', left_on=[self.parts_column, self.man_columns], right_on=['Part', 'Vendor'])[old_columns_target].values
        print('OldDB Done.')

    def flagEngName(self):
        eng= read_file.read(self.pathEngName)
        self.df['Eng. Name']= pd.merge(self.df, eng, how='left', left_on='PL_NAME', right_on='PL Name')['Eng. Name'].values
        self.df['Eng. Name'][self.df['COM_ID'].isna()] = 'No Match Part'
        print('Eng Name Done.')

    def runAll(self):
        self.runVishayTable()
        self.runDeleteTable()
        self.flagDeleteTopSupplier()
        self.runComponentTable()
        self.runPCNTable() 
        self.runArrowTable()
        self.runFastTable()
        self.runLifecycleTable()
        self.flagOldDB()
        self.flagEngName()

    def getUpdatedDF(self):
        return self.df






        



    
