from libqtile.widget import base
from libqtile.widget.groupbox import _GroupBase
from libqtile.log_utils import logger

class FuncWithClick(base.ThreadedPollText):
    """A generic text widget that polls using poll function to get the text"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('label', None, 'return text if poll function returns anything'),
        ('func', None, 'Poll Function'),
        ('click_func', None, 'click function'),
        ('release_func', None, 'click release function'),
        ('func_args', {}, 'function arguments'),
        ('click_func_args', {}, 'function arguments'),
        ('release_func_args', {}, 'function arguments'),
        ('color_func', {}, 'function to get the fg abd bg '),
        ('color_func_args', {}, 'function arguments')
    ]

    def __init__(self, **config):
        base.ThreadedPollText.__init__(self, **config)
        # super().__init__(self, **config)
        self.add_defaults(FuncWithClick.defaults)
        # self.padding = 5

    def button_press(self, x, y, button):
        if self.click_func:
            self.click_func_args.update(
                {'x': x, 'y': y, 'button': button, 'qtile': self.qtile})
            result = self.click_func(**self.click_func_args)
            # if result:
            #     self.update(result)

    def button_release(self, x, y, button):
        if self.release_func:
            self.click_func_args.update(
                {'x': x, 'y': y, 'button': button, 'qtile': self.qtile})
            result = self.release_func(**self.click_func_args)
            # if result:
            #     self.update(result)

    def poll(self, text=None):
        if text is not None:
            return text
        if not self.func:
            return None
        if self.label:
            return self.label if self.func(**self.func_args) else ""

        return self.func(**self.func_args)

    def update(self, text):
        if self.color_func:
            self.color_func_args.update({'qtile': self.qtile})
            colors = self.color_func(**self.colors_func_args)
            self.background = colors['background']
            self.foreground = colors['foreground']
        super().update(text)


class ComboWidget(object):
    def __init__(self, title_poll_func, title_bg, title_fg, title_poll_func_args=None, update_title=False,
                 body_poll_func=None, body_poll_func_args={}, body_fg='111111', body_bg='', click_func=None,
                 click_func_args={}, update_after_click=False, border_font=None, border_font_size=12, title_font=None,
                 title_font_size=12, body_font=None, body_font_size=12, inactive_hide=True,
                 poll_interval=1000, head_text="", tail_text="", center_text=None, hide=False,
                 title_label=None, body_label=None, title_color_func=None, title_color_func_args=None,
                 body_color_func=None, body_color_func_args=None, title_padding=None, body_padding=None):

        if body_poll_func is None and title_poll_func is None:
            raise AttributeError("No poll functions provided")

        self.update_title = update_title
        self.title_poll_func = title_poll_func
        self.title_poll_func_args = title_poll_func_args
        self.title_color_func = title_color_func
        self.title_color_func_args = title_color_func_args
        title_poll_interval = None

        self.body_poll_func = body_poll_func
        self.body_poll_func_args = body_poll_func_args
        self.body_color_func = body_color_func
        self.body_color_func_args = body_color_func_args
        self.inactive_hide = inactive_hide
        self._head_text = head_text
        self._tail_text = tail_text
        center_text = center_text if center_text is not None else tail_text
        self._center_text = center_text if self.body_poll_func else tail_text

        self.click_func = click_func
        self.click_func_args = click_func_args
        self.update_after_click = update_after_click

        if self.body_poll_func is None and self.update_title:
            title_poll_interval = poll_interval

        title_head_func = (lambda: "") if hide else lambda: self._head_text
        title_func = (lambda: "") if hide else self.poll_title
        title_tail_func = (lambda: "") if hide else lambda: self._center_text

        self.title_head = FuncWithClick(func=title_head_func, click_func=self.click, foreground=title_bg,
                                        update_interval=None, font=border_font, fontsize=border_font_size, padding=0)
        self.title = FuncWithClick(func=title_func, func_args={}, click_func=self.click,
                                   foreground=title_fg, background=title_bg, update_interval=title_poll_interval,
                                   font=title_font, fontsize=title_font_size, padding=title_padding, label=title_label, color_fumc=title_color_func,
                                   color_func_args=title_color_func_args)
        self.title_tail = FuncWithClick(func=title_tail_func, click_func=self.click, foreground=title_bg,
                                        update_interval=None, font=border_font, fontsize=border_font_size, padding=0)

        self.body = None
        self.body_tail = None
        if self.body_poll_func is not None:
            body_func = (lambda: "") if hide else self.poll_body
            body_tail_func = (lambda: "") if hide else lambda: self._tail_text
            self.title_tail.background = body_bg
            self.body = FuncWithClick(func=body_func, func_args={}, click_func=self.click,
                                      foreground=body_fg, background=body_bg, update_interval=poll_interval, font=body_font,
                                      fontsize=body_font_size, padding=body_padding, label=body_label, color_fumc=body_color_func,
                                      color_func_args=body_color_func_args)
            self.body_tail = FuncWithClick(func=body_tail_func, click_func=self.click, foreground=body_bg,
                                           update_interval=None, font=border_font, fontsize=border_font_size, padding=0)

    def click(self, x, y, button, qtile):
        if self.click_func is None:
            logger.warn("returned")
            return
        self.click_func_args.update(
            {'x': x, 'y': y, 'button': button, 'qtile': qtile})
        result = self.click_func(**self.click_func_args)
        if self.update_after_click:
            if self.body_poll_func is None and self.update_title:
                self.poll_title(text=result, force=True)
            if self.body_poll_func:
                self.poll_body(text=result, force=True)

    def getWidgets(self):
        if self.body_poll_func:
            return [self.title_head, self.title, self.title_tail, self.body, self.body_tail]
        else:
            return [self.title_head, self.title, self.title_tail]

    def poll_title(self, text=None, force=False):
        if text is not None:
            result = text
        else:
            if self.title_poll_func_args is not None:
                args_t = self.title_poll_func_args
                args_t.update({'qtile':self.title.qtile})
                result = self.title_poll_func(**args_t)
            else:
                result = self.title_poll_func()
        if result:
            # color
            if self.title_color_func:
                args_tc = self.title_color_func_args
                args_tc.update({'qtile':self.title.qtile})
                color = self.title_color_func(**args_tc)
                self.title.background = color['background']
                self.title.foreground = color['foreground']
                self.title_head.foreground = color['background']
                self.title_tail.foreground = color['background']
            if not self.title_head.text:
                self.title_head.update(self._head_text)
            if not self.title_tail.text:
                self.title_tail.update(self._center_text)
        elif self.inactive_hide:
            self.title_head.update("")
            self.title_tail.update("")

        if force:
            self.title.update(result)
        else:
            return result

    def poll_body(self, text=None, force=False):
        if not self.body:
            return
        if text is not None:
            result = text
        else:
            if self.body_poll_func_args is not None:
                args_b = self.body_poll_func_args
                args_b.update({'qtile':self.body.qtile})
                result = self.body_poll_func(**args_b)
            else:
                result = self.body_poll_func()

        if result:
            # color
            if self.body_color_func:
                args_bc = self.body_color_func_args
                args_bc.update({'qtile':self.title.qtile})
                color = self.body_color_func(**args_bc)
                self.body.background = color['background']
                self.body.foreground = color['foreground']
                self.body_tail.foreground = color['background']
            if self.update_title or self.title_head.text != self._head_text:
                self.poll_title(force=True)
            if not self.body_tail.text:
                self.body_tail.update(self._tail_text)
        elif self.inactive_hide:
            for w in [self.title_head, self.title, self.title_tail, self.body, self.body_tail]:
                if w.text:
                    w.update("")
        elif self.update_title:
            self.poll_title(force=True)

        if force:
            self.body.update(result)
        else:
            return result

    def update(self, title_text=None, body_text=None):
        if title_text is not None:
            self.poll_title(text=title_text, force=True)
        if body_text is not None:
            self.poll_body(text=body_text, force=True)
        if title_text is None and body_text is None:
            if self.body:
                self.poll_body(force=True)
            else:
                self.poll_title(force=True)

    def getBody(self):
        return self.body.text

    def getTitle(self):
        return self.title.text

    @property
    def text(self):
        if self.body_poll_func is not None:
            return self.getBody()
        else:
            return self.getTitle()

    @text.setter
    def text(self, value):
        assert isinstance(value, str), "This has to be a string"
        if self.body_poll_func is not None:
            self.poll_title(text=value)
        else:
            self.poll_body(text=value)

    @property
    def head_text(self):
        return self.title_head.text

    @head_text.setter
    def head_text(self, value):
        assert isinstance(value, str), "This has to a string"
        self.title_head.update(value)
        self._head_text = value

    @property
    def center_text(self):
        return self.title_tail.text

    @center_text.setter
    def center_text(self, value):
        assert isinstance(value, str), "This has to a string"
        self.title_tail.update(value)
        self._center_text = value

    @property
    def tail_text(self):
        if self.body_poll_func is None:
            return None
        return self.body_tail.text

    @tail_text.setter
    def tail_text(self, value):
        if self.body_poll_func is not None:
            assert isinstance(value, str), "This has to a string"
            self.body_tail.update(value)
            self._tail_text = value

    def show(self, show=True):
        if show:
            if self.body_poll_func is None:
                self.poll_title(force=True)
            else:
                self.poll_body(force=True)
        else:
            self.hide()

    def hide(self):
        for w in self.getWidgets():
            w.update("")

    def isHidden(self):
        result = [False if w.text else True for w in self.getWidgets()]
        return all(result)
