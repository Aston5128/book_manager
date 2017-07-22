import wx
from book_manager.bookpanel import BookPanel


class BookFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, style=wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX)

        self.__width, self.__height = 555, 460

        screen_size = wx.DisplaySize()
        self.SetPosition(((screen_size[0] - self.__width) / 2, (screen_size[1] - self.__height) / 2))

        self.SetTitle('Leida团队图书管理系统')

        self.SetIcon(wx.Icon('bgi.ico', wx.BITMAP_TYPE_ICO))

        BookPanel(self)

        self.SetSize(self.__width, self.__height)


if __name__ == '__main__':
    app = wx.App()
    BookFrame().Show(True)
    app.MainLoop()
