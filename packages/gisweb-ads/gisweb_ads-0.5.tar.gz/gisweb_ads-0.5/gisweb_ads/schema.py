from typing import Any
from pydantic import BaseModel, EmailStr

class IAmministrazione(BaseModel):
    Denominazione: str
    CodiceAOO: str
    CodiceEnte: str
    IndirizzoTelematico: EmailStr

class IConfigProtocollo(BaseModel):
    wsUrl: str
    wsUser: str
    wsEnte: str
    wsPassword: str
    amministrazione: IAmministrazione
    applicativo: str | None = None
    
class BaseRet(BaseModel):
    lngErrNumber: int = 0
    strErrString: str = ''

class ILoginRet(BaseRet):
    strDST: str | None
    
class IProtocolloResult(BaseRet):
    lngNumPG: int = 0
    lngAnnoPG: int = 0
    strDataPG: str = ''
    lngDocID: int = 0


class IAllegatoProtocollo(BaseModel):
    id: int | None = None
    descrizione: str
    tipo: str
    nome: str
    content: Any
    size: int
    mimetype: str
    ext: str

class IFascicolo(BaseModel):
    numero: str = ""
    anno:str = ""
    
class IParametro(BaseModel):
    nome: str
    valore: str

class ISoggettoProtocollo(BaseModel):

    Nome: str | None = None
    Cognome: str | None = None
    Denominazione: str | None = None
    CodiceFiscale: str
    IndirizzoTelematico: str
    TipoSoggetto: str | None = ""
    Principale: bool = True
    Titolo: str | None = ""
    
class IDataProtocollo(BaseModel):
    Soggetti: list[ISoggettoProtocollo] = []
    Flusso: str
    Oggetto: str
    Classifica: str
    UO: str
    Fascicolo: IFascicolo | None = None
    Parametri: list[IParametro] | None = []
    MittenteInterno: str = ""
    MezzoInvio: str = ""
    TipoDocumento: str = ""
    TipoAllegati: str = ""
    NumeroRegistrazione: str = '0'
    DataRegistrazione: str = '0'
    LivelloRiservatezza: str = ""
    DataFineRiservatezza: str = ""   
    Principale: IAllegatoProtocollo | str = "documento_riepilogo"
    Allegati: list[IAllegatoProtocollo] | list[str] = []
    
    


#### da rinominare in gisweb.ads
esempio = IDataProtocollo(
    Soggetti = [
        ISoggettoProtocollo(
            IndirizzoTelematico = "rstarnini@inwind.it",
            Nome = "Mario",
            Cognome = "Rossi",
            CodiceFiscale = "RSSMRA84C01D969H",
            Titolo = "Richiedente"
        ),
            ISoggettoProtocollo(
            IndirizzoTelematico = "rstarnini@inwind.it",
            Cognome = "Ditta ACME",
            TipoSoggetto= "G",
            CodiceFiscale = "01533090997",
            Titolo = "Amministatore"
        )],
    Flusso = "E",
    Oggetto = "Prova protocollo",
    Classifica = "06-01",
    UO =  "2.5.1",
    Fascicolo = IFascicolo(numero='2', anno="2024"),
    Parametri = [
        IParametro(nome="uo", valore="4.3"), 
        IParametro(nome="tipoSmistamento", valore="COMPETENZA"), #CONOSCENZA/COMPETENZA
        IParametro(nome="azione", valore="ESEGUI"), 
        IParametro(nome="smistamento", valore="4.3@@CONOSCENZA"),
        IParametro(nome="smistamento", valore="0.1@@CONOSCENZA"),
        IParametro(nome="smistamento", valore="0.2@@CONOSCENZA"),
        IParametro(nome="smistamento", valore="0.3@@CONOSCENZA")
    ],
    TipoDocumento = "WSTS",
    Principale = "documento_riepilogo",
    Allegati = ["allegati_osservazione"]
)