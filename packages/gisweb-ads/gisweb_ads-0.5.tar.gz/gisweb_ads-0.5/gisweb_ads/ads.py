
from ast import Dict
import random
from typing import Any
from gisweb_ads.schema import IAllegatoProtocollo, IConfigProtocollo, ILoginRet, IProtocolloResult, IDataProtocollo
from gisweb_ads.soap_attachments import with_soap_attachment
from suds.client import Client
import logging
from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape

_logger = logging.getLogger('gisweb-ads')

env = Environment(
    loader=PackageLoader("gisweb_ads"),
    autoescape=select_autoescape()
)

class Protocollo:

    config: IConfigProtocollo
    wsClient:Any
    DST:str | None = None
    wsError: str
    dataProt: IDataProtocollo
    
    def __init__(self, config:IConfigProtocollo):
        self.config = config
        try:
            self.wsClient = Client(config.wsUrl)
            result:ILoginRet = self.wsClient.service.login(config.wsEnte, config.wsUser, config.wsPassword)
            if result.lngErrNumber!=0:
                self.wsError = result.strErrString
            else:
                self.DST = result.strDST
                
        except Exception as error:
            self.wsError = str(error)

    
    def __inserisciAllegato(self, allegato:IAllegatoProtocollo):

        try:
            fName = allegato.nome#.encode('ascii','ignore')
            mime = allegato.mimetype#.encode('ascii','ignore')
            content = allegato.content
            result = with_soap_attachment(self.wsClient.service.inserimento, [content,fName,mime], self.config.wsUser, self.DST)
        except Exception as error:
            _logger.info(error)
            return error
             
        if result.lngErrNumber != 0:
            _logger.info(result.strErrString)
            return result.strErrString
        
        allegato.content = None
        allegato.id = result.lngDocID
        

    def __getSegnatura(self) -> str:
        
        #inserisco allegato principale
        #if isinstance(self.dataProt.Principale, IAllegatoProtocollo):
        error = self.__inserisciAllegato(self.dataProt.Principale)
        #if error:
        #    return ""
   
        #inserisco altri allegati
        for documento in self.dataProt.Allegati:
            #if isinstance(documento, IAllegatoProtocollo):
            error = self.__inserisciAllegato(documento)


        template = env.get_template("segnatura.xml")
        context = self.dataProt.model_copy(update=dict(
            Principale = self.dataProt.Principale,
            Today = datetime.today().strftime('%d/%m/%Y'),
            totAllegati = len(self.dataProt.Allegati),
            Amministrazione = self.config.amministrazione,
            Applicativo = self.config.applicativo
        ))
        
        return template.render(context)


    def protocollaDocumento(self, data:IDataProtocollo, testXml:bool=True) -> str | IProtocolloResult:
        
                                
        if not self.DST:
            return IProtocolloResult(lngErrNumber=999, strErrString= str(self.wsError))
                
        self.dataProt = data
        xmlSegnatura =  self.__getSegnatura()
        if testXml:
            return xmlSegnatura

        #Protocollazione Documento
        try:
            result = with_soap_attachment(self.wsClient.service.protocollazione,
                                          [xmlSegnatura.encode('utf-8'), 'profilazione', 'text/xml'], self.config.wsUser, self.DST)  
            
            if result.strErrString:
                with open("./errori_protocollo.txt", "a") as f:
                    f.write(result.strErrString)
                
            return result
            
        except Exception as e:
            with open("./errori_protocollo.xml", "a") as f:
                f.write(f"{data.model_dump()} {str(e)}")
            return IProtocolloResult(lngErrNumber=999, strErrString= str(e))
        

        # se protocollazione in uscita aggiungo la segnatura e oggetto
        ''''
        if flusso=='U':
            self.numero_protocollo="%07d" %result['lngNumPG']
            self.data_protocollo=datetime.today().strftime("%d/%m/%Y")
            # Segnatura di protocollazione
            tplSegnatura = ViewPageTemplateFile("templates/segnatura_pec.pt")
            xmlSegnatura = tplSegnatura(self)
        '''

