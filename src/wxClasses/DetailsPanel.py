import wx

from Handlers.Main import MainHandler
from SQLClasses.Asset import Asset
from SQLClasses.Folder import Folder
from SQLClasses.Source import Source


class DetailsPanel(wx.Panel):
    """
    Panel that contains the tree view of a library

    Attributes:

    """

    def __init__(self, parent, data: MainHandler):
        wx.Panel.__init__(self, parent=parent)
        self.data = data
        self.labels = 0
        self.outer_padding = 5
        self.inner_padding = 10

        self._create_widgets()
        self._create_boxes()

    def _create_widgets(self):
        font_title = wx.Font(wx.FontInfo(18))
        font_data = wx.Font(wx.FontInfo(12))

        self.title_label = wx.StaticText(self, label='', style=wx.ALIGN_RIGHT)
        self.title_label.SetFont(font_title)

        self.label_1 = wx.StaticText(self, label='', style=wx.ALIGN_RIGHT)
        self.label_2 = wx.StaticText(self, label='', style=wx.ALIGN_RIGHT)
        self.label_3 = wx.StaticText(self, label='', style=wx.ALIGN_RIGHT)
        self.label_4 = wx.StaticText(self, label='', style=wx.ALIGN_RIGHT)
        self.label_5 = wx.StaticText(self, label='', style=wx.ALIGN_RIGHT)

        self.label_2.SetFont(font_data)
        self.label_1.SetFont(font_data)
        self.label_3.SetFont(font_data)
        self.label_4.SetFont(font_data)
        self.label_5.SetFont(font_data)

        self.value_1 = wx.StaticText(self, label='', style=wx.ALIGN_LEFT)
        self.value_2 = wx.StaticText(self, label='', style=wx.ALIGN_LEFT)
        self.value_3 = wx.StaticText(self, label='', style=wx.ALIGN_LEFT)
        self.value_4 = wx.StaticText(self, label='', style=wx.ALIGN_LEFT)
        self.value_5 = wx.StaticText(self, label='', style=wx.ALIGN_LEFT)

        self.value_1.SetFont(font_data)
        self.value_2.SetFont(font_data)
        self.value_3.SetFont(font_data)
        self.value_4.SetFont(font_data)
        self.value_5.SetFont(font_data)

        self.action_buttons = []
        for label in ['Install', 'Queue', 'Open Zip']:
            self.action_buttons.append(wx.Button(self, label=label))

    def _create_boxes(self):
        name_box = wx.BoxSizer()
        name_box.Add(self.title_label, 0, wx.EXPAND | wx.ALL)

        labels_box = wx.BoxSizer(wx.VERTICAL)
        labels_box.Add(self.label_1, 1, wx.EXPAND | wx.ALL, 5)
        labels_box.Add(self.label_2, 1, wx.EXPAND | wx.ALL, 5)
        labels_box.Add(self.label_3, 1, wx.EXPAND | wx.ALL, 5)
        labels_box.Add(self.label_4, 1, wx.EXPAND | wx.ALL, 5)
        labels_box.Add(self.label_5, 1, wx.EXPAND | wx.ALL, 5)
        labels_box.SetMinSize(80, 0)

        values_box = wx.BoxSizer(wx.VERTICAL)
        values_box.Add(self.value_1, 0, wx.EXPAND | wx.ALL, 5)
        values_box.Add(self.value_2, 0, wx.EXPAND | wx.ALL, 5)
        values_box.Add(self.value_3, 0, wx.EXPAND | wx.ALL, 5)
        values_box.Add(self.value_4, 0, wx.EXPAND | wx.ALL, 5)
        values_box.Add(self.value_5, 0, wx.EXPAND | wx.ALL, 5)

        buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        for i, button in enumerate(self.action_buttons):
            buttons_box.Add(button, 1, wx.EXPAND | wx.ALL, 3)
            if i is not len(self.action_buttons):
                buttons_box.Add(0, 16, 0)

        data_box = wx.BoxSizer(wx.HORIZONTAL)
        # data_box.Add(self.inner_padding, 0, 0)
        data_box.Add(labels_box, 0, wx.ALL, 5)
        data_box.Add(values_box, 1, wx.ALL, 5)

        details_box = wx.BoxSizer(wx.VERTICAL)
        details_box.Add(0, self.outer_padding, 0)
        details_box.Add(name_box, 0, wx.ALL, 5)
        # details_box.Add(0, self.inner_padding, 0)
        details_box.Add(data_box, 0, wx.ALL, 5)
        details_box.Add(buttons_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        main_box = wx.BoxSizer()
        main_box.Add(details_box, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_box)

    def _update_labels_for_asset(self):
        self.label_1.SetLabel('Size:')
        self.label_2.SetLabel('Path:')
        self.label_3.SetLabel('Filename:')
        self.label_4.SetLabel('SKU:')
        self.label_5.SetLabel('Installed:')

    def _update_labels_for_folder(self):
        self.label_1.SetLabel('Size:')
        self.label_2.SetLabel('Path:')
        self.label_3.SetLabel('Zip Count:')
        self.label_4.SetLabel('')
        self.label_5.SetLabel('')

    def update_values_for_asset(self, asset: Asset):
        if self.labels is not 'asset':
            self._update_labels_for_asset()
            self.labels = 'asset'

        source: Source = self.data.sql_handler.sources.select_source_by_id(asset.source_id)
        path = str(asset.path)[len(str(source.path))-len(source.path.name):]

        self.title_label.SetLabel(asset.product_name)
        self.value_1.SetLabel(asset.get_size())
        self.value_2.SetLabel(path)
        self.value_3.SetLabel(asset.filename)
        self.value_3.SetToolTip(asset.filename)
        self.value_4.SetLabel(str(asset.sku))
        self.value_5.SetLabel(asset.get_installed())

    def update_values_for_folder(self, folder: Folder):
        if self.labels is not 'folder':
            self._update_labels_for_folder()
            self.labels = 'folder'

        source: Source = self.data.sql_handler.sources.select_source_by_id(folder.source_id)
        path = str(folder.path)[len(str(source.path))-len(source.path.name):]

        self.title_label.SetLabel(folder.title)
        self.value_1.SetLabel(folder.get_size())
        self.value_2.SetLabel(path)
        self.value_3.SetLabel(str(folder.file_count))
        self.value_4.SetLabel('')
        self.value_5.SetLabel('')
