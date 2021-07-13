import pyWinhook
import pythoncom
import win32api
import win32con
import win32gui
import win32ui

coords = []
dc = win32gui.GetDC(0)
dcObj = win32ui.CreateDCFromHandle(dc)
hwnd = win32gui.WindowFromPoint((0, 0))
monitor = (0, 0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))


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
    coords.append(event.Position)
    return 0


def flipXY(x, y, dx, dy):
    # In the case of inverting the rectangle
    if dx < x:
        tmp_x = x
        x = dx
        dx = tmp_x
    if dy < y:
        tmp_y = y
        y = dy
        dy = tmp_y
    return x, y, dx, dy


def onMouseMove(event):
    if len(coords) > 0:
        x, y = coords[0]
        dx, dy = event.Position
        x, y, dx, dy = flipXY(x, y, dx, dy)
        dcObj.DrawFocusRect((x, y, dx, dy))
        win32gui.InvalidateRect(hwnd, monitor, True)  # Refresh the entire monitor
    return 1


def onMouseUp(event):
    x, y = coords[0]
    dx, dy = event.Position
    x, y, dx, dy = flipXY(x, y, dx, dy)

    # Subscribe the event to the callback
    saveScreenShot(x, y, dx - x, dy - y, "files/saved.png")
    win32api.PostQuitMessage(0)
    return 1


def activateScreenShot():
    coords.clear()
    hm = pyWinhook.HookManager()
    hm.MouseLeftDown = onMouseDown
    hm.MouseLeftUp = onMouseUp
    hm.MouseMove = onMouseMove
    hm.HookMouse()
    pythoncom.PumpMessages()
    hm.UnhookMouse()
