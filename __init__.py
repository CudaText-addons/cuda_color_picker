import string
from cudatext import *
import cudax_lib as appx
from .dlg_choose_color import DialogChooseColor

fn_config = 'plugins.ini'
MAX_COLORS = 30
CHARS = string.ascii_letters + string.digits + '#'


def get_word_info():

    x0, y0, x2, y2 = ed.get_carets()[0]
    text = ed.get_text_line(y0)
    if x0>=len(text):
        return (x0, y0, 0, '')

    x1 = x0
    while x1>0 and text[x1-1] in CHARS: x1-=1
    x2 = x0
    while x2<len(text) and text[x2] in CHARS: x2+=1

    return (x1, y0, x2-x1, text[x1:x2])


class Command:
    items = []
    
    def load_history(self):
        
        s = ini_read(fn_config, 'color_picker', 'recents', '')
        self.items = s.split(',')
        self.items = [i for i in self.items if '#' in i]
        
    def save_history(self):
        
        s = ','.join(self.items[:MAX_COLORS])
        ini_write(fn_config, 'color_picker', 'recents', s)
        
    def add_history(self, item):
        
        if item in self.items:
            self.items.remove(item)
        self.items.insert(0, item)
        self.save_history()


    def run(self):

        x0, y0, nlen, text = get_word_info()
        val = 0
        if text:
            try:
                val = appx.html_color_to_int(text)
            except:
                val = 0

        val = dlg_color(val)
        if not val: return

        val = appx.int_to_html_color(val)
        self.insert(val)
        

    def insert(self, val):

        x0, y0, nlen, text = get_word_info()
        if nlen:
            ed.set_caret(x0, y0)
            ed.delete(x0, y0, x0+nlen, y0)
                
        ed.insert(x0, y0, val)
        ed.set_caret(x0+len(val), y0)

        self.load_history()
        self.add_history(val)

        msg_status('Inserted color: '+val)
        

    def recent_colors(self):

        self.load_history()
        dlg = DialogChooseColor()
        res = dlg.choose_color(self.items)
        if res:
            self.insert(res)
