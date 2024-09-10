#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_chat.entity import *
from evo_package_chat.entity.EChatMapModel import EChatMapModel
from evo_package_chat.utility.IChatProtocol import IChatProtocol
#<
from evo_package_assistant import *
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
# UChatApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""UChatApi
"""
class UChatApi():
    __instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):   
        if UChatApi.__instance != None:
            raise Exception("ERROR:SINGLETON")
        else:
            super().__init__()
            UChatApi.__instance = self
            self.currentPath = os.path.dirname(os.path.abspath(__file__))
            self.eChatMapModel:EChatMapModel = EChatMapModel()
            
# ---------------------------------------------------------------------------------------------------------------------------------------
    """getInstance Singleton

    Raises:
        Exception:  api exception

    Returns:
        _type_: UChatApi instance
    """
    @staticmethod
    def getInstance():
        if UChatApi.__instance is None:
            uObject = UChatApi()  
            uObject.doInit()  
        return UChatApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
    """doInit

    Raises:
        Exception: api exception

    Returns:

    """   
    def doInit(self):   
        try:
#<
           self.eChatMapModel.doGenerateID()
           self.eChatMapModel.doGenerateTime()
           self.eChatMapModel.apiPackage = "evo_package_chat"
#>   
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnChatStream(self, eAction:EAction) -> EAction:
        """doOnChatStream utility callback IChatProtocol
            input: EChatInput
            output: EChatMessage

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:
#<        
            eChatInput, callback = await self.__doGetCallback(eAction)
                
            async for eActionOutput in callback.doOnChatStream(eAction, eChatInput):
                yield eActionOutput      
          
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetMapMessage(self, eAction:EAction) -> EAction:
        """doOnGetMapMessage utility callback IChatProtocol
            input: EChatInput
            output: EChatMapMessage

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:
#<        
            eChatInput, callback = await self.__doGetCallback(eAction)        
            async for eActionOutput in callback.doOnGetMapMessage(eAction, eChatInput):
                yield eActionOutput  
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetMapSession(self, eAction:EAction) -> EAction:
        """doOnGetMapSession utility callback IChatProtocol
            input: EChatInput
            output: EChatMapSession

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

#<        
            eChatInput, callback = await self.__doGetCallback(eAction)        
            async for eActionOutput in callback.doOnGetMapSession(eAction, eChatInput):
                yield eActionOutput     
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetEAssistant(self, eAction:EAction) -> EAction:
        """doOnGetMapSession utility callback IChatProtocol
            input: EChatInput
            output: EChatMapSession

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

#<        
            
            
            async for eActionOutput in await UAssistantApi.getInstance().doOnGet(eAction):
                yield eActionOutput
             
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
        
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetEAssistantMap(self, eAction:EAction) -> EAction:
        """doOnGetMapSession utility callback IChatProtocol
            input: EChatInput
            output: EChatMapSession

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

#<                 
            async for eActionOutput in UAssistantApi.getInstance().doOnQuery(eAction):
                yield eActionOutput
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetMapModel(self, eAction:EAction) -> EAction:
        """doOnGetMapModel utility
            input: EChatInput
            output: EChatModelMap

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eApiQuery:EApiQuery = eAction.doGetInput(EApiQuery)
           
#<        
            #TODO:search ...
            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(self.eChatMapModel)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------

#<
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doGetCallback(self, eAction:EAction) -> Tuple[EChatInput, IChatProtocol]:
        """doOnGetMapSession utility callback
            input: EChatInput
            output: EChatMapSession

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eChatInput:EChatInput = eAction.doGetInput(EChatInput)
           
            #Dispose eAction.input for free memory
            eAction.input = b''
            
            IuLog.doVerbose(__name__, f"eChatInput:{eChatInput}")

            if eChatInput is None:
                raise Exception("ERROR_REQUIRED|eChatInput")
            
            if eChatInput.modelID is None:
                raise Exception("ERROR_REQUIRED|eChatInput.modelID")
            
            if eChatInput.apiToken is None:
                raise Exception("ERROR_REQUIRED|eChatInput.apiToken")
            
            IuLog.doDebug(__name__, self.eChatMapModel)
            IuLog.doDebug(__name__, IuKey.toString(eChatInput.modelID) )
            
            
            if eChatInput.modelID  not in self.eChatMapModel.mapEChatModel.keys():
                raise Exception("ERROR_NOT_VALID|eChatInput.modelID")
            
           
            eChatModel:EChatModel = self.eChatMapModel.mapEChatModel.doGet(eChatInput.modelID)
            
            if eChatModel is None:
                raise Exception("ERROR_NOT_VALID|eChatModel")
            
            if eChatModel.callback is None:
                raise Exception("ERROR_NOT_VALID|eChatModel.callback")
            
            return eChatInput, eChatModel.callback 

        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
