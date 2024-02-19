from abc import ABC, abstractmethod


class Parser(ABC):

    def __int__(self, src, dest, name):
        self.src = src
        self.dest = dest
        self.name = name

    @abstractmethod
    def parse(self):
        pass

