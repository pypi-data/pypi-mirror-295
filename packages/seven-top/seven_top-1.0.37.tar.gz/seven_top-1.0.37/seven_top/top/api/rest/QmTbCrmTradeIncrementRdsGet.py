# -*- coding: utf-8 -*-
'''
Created by auto_sdk on 2021.09.14
'''
from seven_top.top.api.base import RestApi
class QmTbCrmTradeIncrementRdsGet(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.status = ""
		self.type = ""
		self.seller_nick = ""
		self.buyer_nick = ""
		self.created = ""
		self.modified = ""
		self.jdp_hashcode = ""
		self.jdp_response = ""
		self.jdp_created = ""
		self.jdp_modified = ""


	def getapiname(self):
		return 'taobao.trade increment.rds.get'