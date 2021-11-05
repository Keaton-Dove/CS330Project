#!/usr/bin/env python3

# ----------------------------------------------------------------------
# View.py
# Dave Reed
# 09/29/2020
# ----------------------------------------------------------------------

from __future__ import annotations
from typing import List, Optional

from graphics import *

class View:

    _subViews: List[View]
    _isHidden: bool

    # ------------------------------------------------------------------

    def __init__(self):
        self._isHidden = True
        self._subViews = []

    # ------------------------------------------------------------------

    def addSubView(self, view: View):
        self._subViews.append(view)

    # ------------------------------------------------------------------

    def show(self):
        if self._isHidden:
            self._isHidden = False
            for v in self._subViews:
                v.show()

    # ------------------------------------------------------------------

    def hide(self):
        if not self._isHidden:
            self._isHidden = True
            for v in self._subViews:
                v.hide()

    # ------------------------------------------------------------------

    def clicked(self, pt: Point) -> bool:
        for v in self._subViews:
            if v.clicked(pt):
                return True
        return False

    # ------------------------------------------------------------------

# ----------------------------------------------------------------------

class DrawableView(View):

    _graphicsObject: GraphicsObject
    _graphWin: Optional[GraphWin]

    def __init__(self, graphicsObject: GraphicsObject, graphWin: GraphWin):
        super().__init__()
        self._graphicsObject = graphicsObject
        self._graphWin = graphWin

    def show(self):
        if self._isHidden:
            self._graphicsObject.draw(self._graphWin)
            self._isHidden = False

    def hide(self):
        if not self._isHidden:
            self._graphicsObject.undraw()
            self._isHidden = True

    def addSubView(self, view: View):
        raise GraphicsError("cannot add a subview to a DrawableView")

    def graphicsObject(self) -> GraphicsObject:
        return self._graphicsObject

# ----------------------------------------------------------------------

class ClickableView(View):

    _isEnabled: bool

    def __init__(self, clickHandler = None):
        super().__init__()
        self._isEnabled = True
        self._clickHandler = clickHandler

    def enable(self):
        self._isEnabled = True

    def disable(self):
        self._isEnabled = False

    def _hitTest(self, pt: Point) -> bool:
        raise NotImplemented("subclass of ClickableView must implement hitTest")

    def clicked(self, pt: Point) -> bool:
        if self._isEnabled and not self._isHidden:
            if self._hitTest(pt):
                if self._clickHandler is not None:
                    self._clickHandler(self, pt)
                return True
        return False

# ----------------------------------------------------------------------

class RectangularClickableView(ClickableView):

    _xMin: float
    _yMin: float
    _xMax: float
    _yMax: float

    def __init__(self, center: Point, width: float, height: float, clickHandler=None):
        super().__init__(clickHandler)
        halfWidth = 0.5 * width
        halfHeight = 0.5 * height

        # make copies and find min and max corner points
        p1 = center.clone()
        p2 = center.clone()
        p1.move(-halfWidth, -halfHeight)
        p2.move(halfWidth, halfHeight)

        # set instance variables for bounds
        x1, y1 = p1.getX(), p1.getY()
        x2, y2 = p2.getX(), p2.getY()
        self._xMin, self._xMax = x1, x2
        self._yMin, self._yMax = y1, y2

    def _hitTest(self, pt: Point) -> bool:
        return (not self._isHidden) and self._xMin < pt.getX() < self._xMax and self._yMin < pt.getY() < self._yMax
