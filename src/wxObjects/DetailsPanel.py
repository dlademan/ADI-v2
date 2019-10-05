import wx

from Handlers.Data import DataHandler
from sqlObjects.Asset import Asset
from sqlObjects.Folder import Folder
from sqlObjects.Source import Source


class DetailsPanel(wx.Panel):
    """
    Panel that contains the tree view of a library

    Attributes:

    """

    def __init__(self, parent, data: DataHandler):
        wx.Panel.__init__(self, parent=parent)
        self.data = data

        self._create_widgets()
        self._create_boxes()

    def _create_widgets(self):
        font_title = wx.Font(wx.FontInfo(16))
        font_data = wx.Font(wx.FontInfo(11))

        self.name_label = wx.StaticText(self, label='', style=wx.ALIGN_RIGHT)
        self.name_label.SetFont(font_title)

        self.label_1 = wx.StaticText(self, label='SKU:', style=wx.ALIGN_RIGHT)
        self.label_2 = wx.StaticText(self, label='Filename:', style=wx.ALIGN_RIGHT)
        self.label_3 = wx.StaticText(self, label='Directory:', style=wx.ALIGN_RIGHT)
        self.label_4 = wx.StaticText(self, label='Size:', style=wx.ALIGN_RIGHT)
        self.label_5 = wx.StaticText(self, label='Installed:', style=wx.ALIGN_RIGHT)

        self.label_2.SetFont(font_data)
        self.label_1.SetFont(font_data)
        self.label_3.SetFont(font_data)
        self.label_4.SetFont(font_data)
        self.label_5.SetFont(font_data)

        self.value_1 = wx.StaticText(self, label='000000', style=wx.ALIGN_LEFT)
        self.value_2 = wx.StaticText(self, label='asset.zip', style=wx.ALIGN_LEFT)
        self.value_3 = wx.StaticText(self, label='path/to/folder', style=wx.ALIGN_LEFT)
        self.value_4 = wx.StaticText(self, label='1.50 GB', style=wx.ALIGN_LEFT)
        self.value_5 = wx.StaticText(self, label='77/77', style=wx.ALIGN_LEFT)

        self.value_1.SetFont(font_data)
        self.value_2.SetFont(font_data)
        self.value_3.SetFont(font_data)
        self.value_4.SetFont(font_data)
        self.value_5.SetFont(font_data)

    def _create_boxes(self):
        name_box = wx.BoxSizer()
        name_box.Add(self.name_label, 0, wx.EXPAND | wx.ALL)

        labels_box = wx.BoxSizer(wx.VERTICAL)
        labels_box.Add(self.label_1, 0, wx.EXPAND | wx.ALL, 5)
        labels_box.Add(self.label_2, 0, wx.EXPAND | wx.ALL, 5)
        labels_box.Add(self.label_3, 0, wx.EXPAND | wx.ALL, 5)
        labels_box.Add(self.label_4, 0, wx.EXPAND | wx.ALL, 5)
        labels_box.Add(self.label_5, 0, wx.EXPAND | wx.ALL, 5)

        values_box = wx.BoxSizer(wx.VERTICAL)
        values_box.Add(self.value_1, 0, wx.EXPAND | wx.ALL, 5)
        values_box.Add(self.value_2, 0, wx.EXPAND | wx.ALL, 5)
        values_box.Add(self.value_3, 0, wx.EXPAND | wx.ALL, 5)
        values_box.Add(self.value_4, 0, wx.EXPAND | wx.ALL, 5)
        values_box.Add(self.value_5, 0, wx.EXPAND | wx.ALL, 5)

        data_box = wx.BoxSizer()
        data_box.Add(20, 0, 0)
        data_box.Add(labels_box, 0, wx.ALL, 5)
        data_box.Add(values_box, 1, wx.EXPAND | wx.ALL, 5)

        details_box = wx.BoxSizer(wx.VERTICAL)
        details_box.Add(0, 20, 0)
        details_box.Add(name_box, 0, wx.ALL, 5)
        details_box.Add(data_box, 0, wx.ALL, 5)

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(details_box, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_box)

    def update_details(self, obj):

        self.update_values_for_asset(obj)

    def _update_labels_for_asset(self):
        self.label_1.SetLabel('SKU:')
        self.label_2.SetLabel('Filename:')
        self.label_3.SetLabel('Directory:')
        self.label_4.SetLabel('Size:')
        self.label_5.SetLabel('Installed:')

    def _update_labels_for_folder(self):
        self.label_1.SetLabel('Source:')
        self.label_2.SetLabel('Path:')
        self.label_3.SetLabel('Zip Count:')
        self.label_4.SetLabel('Size:')
        self.label_5.SetLabel('')

    def update_values_for_asset(self, asset: Asset):
        self._update_labels_for_asset()

        self.name_label.SetLabel(asset.product_name)
        self.value_1.SetLabel(str(asset.sku))
        self.value_2.SetLabel(asset.filename)
        self.value_3.SetLabel(str(asset.path))
        self.value_4.SetLabel(asset.get_size())
        self.value_5.SetLabel(asset.get_installed())

    def update_values_for_folder(self, folder: Folder):
        self._update_labels_for_folder()
        source: Source = self.data.database.select_source_by_idn(folder.source_id)

        source_name = source.path.name
        path = str(folder.path)[len(str(source.path))+1:]

        self.name_label.SetLabel(folder.title)
        self.value_1.SetLabel(source_name)
        self.value_2.SetLabel(path)
        self.value_3.SetLabel(str(folder.file_count))
        self.value_4.SetLabel(folder.get_size())
        self.value_5.SetLabel('')
