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
    def insert(self, name: str, score: int, level: int):
        """Beilleszt adatot az adatbázisba
        :param name: a játékos neve
        :param score: a játékos pontja
        :param level: a szint
        :returns: True ha sikerült a beillesztés, False ha nem"""
        pass

    @abstractmethod
    def create_table(self):
        """Létrehozza a táblázatot"""
        pass

    @abstractmethod
    def get_all(self, level:int):
        """Visszadja az összes játékost a megadott szinthez, pontszám szerint csökkenő sorrendbe
        :param level: a szint amit kilistáznánk
        :returns: lista amibe a név és a pont objektum van"""
        pass
