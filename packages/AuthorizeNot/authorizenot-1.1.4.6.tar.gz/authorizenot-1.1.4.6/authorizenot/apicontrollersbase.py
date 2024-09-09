'''
Created on Nov 1, 2015

@author: krgupta
@updated: William Hinz
'''
import abc
import logging
import pyxb
import xml.dom.minidom
import requests
from lxml import objectify

from authorizenot.constants import constants
from authorizenot import apicontractsv1
from authorizenot.utility import Helper

'''
from authorizenet.apicontractsv1 import merchantAuthenticationType
from authorizenet.apicontractsv1 import ANetApiRequest
from authorizenet.apicontractsv1 import ANetApiResponse
'''

anetLogger = logging.getLogger(constants.defaultLoggerName)
anetLogger.addHandler(logging.NullHandler())
logging.getLogger('pyxb.binding.content').addHandler(logging.NullHandler())


class APIOperationBaseInterface(abc.ABC):
    
    @abc.abstractmethod
    def execute(self):
        """
        Makes a http-post call.
        Uses request xml and response class type to check that the response was of correct type
        """
        pass

    @abc.abstractmethod
    def getresponseclass(self):
        """ Returns the response class """
        pass
    
    @abc.abstractmethod
    def getrequesttype(self):
        """ Returns the request class """
        pass
    
    @abc.abstractmethod
    def getresponse(self):
        """ Returns the de-serialized response """
        pass

    @abc.abstractmethod
    def getresultcode(self):
        """ Returns the result code from the response """
        pass
    
    @abc.abstractmethod
    def getmessagetype(self):
        """ Returns the message type enum from the response """
        pass

    @abc.abstractmethod
    def afterexecute(self):
        """ Returns the message received from binding after processing request """
        pass

    @abc.abstractmethod
    def beforeexecute(self):
        """ TODO """
        pass


class APIOperationBase(APIOperationBaseInterface, abc.ABC):

    __merchantauthentication = 'null'
    __environment = 'null'
    __initialized = 'null'

    @staticmethod
    def __classinitialized():
        return APIOperationBase.__initialized

    def __init__(self, api_request):
        super().__init__()
        self.helper = Helper('anet_python_sdk_properties.ini')
        self._httpResponse = None
        self._request = None
        self._response = None
        # objectify variables
        self._responseXML = None
        self._reponseObject = None
        self._mainObject = None

        if api_request is None:
            raise ValueError('Input request cannot be null')

        self._request = api_request
        APIOperationBase.__environment = constants.SANDBOX
        APIOperationBase.__merchantauthentication = apicontractsv1.merchantAuthenticationType()
        self.validate()

    @abc.abstractmethod
    def validaterequest(self):
        return
    
    def validate(self):
        anet_api_request = self._getrequest()
        self.validateandsetmerchantauthentication()       
        self.validaterequest()

    def setClientId(self):
        self._request.clientId = constants.clientId

    def _getrequest(self):
        return self._request 
     
    def buildrequest(self):
        anetLogger.debug('building request..')
        
        xmlRequest = self._request.toxml(encoding=constants.xml_encoding, element_name=self.getrequesttype())
        #remove namespaces that toxml() generates
        xmlRequest = xmlRequest.replace(constants.nsNamespace1, b'')
        xmlRequest = xmlRequest.replace(constants.nsNamespace2, b'')

        return xmlRequest
    
    def getprettyxmlrequest(self):
        xmlRequest = self.buildrequest()
        requestDom = xml.dom.minidom.parseString(xmlRequest)
        anetLogger.debug('Request is: %s' % requestDom.toprettyxml())

        return requestDom
    
    def execute(self):
        anetLogger.debug('Executing http post to url: %s', self.__environment)
        self.beforeexecute()
        proxy_dictionary = {'http': self.helper.get_property("http_proxy"),
                            'https': self.helper.get_property("https_proxy"),
                            'ftp': self.helper.get_property("ftp")}

        # requests is http request
        try:
            self.setClientId()
            xmlRequest = self.buildrequest()
            self._httpResponse = requests.post(self.__environment, data=xmlRequest, headers=constants.headers, proxies=proxy_dictionary)
        except Exception as httpException:
            anetLogger.error('Error retrieving http response from: %s for request: %s', self.__environment, self.getprettyxmlrequest())
            anetLogger.error('Exception: %s, %s', type(httpException), httpException.args)

        if self._httpResponse:
            self._httpResponse.encoding = constants.response_encoding
            self._httpResponse = self._httpResponse.text[3:]  # strip BOM
            self.afterexecute()

            try:
                self._response = apicontractsv1.CreateFromDocument(self._httpResponse) 
                # objectify code
                xmlResponse = self._response.toxml(encoding=constants.xml_encoding, element_name=self.getrequesttype())
                xmlResponse = xmlResponse.replace(constants.nsNamespace1, b'')
                xmlResponse = xmlResponse.replace(constants.nsNamespace2, b'')
                self._mainObject = objectify.fromstring(xmlResponse)
            except Exception as objectifyexception:
                anetLogger.error( 'Create Document Exception: %s, %s', type(objectifyexception), objectifyexception.args )
                responseString = self._httpResponse
                # removing encoding attribute as objectify fails if it is present
                responseString = responseString.replace('encoding=\"utf-8\"', '')
                self._mainObject = objectify.fromstring(responseString) 
            else:
                if type(self.getresponseclass()) is not type(self._mainObject):
                    if self._response.messages.resultCode == "Error":
                        anetLogger.debug("Response error")
                    domResponse = xml.dom.minidom.parseString(self._httpResponse.encode('utf-8'))
                    anetLogger.debug('Received response: %s' % domResponse.toprettyxml(encoding='utf-8'))
                else:
                    # Need to handle ErrorResponse
                    anetLogger.debug('Error retrieving response for request: %s' % self._request)
        else:
            anetLogger.debug("Did not receive http response")

    def getresponse(self):
        # return self._response  # pyxb object
        return self._mainObject  # objectify object
    
    def getresultcode(self):
        resultcode = 'null'
        if self._response:
            resultcode = self._response.resultCode
        return resultcode
    
    def getmessagetype(self):
        message = 'null'
        if self._response:
            message = self._response.message
        return message
    
    def afterexecute(self):
        pass
    
    def beforeexecute(self):
        pass

    def getmerchantauthentication(self):
        return self.__merchantauthentication
    
    @staticmethod
    def setmerchantauthentication(merchant_authentication):
        APIOperationBase.__merchantauthentication = merchant_authentication

    def validateandsetmerchantauthentication(self):
        anetapirequest = apicontractsv1.ANetApiRequest()
        if anetapirequest.merchantAuthentication == 'null':
            if self.getmerchantauthentication() != 'null':
                anetapirequest.merchantAuthentication = self.getmerchantauthentication()
            else:
                raise ValueError('Merchant Authentication can not be None')

    @staticmethod
    def getenvironment():
        return APIOperationBase.__environment

    @staticmethod
    def setenvironment(userenvironment):
        APIOperationBase.__environment = userenvironment
