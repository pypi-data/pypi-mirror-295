from enum import Enum


class DocumentStatus(Enum):
    INTEGRATED = 'INTEGRADO'
    PENDING_INTEGRATION = 'PENDENTE_INTEGRACAO'
    CONVERTER_ERROR = 'ERRO_CONVERSAO'


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


class IntegrationType(Enum):
    SERVICE = 1
    ISS_SERVICE = 2
    PRODUCT = 3
    STOCK_MOVEMENT = 4
    FINISHED_PRODUCT_WITHOUT_PACKAGING = 5
    FINISHED_PRODUCT_WITH_PACKAGING = 6
    PRODUCTION_ORDER = 7
    CORRECTION_NOTE = 8


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
