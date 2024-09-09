"""
Created on Nov 16, 2015

@author: krgupta
@updated: William Hinz
"""
from authorizenot.apicontrollers import *
from decimal import *
import random
import unittest
from tests import apitestbase


class TestReadProperty(apitestbase.ApiTestBase):

    def testPropertyFromFile(self):
        login = self.helper.get_property("api.login.id")
        if login is None:
            login = self.helper.get_property("api_login_id")
        transactionkey = self.helper.get_property("transaction.key")
        if transactionkey is None:
            transactionkey = self.helper.get_property("transaction_key")
        self.assertIsNotNone(login)
        self.assertIsNotNone(transactionkey)


class TestTransactionReportingUnitTest(apitestbase.ApiTestBase):

    def testchargeCreditCard(self):
        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = "4111111111111111"
        creditCard.expirationDate = "2100-12"
        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard
        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authCaptureTransaction"
        transactionrequest.amount = Decimal(str(round(random.random()*100, 2)))
        transactionrequest.payment = payment
        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = self.merchantAuthentication
        createtransactionrequest.refId = "MerchantID-0001"
        createtransactionrequest.transactionRequest = transactionrequest
        createtransactioncontroller = createTransactionController(createtransactionrequest)
        createtransactioncontroller.execute()
        response = createtransactioncontroller.getresponse()
        if hasattr(response, 'messages') == True:
            if hasattr(response.messages, 'resultCode') == True:
                self.assertEqual('Ok', response.messages.resultCode)
        if hasattr(response, 'transactionResponse') == True:
            if hasattr(response.transactionResponse, 'transId') == True:
                createdTransactionId = response.transactionResponse.transId
        return str(createdTransactionId)
                  
    def testgetTransactionDetails(self):    
        gettransactiondetailsrequest = apicontractsv1.getTransactionDetailsRequest()
        gettransactiondetailsrequest.merchantAuthentication = self.merchantAuthentication
        transactionID = self.testchargeCreditCard()
        gettransactiondetailsrequest.transId = transactionID #update valid transaction id
        gettransactiondetailscontroller = getTransactionDetailsController(gettransactiondetailsrequest)
        gettransactiondetailscontroller.execute()
        response =  gettransactiondetailscontroller.getresponse()
        if hasattr(response, 'messages') == True:
            if hasattr(response.messages, 'resultCode') == True:
                self.assertEqual('Ok', response.messages.resultCode)


class TestRecurringBillingTest(apitestbase.ApiTestBase):

    def testCreateSubscription(self):
        createsubscriptionrequest = apicontractsv1.ARBCreateSubscriptionRequest()
        createsubscriptionrequest.merchantAuthentication = self.merchantAuthentication
        createsubscriptionrequest.refId = 'Sample'
        createsubscriptionrequest.subscription = self.subscriptionOne
        arbcreatesubscriptioncontroller = ARBCreateSubscriptionController(createsubscriptionrequest)
        arbcreatesubscriptioncontroller.execute()
        response = arbcreatesubscriptioncontroller.getresponse()
        createdSubscriptionId = None
        if hasattr(response, 'messages') and hasattr(response.messages, 'resultCode'):
            self.assertEqual('Ok', response.messages.resultCode)
        if hasattr(response, 'subscriptionId'):
            createdSubscriptionId = response.subscriptionId
        return str(createdSubscriptionId)

    def testGetSubscription(self):
        getSubscription = apicontractsv1.ARBGetSubscriptionRequest()
        getSubscription.merchantAuthentication = self.merchantAuthentication
        subscriptionID = self.testCreateSubscription()
        getSubscription.subscriptionId = subscriptionID #update valid subscription id
        getSubscriptionController = ARBGetSubscriptionController(getSubscription)
        getSubscriptionController.execute()
        response = getSubscriptionController.getresponse()
        if hasattr(response, 'messages') == True:
            if hasattr(response.messages, 'resultCode') == True:
                self.assertEqual('Ok', response.messages.resultCode)
       
    def testCancelSubscription(self):   
        cancelsubscriptionrequest = apicontractsv1.ARBCancelSubscriptionRequest()
        cancelsubscriptionrequest.merchantAuthentication = self.merchantAuthentication
        cancelsubscriptionrequest.refId = 'Sample'
        subscriptionID = self.testCreateSubscription()
        cancelsubscriptionrequest.subscriptionId = subscriptionID  # input valid subscriptionId
        cancelsubscriptioncontroller = ARBCancelSubscriptionController(cancelsubscriptionrequest)
        cancelsubscriptioncontroller.execute()  
        response = cancelsubscriptioncontroller.getresponse()
        if hasattr(response, 'messages'):
            if hasattr(response.messages, 'resultCode'):
                self.assertEqual('Ok', response.messages.resultCode)


