#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
assert sys.platform == "linux"

from typing import Union, Optional

from Xlib.xobject.drawable import Window as XWindow
from ._main import Box
from ewmhlib import EwmhWindow


def _getHandle(handle: Union[int, XWindow]) -> Optional[EwmhWindow]:

    newHandle = None
    if isinstance(handle, int):
        newHandle = EwmhWindow(handle)
    elif isinstance(handle, XWindow):
        newHandle = EwmhWindow(handle.id)
    return newHandle


def _getWindowBox(handle: EwmhWindow) -> Box:
    # https://stackoverflow.com/questions/12775136/get-window-position-and-size-in-python-with-xlib
    geom = handle.xWindow.get_geometry()
    pos = handle.root.translate_coords(handle.id, 0, 0)
    return Box(pos.x, pos.y, geom.width, geom.height)


def _moveResizeWindow(handle: EwmhWindow, newBox: Box):
    newLeft = max(0, newBox.left)  # Xlib won't accept negative positions
    newTop = max(0, newBox.top)
    handle.setMoveResize(x=newLeft, y=newTop, width=newBox.width, height=newBox.height, userAction=True)
    # handle.configure(x=newLeft, y=newTop, width=newBox.width, height=newBox.height)

