import oracledb
from pandas import DataFrame
import os
from read_file import read

class QueryExecuter:
    def __init__(self):

        # Get the directory where this script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        instant_client_path = os.path.join(current_dir, 'instantclient')
        oracledb.init_oracle_client(lib_dir=instant_client_path)
        try:
            config= read(r"Config.txt")
        except:
            config_path = os.path.join(current_dir, 'Config.txt')
            config= read(config_path)
        username=config['username'][0]
        password=config['password'][0]
        host=config['host'][0]
        port=config['port'][0]
        sid=config['sid'][0]
        connection = oracledb.connect(user=username, password=password, host=host, port=port, sid=sid)
        self.connection= connection
        print("Connection successful.")
        

    def generateParamsPlaceholders(self, parts, chunk_size=995):
        """
        Generates placeholders for SQL queries in chunks based on batch size.
        and Generates parameters for SQL queries in chunks based on batch size.
    
        :return: A tuple of list of chunks, placeholders and params
        """
        # Create placeholder pairs for each part and man
        x = [f"(:place{i})" for i in range(len(parts))]
        placeholders = [', '.join(x[i: i + chunk_size]) for i in range(0, len(x), chunk_size)]
        #Generates parameters for SQL queries in chunks based on batch size.
        params = [ {
            f"place{idx+i}": part 
            for idx, part in enumerate(parts[i:i+chunk_size])
            }  
            for i in range(0, len(parts), chunk_size)
            ]
        return placeholders, params

    def execute_query(self, query, param=None):
        try:
            with self.connection.cursor() as cursor:
                # Set session parameters for case-insensitive search
                cursor.execute(query, param)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                return DataFrame(rows, columns=columns)
        except oracledb.DatabaseError as e:
            print("There was a problem executing the query: ", e)
            raise 