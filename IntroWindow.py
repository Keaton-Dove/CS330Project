from BookingApp import *

class IntroWindow(View):

    def __init__(self, app: BookingApp):
        super().__init__()

        self.app = app
        self.window = self.app.getWindow()

        # Set background (Plane.png)
        try:
            backgroundPic = Image(Point(400, 400), "Plane.png")
            backgroundPicV = DrawableView(backgroundPic, self.window)
            self.addSubView(backgroundPicV)
            backgroundPicV.show()
        except:
            pass

        # Creating the title
        title = Text(Point(400, 150), "Capital Airlines")
        title.setStyle('bold')
        title.setSize(56)
        title.setFace('courier')
        titleV = DrawableView(title, self.window)
        self.addSubView(titleV)

        whiteBG = Rectangle(Point(325, 520), Point(640, 640))
        whiteBG.setFill("white")
        whiteBGV = DrawableView(whiteBG, self.window)
        self.addSubView(whiteBGV)

        enterIDText = Text(Point(480, 555), "Please enter group ID number:")
        enterIDText.setSize(16)
        enterIDTextV = DrawableView(enterIDText, self.window)
        self.addSubView(enterIDTextV)

        self.groupIDEntry = Entry(Point(480, 595), 30)
        self.groupIDEntry.setFill("light gray")
        groupIDEntryV = DrawableView(self.groupIDEntry, self.window)
        self.addSubView(groupIDEntryV)


        # Buttons to specify if you are a new or returning customer
        idEnterButton = Button(self.window, "Enter", 14, Point(700, 580), 75, 50, clickHandler=self.idEnterButtonCallback)
        self.addSubView(idEnterButton)

        newButton = Button(self.window, "New customer?", 18, Point(175, 580), 200, 120, clickHandler=self.newButtonCallback)
        self.addSubView(newButton)

    def newButtonCallback(self, b: Button, p: Point):
        mainWin = self.app.strToWin("MainWindow")
        self.app.switchWindow(self, mainWin)

    def idEnterButtonCallback(self, b: Button, p: Point):

        try:
            # If any of this fails, "Invalid group ID" is displayed

            # Getting group ID from Text entry
            groupID = int(self.groupIDEntry.getText())

            # First checking if the int entered is the manager pin
            if self.app.checkManagerPin(groupID):
                managerWin = self.app.strToWin("ManagerWindow")
                self.app.switchWindow(self, managerWin)

            # Getting a bool as to whether or not the num corresponds to a group
            if self.app.setActiveGroup(groupID):
                mainWin = self.app.strToWin("MainWindow")
                self.app.switchWindow(self, mainWin)

        except:
            pass