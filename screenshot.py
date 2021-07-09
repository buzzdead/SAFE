import sys

import pyWinhook
import pythoncom
import win32con
import win32gui
import win32ui


def saveScreenShot(x, y, width, height, path):
    # grab a handle to the main desktop window
    hdesktop = win32gui.GetDesktopWindow()

    # create a device context
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    # create a memory based device context
    mem_dc = img_dc.CreateCompatibleDC()

    # create a bitmap object
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

    # copy the screen into our memory device context
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (x, y), win32con.SRCCOPY)

    # save the bitmap to a file
    screenshot.SaveBitmapFile(mem_dc, path)
    # free our objects
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())


# Callback function when the event is fired
def onMouseDown(event):
    # Here, the beginning of your rectangle drawing
    # [...]

    # Subscribe the event to the callback
    print(event.Position)
    coords.append(event.Position)
    return 0


def onMouseUp(event):
    # Here, the beginning of your rectangle drawing
    # [...]

    # Subscribe the event to the callback
    print(event.Position)
    hdc = win32gui.GetWindowDC(0)
    x, y = coords[0]
    dx, dy = event.Position

    if dx < x:
        tmp_x = x
        x = dx
        dx = tmp_x
    if dy < y:
        tmp_y = y
        y = dy
        dy = tmp_y

    #win32gui.DrawFocusRect(hdc, (x, y, dx, dy))
    #win32gui.DeleteDC(hdc)
    saveScreenShot(x, y, dx - x, dy - y, "saved.png")
    sys.exit()


if __name__ == '__main__':
    coords = []
    hdc = win32gui.GetWindowDC(0)
    hm = pyWinhook.HookManager()
    hm.MouseLeftDown = onMouseDown
    hm.MouseLeftUp = onMouseUp
    hm.HookMouse()
    pythoncom.PumpMessages()
