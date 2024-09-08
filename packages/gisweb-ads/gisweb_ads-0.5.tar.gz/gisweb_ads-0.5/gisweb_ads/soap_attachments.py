# -*- coding: utf-8 -*-
import uuid
import logging
from gisweb_ads.schema import IProtocolloResult
from bs4 import BeautifulSoup

_logger = logging.getLogger('gisweb.sicraweb')


def parseMessage(xmlMessage) -> IProtocolloResult:
    # memo xml tiene conto delle maiuscole lxml tutto minuscolo
    soup = BeautifulSoup(xmlMessage, 'xml')
    keys = ["lngDocID", "lngErrNumber", "strErrString",
            "lngNumPG", "lngAnnoPG", "strDataPG"]
    dz = dict()

    for key in keys:
        dz[key] = soup.find(key) and soup.find(key).string  # type: ignore

    return IProtocolloResult(
        lngDocID=int(dz.get('lngDocID') or 0),
        lngNumPG=int(dz.get('lngNumPG') or 0),
        lngAnnoPG=int(dz.get('lngAnnoPG') or 0),
        lngErrNumber=int(dz.get('lngErrNumber') or 0),
        strErrString=dz.get('strErrString') or '',
        strDataPG=dz.get('strDataPG') or '',
    )


def with_soap_attachment(suds_method, attachment_data, *args, **kwargs) -> IProtocolloResult:
    """ Add an attachment to a suds soap request.

    attachment_data is assumed to contain a list:
      ( <attachment content>, <content id>, <mime-type> )

    The attachment content is only required required list element.

    http://stackoverflow.com/questions/17046779/passing-file-attachments-in-soap-using-suds

    """

    from suds.transport import Request

    # Suds doesn't currently support SOAP Attachments, so we have to build our
    # own attachment support, using parts of the suds library

    MIME_DEFAULT = 'text/plain'
    attachment_encoding = '8bit'
    attachment_mimetype = MIME_DEFAULT
    attachment_id = ''
    soap_method = suds_method.method
    data: bytes

    if len(attachment_data) == 3:
        data, attachment_id, attachment_mimetype = attachment_data
    elif len(attachment_data) == 2:
        data, attachment_id = attachment_data
    elif len(attachment_data) == 1:
        data = attachment_data
        attachment_id = uuid.uuid4()

    # Generate SOAP XML appropriate for this request
    binding = soap_method.binding.input
    soap_xml = binding.get_message(
        soap_method, args, kwargs).str().encode('utf-8')

    # Prepare MIME headers & boundaries
    boundary_id = f'uuid:{uuid.uuid4()}'
    root_part_id = f'uuid:{uuid.uuid4()}'
    request_headers = {
        'Content-Type': '; '.join([
            'multipart/related',
            'type="text/xml"',
            f'start="<{root_part_id}>"',
            f'boundary="{boundary_id}"',
        ]),
        'SOAPAction': ''
    }
    soap_headers = '\n'.join([
        'Content-Type: text/xml; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
        f'Content-Id: <{root_part_id}>',
        '',
    ]).encode('utf-8')
    attachment_headers = '\n'.join([
        f'Content-Type: {attachment_mimetype}',
        f'Content-Transfer-Encoding: {attachment_encoding}',
        f'Content-Id: <{attachment_id}>',
        '',
    ]).encode('utf-8')

    boundary = f"--{boundary_id}".encode('utf-8')

    # Build the full request
    request_text = b'\r\n'.join([
        boundary,
        soap_headers,
        soap_xml,
        boundary,
        attachment_headers,
        data,
        boundary + '--'.encode('utf-8')
    ])

    # with open("./test.xml", "w") as f:
    #  f.write(request_text.decode('latin-1'))

    # Stuff everything into a request object
    headers = suds_method.client.options.headers.copy()
    headers.update(request_headers)
    request = Request(suds_method.client.wsdl.url, request_text)
    request.headers = headers
    # Send the request
    # _logger.info(request_text)

    response = suds_method.client.options.transport.send(request)

    if response.code == 200:
        try:
            return parseMessage(response.message)
        except Exception as e:
            with open("./errori_protocollo.txt", "a") as f:
                f.write(str(response.message))
            return IProtocolloResult(lngErrNumber=999, strErrString=str(response.message))
    else:
        return IProtocolloResult(lngErrNumber=999, strErrString="ERRORE NELLA RISPOSTA DEL SERVIZIO")
