from abc import ABC, abstractmethod

class Machine(ABC):

    @abstractmethod
    async def get_ticker(self):
        """마지막 체결정보(Tick)을 얻기 위한 메소드입니다.
        """
        pass
