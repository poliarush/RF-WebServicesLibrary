from suds.client import Client
from suds.sax.enc import Encoder
from suds.sax.text import Raw
from robot.api import logger

class SoapWebService(object):
    
    def __init__(self):
        self._client = None
        self._response = None
        
    def call_soap_webservice(self, url):
        '''
        Initialize soap web-service by passing URL in format http://site.com to call webservice's methods later
        '''
        try:
            self._client = Client(url)
        except:
            raise Exception("Can't call web-service by WSDL %s" % url)

    def invoke_method_synchronously(self, name, *parameters):
        '''
        Invoke webservice method synchronously by name with parameters to be passed to it.  
        '''
        parameters = [self._decode_text(i) 
                      if self._check_if_need_to_encode(i) else i 
                      for i in parameters]
        try:
            logger.debug("Passing input for methods:\n%s" % parameters)
            exec "self._response  = self._client.service.%s(*parameters)" % name        
        except:
            raise Exception("Can't invoke method %s with parameters %s" % (name, parameters))
        logger.debug("Get response as result of invoking method:\n%s" % self._response)
        self.load_data_for_assertion(str(self._response))
        return str(self._response)
    
    def invoke_method_asynchronously(self, name, reply, timeout, succeeded, *parameters):
        '''
        Invoke webservice method asynchronously with later reply.
        @param name: name of method
        @param reply: xml file to be send after some time as reply
        @param timeout: timeout for method
        @param succeeded: True or False to define what message should be returned by async response
        '''
#        self._client.options.nosend=True
#        reply = '<?xml version="1.0" encoding="utf-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><ns1:addPersonResponse soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:ns1="http://basic.suds.fedora.org"><addPersonReturn xsi:type="xsd:string">person (jeff&#x4D2;,ortel) at age 43 with phone numbers (410-555-5138,919-555-4406,205-777-1212, and pets (Chance,) - added.</addPersonReturn></ns1:addPersonResponse></soapenv:Body></soapenv:Envelope>'
#        request = client.service.addPerson(person)
#        result = request.succeeded(reply)
        #    error = Object()
        #    error.httpcode = '500'
        #    request.failed(error)
#        self._client.options.nosend=False
        pass
        
    def _check_if_need_to_encode(self, text):
        return Encoder().needsEncoding(text)
        
    def _decode_text(self, text):
        return Raw(text)
