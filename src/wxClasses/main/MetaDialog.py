# MetaDialog.py
import wx
import logging

from ObjectListView2 import ObjectListView, ColumnDefn

from handlers.Data import DataHandler


class MetaDialog(wx.Dialog):

    def __init__(self, parent, data):

        wx.Dialog.__init__(self, parent, title='Metadata Import',
                           pos=wx.DefaultPosition,
                           size=(400, 300),
                           style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.YES_NO)

        self.parent: wx.Frame = parent
        self.data: DataHandler = data

        self._create_widgets()
        self._create_boxes()
        self._create_binds()

    def _create_widgets(self):
        unimported_assets = self.data.db.assets.filter_by(imported_raw=False, installed_raw=True).all()

        if len(unimported_assets) > 1:
            label = f'Would you like to open Daz and import {len(unimported_assets)} assets?'
        elif len(unimported_assets) > 0:
            label = f'Would you like to open Daz and import 1 asset?'
        else:
            label = f'No assets to be imported into Daz.'

        self.message = wx.StaticText(self, label=label)
        self.message.SetFont(wx.Font(wx.FontInfo(12)))

        product_name_column = ColumnDefn("Product Name", "left", 160, "product_name", isSpaceFilling=True)

        columns = [product_name_column]

        self.olv = ObjectListView(parent=self, style=wx.LC_REPORT | wx.SUNKEN_BORDER,
                                  useAlternateBackColors=True, sortable=False)

        self.olv.SetEmptyListMsg('No Assets to be Imported')

        self.olv.SetColumns(columns)
        self.olv.SetObjects(unimported_assets)

        self.olv.oddRowsBackColor = wx.Colour(255, 255, 255)
        self.olv.evenRowsBackColor = wx.Colour(240, 240, 240)
        self.olv._FormatAllRows()

        self.yes_button = wx.Button(self, label='Yes')
        self.no_button = wx.Button(self, label='No')

        if not len(unimported_assets) > 0:
            self.yes_button.Disable()

    def _create_boxes(self):
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        button_box.Add(0, 0, 1)
        button_box.Add(self.yes_button, 0, border=5)
        button_box.Add(5, 0, 0)
        button_box.Add(self.no_button, 0, border=5)
        button_box.Add(0, 0, 1)

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(self.message, 0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(self.olv, 1, wx.EXPAND | wx.ALL, 5)
        main_box.Add(button_box, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_box)

    def _create_binds(self):
        self.yes_button.Bind(wx.EVT_BUTTON, self._on_yes_button)
        self.no_button.Bind(wx.EVT_BUTTON, self._on_no_button)

    def _on_close(self, event=None):
        self.EndModal(wx.ID_CLOSE)

    def _on_yes_button(self, event=None):
        self.EndModal(wx.ID_YES)

    def _on_no_button(self, event=None):
        self.EndModal(wx.ID_NO)
