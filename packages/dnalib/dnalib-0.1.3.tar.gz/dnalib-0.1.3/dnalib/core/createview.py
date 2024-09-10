from dnalib.utils import TableUtils, Utils
from .tablecomment import TableComment
from dnalib.log import log

class CreateView:
    """
        Classe que implementa a criação de views voltadas ao consumo da área de negócios. As views fazem hash dos campos indicados como anonimizados.

        Args:
            schema (df.schema): schema do dataframe, mesmo que df.schema.
            layer (str): camada da tabela no lake.   
            table_name (str): string que representa o nome da tabela.
            yml (yml object or str, optional): caminho do arquivo yml ou instância do objeto com os parâmetros necessários para o Create View. Padrão é None.
            parsed_comment (str, optional): string com comentário parseado a partir da TableComment. Se não for informado é obtido a partir de uma istância de TableComment.
            anonimized_fields (list, optional): lista de campos para serem anonimizados.            
            fields (dict, optional): dicionário com o padrão field_name:comment. Se não for informado, será inferido a partir do yml.
            replace (bool, optional): opção que força o replace da tabela caso ela exista. Por padrão é False.

        Attributes:
            schema (df.schema): schema do dataframe, mesmo que df.schema.
            layer (str): camada da tabela no lake.   
            table_name (str): string que representa o nome da tabela.
            yml (yml object ou None): instância do objeto yml, é None caso nenhum arquivo seja informado.
            parsed_comment (str): string com comentário parseado.
            anonimized_fields (list): lista de campos para serem anonimizados.
            fields (dict): dicionário com o padrão field_name:comment. 
            replace (bool): opção que força o replace da tabela caso ela exista. Por padrão é False.
            parsed_template (str): template do comentário da tabela compilado, preenchido após a chamada do método parse.
            parsed_fields (str): string com os comentários das fields parseados no padrão do Create View, preenchido após a chamada do método parse_fields().
    """

    def __init__(self, 
                 schema,
                 layer, 
                 table_name, 
                 yml=None,                   
                 parsed_comment=None, 
                 anonimized_fields=[],   
                 comment={},
                 comment_squad={},               
                 fields={},
                 replace=False):                                 
        self.yml = yml
        self.replace = replace 
        # yml must be either a string or a dict from the yml file        
        if isinstance(self.yml, str):
            self.yml = Utils.safe_load_and_parse_yml(yml)
        self.table_name = table_name.strip().lower()
        self.schema = schema
        self.layer = layer.strip().lower()   
        self.parsed_comment = parsed_comment
        if self.parsed_comment is None: 
            self.parsed_comment = TableComment(layer, table_name, yml, anonimized_fields, comment, comment_squad).parse().parsed_comment
        self.anonimized_fields = anonimized_fields
        self.fields = fields
        self.parsed_template = ""
        self.parsed_fields = ""
    
    # by default the python parameter overwrite the yml if both are informed
    def __load_and_verify_params(self):
        """
            Método interno que carrega as estruturas principais para popular a estrutura da view.

            Raises:
                ValueError: Ocorre se a estrutura fields não for passada. Ou deve se passada por parâmetro, ou deve estar dentro do yml.
        """

        if len(self.anonimized_fields) == 0 and self.yml != None:
            if "anonimized_fields" in self.yml:    
                self.anonimized_fields = self.yml["anonimized_fields"]

        if len(self.fields) == 0:
            if not "fields" in self.yml:
                log(__name__).error(f"If not informed, the fields parameter is required in yml table template for {self.layer} layer.")
                raise ValueError(f"If not informed, the fields parameter is required in yml table template for {self.layer} layer.")  
            self.fields = self.yml["fields"]

            # we manually insert dataCarga to the object (if it is passed it will be generated in comments)
            if "dataCarga" in self.schema.names:            
                #self.fields["dataCarga"] = "Data de carga dos dados."
                self.fields["dataCarga"] = ["Data de carga dos dados.", 'timestamp', None, None]

    def parse(self):
        """
            Método que faz o parse dos comentários baseados na estrutura do Atlan. 

            Returns:
                self: a instância da classe CreateView.
        """

        self.__load_and_verify_params()
        list_of_parsed_fields = ["{} COMMENT '{}'".format(field_name, TableUtils.format_comment_content(self.fields[field_name][0])) for field_name in self.schema.names]
        self.parsed_fields = ", ".join(list_of_parsed_fields)
        return self        
    
    def template(self):   
        """
            Método que constroí o template da estrutura da view.

            .. code-block:: SQL

                CREATE OR REPLACE VIEW layer.table_name_vw (parsed_fields)                
                    COMMENT "parsed_comment"
                AS
                    SELECT fields FROM layer.table_name
            
            Returns:
                self: a instância da classe CreateView.
        """

        # parsed fields
        self.parse()   
        
        list_of_fields = []
        # take each field and format do hash it
        for field in self.schema.names:            
            list_of_fields.append(TableUtils.hash_field_str(field) if field in self.anonimized_fields else field)
          
        self.parsed_template = """
            CREATE OR REPLACE VIEW {}.{}_vw             
            ({}) 
            COMMENT "{}"
            AS
            SELECT {} FROM {}.{}
        """.format(self.layer, self.table_name, self.parsed_fields, self.parsed_comment, ", ".join(list_of_fields), self.layer, self.table_name)         
        return self
    
    def execute(self):        
        """
            Método que executa todo processo para gerar e escrever a view.              
            
            Returns:                
                self: a instância da classe CreateView.

            Raises:
                ValueError: Se a tabela informada não existir.
        """
        
        # verify if table exists
        if not TableUtils.table_exists(self.layer, self.table_name):
            log(__name__).error(f"Table {self.layer}.{self.table_name} does not exist")
            raise ValueError(f"Table {self.layer}.{self.table_name} does not exist")

        if not TableUtils.view_exists(self.layer, self.table_name) or self.replace:
            # generate final template
            self.template()

            # creating view
            Utils.spark_instance().sql(self.parsed_template)  
        else:
            log(__name__).warning(f"The view {self.layer}.{self.table_name}_vw already exists, so nothing will be done. To replace the view, set the parameter replace=True.")
        return self
