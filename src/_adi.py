from src.MainFrame import MainFrame
import wx.adv


class ADI(wx.App):
    """ADI application class"""

    def OnInit(self):
        # todo add check for debug in arguments
        frame = MainFrame(None, -1, "Alternative Daz Importer")

        return True


if __name__ == '__main__':
    app = ADI()
    app.MainLoop()
