import wx
import logging


class MenuBar(wx.MenuBar):

    def __init__(self):
        wx.MenuBar.__init__(self)

        self.menus = {}

        logging.debug("Creating menu_bar")

        ##### File Menu #################
        self.menus['file_menu'] = file_menu = wx.Menu()
        self.menus['file_refresh'] = file_refresh = wx.MenuItem(file_menu, -1, '&Refresh')
        self.menus['file_quit'] = file_quit = wx.MenuItem(file_menu, wx.ID_EXIT, '&Quit')

        file_menu.Append(file_refresh)
        file_menu.AppendSeparator()
        file_menu.Append(file_quit)

        ##### Library Menu ###############
        self.menus['library_menu'] = library_menu = wx.Menu()
        self.menus['library_import_meta'] = library_import_meta = wx.MenuItem(file_menu, -1, '&Import Metadata')

        library_menu.Append(library_import_meta)

        ##### View Menu ##################
        self.menus['view_menu'] = view_menu = wx.Menu()
        self.menus['view_settings'] = view_settings = wx.MenuItem(view_menu, wx.ID_ANY, '&Configuration')

        view_menu.Append(view_settings)

        ##### Menu Bar ##################
        self.Append(file_menu, '&File')
        self.Append(library_menu, '&Library')
        self.Append(view_menu, '&View')

        logging.debug("Finished menu_bar")
