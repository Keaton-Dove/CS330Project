#!/usr/bin/env python3

# ----------------------------------------------------------------------
# EventLoop.py
# Dave Reed
# 09/29/2020
# ----------------------------------------------------------------------

from View import *

class EventLoop:

    _window: GraphWin
    _view: View

    # ------------------------------------------------------------------

    def __init__(self, title: str, width: int, height: int):
        self._window = GraphWin(title, width, height)
        self._view = View()

    # ------------------------------------------------------------------

    def window(self) -> GraphWin:
        return self._window

    # ------------------------------------------------------------------

    def addSubView(self, view: View):
        self._view.addSubView(view)

    # ------------------------------------------------------------------

    def run(self):

        # Commenting this line out because our windows are made up of views that should not all be showing at runtime
        #self._view.show()

        while True:
            pt = self._window.getMouse()
            self._view.clicked(pt)

    # ------------------------------------------------------------------

    # ------------------------------------------------------------------

# ----------------------------------------------------------------------
