from authorizenot.constants import constants
from decimal import *
import logging
import datetime
import unittest
from authorizenot import apicontractsv1
from authorizenot.utility import Helper


class TestCreateTransactionUnitTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.helper = Helper('anet_python_sdk_properties.ini')

    def testPyxbDeserializationElementAtMid(self):
        self.__PyxbDeserialization(False)
      
    def testPyxbDeserializationElementAtLast(self):
        self.__PyxbDeserialization(True)
      
    def testPyxbDeserializationGoodXML(self):
        self.__PyxbDeserialization()
                          
    def __PyxbDeserialization(self, last_element: bool = None):
        logging_filename = self.helper.get_property(constants.propertiesloggingfilename)
        logging_level = self.helper.get_property(constants.propertiesexecutionlogginglevel)
        
        deserializedObject = None
        deserializedBadObject = None
        
        if logging_filename is None:
            logging_filename = constants.defaultLogFileName
        if logging_level is None:
            logging_level = constants.defaultLoggingLevel
            
        logging.basicConfig(filename=logging_filename, level=logging_level, format=constants.defaultlogformat)
          
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = "unknown"
        merchantAuth.transactionKey = "anon"
    
        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = "4111111111111111"
        creditCard.expirationDate = "2020-12"
    
        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard
    
        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authCaptureTransaction"
        transactionrequest.amount = Decimal( 6.99)
        transactionrequest.payment = payment
    
        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        createtransactionrequest.transactionRequest = transactionrequest
        createtransactionrequest.refId = "MerchantID-0001"

        logging.debug("Request: %s " % datetime.datetime.now())
        logging.debug("       : %s " % createtransactionrequest)
        
        try:    
            xmlRequest = createtransactionrequest.toxml(encoding=constants.xml_encoding, element_name='createTransactionRequest')
            xmlRequest = xmlRequest.replace(constants.nsNamespace1, '')
            xmlRequest = xmlRequest.replace(constants.nsNamespace2, '')
            ##print ("xmlRequest %s " %xmlRequest)
            logging.debug( "Xml Request: %s" % xmlRequest)
        except Exception as ex:
            logging.debug( "Xml Exception: %s" % ex)
        
        badXmlElement = None
        
        if (last_element == None):
            try:
                deserializedObject = apicontractsv1.CreateFromDocument(xmlRequest)           
                self.assertIsNotNone(deserializedObject, "Null deserializedObject ")
                
                if type(createtransactionrequest) == type(deserializedObject):
                    ##print (" for good xml objects are equal")
                    logging.debug( "createtransactionrequest object is equal to deserializedObject") 
                else:
                    ##print ("for good xml some error: objects are NOT equal" )
                    logging.debug( "createtransactionrequest object is NOT equal to deserializedObject") 
                    
                deseriaziedObjectXmlRequest = deserializedObject.toxml(encoding=constants.xml_encoding, element_name='deserializedObject')
                deseriaziedObjectXmlRequest = deseriaziedObjectXmlRequest.replace(constants.nsNamespace1, '')
                deseriaziedObjectXmlRequest = deseriaziedObjectXmlRequest.replace(constants.nsNamespace2, '')
                logging.debug( "Good Dom Request: %s " % deseriaziedObjectXmlRequest ) 
                ##print ( "Good De-serialized XML: %s \n" % deseriaziedObjectXmlRequest )
            except Exception as ex:
                logging.error( 'Create Document Exception: %s, %s', type(ex), ex.args )      
        else:
            if (last_element == False):
                try:
                    splitString = "<amount>"
                    lines = xmlRequest.split( splitString)
                    badXmlElement = "<badElement>BadElement</badElement>"
                    badXmlRequest = lines[0] + badXmlElement + splitString + lines[1]
                    logging.debug( "Bad XmlRequest: %s" % badXmlRequest)
                    ##print ("ElementInMidXML Request:  %s \n" %badXmlRequest)
                except Exception as ex:
                    ##print ("ElementInMidXML can not be inserted: %s, %s",type(ex), ex.args)
                    logging.debug( "ElementInMidXML can not be inserted: %s, %s" ,type(ex), ex.args)             
            if (last_element == True):
                try:    
                    splitStringAtLast = "</payment>"
                    lines = xmlRequest.split( splitStringAtLast)
                    badXmlElementAtLast = "<badElementAtLast>BadElementAtLast</badElementAtLast>"
                    badXmlRequest = lines[0] + badXmlElementAtLast + splitStringAtLast + lines[1]
                    logging.debug( "Bad XmlRequest at Last: %s" % badXmlRequest)
                    ##print ("ElementAtLastXML Request: %s \n" %badXmlRequest)
                except Exception as ex:
                    ##print ("ElementAtLastXML can not be inserted: %s, %s",type(ex), ex.args)  
                    logging.debug("ElementAtLastXML can not be inserted: %s, %s",type(ex), ex.args)           
            try:     
                deserializedBadObject = apicontractsv1.CreateFromDocument(badXmlRequest)           
                self.assertIsNotNone(deserializedBadObject, "Null deserializedObject ")
                badDomXml = deserializedBadObject.toxml(encoding=constants.xml_encoding, element_name='deserializedBadObject')
                badDomXml = badDomXml.replace(constants.nsNamespace1, '')
                badDomXml = badDomXml.replace(constants.nsNamespace2, '')
                logging.debug( "Bad Dom Request: %s " % badDomXml ) 
                ##print ("Bad Dom De-serialized: %s \n" %badDomXml)
            except Exception as ex:
                logging.error( 'Create Document Exception: %s, %s', type(ex), ex.args )
                ##print ("Exception while de-serializing bad dom: %s, %s",type(ex), ex.args)


