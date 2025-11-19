import os
from cudatext import *
import cudax_lib as appx

CHOOSE_FORM_W = 200
CHOOSE_FORM_H = 580


class DialogChooseColor:

    def __init__(self):

        self.icon_w = 45
        self.icon_h = 19
        self.h_dlg = self.init_dlg()
        listbox_proc(self.h_list, LISTBOX_SET_ITEM_H, index=self.icon_h+2)
        self.items = []

    def init_theme(self):

        th = app_proc(PROC_THEME_UI_DICT_GET, '')
        self.THEME_BG = th['ListBg']['color']
        self.THEME_BG_SEL = th['ListSelBg']['color']
        self.THEME_FONT = th['ListFont']['color']
        self.THEME_FONT_SEL = th['ListSelFont']['color']

    def callback_btn_ok(self, id_dlg, id_ctl, data='', info=''):

        sel = listbox_proc(self.h_list, LISTBOX_GET_SEL)
        cnt = listbox_proc(self.h_list, LISTBOX_GET_COUNT)
        self.result = self.items[sel] if 0<=sel<cnt else None
        dlg_proc(self.h_dlg, DLG_HIDE)


    def callback_listbox_drawitem(self, id_dlg, id_ctl, data='', info=''):

        id_canvas = data['canvas']
        index = data['index']
        rect = data['rect']
        index_sel = listbox_proc(self.h_list, LISTBOX_GET_SEL)
        item_text = listbox_proc(self.h_list, LISTBOX_GET_ITEM_PROP, index=index)['text']

        back_color = self.THEME_BG_SEL if index==index_sel else self.THEME_BG
        font_color = self.THEME_FONT_SEL if index==index_sel else self.THEME_FONT

        canvas_proc(id_canvas, CANVAS_SET_BRUSH, color=back_color, style=BRUSH_SOLID)
        canvas_proc(id_canvas, CANVAS_RECT_FILL, x=rect[0], y=rect[1], x2=rect[2], y2=rect[3])

        ncolor = appx.html_color_to_int(item_text)

        canvas_proc(id_canvas, CANVAS_SET_BRUSH, color=ncolor, style=BRUSH_SOLID)
        canvas_proc(id_canvas, CANVAS_RECT_FILL, x=rect[0], y=rect[1], x2=rect[0]+self.icon_w, y2=rect[3])

        canvas_proc(id_canvas, CANVAS_SET_BRUSH, color=back_color, style=BRUSH_SOLID)
        canvas_proc(id_canvas, CANVAS_SET_FONT, color=font_color)
        size = canvas_proc(id_canvas, CANVAS_GET_TEXT_SIZE, text=item_text)
        canvas_proc(id_canvas, CANVAS_TEXT,
            text = item_text,
            x = rect[0] + self.icon_w + 5,
            y = (rect[1]+rect[3]-size[1])//2 )


    def init_dlg(self):

        h=dlg_proc(0, DLG_CREATE)
        dlg_proc(h, DLG_PROP_SET, prop={'cap':'Recent colors',
          'w':CHOOSE_FORM_W,
          'h':CHOOSE_FORM_H,
          })

        n=dlg_proc(h, DLG_CTL_ADD, 'listbox_ex')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'list1',
            'align': ALIGN_CLIENT,
            'sp_a': 6,
            'on_draw_item': self.callback_listbox_drawitem,
            })

        self.h_list = dlg_proc(h, DLG_CTL_HANDLE, index=n)
        dlg_proc(h, DLG_CTL_FOCUS, index=n)
        listbox_proc(self.h_list, LISTBOX_SET_DRAWN, index=1)

        n=dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'btn_ok',
            'cap': '&OK',
            'align': ALIGN_BOTTOM,
            'sp_a': 6,
            'on_change': self.callback_btn_ok,
            'ex0': True,
            })

        return h


    def dialog(self, items):

        self.init_theme()
        self.result = ''
        self.items = items

        listbox_proc(self.h_list, LISTBOX_DELETE_ALL)
        for item in items:
            listbox_proc(self.h_list, LISTBOX_ADD, index=-1, text=item)

        dlg_proc(self.h_dlg, DLG_SHOW_MODAL)
        return self.result
