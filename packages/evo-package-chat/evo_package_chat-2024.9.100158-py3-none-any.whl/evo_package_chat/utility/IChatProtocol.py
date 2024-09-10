from evo_framework.core.evo_core_api.entity.EAction import EAction
from evo_package_chat.entity import *
from abc import ABC, abstractmethod
from typing import Any
from typing_extensions import Protocol

class IChatProtocol(Protocol):
    @abstractmethod
    async def doOnChatStream(self, eAction:EAction, eChatInput:EChatInput|Any = None) -> EAction:
        pass
    
    @abstractmethod
    async def doOnGetMapSession(self, eAction:EAction, eChatInput:EChatInput|Any = None ) -> EAction:
        pass
    
    @abstractmethod
    async def doOnGetMapMessage(self, eAction:EAction, eChatInput:EChatInput|Any = None ) -> EAction:
        pass