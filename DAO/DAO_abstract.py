from abc import ABC, abstractmethod


class DAO(ABC):
    """A DAO alap osztálya"""
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.con = None

    @abstractmethod
    def connect(self):
        """Csatlakozik az adatbázishoz"""
        pass

    @abstractmethod
    def close(self):
        """Lezárja a kapcsolatot az adatbázissal"""
        pass

    @abstractmethod
    def insert(self, name:str, score:str, level:int):
        """Beilleszt adatot az adatbázisba"""
        pass

    @abstractmethod
    def create_table(self):
        """Létrehozza a táblázatot"""
        pass

    @abstractmethod
    def get_all(self, level:int):
        """Kilistázza az összes elemet a megadott szinthez"""
        pass