class TestPaymentTransactionUnitTest(apitestbase.ApiTestBase):

    def testAuthCaptureTransaction(self):  
        transaction_request_type = apicontractsv1.transactionRequestType()
        transaction_request_type.transactionType = "authCaptureTransaction"
        transaction_request_type.amount = self.amount
        transaction_request_type.payment = self.payment
        transaction_request_type.order = self.order
        transaction_request_type.customer = self.customerData
        transaction_request_type.billTo = self.billTo
        create_transaction_request = apicontractsv1.createTransactionRequest()
        create_transaction_request.merchantAuthentication = self.merchantAuthentication
        create_transaction_request.refId = self.ref_id
        create_transaction_request.transactionRequest = transaction_request_type
        create_transaction_controller = createTransactionController(create_transaction_request)
        create_transaction_controller.execute()
        response = create_transaction_controller.getresponse()
        if hasattr(response, 'messages') and hasattr(response.messages, 'resultCode'):
            self.assertEqual('Ok', response.messages.resultCode)
        if hasattr(response, 'transactionResponse'):
            self.assertIsNotNone(response.transactionResponse)
            if hasattr(response.transactionResponse, 'transId'):
                self.assertIsNotNone(response.transactionResponse.transId)
               
    def testAuthOnlyContinueTransaction(self):      
        transactionrequesttype = apicontractsv1.transactionRequestType()
        transactionrequesttype.transactionType = "authCaptureTransaction"
        transactionrequesttype.amount = self.amount
        transactionrequesttype.payment = self.payment
        transactionrequesttype.order = self.order
        transactionrequesttype.customer = self.customerData
        transactionrequesttype.billTo = self.billTo
        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = self.merchantAuthentication
        createtransactionrequest.refId = self.ref_id
        createtransactionrequest.transactionRequest = transactionrequesttype
        createtransactioncontroller = createTransactionController(createtransactionrequest)
        createtransactioncontroller.execute()
        response = createtransactioncontroller.getresponse()
        if hasattr(response, 'messages') == True:
            if hasattr(response.messages, 'resultCode') == True:
                self.assertEqual('Ok', response.messages.resultCode)
        if hasattr(response, 'transactionResponse') == True:
            self.assertIsNotNone(response.transactionResponse)
            if hasattr(response.transactionResponse, 'transId') == True:    
                self.assertIsNotNone(response.transactionResponse.transId)
                  
