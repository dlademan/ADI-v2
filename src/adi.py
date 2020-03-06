from wxClasses.main._MainFrame import MainFrame
import wx.lib.mixins.inspection


class ADI(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    """ADI application class"""

    def OnInit(self):
        self.Init()
        frame = MainFrame(None, -1, "Alternative Daz Importer")
        return True


if __name__ == '__main__':
    app = ADI()
    app.MainLoop()
