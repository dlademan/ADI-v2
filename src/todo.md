1. Implement Queue
    1. Implement QueueItem in db
        1. ~~Create QueueItem table~~
        1. Create QueueHandler
    1. Create Dialog for Queue
        1. Create wx classes
            1. MenuBar
            1. ListView
            1. Context Menu
    1. Create binds
        1. Create QueueItem context menu option
        1. Update queue on install/uninstall
        
1. Finish SettingsDialog        
    1. Finish ConfigFrame
        1. Directories panel
            1. Allow adding of more source/library inputs
            1. Allow removal of source/library inputs
        1. Startup Options
            1. Default view (tree/list)
            1. Default source
            1. Default library
            1. refresh source on startup
            
1. DetailsPanel
    1. Create better looking data
    1. Fix issue at initial state that is fixed by resizing
    1. Add library chooser
    
1. Asset Installation/Uninstallation
    1. Test with new SQLAlch methods
        1. Verify that installed status is updated
        1. Verify that installed status is represented in tree and list view
        1. Verify that all files are (installed to/uninstalled from) disk
    1. Implement Metadata Importing
        1. Create Metadata table
        1. Create script to write importing of Metadata
    
1. Create toolbar
    1. 