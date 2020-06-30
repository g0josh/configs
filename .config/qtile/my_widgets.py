from typing import Callable, Optional, TypedDict

from libqtile.core.manager import Qtile
from libqtile.widget import base
from libqtile.widget import TextBox
# from libqtile.widget.generic_poll_text import GenPollText
from libqtile.widget import base
from libqtile.log_utils import logger


class PollText(base.ThreadedPollText):
    """
    A generic text widget that polls using poll function to get the text
    The only difference between this and the inbuilt GenPollText is that
    unlike the inbuilt one this does not update text on click
    """
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('func', None, 'Poll Function'),
    ]

    def __init__(self, **config):
        base.ThreadedPollText.__init__(self, **config)
        self.add_defaults(PollText.defaults)

    def poll(self):
        if not self.func:
            return "You need a poll function"
        return self.func()

    def button_press(self, x, y, button):
        name = 'Button{0}'.format(button)
        if name in self.mouse_callbacks:
            self.mouse_callbacks[name](self.qtile)

    def button_release(self, x, y, button):
        name = 'ButtonRelease{0}'.format(button)
        if name in self.mouse_callbacks:
            self.mouse_callbacks[name](self.qtile)


def ComboWidgetPollFuncTemplate(qtile:Qtile, args: Optional[dict]) -> str:
    """
    Template function
    """
    return ""

def ComboWidgetClickFuncTemplate(qtile: Qtile, button:int, args: Optional[dict]) -> None:
    """
    Template function
    """
    pass

class ComboWidgetColor(object):
    def __init__(self, foreground:str, background:str):
        self.foreground = foreground
        self.background = background

def ComboWidgetColorFuncTemplate(qtile: Qtile, args: Optional[dict]) -> ComboWidgetColor:
    """
    Template function
    """
    return ComboWidgetColor(foreground="ffffff", background="000000")


