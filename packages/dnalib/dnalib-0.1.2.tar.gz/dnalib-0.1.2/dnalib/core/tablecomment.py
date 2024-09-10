from dnalib.utils import TableUtils, Utils
from dnalib.log import log

class TableComment:             
    """
        Classe construída para compilar o template do comentário da tabela, seguindo os critérios do catalogo do Atlan.

        Args:
            layer (str): camada da tabela no lake.   
            table_name (str): string que representa o nome da tabela.
            yml (yml object or str, optional): caminho do arquivo yml ou instância do objeto com os parâmetros necessários para o Create Table. Padrão é None.
            anonimized_fields (list, optional): lista de campos para serem anonimizados.
            comment (dict, optional): dicionário com o padrão table_comment_atlan_pattern.key:comment (veja TableComment.table_comment_atlan_pattern). Se não for informado, será inferido a partir do yml.
            comment_squad (dict, optional): dicionário com o padrão table_comment_atlan_pattern.key:comment_squad (veja TableComment.table_comment_atlan_pattern). Se não for informado, será inferido a partir do yml.

        Attributes:
            table_comment_atlan_pattern (dict): dicionário com as chaves para o comentário da tabela, seguindo os critérios do catalogo do Atlan.
            yml (yml object ou None): instância do objeto yml, é None caso nenhum arquivo seja informado.
            layer (str): camada da tabela no lake.   
            table_name (str): string que representa o nome da tabela.
            anonimized_fields (list): lista de campos para serem anonimizados.
            comment (dict): dicionário com o padrão table_comment_atlan_pattern.key.
            comment_squad (dict): dicionário com o padrão table_comment_atlan_pattern.key.
            parsed_comment (str): string com o template do comentário da tabela compilado, preenchido após a chamada do método parse.
            comment_complete (dict): merge entre os dicionários comment e comment_squad, preenchido após a chamada do método parse.
            parsed_template (str): template do comentário da tabela compilado, preenchido após a chamada do método parse.
    """ 

    table_comment_atlan_pattern = {
        'descricao': '- **Descrição**:',
        'sistema_origem': '- **Sistema Origem**:',
        'calendario': '- **Calendário de Disponibilização**:',
        'tecnologia': '- **Tecnologia Sistema Origem**:',
        'camada': '- **Camada de Dados**:',
        'peridiocidade': '- **Periodicidade de Atualização**:',
        'retencao': '- **Período de Retenção**:',
        'vertical': '- **Vertical**:',
        'dominio': '- **Domínio**:',
        'gi': '- **GI - Gestor da Informação**:',
        'gdn': '- **GDN - Gestor de Negócio**:',
        'curador': '- **Curador**:',
        'custodiante': '- **Custodiante**:',
        'squad': '- **Squad Responsável**:',
        'categoria_portosdm': '- **Categoria e Grupo PortoSDM**:',
        'confidencialidade': '- **Classificação da Confidencialidade**:',
        'classificacao': '- **Classificacao**:',
        'campos_anonimizados': '- **Campos Anonimizados**:'
    }

    def __init__(self, 
                 layer, 
                 table_name, 
                 yml=None, 
                 anonimized_fields=[], 
                 comment={}, 
                 comment_squad={}):
        self.yml = yml
        # yml must be either a string or a dict from the yml file
        if isinstance(self.yml, str):
            self.yml = Utils.safe_load_and_parse_yml(yml)
        self.table_name = table_name.strip().lower()
        self.layer = layer.strip().lower()   
        self.anonimized_fields = anonimized_fields
        self.comment = comment
        self.comment_squad = comment_squad
        self.parsed_comment = ""
        self.comment_complete = {}
        self.parsed_template = ""

    
    def __load_and_verify_params(self):
        """
            Método interno que carrega as estruturas principais para popular os comentários da tabela.

            Raises:
                ValueError: Ocorre se alguma das estruturas comment ou comment_squad não forem informadas. Ou devem ser passadas por parâmetros, ou devem estar dentro do yml.
        """
        
        if len(self.anonimized_fields) == 0 and self.yml != None:
            if "anonimized_fields" in self.yml:    
                self.anonimized_fields = self.yml["anonimized_fields"]

        if len(self.comment) == 0:
            if not "comment" in self.yml:
                log(__name__).error(f"If not informed, the comment parameter is required in yml table template for {self.layer} layer.")
                raise ValueError(f"If not informed, the comment parameter is required in yml table template for {self.layer} layer.")  
            self.comment = self.yml["comment"]

        if len(self.comment_squad) == 0:
            if not "comment_squad" in self.yml:
                log(__name__).error(f"If not informed, the comment_squad parameter is required in yml table template for {self.layer} layer.")
                raise ValueError(f"If not informed, the comment_squad parameter is required in yml table template for {self.layer} layer.")  
            self.comment_squad = self.yml["comment_squad"]

        # merge both dicts
        self.comment_complete = {**self.comment, **self.comment_squad}
        self.comment_complete["campos_anonimizados"] = ", ".join(self.anonimized_fields)
        
    def parse(self): 
        """
            Método que faz o parse dos comentários baseados na estrutura do Atlan. Os valores estão no dicionário TableComment.table_comment_atlan_pattern.

            Returns:
                self: a instância da classe TableComment.

            Raises:
                ValueError: Se a estrutura do comentário não for informada corretamente (ou seja, se faltar alguma chave).
        """

        self.__load_and_verify_params()                      
        for key in self.table_comment_atlan_pattern:
            if not key in self.comment_complete:
                log(__name__).error(f"You must inform the parameter {key} in table comment.")
                raise ValueError(f"You must inform the parameter {key} in table comment.")
            else:                
                self.parsed_comment += f"{self.table_comment_atlan_pattern[key]} {TableUtils.format_comment_content(self.comment_complete[key])}\n"
        return self
    
    def template(self):             
        """
            Método que constroí o template da estrutura do comentário da tabela baseado nos parâmetros informados.

            .. code-block:: SQL

                COMMENT ON TABLE layer.table_name IS "comentário compilado"
            
            Returns:
                self: a instância da classe TableComment.
        """   

        self.parse()    
        self.parsed_template = """
            COMMENT ON TABLE {}.{} IS "{}"
        """.format(self.layer, self.table_name, self.parsed_comment)           

        return self             

    def execute(self):        
        """
            Método que executa todo processo para gerar e escrever o comentário da tabela.              
            
            Returns:                
                self: a instância da classe TableComment.

            Raises:
                Exception: Se a tabela informada não existir.
        """

        # verify if table exists
        if not TableUtils.table_exists(self.layer, self.table_name):
            log(__name__).error(f"Table {self.layer}.{self.table_name} does not exist")
            raise Exception(f"Table {self.layer}.{self.table_name} does not exist")

        # generate final template
        self.template()

        # run comment on table
        Utils.spark_instance().sql(self.parsed_template)        
        return self
