from typing import Callable, Optional, TypedDict

from libqtile.core.manager import Qtile
from libqtile.widget import base
from libqtile.widget import TextBox
from libqtile.widget import base
from libqtile.log_utils import logger


class PollText(base.ThreadedPollText):
    """
    A generic text widget that polls using poll function to get the text
    Differences between this and the inbuilt GenPollText:
        - Does not update text on click
        - The first update interval is set to 1 and the later ones are
          as provided in args  
    """
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('func', None, 'Poll Function'),
    ]

    def __init__(self, **config):
        self.actual_update_interval = config["update_interval"]
        config['update_interal'] = 1
        base.ThreadedPollText.__init__(self, **config)
        self.add_defaults(PollText.defaults)

    def poll(self):
        if not self.func:
            return "You need a poll function"
        return self.func()

    def tick(self):
        text = self.poll()
        self.update(text)
        return self.actual_update_interval

    def button_press(self, x, y, button):
        name = 'Button{0}'.format(button)
        if name in self.mouse_callbacks:
            self.mouse_callbacks[name](self.qtile)

    def button_release(self, x, y, button):
        name = 'ButtonRelease{0}'.format(button)
        if name in self.mouse_callbacks:
            self.mouse_callbacks[name](self.qtile)


class ComboWidgetColor(object):
    def __init__(self, foreground: str, background: str):
        self.foreground = foreground
        self.background = background

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

    def __init__(self, title_func: Callable[[Qtile], str], title_bg: str, title_fg: str,
                 title_update: Optional[bool] = None, title_padding: Optional[int] = None,
                 title_color_func: Optional[Callable[[Qtile], ComboWidgetColor]] = None,
                 body_func: Optional[Callable[[Qtile], str]] = None, body_bg: Optional[str] = None, body_fg: Optional[str] = None,
                 body_padding: Optional[int] = None, body_color_func: Optional[Callable[[Qtile], ComboWidgetColor]] = None,
                 poll_interval: Optional[int] = None, title_label: Optional[str] = None, body_label: Optional[str] = None,
                 title_head_text: str = "", title_tail_text: str = "", body_tail_text: str = "",
                 head_tail_font: str = "sans", head_tail_font_size: Optional[int] = None,
                 title_font: str = "sans", title_font_size: Optional[int] = None,
                 body_font: Optional[str] = "sans", body_font_size: Optional[int] = None,
                 click_func: Optional[Callable[[Qtile, int], None]] = None, click_update: Optional[bool] = None,
                 hide: Optional[bool] = None, inactive_hide: Optional[bool] = None, margin_text:str=""
                 ):

        if not body_func and not title_func:
            raise AttributeError("No poll functions provided")
        
        self.margin_text = margin_text
        self.title_func = title_func
        self.title_color_func = title_color_func
        self.update_title = title_update if title_update else False
        title_poll_interval = poll_interval if not body_func and title_update else None
        self.title_label = title_label

        self.body_func = body_func
        self.body_color_func = body_color_func
        self.body_label = body_label


        self.title_head_text = title_head_text if title_head_text else ""
        self.title_tail_text = title_tail_text if title_tail_text else ""
        self.body_tail_text = body_tail_text if body_tail_text else ""

        self.click_func = click_func
        self.click_update = click_update if click_update else False

        self.inactive_hide = inactive_hide if inactive_hide else False

        _mouse_callbacks = {
            'Button1': lambda q: self.click(q, 1),
            'Button2': lambda q: self.click(q, 2),
            'Button3': lambda q: self.click(q, 3),
            'Button4': lambda q: self.click(q, 4),
            'Button5': lambda q: self.click(q, 5),
        }

        title_func = (lambda: "") if (hide or self.body_func) else self.pollTitle
        title_head = "" if hide else self.title_head_text
        title_tail = "" if hide else self.title_tail_text
        margin_text = "" if hide else self.margin_text
        self.margin = TextBox(text=margin_text, foreground=title_bg, font=head_tail_font, fontsize=head_tail_font_size,
                                  padding=0)
        self.title_head = TextBox(text=title_head, foreground=title_bg, font=head_tail_font, fontsize=head_tail_font_size,
                                  mouse_callbacks=_mouse_callbacks, padding=0)
        self.title_tail = TextBox(text=title_tail, foreground=title_bg, font=head_tail_font, fontsize=head_tail_font_size,
                                  mouse_callbacks=_mouse_callbacks, padding=0)
        self.title = PollText(func=title_func, update_interval=title_poll_interval, foreground=title_fg, background=title_bg,
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
            return [self.margin, self.title_head, self.title, self.title_tail, self.body, self.body_tail]
        else:
            return [self.margin, self.title_head, self.title, self.title_tail]

    def click(self, qtile: Qtile, button: int):
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
            if self.margin.text != self.margin_text:
                self.margin.update(self.margin_text)
        elif self.inactive_hide:
            self.title_head.update("")
            self.title_tail.update("")
            self.margin.update("")

        _result = self.title_label if (self.title_label and result) else result

        if force:
            self.title.update(_result)

        return _result

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
            if not self.title.text or self.title.text == "N/A":
                _poll_title = False
                self.pollTitle(force=True)
        elif self.inactive_hide:
            _poll_title = False
            for w in [self.margin, self.title_head, self.title, self.title_tail, self.body_tail]:
                if w.text:
                    w.update("")

        if self.update_title and _poll_title:
            self.pollTitle(force=True)

        _result = self.body_label if self.body_label else result

        if force:
            self.body.update(_result)

        return _result

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
