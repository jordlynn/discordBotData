from amazon_pay.client import AmazonPayClient

class amznPay:

	def __init__(self):
		self.client = AmazonPayClient(
			mws_access_key='AKIAF6ILPFUI7P4CRPKQ',
		    mws_secret_key='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',
		    merchant_id='AAWEKE0NG9LB5',
		    region='na',
		    currency_code='USD',
		    sandbox=False
			)
	
	def SetORD(self):
		ret = self.client.get_order_reference_details(
			amazon_order_reference_id='AMAZON_ORDER_REFERENCE_ID',
			address_consent_token='ADDRESS_CONSENT_TOKEN')
		print(ret.to_json())

	def StartOrder(self):
		ret = self.client.get_order_reference_details(
			amazon_order_reference_id='AMAZON_ORDER_REFERENCE_ID',
			address_consent_token='ADDRESS_CONSENT_TOKEN')
		print(ret.to_json()) # to_xml and to_dict are also valid

	def ChargerOrder(self):
		ret = self.client.charge( 
			amazon_order_reference_id='ORDER_REFERENCE_ID or BILLING_AGREEMENT_ID',
			charge_amount='10.00',
		    charge_note='MY_CHARGE_NOTE',
		    authorize_reference_id='MY_UNIQUE_AUTHORIZATION_ID')
		print(ret.to_json())


