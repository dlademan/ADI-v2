import wx
import logging


class MenuBar(wx.MenuBar):

    def __init__(self):
        wx.MenuBar.__init__(self)

        self.menus = {}

        logging.info("Creating menu_bar")

        ##### File Menu #################
        self.menus['file_menu'] = file_menu = wx.Menu()
        self.menus['file_refresh'] = file_refresh = wx.MenuItem(file_menu, -1, '&Refresh')
        self.menus['file_quit'] = file_quit = wx.MenuItem(file_menu, wx.ID_EXIT, '&Quit')

        file_menu.Append(file_refresh)
        file_menu.AppendSeparator()
        file_menu.Append(file_quit)

        ##### Library Menu ###############

        ##### View Menu ##################
        self.menus['view_menu'] = view_menu = wx.Menu()
        self.menus['view_settings'] = view_settings = wx.MenuItem(view_menu, wx.ID_ANY, '&Configuration')

        view_menu.Append(view_settings)

        ##### Menu Bar ##################

        self.Append(file_menu, '&File')
        # menu_bar.Append(lib_menu, '&Library')
        self.Append(view_menu, '&View')