class TestCustomerProfile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.helper = Helper('anet_python_sdk_properties.ini')

    def testGetCustomerProfile(self):    
        logging_filename = self.helper.get_property(constants.propertiesloggingfilename)
        logging_level = self.helper.get_property(constants.propertiesexecutionlogginglevel)
        logging.basicConfig(filename=logging_filename, level=logging_level, format=constants.defaultlogformat)
          
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = "unknown"
        merchantAuth.transactionKey = "anon"
        
        getCustomerProfileRequest = apicontractsv1.getCustomerProfileRequest() 
        getCustomerProfileRequest.merchantAuthentication = merchantAuth 
        getCustomerProfileRequest.customerProfileId = '36152115'   
        getCustomerProfileRequest.abc = 'aaaaaaaa' #extra property not in getCustomerProfileRequest object
        
        logging.debug("Request: %s " % datetime.datetime.now())
        logging.debug("       : %s " % getCustomerProfileRequest)
        
        try:    
            '''serialzing object to XML '''
            xmlRequest = getCustomerProfileRequest.toxml(encoding=constants.xml_encoding, element_name='getCustomerProfileRequest')
            xmlRequest = xmlRequest.replace(constants.nsNamespace1, b'')
            xmlRequest = xmlRequest.replace(constants.nsNamespace2, b'')
            logging.debug( "Xml Request: %s" % xmlRequest)
            #print( "Xml Request: %s" % xmlRequest)
        except Exception as ex:
            logging.debug( "Xml Exception: %s" % ex)    
            
        try:
            '''deserialize XML to object '''    
            deserializedObject = None
            deserializedObject = apicontractsv1.CreateFromDocument(xmlRequest)           
            self.assertIsNotNone(deserializedObject, "Null deserializedObject ")
            
            if type(getCustomerProfileRequest) == type(deserializedObject):
                #print ("objects are equal")
                logging.debug( "createtransactionrequest object is equal to deserializedObject") 
            else:
                #print ("some error: objects are NOT equal" )
                logging.debug( "createtransactionrequest object is NOT equal to deserializedObject") 
            
            deseriaziedObjectXmlRequest = deserializedObject.toxml(encoding=constants.xml_encoding, element_name='deserializedObject')
            deseriaziedObjectXmlRequest = deseriaziedObjectXmlRequest.replace(constants.nsNamespace1, '')
            deseriaziedObjectXmlRequest = deseriaziedObjectXmlRequest.replace(constants.nsNamespace2, '')
            logging.debug( "Good Dom Request: %s " % deseriaziedObjectXmlRequest )
            #print( "Good Dom Request: %s " % deseriaziedObjectXmlRequest )
            #print("de-serialized successfully. GOOD CASE COMPLETE  \n ")
        except Exception as ex:
            
            logging.error( 'Create Document Exception: %s, %s', type(ex), ex.args )
        
        self.assertEqual(type(getCustomerProfileRequest), type(deserializedObject), "deseriaziedObject does not match original object")
        
        try:
            #print("starting with element in mid")
            newxml = '<?xml version="1.0" encoding="utf-8"?><getCustomerProfileRequest xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd"><merchantAuthentication><name>unknown</name><transactionKey>anon</transactionKey></merchantAuthentication><kriti>11Jan</kriti><customerProfileId>36152115</customerProfileId></getCustomerProfileRequest>'
            
            #print ("newxml: %s" %newxml)
            DEserializedNEWObject = apicontractsv1.CreateFromDocument(newxml)           
            self.assertIsNotNone(DEserializedNEWObject, "Null deserializedObject ")
            
            
            DEseriaziedNEWObjectXmlRequest = DEserializedNEWObject.toxml(encoding=constants.xml_encoding, element_name='deserializedObject')
            DEseriaziedNEWObjectXmlRequest = DEseriaziedNEWObjectXmlRequest.replace(constants.nsNamespace1, '')
            DEseriaziedNEWObjectXmlRequest = DEseriaziedNEWObjectXmlRequest.replace(constants.nsNamespace2, '')
            logging.debug( "Good Dom Request: %s " % DEseriaziedNEWObjectXmlRequest )
            #print( " DEseriaziedNEWObjectXmlRequest Request: %s " % DEseriaziedNEWObjectXmlRequest )
            #print("de-serialized successfully")
            #print("FINISHED element in mid \n ")
        except Exception as ex:    
            #print("DEseriaziedNEWObjectXmlRequest is NOT DESerialized")
            logging.error( 'Create Document Exception: %s, %s', type(ex), ex.args )
            
            
        try:
            #print("starting with element at last")
            newxmlATLAst = '<?xml version="1.0" encoding="utf-8"?><getCustomerProfileRequest xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd"><merchantAuthentication><name>unknown</name><transactionKey>anon</transactionKey></merchantAuthentication><customerProfileId>36152115</customerProfileId><gupta>11Jan</gupta></getCustomerProfileRequest>'
            #print ("newxmlATLAst: %s" %newxmlATLAst)
            DEserializedNEWObject = apicontractsv1.CreateFromDocument(newxmlATLAst)           
            self.assertIsNotNone(DEserializedNEWObject, "Null deserializedObject ")
            DEseriaziedNEWObjectXmlRequest = DEserializedNEWObject.toxml(encoding=constants.xml_encoding, element_name='deserializedObject')
            DEseriaziedNEWObjectXmlRequest = DEseriaziedNEWObjectXmlRequest.replace(constants.nsNamespace1, '')
            DEseriaziedNEWObjectXmlRequest = DEseriaziedNEWObjectXmlRequest.replace(constants.nsNamespace2, '')
            logging.debug( "Good Dom Request: %s " % DEseriaziedNEWObjectXmlRequest )
            #print( " DEseriaziedNEWATLASTObjectXmlRequest Request: %s " % DEseriaziedNEWObjectXmlRequest )
            #print("de-serialized successfully")
            #print("Finished element at last \n " )
        except Exception as ex:    
            #print("DEseriaziedNEWATLASTObjectXmlRequest is NOT DESerialized")
            logging.error( 'Create Document Exception: %s, %s', type(ex), ex.args )    


if __name__ == '__main__':
    unittest.main()  
