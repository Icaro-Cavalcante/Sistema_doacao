# src/repositories/repository.py
from abc import ABC, abstractmethod

class Repo(ABC):
    '''Classe abstrata de repositórios.'''
    def __init__(self, database, table):
        self.database = database
        self.table = table

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def get_all(self):
        pass