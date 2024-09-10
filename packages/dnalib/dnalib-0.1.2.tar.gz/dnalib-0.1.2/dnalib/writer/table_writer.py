from dnalib.log import log
from dnalib.utils import Utils
from delta.tables import DeltaTable
from enum import Enum

class WriteModes(Enum):
    """ Classe com os modos de escritas válidos: overwrite, append e upsert. """
    OVERWRITE = "overwrite"    
    APPEND = "append"    
    UPSERT = "upsert"

class TableWriter:
    """ 
        Uma classe que implementa os três modos mais simples de escrita de dados: overwrite (sobreescrita completa), append (equivalente ao insert) e upsert (insert e update). 

        Args:
            table_name (str): string que representa o nome da tabela.
            layer (str): camada da tabela no lake.   
    """

    def __init__(self, table_name, layer):
        """            
            Construtor da classe. 
        """
        self.table_name = table_name
        self.layer = layer        

    def __upsert(self, df_update, merge_condition, source_df_name="source", update_df_name="update", has_checksum_field=False):
        """
            Método interno que executa o upsert.
                
            Args:   
                merge_condition (str): uma condição valida para fazer merge entre o "source_df_name" e o "update_df_name".
                has_checksum_field (bool): uma flag que indica se a tabela tem ou não o campo de checksum.            
        """
        df_source = DeltaTable.forName(Utils.spark_instance(), f"{self.layer}.{self.table_name}")
        # it improves merge performance in write operations
        update_condition = None
        if has_checksum_field:
            update_condition = f"nvl({source_df_name}.checksum, '') != {update_df_name}.checksum"
        # runing a normal merge operation
        (df_source.alias(source_df_name)
            .merge(
                df_update.alias(update_df_name),
                merge_condition
            )
            .whenMatchedUpdateAll(condition=update_condition)
            .whenNotMatchedInsertAll()
            .execute())
        
    def delete(self, key_columns):
        """
        Método que executa a exclusão de dados da tabela com base em uma condição.

        Args:
            key_columns (str): Chaves para realizar o delete.
        
        Returns:
            self: uma instância da classe TableWriter.
        """
            
        delete_condition = f"SELECT concat({key_columns}) FROM vw_table_logs_rownumber WHERE operation = 1"
        try:
            # Referencia a tabela Delta
            df_delete = Utils.spark_instance().sql(f"""DELETE FROM  {self.layer}.{self.table_name}
                           WHERE concat({key_columns}) IN ({delete_condition}) """)                        
            num_affected_rows = df_delete.first()["num_affected_rows"]
            log(__name__).info(f"{num_affected_rows} records where deleted from {self.layer}.{self.table_name}.")
        except Exception as e:
            log(__name__).error(f"Error while trying to delete records from {self.layer}.{self.table_name}: {e}")
            raise

        return self
    
    def __optimize(self):        
        """ 
            Método interno para executar o OPTIMIZE.
        """
        Utils.spark_instance().sql(f"OPTIMIZE {self.layer}.{self.table_name}")

    def persist(self, df, mode=WriteModes.OVERWRITE, partition_fields=[], optimize=True, source_df_name="source", update_df_name="update", merge_condition=None, has_checksum_field=False):              
        """
            Método que implementa escrita de dados no lake, a partir de um dataframe. Aceita um dos três modos: overwrite, append ou upsert.
                
            Args:  
                df (Spark Dataframe): dataframe Spark que vai ser persistido na tabela passada em table_name.
                mode (WriteModes): modo valido de escrita, por padrão é mode = C.OVERWRITE.
                partition_fields (list): uma lista de campos utilizadas para particionar o dataframe antes da escrita, utilizado apenas se mode != WriteModes.UPSERT.
                optimize (bool): se verdadeiro, aplica OPTIMIZE na tabela após a escrita.
                source_df_name (str): um alias para o dataframe da origem (usado apenas se o mode = WriteModes.UPSERT).
                update_df_name (str): um alias para o dataframe de update (usado apenas se o mode = WriteModes.UPSERT).
                merge_condition (str): uma condiçao valida para merge (note que source_df_name = "source" e update_df_name = "updates").
                has_checksum_field (bool): uma flag que indica se a tabela tem ou não o campo de checksum. Se verdadeiro é usado no método whenMatchedUpdateAll, isso implica que apenas registros que mudaram serão realmente reescritos nos arquivos delta.        

            Returns:
                self: uma instância da classe TableWriter.    
        """
        # it prevents to overwrite table if no data is provided
        if df.count() == 0:                                        
            log(__name__).warning(f"No data to persist in {self.table_name}, so nothing will be done.")       
        else:              
            # overwrite or append has same sintax
            if mode.value == WriteModes.OVERWRITE.value or mode.value == WriteModes.APPEND.value:         
                # load df and mode
                df_write = df.write.format("delta").mode(mode.value)
                if mode.value == WriteModes.OVERWRITE.value:
                    df_write = df_write.option("overwriteSchema", "True")
                # verify partitions
                if len(partition_fields) > 0:
                    df_write = df_write.partitionBy(partition_fields)          
                # saving data in delta table                                
                df_write.saveAsTable(f"{self.layer}.{self.table_name}")        
            elif mode.value == WriteModes.UPSERT.value:
                if merge_condition is None:
                    log(__name__).error(f"The merge_condition parameter is required for upsert mode")           
                    raise Exception(f"The merge_condition parameter is required for upsert mode")
                self.__upsert(df, merge_condition)
            else:
                log(__name__).error(f"The mode parameter {mode} is not valid. Valid values are: {[m.value for m in WriteModes]}")            
                raise Exception(f"The mode parameter {mode} is not valid. Valid values are: {[m.value for m in WriteModes]}")
            # runing optimize operation
            if optimize:            
                self.__optimize()
        return self