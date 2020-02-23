import wx
import logging
from pathlib import Path


class DirectoriesPanel(wx.Panel):

    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.data = data

        self._create_widgets()
        self._create_boxes()
        self._create_binds()

    def _create_widgets(self):
        header_font = wx.Font(wx.FontInfo(16))

        self.sources_header_label = wx.StaticText(self, name='sources_header', label='Sources',
                                                  style=wx.ALIGN_LEFT)
        self.sources_header_label.SetFont(header_font)

        self.sources = {}

        for i, source in enumerate(self.data.sources.values()):
            i = i+10
            self.sources[str(i)] = {}
            text_ctrl: wx.TextCtrl = wx.TextCtrl(self, id=i, name=f'{i}', value=str(source.path))
            browse_button = wx.Button(self, id=i, name=f'browse_button_{i}', label='...', size=wx.Size(30, 0))
            delete_button = wx.Button(self, id=i, name=f'delete_button_{i}', label='X', size=wx.Size(30, 0))

            self.sources[str(i)]['text_ctrl'] = text_ctrl
            self.sources[str(i)]['browse'] = browse_button
            self.sources[str(i)]['delete'] = delete_button

        self.add_source_button = wx.Button(self, name='add_source', label='Add Source', style=wx.BORDER_NONE)

        ######################################################

        self.libraries_header_label = wx.StaticText(self, name='libraries_header', label='Libraries',
                                                    style=wx.ALIGN_LEFT)
        self.libraries_header_label.SetFont(header_font)

        self.libraries = {}

        for i, library in enumerate(self.data.config.libraries.values()):
            i = i + 20
            self.libraries[str(i)] = {}
            text_ctrl: wx.TextCtrl = wx.TextCtrl(self, id=i, name=f'{i}', value=str(library))
            browse_button = wx.Button(self, id=i, name=f'browse_button_{i}', label='...', size=wx.Size(30, 0))
            delete_button = wx.Button(self, id=i, name=f'delete_button_{i}', label='X', size=wx.Size(30, 0))

            self.libraries[str(i)]['text_ctrl'] = text_ctrl
            self.libraries[str(i)]['browse'] = browse_button
            self.libraries[str(i)]['delete'] = delete_button

        self.add_library_button = wx.Button(self, name='add_library', label='Add Library', style=wx.BORDER_NONE)

        self.save_button = wx.Button(self, name='save_button', label='Save', style=wx.BORDER_NONE)
        self.close_button = wx.Button(self, name='closebutton', label='Close', style=wx.BORDER_NONE)

    def _create_boxes(self):
        self.sources_box = wx.BoxSizer(wx.VERTICAL)
        self.sources_box.Add(self.sources_header_label, 1, wx.EXPAND | wx.ALL)

        for key in self.sources.keys():
            self.sources[key]['box'] = wx.BoxSizer()

            self.sources[key]['box'].Add(self.sources[key]['text_ctrl'], 4,
                                         wx.EXPAND | wx.RIGHT | wx.CENTER,
                                         border=4)

            self.sources[key]['box'].Add(self.sources[key]['browse'], 0,
                                         wx.EXPAND | wx.RIGHT | wx.LEFT | wx.CENTER,
                                         border=4)

            self.sources[key]['box'].Add(self.sources[key]['delete'], 0,
                                         wx.EXPAND | wx.LEFT | wx.CENTER,
                                         border=4)

            self.sources_box.Add(self.sources[key]['box'], 1, wx.EXPAND | wx.ALL, border=4)

        add_source_box = wx.BoxSizer()
        add_source_box.Add(self.add_source_button, 0, wx.EXPAND | wx.RIGHT)
        add_source_box.Add(0, 0, 1, wx.EXPAND)

        ######################################################

        self.libraries_box = wx.BoxSizer(wx.VERTICAL)
        self.libraries_box.Add(self.libraries_header_label, 1, wx.EXPAND | wx.ALL)

        for key in self.libraries.keys():
            self.libraries[key]['box'] = wx.BoxSizer()

            self.libraries[key]['box'].Add(self.libraries[key]['text_ctrl'], 4,
                                           wx.EXPAND | wx.RIGHT | wx.CENTER,
                                           border=4)

            self.libraries[key]['box'].Add(self.libraries[key]['browse'], 0,
                                           wx.EXPAND | wx.RIGHT | wx.LEFT | wx.CENTER,
                                           border=4)

            self.libraries[key]['box'].Add(self.libraries[key]['delete'], 0,
                                           wx.EXPAND | wx.LEFT | wx.CENTER,
                                           border=4)

            self.libraries_box.Add(self.libraries[key]['box'], 1, wx.EXPAND | wx.ALL, border=4)

        add_library_box = wx.BoxSizer()
        add_library_box.Add(self.add_library_button, 0, wx.EXPAND | wx.RIGHT)
        add_library_box.Add(0, 0, 1, wx.EXPAND)

        save_close_box = wx.BoxSizer()
        save_close_box.Add(0, 0, 1, wx.EXPAND)
        save_close_box.Add(self.save_button, 0, wx.EXPAND | wx.ALL, border=4)
        save_close_box.Add(self.close_button, 0, wx.EXPAND | wx.ALL, border=4)

        vert_box = wx.BoxSizer(wx.VERTICAL)
        vert_box.Add(self.sources_box, 0, wx.EXPAND | wx.ALL, 5)
        vert_box.Add(add_source_box, 0, wx.EXPAND | wx.ALL, 5)
        vert_box.Add(self.libraries_box, 0, wx.EXPAND | wx.ALL, 5)
        vert_box.Add(add_library_box, 0, wx.EXPAND | wx.ALL, 5)
        vert_box.Add(save_close_box, 0, wx.EXPAND | wx.ALL, 5)

        self.pad_box = wx.BoxSizer(wx.HORIZONTAL)
        self.pad_box.Add(30, 0, 0)
        self.pad_box.Add(vert_box, 1, wx.EXPAND | wx.ALL)
        self.pad_box.Add(30, 0, 0)

        self.SetSizerAndFit(self.pad_box)

    def _create_binds(self):
        logging.debug('Creating ConfigFrame binds')
        self.Bind(wx.EVT_SET_FOCUS, self._on_focus)

        for key in self.sources.keys():
            self.sources[key]['browse'].Bind(wx.EVT_BUTTON, self._on_picker_browse)
            self.sources[key]['delete'].Bind(wx.EVT_BUTTON, self._on_picker_delete)

        self.add_source_button.Bind(wx.EVT_BUTTON, self._on_picker_add)
        self.save_button.Bind(wx.EVT_BUTTON, self._on_save)

    def _on_focus(self, event=None):
        logging.debug('ConfigFrame received focus')

    def _on_picker_delete(self, event: wx.Event = None):
        logging.info(f'{self.sources.keys()}')
        id_ = str(event.GetEventObject().GetId())

        button: wx.Button = event.GetEventObject()
        sizer: wx.Sizer = self.sources[id_]['box']
        logging.debug(f'{button.GetName()} pressed')

        child_count = range(len(sizer.GetChildren()))
        for i in reversed(child_count):
            sizer.Hide(i)
            sizer.Remove(i)

        del self.sources[id_]['box']
        self.sources.pop(id_)

        # self.parent.GetParent().SetSize(self.GetBestVirtualSize())
        # self.parent.SetSize(self.GetBestVirtualSize())

    def _on_picker_add(self, event: wx.Event = None):
        id_ = 0
        while str(id_) in self.sources.keys(): id_ += 1
        key = str(id_)

        text_ctrl: wx.TextCtrl = wx.TextCtrl(self, id=id_, name=f'{id_}', value='')
        browse_button = wx.Button(self, id=id_, name=f'browse_button_{id_}', label='...', size=wx.Size(30, 0))
        delete_button = wx.Button(self, id=id_, name=f'delete_button_{id_}', label='X', size=wx.Size(30, 0))

        self.sources[key] = {
            'text_ctrl':  text_ctrl,
            'browse': browse_button,
            'delete': delete_button,
            'box': wx.BoxSizer()
        }

        self.sources[key]['box'].Add(self.sources[key]['text_ctrl'], 4,
                                     wx.EXPAND | wx.RIGHT | wx.CENTER, border=4)

        self.sources[key]['box'].Add(self.sources[key]['browse'], 0,
                                     wx.EXPAND | wx.RIGHT | wx.LEFT | wx.CENTER, border=4)

        self.sources[key]['box'].Add(self.sources[key]['delete'], 0,
                                     wx.EXPAND | wx.LEFT | wx.CENTER, border=4)

        self.sources_box.Add(self.sources[key]['box'], 1, wx.EXPAND | wx.ALL, border=4)

        self.sources[key]['browse'].Bind(wx.EVT_BUTTON, self._on_picker_browse)
        self.sources[key]['delete'].Bind(wx.EVT_BUTTON, self._on_picker_delete)

        # size = self.parent.GetBestSize().Get()
        # self.parent.SetSize(*size)

    def _on_picker_browse(self, event: wx.Event = None):
        i: int = event.GetEventObject().GetId()
        browse_button: wx.Button = event.GetEventObject()
        text_ctrl = self.sources[str(i)]['text_ctrl']
        old_path = text_ctrl.GetValue()

        logging.debug(f'{browse_button.GetName()} pressed')

        dir_dialog: wx.DirDialog = wx.DirDialog(None, "Choose source directory", "",
                                                wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        dir_dialog.ShowModal()
        directory = dir_dialog.GetPath() if dir_dialog.GetPath() is not '' else old_path
        text_ctrl.SetValue(directory)

    def _on_save(self, event: wx.Event = None):
        source_paths = {}

        for source in self.sources.values():
            path = Path(source['text_ctrl'].GetValue())
            if not path.exists():
                error_dialog = wx.MessageDialog(self, 'Please ensure that all sources have valid paths.')
                error_dialog.ShowModal()
                return

            logging.info(path)

        self.Layout()