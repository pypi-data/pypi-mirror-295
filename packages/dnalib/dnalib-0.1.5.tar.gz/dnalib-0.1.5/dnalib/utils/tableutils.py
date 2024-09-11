from pyspark.sql import SparkSession
from .utils import Utils 
from dnalib.log import log
from delta.tables import DeltaTable

class TableUtils:

    #  
    #   Description:
    #       This method formats a comment (for field or table).
    #
    #   Parameters:      
    #       comment_content = the content of the comment.
    # 
    @staticmethod
    def format_comment_content(comment_content):
        # remove whitespaces        
        if len(comment_content) > 0:
            value = comment_content.strip()
            # insert ponctuation at the end of string
            if value[-1] != '.':
                value += '.'
            # first digit in upper case        
            return value[0].upper() + value[1:]
        else: 
            return comment_content

    #  
    #   Description:
    #       This method formats a field to a hash type.
    #
    #   Parameters:      
    #       layer = field name to be a hashed field
    # 
    @staticmethod
    def hash_field_str(field):        
        return f"sha2(cast({field} as string), 256) AS {field}"

    #  
    #   Description:
    #       This method loads a dataframe from path (usefull if table does not exists in catalog yet).
    #
    #   Parameters:      
    #       layer = table layer (bronze, silver, gold, diamond or export)
    #       table_name = the name of the table.    
    # 
    @staticmethod
    def load_df_from_lakehouse(layer, table_name):        
        root_path = Utils.lakehouse_path()
        try:
           df = Utils.spark_instance().read.load(f'{root_path}/{layer}/{table_name}')
        except:
            log(__name__).error(f"Unable to read '{root_path}/{layer}/{table_name}'")
            raise Exception(f"Unable to read '{root_path}/{layer}/{table_name}'")
        return df
    #  
    #   Description:
    #       This method gets schema table from path (usefull if table does not exists in catalog yet).
    #
    #   Parameters:      
    #       layer = table layer (bronze, silver, gold, diamond or export)
    #       table_name = the name of the table.    
    #     
    @staticmethod
    def table_schema_from_lakehouse(layer, table_name):                        
        return TableUtils.load_df_from_lakehouse(layer, table_name).schema
    
    #  
    #   Description:
    #       This method checks if a view exists from a table name in catalog.
    #
    #   Parameters:      
    #       layer = table layer (bronze, silver, gold, diamond or export)
    #       table_name = the name of the table.    
    # 
    @staticmethod
    def view_exists(layer, table_name):                                
        return Utils.spark_instance().catalog.tableExists(f"{layer}.{table_name}_vw")        
    
    #  
    #   Description:
    #       This method checks if a table exists in catalog.
    #
    #   Parameters:      
    #       layer = table layer (bronze, silver, gold, diamond or export)
    #       table_name = the name of the table.    
    # 
    @staticmethod
    def table_exists(layer, table_name):        
        #return Utils.spark_instance()._jsparkSession.catalog().tableExists(f"{layer}.{table_name}")
        try:
            DeltaTable.forName(Utils.spark_instance(), f"{layer}.{table_name}")
            return True
        except:
            return False
            
    #  
    #   Description:
    #       This method drop the table and remove data from lakehouse (delete path files).
    #
    #   Parameters:      
    #       layer = table layer (bronze, silver, gold, diamond or export)
    #       table_name = the name of the table.    
    #
    @staticmethod
    def drop_table(layer, table_name):
        Utils.spark_instance().sql(f"drop table if exists {layer}.{table_name}")
        is_removed = Utils.remove_table_from_lakehouse(layer, table_name)
        if not is_removed:
            log(__name__).warning(f"Table {layer}.{table_name} does not exists in lakehouse")  

    #  
    #   Description:
    #       This method drop the view from a table.
    #
    #   Parameters:      
    #       layer = table layer (bronze, silver, gold, diamond or export)
    #       table_name = the name of the table.    
    #
    @staticmethod
    def drop_view(layer, table_name):
        Utils.spark_instance().sql(f"drop view if exists {layer}.{table_name}_vw")        
                            