class ComboWidget(object):
    """ 
    Combowidget is wrapper around PollText and TextBox widgets so that a widget can 
    can be prefixed and suffixed with text/icons. It contains 5 widgets
        1. title_head(glyph mostly): TextBox,
        2. title(icon mostly)): Polltext,
        3. title_tail(glyph mostly)): TextBox,
        4. body(the widget text): Polltext,
        5. body_tail (glyph mostly)): TextBox
    """

    def __init__(self, title_func: ComboWidgetPollFuncTemplate, title_bg: str, title_fg: str,
                 title_update: Optional[bool]=None, title_padding: Optional[int]=None,
                 title_color_func: Optional[ComboWidgetColorFuncTemplate]=None,
                 body_func: Optional[ComboWidgetPollFuncTemplate]=None, body_bg: Optional[str]=None, body_fg: Optional[str]=None,
                 body_padding: Optional[int]=None, body_color_func: Optional[ComboWidgetColorFuncTemplate]=None,
                 poll_interval: Optional[int]=None, title_label: Optional[str]=None, body_label: Optional[str]=None,
                 title_head_text: Optional[str]=None, title_tail_text: Optional[str]=None, body_tail_text: Optional[str]=None,
                 head_tail_font: Optional[str]=None, head_tail_font_size: Optional[int]=None,
                 title_font: Optional[str]=None, title_font_size: Optional[int]=None,
                 body_font: Optional[str]=None, body_font_size: Optional[int]=None,
                 click_func: Optional[ComboWidgetClickFuncTemplate]=None, click_update: Optional[bool]=None,
                 hide: Optional[bool]=None, inactive_hide: Optional[bool]=None
                 ):

        if not body_func and not title_func:
            raise AttributeError("No poll functions provided")

        self.title_func = title_func
        self.title_color_func = title_color_func
        self.update_title = title_update if title_update else False
        title_poll_interval = poll_interval if not body_func and title_update else None

        self.body_func = body_func
        self.body_color_func = body_color_func

        self.title_head_text = title_head_text if title_head_text else ""
        self.title_tail_text = title_tail_text if title_tail_text else ""
        self.body_tail_text = body_tail_text if body_tail_text else ""

        self.click_func = click_func
        self.click_update = click_update if click_update else False

        self.inactive_hide = inactive_hide if inactive_hide else False

        _mouse_callbacks = {
            'Button1': lambda q : self.click(q, 1),
            'Button2': lambda q : self.click(q, 2),
            'Button3': lambda q : self.click(q, 3),
            'Button4': lambda q : self.click(q, 4),
            'Button5': lambda q : self.click(q, 5),
        }

        title_func = (lambda: "") if hide else self.pollTitle
        title_head = "" if hide else self.title_head_text
        title_tail = "" if hide else self.title_tail_text
        self.title_head = TextBox(text=title_head, foreground=title_bg, font=head_tail_font, fontsize=head_tail_font_size,
                            mouse_callbacks=_mouse_callbacks, padding=0)
        self.title_tail = TextBox(text=title_tail, foreground=title_bg, font=head_tail_font, fontsize=head_tail_font_size,
                            mouse_callbacks=_mouse_callbacks, padding=0)
        self.title = PollText(func=title_func, update_interval=title_poll_interval, foreground=title_fg, background=title_bg, markup=True,
                                           font=title_font, fontsize=title_font_size, padding=title_padding, mouse_callbacks=_mouse_callbacks)

        self.body = self.body_tail = None
        if self.body_func:
            body_func = (lambda: "") if hide else self.pollBody
            body_tail = "" if hide else self.body_tail_text
            self.title_tail.background = body_bg
            self.body = PollText(func=body_func, update_interval=poll_interval, foreground=body_fg,
                                              background=body_bg, padding=body_padding, font=body_font,
                                              fontsize=body_font_size, mouse_callbacks=_mouse_callbacks)
            self.body_tail = TextBox(text=body_tail, foreground=body_bg, font=head_tail_font,
                                     fontsize=head_tail_font_size, mouse_callbacks=_mouse_callbacks, padding=0)

    def getWidgets(self):
        if self.body:
            return [self.title_head, self.title, self.title_tail, self.body, self.body_tail]
        else:
            return [self.title_head, self.title, self.title_tail]

    def click(self, qtile:Qtile, button:int):
        if self.click_func:
            self.click_func(qtile, button)
        if self.click_update:
            self.update()
         
    def pollTitle(self, force=False):
        if not self.title or not self.title_func:
            return
        result = self.title_func(qtile=self.title.qtile)
        if result:
            if self.title_color_func:
                colors = self.title_color_func(qtile=self.title.qtile)
                self.title.background = colors.background
                self.title.foreground = colors.foreground
                self.title_head.foreground = colors.background
                self.title_tail.foreground = colors.background
            if self.title_head.text != self.title_head_text:
                self.title_head.update(self.title_head_text)
            if self.title_tail.text != self.title_tail_text:
                self.title_tail.update(self.title_tail_text)
        elif self.inactive_hide:
            self.title_head.update("")
            self.title_tail.update("")

        if force:
            self.title.update(result)

        return result

    def pollBody(self, force=False):
        if not self.body or not self.body_func:
            return
        result = self.body_func(qtile=self.body.qtile)
        _poll_title = True
        if result:
            if self.body_color_func:
                colors = self.body_color_func(qtile=self.body.qtile)
                self.body.background = colors.background
                self.body.foreground = colors.foreground
                self.body_tail.foreground = colors.background
            if self.body_tail.text != self.body_tail_text:
                self.body_tail.update(self.body_tail_text)
        elif self.inactive_hide:
            _poll_title = False
            for w in [self.title_head, self.title, self.title_tail, self.body, self.body_tail]:
                if w.text:
                    w.update("")

        if self.update_title and _poll_title:
            self.pollTitle(force=True)
        
        if force:
            self.body.update(result)
        
        return result

    def update(self):
        if self.body:
            self.pollBody(force=True)
        else:
            self.pollTitle(force=True)

    def show(self, show=True):
        if show:
            if self.body is None:
                self.pollTitle(force=True)
            else:
                self.pollBody(force=True)
        else:
            self.hide()

    def hide(self):
        for w in self.getWidgets():
            w.update("")

    def isHidden(self):
        result = [False if w.text else True for w in self.getWidgets()]
        return all(result)

