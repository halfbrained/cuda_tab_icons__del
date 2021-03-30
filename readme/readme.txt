Plugin for CudaText.
Allows to assign custom icons to tabs in the editor. 

If tab has been assigned an icon, its header shows it for all next CudaText sessions, 
until you call the "Reset" command, or until plugin is uninstalled. Icons of tabs 
are stored in a file in the CudaText "settings" folder.

Additional icons can be added to the 'icons' directory in plugin's folder: py/cuda_tab_icons
Dimensions should be 16x16.

Adds menu item "Set tab icon..." to editor tab context menu. 
And commands to assign icon to tab and reset reset it to the main menu in:
	"Plugins > Tab-Icons" 

-----------------------------
    
Author: Shovel (CudaText forum user)
License: MIT
