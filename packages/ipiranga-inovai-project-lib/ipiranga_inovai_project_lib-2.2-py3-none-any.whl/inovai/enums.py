from enum import Enum, IntEnum


class DocumentStatus(Enum):
    INTEGRATED = 'INTEGRADO'
    PENDING_INTEGRATION = 'PENDENTE_INTEGRACAO'
    CONVERTER_ERROR = 'ERRO_CONVERSAO'


class IntegrationStatus(Enum):
    SENDED = 'ENVIADO'
    INTEGRATED = 'INTEGRADO'
    PENDING_INTEGRATION = 'PENDENTE_INTEGRACAO'
    CONVERTER_ERROR = 'ERRO_CONVERSAO'
    ERROR = "ERRO"


class BatchStatus(Enum):
    PENDING = 'PENDENTE'
    INTEGRATED = 'INTEGRADO'
    ERROR = "ERRO"


class DocumentMovementType(Enum):
    INPUT = 'E',
    OUTPUT = 'S'


class ResponsibleMovement(Enum):
    ISSUER = 'EMITENTE'
    RECIPIENT = 'DESTINATARIO'


class Origin(Enum):
    JDE = "JDE"
    ABADI = "ABADI"


class DocumentType(Enum):
    SERVICE = 'SERV'
    PRODUCT = 'PROD'
    ISS_SERVICE = "SERV_ISS"


class IntegrationType(IntEnum):
    SERV = 1
    SERV_ISS = 2
    PROD = 3
    MOVIMENTACAO_ESTOQUE = 4
    PRODUTO_ACABADO_SEM_EMBALAGEM = 5
    PRODUTO_ACABADO_COM_EMBALAGEM = 6
    ORDEM_PRODUCAO = 7
    CORRECAO_APONTAMENTO = 8
    DEFAULT = 9


class TaxType(Enum):
    PIS = "PIS"
    IPI = "IPI"
    ISS = "ISS"
    INSS = "INSSRet"
    COFINS = "COFINS"
    ISSRET = "ISSRET"
    ICMS = "ICMS"
    ICMSST = "ICMSST"
    ICMSFCP = "ICMSFCP"
    ICMSFCPST = "ICMSFCPST"
    ICMSMONORETEN = "ICMSMONORETEN"
    ICMSMONOPROP = "ICMSMONOPROP"
    ICMSMONODIFER = "ICMSMONODIFER"
    ICMSMONORET = "ICMSMONORET"
    CSLL = "CSLL"
    IRRF = "IRRF"


class KitId(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    SEVEN = 7
    EIGHT = 8
    NINE = 9
