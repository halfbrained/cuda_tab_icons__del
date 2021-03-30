import os
import json

from cudatext import *
from cudax_lib import get_translation

_   = get_translation(__file__)  # I18N

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_tab_icons.json')
icons_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icons')

USER_DIR = os.path.expanduser('~')

ic_map = {}

def collapse_path(path):
    if (path + os.sep).startswith(USER_DIR + os.sep):
        path = path.replace(USER_DIR, '~', 1)
    return path

class Command:
    
  def __init__(self):
    self.h_im = app_proc(PROC_GET_TAB_IMAGELIST, '')
    self._load_config()
    self._loaded_ims = {} # name -> imglist index
      
    menu_proc('tab', MENU_ADD, command='cuda_tab_icons.iconify_current', caption=_('Set tab icon...'))
      
  def config(self):
    if not os.path.exists(fn_config):
      self._save_cfg()
    file_open(fn_config)
      
        
  def iconify_current(self):
    path = ed.get_filename()
    if path:
      ic_fns = [name for name in os.listdir(icons_path)  if name.lower().endswith('.png')]
      ic_fns.sort(key=lambda n: icon_aliases.get(n, n))
      ic_names_aliased = [icon_aliases.get(name, name) for name in ic_fns]
      ic_names_noext = [os.path.splitext(name)[0] for name in ic_names_aliased] # no exts
      
      doc_fn = os.path.basename(path)
      ic_ind = dlg_menu(DMENU_LIST, ic_names_noext, caption=_('Choose icon for:\n  ')+doc_fn)
      
      if ic_ind is not None:
        ic_name = ic_fns[ic_ind]
        imind = self._load_icon(ic_name)
        ed.set_prop(PROP_TAB_ICON, imind)
        
        ic_map[path] = ic_name
        self._save_cfg()

  def clear_current(self):
    path = ed.get_filename()
    if path  and path in ic_map:
      del ic_map[path]
      
    ed.set_prop(PROP_TAB_ICON, -1)
    self._save_cfg()
        
        
  def on_open(self, ed_self):
    path = ed_self.get_filename()
    ic_name = ic_map.get(path)
    if ic_name is not None:
      imind = self._load_icon(ic_name)
      ed_self.set_prop(PROP_TAB_ICON, imind)


  def _load_icon(self, ic_name):
    if ic_name not in self._loaded_ims:
      # allow absolute path to icon in config, "advanced feature"
      ic_path = os.path.join(icons_path, ic_name)  if os.sep not in ic_name else  ic_name 
      imind = imagelist_proc(self.h_im, IMAGELIST_ADD, ic_path)
      if imind is not None: 
        self._loaded_ims[ic_name] = imind
      
    return self._loaded_ims[ic_name]

  def _save_cfg(self):
    collapsed = {collapse_path(path):ic_name for path,ic_name in ic_map.items()}
    with open(fn_config, 'w', encoding='utf-8') as f:
      json.dump(collapsed, f, indent=2)

  def _load_config(self):
    if os.path.exists(fn_config):
      with open(fn_config, 'r', encoding='utf-8') as f:
        j = json.load(f)
      j = {os.path.expanduser(path):ic_name for path,ic_name in j.items()}

      ic_map.clear()
      ic_map.update(j)


icon_aliases = {
  'appointment-soon.png': 'clock',
  #'audio-headphones.png': '',
  #'audio-speakers.png': '',
  'avatar-default.png': 'avatar',
  'changes-prevent.png': 'lock',
  #'computer.png': '',
  #'drive-multidisk.png': '',
  'edit-delete.png': 'delete',
  'edit-find.png': 'search purple',
  'emblem-default.png': 'success',
  'emblem-downloads.png': 'download',
  'emblem-mail.png': 'mail',
  'emblem-readonly.png': 'lock2',
  'emblem-unreadable.png': 'X',
  'emblem-web.png': 'web',
  'help-faq.png': '???',
  #'input-dialpad.png': '',
  'input-tablet.png': 'edit',
  'mail-attachment.png': 'attachment',
  'media-playback-start.png': 'start',
  'media-playback-stop.png': 'stop',
  'network-vpn.png': 'lock3',
  'non-starred.png': 'star empty',
  'preferences-desktop-font.png': 'alphabet',
  'preferences-system-privacy.png': 'privacy',
  'preferences-system-sharing.png': 'sharing',
  'security-high.png': 'shield green',
  'security-low.png': 'shield yellow',
  'security-medium.png': 'shield grey',
  'software-update-available.png': 'orange thingy',
  'software-update-urgent.png': 'warning',
  'starred.png': 'star',
  'system-file-manager.png': 'storage',
  'system-search.png': 'search yellow',
  #'trophy-bronze.png': '',
  #'trophy-gold.png': '',
  #'trophy-silver.png': '',
  'zoom-in.png': 'plus',
  'zoom-out.png': 'minus',
}