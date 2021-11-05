#!/usr/bin/env python3

# ----------------------------------------------------------------------
# Button.py
# Dave Reed
# 09/29/2020
# ----------------------------------------------------------------------

from View import *

# ----------------------------------------------------------------------

class Button(RectangularClickableView):

    def __init__(self, window: GraphWin, title: str, textSize: int, center: Point, width: float, height: float, clickHandler = None):
        """
        :param window: GraphWin to create the button
        :param title: title string for the button
        :param center: center Point for the button
        :param width: width of button
        :param height: height of button
        :param clickHandler: function or method that takes a Button and Point and is called if the button is pressed with this Button and
        coordinate of the click that is inside the button
        """

        super().__init__(center, width, height, clickHandler)
        r = Rectangle(Point(self._xMin, self._yMin), Point(self._xMax, self._yMax))
        r.setFill("white")
        t = Text(center, title)
        t.setSize(textSize)
        self.addSubView(DrawableView(r, window))
        self.addSubView(DrawableView(t, window))

# ----------------------------------------------------------------------
