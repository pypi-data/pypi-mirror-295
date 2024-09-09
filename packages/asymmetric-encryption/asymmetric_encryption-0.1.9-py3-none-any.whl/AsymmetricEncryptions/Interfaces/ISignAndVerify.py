from __future__ import annotations
from abc import ABC, abstractmethod

class ISignAndVerify(ABC):

    @staticmethod
    @abstractmethod
    def generate_key_pair(nBit: int):
        raise NotImplementedError("Function should be implemented inside of class")

    @abstractmethod
    def sign(self, *args, **kwargs):
        raise NotImplementedError("Function should be implemented inside of class")

    @abstractmethod
    def verify(self, *args, **kwargs):
        raise NotImplementedError("Function should be implemented inside of class")




