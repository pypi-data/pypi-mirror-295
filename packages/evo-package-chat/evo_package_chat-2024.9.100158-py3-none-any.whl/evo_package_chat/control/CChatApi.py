#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_chat.entity import *
from evo_package_chat.utility import *
from evo_framework.core.evo_core_api.entity.EApiQuery import EApiQuery
#<
from evo_package_assistant.entity.EAssistant import EAssistant
from evo_package_assistant.entity.EAssistantMap import EAssistantMap
#>

# ---------------------------------------------------------------------------------------------------------------------------------------
# CChatApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CChatApi
"""
class CChatApi(CApi):
	__instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):   
		if CChatApi.__instance != None:
			raise Exception("ERROR:SINGLETON")
		else:
			super().__init__()
			CChatApi.__instance = self
			self.currentPath = os.path.dirname(os.path.abspath(__file__))
			
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""getInstance Singleton

	Raises:
		Exception:  api exception

	Returns:
		_type_: CChatApi instance
	"""
	@staticmethod
	def getInstance():
		if CChatApi.__instance is None:
			cObject = CChatApi()  
			cObject.doInit()  
		return CChatApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doInit

	Raises:
		Exception: api exception

	Returns:

	"""   
	def doInit(self):   
		try:			
			UChatApi.getInstance()
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise	  
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doAddApi

	Raises:
		Exception: api exception

	Returns:

	"""
	@override   
	def doAddApi(self):
		try:			
			
			api0 = self.newApi("chat-chatstream", callback=self.onChatStream, input=EChatInput, output=EChatMessage )
			api0.description="chat-chatstream _DESCRIPTION_"
			api0.required="eChatInput.apiToken|eChatInput.modelID"

			api1 = self.newApi("chat-get_mapmodel", callback=self.onGetMapModel, input=EApiQuery, output=EChatMapModel )
			api1.description="chat-get_mapmodel _DESCRIPTION_"
			api1.required="*"

			api2 = self.newApi("chat-get_mapmessage", callback=self.onGetMapMessage, input=EChatInput, output=EChatMapMessage )
			api2.description="chat-get_mapmessage _DESCRIPTION_"
			api2.required="eChatInput.apiToken|eChatInput.modelID|eChatInput.sessionID"

			api3 = self.newApi("chat-get_mapsession", callback=self.onGetMapSession, input=EChatInput, output=EChatMapSession )
			api3.description="chat-get_mapsession _DESCRIPTION_"
			api3.required="eChatInput.apiToken|eChatInput.modelID"

			api4 = self.newApi("chat-get_assistant", callback=self.onGetEAssistant, input=EApiQuery, output=EAssistant )
			api4.description="chat-get_assistant _DESCRIPTION_"
			api4.required="eApiQuery.eObjectID"

			api5 = self.newApi("chat_query_assistant", callback=self.onGetEAssistantMap, input=EApiQuery, output=EAssistantMap )
			api5.description="chat-chat_query_assistant _DESCRIPTION_"
			api5.required="eApiQuery.query"
  
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onChatStream api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onChatStream(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onChatStream: {eAction} ")

					
			async for eActionOutput in UChatApi.getInstance().doOnChatStream(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGetMapModel api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGetMapModel(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGetMapModel: {eAction} ")

					
			async for eActionOutput in UChatApi.getInstance().doOnGetMapModel(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGetMapMessage api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGetMapMessage(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGetMapMessage: {eAction} ")

					
			async for eActionOutput in UChatApi.getInstance().doOnGetMapMessage(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGetMapSession api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGetMapSession(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGetMapSession: {eAction} ")

					
			async for eActionOutput in UChatApi.getInstance().doOnGetMapSession(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGetEAssistant api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGetEAssistant(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGetEAssistant: {eAction} ")

					
			async for eActionOutput in UChatApi.getInstance().doOnGetEAssistant(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGetEAssistantMap api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGetEAssistantMap(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGetEAssistantMap: {eAction} ")

					
			async for eActionOutput in UChatApi.getInstance().doOnGetEAssistantMap(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------
