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
        self.menus['daz_menu'] = daz_menu = wx.Menu()
        self.menus['daz_import_meta'] = daz_import_meta = wx.MenuItem(file_menu, -1, '&Import Metadata')

        daz_menu.Append(daz_import_meta)

        ##### View Menu ##################
        self.menus['view_menu'] = view_menu = wx.Menu()
        self.menus['view_settings'] = view_settings = wx.MenuItem(view_menu, wx.ID_ANY, '&Configuration')
        self.menus['view_queue'] = view_queue = wx.MenuItem(view_menu, wx.ID_ANY, '&Queue')

        view_menu.Append(view_settings)
        view_menu.Append(view_queue)

        ##### Menu Bar ##################
        self.Append(file_menu, '&File')
        self.Append(daz_menu, '&Daz Studio')
        self.Append(view_menu, '&View')
