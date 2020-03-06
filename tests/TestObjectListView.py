import wx
import logging
from ObjectListView2 import ColumnDefn, ObjectListView

from handlers.Data import DataHandler


class TestObjectListViewApp(wx.App):
    """Application class for testing FolderTree generation"""

    def OnInit(self):
        frame = TestObjectListViewFrame(None, "TestObjectListViewFrame")

        return True


class TestObjectListViewFrame(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, wx.ID_ANY, title,
                          pos=wx.DefaultPosition,
                          size=(600, 800),
                          style=wx.DEFAULT_FRAME_STYLE)

        self.data = DataHandler()

        self._create_body()
        self.Show()
        logging.info('---------------- TestListView Shown')

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def _disable_frame(self, event=None):
        # self.library_panel.Disable()
        pass

    def _enable_frame(self, event=None):

        pass

    def _create_body(self):
        idn_column = ColumnDefn("ID", "right", 60, "idn")
        sku_column = ColumnDefn("SKU", "right", 80, "sku")
        product_name_column = ColumnDefn("Product Name", "left", 160, "product_name", isSpaceFilling=True)
        filename_column = ColumnDefn("File Name", "left", 180, "filename", isSpaceFilling=True)
        zip_size_column = ColumnDefn("Zip Size", "right", 90, "get_size")
        installed_column = ColumnDefn("Installed", "right", 90, "get_installed")

        columns = [idn_column, sku_column, product_name_column, zip_size_column, installed_column]
        assets = self.data.db.select_all_assets()

        panel = wx.Panel(self)
        box = wx.BoxSizer()

        self.olv = ObjectListView(parent=panel, style=wx.LC_REPORT | wx.SUNKEN_BORDER,
                                  useAlternateBackColors=True)
        self.olv.SetColumns(columns)
        self.olv.SetObjects(assets)

        self.olv.oddRowsBackColor = wx.Colour(255, 255, 255)
        self.olv.evenRowsBackColor = wx.Colour(240, 240, 240)
        self.olv._FormatAllRows()

        box.Add(self.olv, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(box)

    def on_close(self, event):
        self.data.close()
        event.Skip()


app = TestObjectListViewApp()
app.MainLoop()
