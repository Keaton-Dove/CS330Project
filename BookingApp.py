import sys

sys.path.append('./Reed files')
from View import *
from graphics import *
from Button import *
from RadioButtons import *

from Group import *
from typing import List
from random import *

class BookingApp:

    def __init__(self, amountSeats: int, window: GraphWin):
        self.amountSeats = amountSeats
        self.window = window

        # Seat arrays
        self._seats: List[Seat] = []
        self._openSeats: List[Seat] = []
        self._seatIDToSeat: [int, Seat] = {}

        # Group arrays
        self._activeGroupID = None
        self._groups: List[Group] = []
        self._groupIDToGroup: [int, Group] = {}

        self._strToWinDict: [str, View] = {}

        self._managerPin = 9999

    #--------------------------------------------------------------------
    """ DATA MANAGEMENT """

    def loadData(self):

        for i in range(0, self.amountSeats):
            s = Seat(i)
            self._seats.append(s)
            self._seatIDToSeat[i] = s

        try:
            # Load seats
            self._groups = Group.readFromCSV()

            for i in range(len(self._groups)):
                self._initGroup(self._groups[i])

            self._updateSeats()

        except:
            self._groups = []

    def saveData(self):
        Group.saveToCSV(self._groups)

    def deleteData(self):
        self._groups = []
        self._groupIDToGroup = {}

        for i in self._seats:
            i.setStatus(False)
            i.setGroupID()

    def _initGroup(self, g: Group):
        # Creating dictionary entry linking groupID to group
        self._groupIDToGroup[g.getID()] = g

        # For each group, we will get the str seat IDs and get the corresponding seat
        actualSeats = []
        seatIDs = g.getSeats()

        for j in seatIDs:
            actualSeats.append(self.idToSeat(j))

        # And switch the list of IDs with the actual seats.
        g.updateSeats(actualSeats)

    def _updateSeats(self):
        # Refreshing seat groupIDs
        for s in self._seats:
            s.setGroupID()
        for g in self._groups:
            for i in g.getSeats():
                i.setGroupID(g.getID())

        self._openSeats = []
        # Updating which seats are open based on each seat's status
        for s in self._seats:
            if not s.getStatus():
                self._openSeats.append(s)

    #--------------------------------------------------------------------
    """ DICTIONARY MANAGEMENT """

    # Return window based on winName keyword
    def strToWin(self, winName: str) -> View:
        return self._strToWinDict[winName]

    # Return seat based on ID
    def idToSeat(self, seatID: int) -> Seat:
        return self._seatIDToSeat[seatID]

    # Return group based on ID
    def idToGroup(self, groupID: int):
        try:
            return self._groupIDToGroup[groupID]
        except:
            return None

    # Add dictionary entry
    def addStrToWin(self, info: [str, View]):
        self._strToWinDict[info[0]] = info[1]

    #--------------------------------------------------------------------
    """ GETTERS """

    def getAmntSeats(self) -> int:
        return len(self._seats)

    def getActiveGroupID(self) -> int:
        if self._activeGroupID == None:
            return -1
        else:
            return self._activeGroupID

    def getWindow(self) -> GraphWin:
        return self.window

    #---------------------------------------------------------------------
    """ BOOKING ALGORITHMS """

    def book(self, amnt: int) -> bool:
        # Updating the seats before beginning the booking process
        self._updateSeats()

        # If the amount of seats requested is more than the amount of available seats, booking cannot be performed
        if amnt > len(self._openSeats):
            return False

        group = self._amntToBooking(amnt)

        # Implementing the group into the booking app and setting the new group as the active group
        self._groups.append(group)
        self._initGroup(group)
        self.setActiveGroup(group.getID())

        return True

    def changeBooking(self) -> bool:
        group = self.idToGroup(self._activeGroupID)

        currentSeats = group.getSeats()

        if len(currentSeats) > len(self._openSeats):
            return False

        tempGroup = self._amntToBooking(len(currentSeats))

        # Messy code, turning the seat IDs from the temp group into a list of actual seats
        seats = []
        for s in tempGroup.getSeats():
            seats.append(self.idToSeat(s))

        # Updating the active group with its new seats and rating
        group.updateSeats(seats)
        group.setSatisfactionRating(tempGroup.getSatisfactionRating())
        # And decreasing the changes left
        group.decreaseChangesLeft()

        self._updateSeats()

        return True

    def _bookFamily(self, amnt: int, id: int) -> Group:
        score = 0
        seatsList: List[Seat] = []
        seatIndex = 0

        """ Best case, there are adjacent aisle seats """
        aisleSeats = self._sectionSeats("aisle")
        # Since we check seats beyond the current index, we will stop before reaching the end of the list
        lastSeatIndexToCheck = len(aisleSeats) - (amnt)

        while seatIndex <= lastSeatIndexToCheck:

            # Creating a temp list of seats
            tempSeats: List[Seat] = []
            for i in range(amnt):
                # Appending the aisle seats from the beginning of the index
                tempSeats.append(aisleSeats[seatIndex + i])

            # If the tempSeats are adjacent, they are a match
            if self._checkAdjacent(tempSeats):
                seats = self._seatsToStr(tempSeats)
                score += 15
                # Creating a group with these seats
                return Group(str(id), seats, str(score))

            # Otherwise we keep checking
            seatIndex += 1

        """ Middling scenario, checking left side for grouped seats """
        leftSeats = self._sectionSeats("left")
        lastSeatIndexToCheck = len(leftSeats) - (amnt)

        while seatIndex <= lastSeatIndexToCheck:

            tempSeats: List[Seat] = []
            for i in range(amnt):
                tempSeats.append(leftSeats[seatIndex + i])

            if self._checkAdjacent(tempSeats):
                seats = self._seatsToStr(tempSeats)
                score += 10
                return Group(str(id), seats, str(score))

            seatIndex += 1

        """ Middling scenario, checking right side for grouped seats """
        rightSeats = self._sectionSeats("right")
        lastSeatIndexToCheck = len(rightSeats) - (amnt)

        while seatIndex <= lastSeatIndexToCheck:

            tempSeats: List[Seat] = []
            for i in range(amnt):
                tempSeats.append(rightSeats[seatIndex + i])

            if self._checkAdjacent(tempSeats):
                seats = self._seatsToStr(tempSeats)
                score += 10
                return Group(str(id), seats, str(score))

            seatIndex += 1

        """ Middling scenario, checking each row for available seats """
        for i in range(20):
            rowSeats = self._checkRow(i, amnt)

            if rowSeats is not False:
                seats = self._seatsToStr(rowSeats)
                score += 10
                return Group(str(id), seats, str(score))

        """ Base case, booking the first available seats for the family """
        seatsList = self._openSeats[0:amnt]
        seats = self._seatsToStr(seatsList)
        score -= 10

        return Group(str(id), seats, str(score))

    def _bookTourists(self, id: int) -> Group:

        """Initializing the variables for the loops"""
        score = 0
        seats = ""

        seatIndex = 0
        seatID = self._openSeats[seatIndex].getID()
        # Does not need updated
        lastSeatID = self._openSeats[-1].getID()

        # Starting at the first non-select seat
        while seatID < 12:
            seatIndex += 1
            seatID = self._openSeats[seatIndex].getID()

        # Getting the seat name and the id of the next open seat
        seatName = self._openSeats[seatIndex].getName()
        nextSeatID = self._nextSeat(seatIndex)

        """Best case scenario: looking for window seat and adjacent seat"""
        while seatID is not lastSeatID:
            # If the column identifier is 1 or 5 and the next seat is next to the current seat, match
            if (seatName[1] == "1" or seatName[1] == "5") and nextSeatID == seatID + 1:
                seats += str(seatID) + " " + str(nextSeatID)
                score += 15
                return Group(str(id), seats, str(score))

            seatIndex += 1
            seatID = self._openSeats[seatIndex].getID()
            nextSeatID = self._nextSeat(seatIndex)
            seatName = self._openSeats[seatIndex].getName()

        """Second scenario: looking for two adjacent seats anywhere"""
        seatIndex = 0
        seatID = self._openSeats[seatIndex].getID()
        nextSeatID = self._nextSeat(seatIndex)
        seatName = self._openSeats[seatIndex].getName()

        while seatID is not lastSeatID:
            # If the column identifier is less than 6, and the next seat is next to the current seat, they are adjacent
            if int(seatName[1]) < 6 and nextSeatID == seatID + 1:
                seats += str(seatID) + " " + str(nextSeatID)
                score += 10
                return Group(str(id), seats, str(score))

            seatIndex += 1
            seatID = self._openSeats[seatIndex].getID()
            nextSeatID = self._nextSeat(seatIndex)
            seatName = self._openSeats[seatIndex].getName()

        """Third scenario: first two available seats"""
        # If we aren't able to find adjacent seats, we just take the first two available seats
        seatID = self._openSeats[0].getID()
        nextSeatID = self._nextSeat(0)

        seats += str(seatID) + " " + str(nextSeatID)
        score -= 10
        return Group(str(id), seats, str(score))

    def _bookBusiness(self, id: int) -> Group:
        # Score starts at 10, group can't be split up because there is only 1 person
        score = 10

        # Starting at the first available seat, if there are any select seats, the first open seat will be one of them
        seat = self._openSeats[0].getID()

        # If the first available seat is business select, +5 points for preference
        if seat < 12:
            score += 5

        # Create and return group
        return Group(str(id), str(seat), str(score))

    # Booking helper methods
    def _amntToBooking(self, amnt: int) -> Group:

        # Start booking by generating an ID
        groupID = self._genGroupID(amnt)
        group = None

        # Calling the respective booking algorithm for the given group
        if amnt == 1:
            group = self._bookBusiness(groupID)
        elif amnt == 2:
            group = self._bookTourists(groupID)
        else:
            group = self._bookFamily(amnt, groupID)

        return group

    def _genGroupID(self, amnt: int) -> int:
        groupID = str(amnt)

        while (True):
            idGen = randrange(0, 1000)
            if (idGen < 10):
                idGen = "00" + str(idGen)
            elif (idGen < 100):
                idGen = "0" + str(idGen)
            else:
                idGen = str(idGen)

            tempID = groupID + idGen
            tempID = int(tempID)

            if self.idToGroup(tempID) == None:
                break

        groupID = tempID
        return groupID

    def _nextSeat(self, index: int) -> int:
        # Trying to get the next seat in the list of open seats
        try:
            nextSeatID = self._openSeats[index + 1].getID()
        # If there aren't any more, try resetting back to the beginning of the open seat list
        except:
            nextSeatID = self._openSeats[0].getID()

        return nextSeatID

    def _sectionSeats(self, area: str) -> List[Seat]:

        seatGroup: List[Seat] = []

        """ Checking for seats in the left two columns """
        if area == "left":
            # Checking all open seats...
            for s in self._openSeats:
                # If the seat name is column 1 or 2, it is a left seat
                sName = s.getName()
                if int(sName[1]) < 4:
                    seatGroup.append(s)

        """ Checking for aisle seats """
        if area == "aisle":
            # Checking all open seats...
            for s in self._openSeats:
                # If the seat name is column 3 or 4, it is an aisle seat
                sName = s.getName()
                if sName[1] == "3" or sName[1] == "4":
                    seatGroup.append(s)

        """ Checking for seats in the right two columns"""
        if area == "right":
            # Checking all open seats...
            for s in self._openSeats:
                # If the seat name is column 5 or 6, it is a right seat
                sName = s.getName()
                if int(sName[1]) > 3:
                    seatGroup.append(s)

        return seatGroup

    def _seatsToStr(self, seats: List[Seat]) -> str:
        # Creating an empty string to be added to
        seatStr = ""
        # Adding the ID of each seat and a space after
        for i in range(len(seats) - 1):
            seatStr += str(seats[i].getID()) + " "
        # Except for the last which doesn't have a space after the ID
        seatStr += str(seats[-1].getID())

        return seatStr

    def _checkAdjacent(self, seats: List[Seat]) -> bool:
        rows = "ABCDEFGHJKLMNPRTUVXY"

        # List of all seat names within the list
        seatNames: List[str] = []

        for s in seats:
            seatNames.append(s.getName())

        adjacentSeats = 0
        multiAdjacentSeats = 0

        for i in seatNames:
            adjacency = 0

            for j in seatNames:
                # If two seats are left or right of one another, they are adjacent
                if i[0] == j[0] and ((int(i[1]) == int(j[1]) - 1) or (int(i[1]) == int(j[1]) + 1)):
                    adjacency += 1
                # If two seats are in the same column and 1 above or below the other, they are adjacent
                elif i[1] == j[1] and ((rows.index(i[0]) == rows.index(j[0]) - 1) or (rows.index(i[0]) == rows.index(j[0]) + 1)):
                    adjacency += 1

            # If the the given seat is adjacent to at least one other seat, the amount of adjacent seats is incremented
            if adjacency > 0:
                adjacentSeats += 1
            if adjacency > 1:
                multiAdjacentSeats += 1

        # All seats must have at least one adjacency for the group to be together
        return (multiAdjacentSeats >= len(seats) - 2) and (adjacentSeats == len(seats))

    def _checkRow(self, index: int, amnt: int):
        rows = "ABCDEFGHJKLMNPRTUVXY"

        rowOpenSeats: List[Seat] = []

        # Filling array with open seats in a given row
        for s in self._openSeats:
            # If the letter in the seat name is the same as the given row, it gets added
            if s.getName()[0] == rows[index]:
                rowOpenSeats.append(s)

        # If there are not enough seats for the group, it is not suitable
        if len(rowOpenSeats) < amnt:
            return False

        # Otherwise we check every possibility for a group of open seats
        loopAmnt = (len(rowOpenSeats) - amnt) + 1
        for i in range(loopAmnt):
            # If we find a cluster that is open, take it
            if self._checkAdjacent(rowOpenSeats[i : amnt + i]):
                return rowOpenSeats[i : amnt + i]

        # Otherwise nothing could be found grouped
        return False

    # ---------------------------------------------------------------------
    """ MANAGER REPORT """

    def managerReport(self) -> (int, float):
        # Calling both helper methods that calc the num of passengers and average satisfaction score
        numPassengers = self._numPassengers()
        averageScore = self._averageScore()

        return numPassengers, averageScore

    def _numPassengers(self) -> int:
        # Return total amount of seats - the amount that are open
        return self.amountSeats - len(self._openSeats)

    def _averageScore(self) -> float:

        # If there aren't any groups, just return 0
        if len(self._groups) == 0:
            return 0

        # Array for the random groups
        randomGroups: List[Group] = []

        # If there are more than 10 groups, we will select a random 10 of them
        if len(self._groups) > 10:

            # Creating array of the indexes currently added to the randomGroups array and initializing a count
            selectedGroups: List[int] = []
            amntGroups = 0

            # Adding random groups until we have 10
            while amntGroups < 10:
                random = randrange(0, len(self._groups))

                if selectedGroups.count(random) == 0:

                    randomGroups.append(self._groups[random])
                    selectedGroups.append(random)
                    amntGroups += 1

        # If there are 10 or less groups, the random groups are just all the groups we have
        else:
            randomGroups = self._groups

        # Accumulate the scores for every group
        totalScore = 0
        for g in randomGroups:
            totalScore += g.getSatisfactionRating()

        # Return the average
        return totalScore / len(randomGroups)

    # ---------------------------------------------------------------------
    """ EXTRANEOUS METHODS """

    @staticmethod
    def switchWindow(oldWin: View, newWin: View):
        # Hiding all elements from the old window and showing the new window
        if oldWin is not None:
            oldWin.hide()
        newWin.show()

    def setActiveGroup(self, groupID: int) -> bool:
        # Trying to set the active group to the given ID
        activeGroup = self.idToGroup(groupID)

        # If there is no group by that ID, return false
        if activeGroup is None:
            return False
        # Otherwise the group has been set and we can return true
        else:
            self._activeGroupID = activeGroup.getID()
            return True

    def checkManagerPin(self, pin: int) -> bool:
        # Checking the manager login key
        return pin == self._managerPin

    def exit(self):
        self.saveData()
        sys.exit(0)
