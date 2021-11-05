from __future__ import annotations
from Seat import *

class Group:

    IDENTIFIER = "ID"
    SEATS = "seats"
    RATING = "rating"
    CHANGES = "changes"

    def __init__(self, groupIdentifier: str, seats: str, satisfactionRating: str, changesLeft: str = "3"):

        self.groupID = int(groupIdentifier)
        self.seats = []
        self.groupType = ""
        self.changesLeft = int(changesLeft)
        self.satisfactionRating = int(satisfactionRating)

        self._strToSeats(seats)
        self._updateType()

    def getSeats(self):
        return self.seats

    def getID(self):
        return self.groupID

    def getChangesLeft(self):
        return self.changesLeft

    def getSatisfactionRating(self):
        return self.satisfactionRating

    def setSatisfactionRating(self, rating: int):
        self.satisfactionRating = rating

    def updateSeats(self, seats: List[Seat]):
        self.seats = seats

        for s in seats:
            s.setStatus(True)
            s.setGroupID(self.groupID)

    def decreaseChangesLeft(self):
        self.changesLeft -= 1

    def _updateType(self):
        if len(self.seats) == 2:
            self.groupType = "Tourists"
        elif len(self.seats) > 2:
            self.groupType = "Family"
        else:
            self.groupType = "Business"

    def _strToSeats(self, string):
        self.seats = string.split(" ")

        for i in range(len(self.seats)):

            self.seats[i] = int(self.seats[i])

    #------------------------------------------------------------------------

    def writeToCSV(self):
        seatNums = str(self.seats[0].getID())
        for i in range(1, len(self.seats)):
            seatNums += " " + str(self.seats[i].getID())

        return {Group.IDENTIFIER: self.groupID, Group.SEATS: seatNums, Group.RATING: self.satisfactionRating, Group.CHANGES: self.changesLeft}

    @staticmethod
    def initFromCSV(d: Dict[str, str, str, str]) -> Group:
        return Group(d[Group.IDENTIFIER], d[Group.SEATS], d[Group.RATING], d[Group.CHANGES])

    @staticmethod
    def saveToCSV(groups: List[Group], filename: str = "groupData.csv"):

        with open(filename, 'w', newline='') as csvFile:
            fieldnames = [Group.IDENTIFIER, Group.SEATS, Group.RATING, Group.CHANGES]
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            for g in groups:
                writer.writerow(g.writeToCSV())

    @staticmethod
    def readFromCSV(filename: str = "groupData.csv") -> List[Group]:

        groups = []
        with open(filename, newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                groups.append(Group.initFromCSV(row))
        return groups