class test_CustomerProfile(apitestbase.ApiTestBase):
    def testCreateCustomerProfile(self):
        createdCustomerProfileID = None
        createCustomerProfile = apicontractsv1.createCustomerProfileRequest()
        createCustomerProfile.merchantAuthentication = self.merchantAuthentication
        randomInt = random.randint(0, 10000)
        createCustomerProfile.profile = apicontractsv1.customerProfileType()
        createCustomerProfile.profile.merchantCustomerId = 'jdoe%s' % randomInt
        createCustomerProfile.profile.description = 'John Doe%s' % randomInt
        createCustomerProfile.profile.email = 'jdoe%s@mail.com' % randomInt
        controller = createCustomerProfileController(createCustomerProfile)
        controller.execute()
        response = controller.getresponse()
        if hasattr(response, 'messages') == True:
            if hasattr(response.messages, 'resultCode') == True:
                self.assertEqual('Ok', response.messages.resultCode)
        if hasattr(response, 'customerProfileId') == True: 
            createdCustomerProfileID = response.customerProfileId
        return str(createdCustomerProfileID)
             
    def testGetCustomerProfile(self):
        getCustomerProfile = apicontractsv1.getCustomerProfileRequest()
        getCustomerProfile.merchantAuthentication = self.merchantAuthentication
          
        CustomerProfileID = self.testCreateCustomerProfile()   
        getCustomerProfile.customerProfileId = CustomerProfileID 
        controller = getCustomerProfileController(getCustomerProfile)
        controller.execute()
        response = controller.getresponse()
        self.assertEqual('Ok', response.messages.resultCode)
        if hasattr(response, 'messages') == True:
            if hasattr(response.messages, 'resultCode') == True:
                self.assertEqual('Ok', response.messages.resultCode)

    def testCreateAndGetCustomerShippingAddress(self):
        officeAddress = apicontractsv1.customerAddressType();
        officeAddress.firstName = "John"
        officeAddress.lastName = "Doe"
        officeAddress.address = "123 Main St."
        officeAddress.city = "Bellevue"
        officeAddress.state = "WA"
        officeAddress.zip = "98004"
        officeAddress.country = "USA"
        officeAddress.phoneNumber = "000-000-0000"
        shippingAddressRequest = apicontractsv1.createCustomerShippingAddressRequest()
        shippingAddressRequest.address = officeAddress
        CustomerProfileID = self.testCreateCustomerProfile() 
        shippingAddressRequest.customerProfileId = CustomerProfileID
        shippingAddressRequest.merchantAuthentication = self.merchantAuthentication
        controller = createCustomerShippingAddressController(shippingAddressRequest)
        controller.execute()
        response = controller.getresponse()
        if hasattr(response, 'messages') == True:
            if hasattr(response.messages, 'resultCode') == True:
                self.assertEqual('Ok', response.messages.resultCode)
        if hasattr(response, 'customerAddressId') == True: 
            createdShippingAddressId = str(response.customerAddressId)
        #return str(createdShippingAddressId)
        
    #def testGetCustomerShippingAddress(self):
        getShippingAddress = apicontractsv1.getCustomerShippingAddressRequest()
        getShippingAddress.merchantAuthentication = self.merchantAuthentication
         
         
        getShippingAddress.customerProfileId = CustomerProfileID
        getShippingAddress.customerAddressId = createdShippingAddressId
        
        getShippingAddressController = getCustomerShippingAddressController(getShippingAddress)
        getShippingAddressController.execute()
        response = getShippingAddressController.getresponse()
        if hasattr(response, 'messages') == True:
            if hasattr(response.messages, 'resultCode') == True:
                self.assertEqual('Ok', response.messages.resultCode)
            
'''    
class test_ProductionURL(apitestbase.ApiTestBase):  
    #Tests will run only with production credentials
    
          
    def testGetSettledBatchList(self):
        settledBatchListRequest = apicontractsv1.getSettledBatchListRequest() 
        settledBatchListRequest.merchantAuthentication = self.merchantAuthentication
        settledBatchListController = getSettledBatchListController(settledBatchListRequest)
        customEndpoint = constants.PRODUCTION 
        apicontrollersbase.APIOperationBase.setenvironment(customEndpoint)
        settledBatchListController.execute() 
        response = settledBatchListController.getresponse() 
        self.assertEqual('Ok', response.messages.resultCode) 
    
    def testGetListofSubscriptions(self):    
        sorting = apicontractsv1.ARBGetSubscriptionListSorting()
        sorting.orderBy = apicontractsv1.ARBGetSubscriptionListOrderFieldEnum.id
        sorting.orderDescending = "false"
        paging = apicontractsv1.Paging()
        paging.limit = 1000
        paging.offset = 1
        GetListofSubscriptionRequest = apicontractsv1.ARBGetSubscriptionListRequest()
        GetListofSubscriptionRequest.merchantAuthentication = self.merchantAuthentication
        GetListofSubscriptionRequest.refId = "Sample"
        GetListofSubscriptionRequest.searchType = apicontractsv1.ARBGetSubscriptionListSearchTypeEnum.subscriptionInactive
        GetListofSubscriptionRequest.sorting = sorting
        GetListofSubscriptionRequest.paging = paging
        arbgetsubscriptionlistcontroller = ARBGetSubscriptionListController(GetListofSubscriptionRequest)
        customEndpoint = constants.PRODUCTION 
        apicontrollersbase.APIOperationBase.setenvironment(customEndpoint)
        arbgetsubscriptionlistcontroller.execute()
        response = arbgetsubscriptionlistcontroller.getresponse()
        self.assertEqual('Ok', response.messages.resultCode) 
'''        
if __name__ =='__main__':
    unittest.main()  
