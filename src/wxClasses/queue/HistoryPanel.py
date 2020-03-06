# HistoryPanel.py
import wx
import logging
from pathlib import Path
from ObjectListView2 import ObjectListView, ColumnDefn


class HistoryPanel(wx.Panel):

    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.data = data

        self._create_widgets()
        self._create_boxes()
        self._create_binds()

    def _create_widgets(self):

        asset_column = ColumnDefn("Asset", "left", 60, "asset.product_name", isSpaceFilling=True)
        date_column = ColumnDefn("Completed", "right", 100, "completed")
        process_column = ColumnDefn("Process", "right", 100, "process")
        status_column = ColumnDefn("Status", "right", 80, "status")

        columns = [asset_column, date_column, process_column, status_column]

        self.olv = ObjectListView(parent=self, style=wx.LC_REPORT | wx.SUNKEN_BORDER,
                                  useAlternateBackColors=True, sortable=False)

        self.olv.SetEmptyListMsg('No items in history')

        assets = self.data.db.queue.not_pending
        logging.debug(f'history panel assets: {assets}')

        self.olv.SetColumns(columns)
        self.olv.SetObjects(assets)

        self.olv.oddRowsBackColor = wx.Colour(255, 255, 255)
        self.olv.evenRowsBackColor = wx.Colour(240, 240, 240)
        self.olv._FormatAllRows()

    def _create_boxes(self):
        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(self.olv, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_box)

    def _create_binds(self):
        pass

    def refresh(self):
        self.olv.DeleteAllItems()
        self.olv.SetObjects(self.data.db.queue.pending)
