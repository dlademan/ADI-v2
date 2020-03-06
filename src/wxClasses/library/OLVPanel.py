import wx
import logging
from ObjectListView2 import ObjectListView, ColumnDefn

from handlers.Data import DataHandler


class OLVPanel(wx.Panel):
    """
    Panel that contains the list view of a library

    Attributes:
        self.olv: ObjectListView: wx.ListCtrl

    """

    def __init__(self, parent, data: DataHandler):
        wx.Panel.__init__(self, parent)
        self.data = data
        self.id_s = [0]

        self._create_widgets()
        self._create_boxes()
        self._create_binds()

    def _create_widgets(self):
        self.source_choice = wx.Choice(self, choices=self._get_choices())
        self.source_choice.SetSelection(0)

        id_column = ColumnDefn("ID", "right", 60, "id")
        sku_column = ColumnDefn("SKU", "right", 80, "sku")
        product_name_column = ColumnDefn("Product Name", "left", 160, "product_name", isSpaceFilling=True)
        zip_size_column = ColumnDefn("Zip Size", "right", 90, "size")
        installed_column = ColumnDefn("Installed", "right", 90, "installed")

        columns = [sku_column, product_name_column, installed_column, zip_size_column]

        self.olv = ObjectListView(parent=self, style=wx.LC_REPORT | wx.SUNKEN_BORDER,
                                  useAlternateBackColors=True)

        self.olv.SetColumns(columns)
        self.olv.SetObjects(self.data.db.assets.all)

        self.olv.oddRowsBackColor = wx.Colour(255, 255, 255)
        self.olv.evenRowsBackColor = wx.Colour(240, 240, 240)
        self.olv._FormatAllRows()

    def _create_boxes(self):
        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(self.source_choice, 0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(self.olv, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_box)

    def _create_binds(self):
        self.source_choice.Bind(wx.EVT_CHOICE, self.on_source_change)

    def _get_choices(self):
        choices = ['All Assets']

        for source in self.data.db.sources:
            choices.append(source.path_raw)
            self.id_s.append(source.id)

        return choices

    def on_source_change(self, event: wx.Event = None):
        selection: int = self.source_choice.GetSelection()
        id: int = self.id_s[selection]
        source = self.data.db.sources[id]

        if selection == 0:
            assets = self.data.db.assets.all
        else:
            assets = self.data.db.assets.filter_by(source_id=source.id).all()

        self.olv.DeleteAllItems()
        self.olv.SetObjects(assets)
