from __future__ import annotations
from typing import List, Dict
import csv

class Seat:

    IDENTIFIER = "ID"

    ROW_TITLES = "ABCDEFGHJKLMNPRTUVXY"

    def __init__(self, idNum: int, status: bool = False):
        # True is for taken, False is for available
        self.status = status
        self.id = idNum
        self.name = ""
        self.groupID = None

        self._calcSeatName()

    def setStatus(self, status: bool):
        self.status = status

    def setGroupID(self, id: int=None):
        self.groupID = id

    def getStatus(self) -> bool:
        return self.status

    def getGroupID(self) -> int:
        return self.groupID

    def getID(self) -> int:
        return self.id

    def getName(self) -> str:
        return self.name

    def _calcSeatName(self):
        name = ""
        # Getting row letter
        name += Seat.ROW_TITLES[self.id // 6]
        # Getting seat number for corresponding row
        name += str((self.id % 6) + 1)
        self.name = name