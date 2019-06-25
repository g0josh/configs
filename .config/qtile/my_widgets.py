from libqtile.widget import base
from libqtile.widget.groupbox import _GroupBase
from libqtile.log_utils import logger


class GroupTextBox(_GroupBase):
    """A widget that graphically displays the current group"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [("border", "000000", "group box border color")]

    def __init__(self, track_group, label, active_fg, active_bg,
            inactive_fg, inactive_bg, urgent_fg, urgent_bg,
            not_empty_fg, not_empty_bg, **config):
        _GroupBase.__init__(self, **config)
        self.add_defaults(GroupTextBox.defaults)
        self.track_group_name = track_group
        self.tracking_group = None
        self._label = label
        self.label=label
        self.active_fg = active_fg
        self.active_bg = active_bg
        self.inactive_fg = inactive_fg
        self.inactive_bg = inactive_bg
        self.urgent_fg = urgent_fg
        self.urgent_bg = urgent_bg
        self.not_empty_fg = not_empty_fg
        self.not_empty_bg = not_empty_bg

    def button_press(self, x, y, button):
        if self.tracking_group:
            self.bar.screen.setGroup(self.tracking_group)

    def calculate_length(self):
        width, _ = self.drawer.max_layout_size(
           [self.label],
           self.font,
           self.fontsize
        )
        return width

    def group_has_urgent(self, group):
        return len([w for w in group.windows if w.urgent]) > 0

    def get_group(self):
        for g in self.qtile.groups:
            if g.name == self.track_group_name:
            #if g.name == self.track_group and (g.windows or g.screen):
                return g
        return None

    def draw(self):
        tracking_group = self.get_group()
        # if tracking_group is None:
        #     self.drawer.clear(self.bar.background)
        #     # self.drawbox(self.margin_x, " ", self.border, self.foreground)
        #     self.drawer.draw(offsetx=self.offset, width=self.width)
        #     # self.bar.draw()

        # if tracking_group == self.tracking_group:
            # return True
        self.tracking_group = tracking_group
        # self.text = self.tracking_group.label if self.text == 'NA' else self.text
        # self.label = self._label
        if self.tracking_group == self.qtile.currentGroup:
            self.foreground = self.active_fg
            self.background = self.active_bg
        elif self.group_has_urgent(self.tracking_group):
            self.foreground = self.urgent_fg
            self.background = self.urgent_bg
        elif self.tracking_group.windows or self.tracking_group.screen:
            self.foreground = self.not_empty_fg
            self.background = self.not_empty_bg
        else:
            self.foreground = self.inactive_fg
            self.background = self.inactive_bg
            # self.label = ""
        self.drawer.clear(self.background or self.bar.background)
        self.drawbox(0, self.label, self.border, self.foreground)
        self.drawer.draw(offsetx=self.offset, width=self.width)

# class FuncWithClick(base.ThreadPoolText):
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
        ('release_func_args', {}, 'function arguments')
    ]

    def __init__(self, **config):
        base.ThreadedPollText.__init__(self, **config)
        self.add_defaults(FuncWithClick.defaults)

    def button_press(self, x, y, button):
        if self.click_func:
            result = self.click_func(x, y, button, **self.click_func_args)
            if result:
                self.update(result)

    def button_release(self, x, y, button):
        if self.release_func:
            result = self.release_func(x, y, button, **self.click_func_args)
            if result:
                self.update(result)

    def poll(self, text=None):
        if text is not None:
            return text
        if not self.func:
            return None
        if self.label:
            return self.label if self.func(**self.func_args) else ""

        return self.func(**self.func_args)


class ComboWidget(object):
    def __init__(self, title_poll_func, title_bg, title_fg, title_poll_func_args={}, update_title=False,
                body_poll_func=None, body_poll_func_args={}, body_fg='111111', body_bg='000000',
                click_func=None, click_func_args={}, border_font=None, border_font_size=12, title_font=None,
                title_font_size=12, body_font=None, body_font_size=12, collapsible=True, inactive_disappear=True,
                poll_interval=1000, head="", tail="", ):

        if body_poll_func is None and title_poll_func is None:
            raise AttributeError("No poll functions provided")

        self.update_title = update_title
        self.title_func = title_poll_func
        self.title_func_args = title_poll_func_args
        title_poll_interval = None

        self.body_func = body_poll_func
        self.body_func_args = body_poll_func_args
        self.inactive_disappear = inactive_disappear
        self.head_text = head
        self.tail_text = tail

        if self.body_func is None and self.update_title:
            title_poll_interval = poll_interval
        logger.warning(title_poll_interval)
        self.title_head = FuncWithClick(func=lambda:head, click_func=click_func, click_func_args=click_func_args,
            foreground=title_bg, update_interval=None, font=border_font, fontsize=border_font_size, padding=0)
        self.title = FuncWithClick(func=self.poll_title, func_args={},click_func=click_func,
            click_func_args=click_func_args, foreground=title_fg, background=title_bg,
            update_interval=title_poll_interval, font=title_font, fontsize=title_font_size, padding=0)
        self.title_tail = FuncWithClick(func=lambda:tail, click_func=click_func, click_func_args=click_func_args,
            foreground=title_bg, background=body_bg, update_interval=None, font=border_font, fontsize=border_font_size, padding=0)

        if self.body_func is not None:
            self.body =  FuncWithClick(func=self.poll_body, func_args={},click_func=click_func,
            click_func_args=click_func_args, foreground=body_fg, background=body_bg,
            update_interval=poll_interval, font=body_font, fontsize=body_font_size, padding=0)
            self.body_tail = FuncWithClick(func=lambda:tail, click_func=click_func, click_func_args=click_func_args,
                foreground=body_bg, update_interval=None, font=border_font, fontsize=border_font_size, padding=0)

    def getWidgets(self):
        if self.body_func:
            return [self.title_head, self.title, self.title_tail, self.body, self.body_tail]
        else:
            return [self.title_head, self.title, self.title_tail]

    def hideWidgets(self):
        for w in self.getWidgets():
            w.update("")

    def poll_title(self, force=False):
        # if self.body_func and not force:
        #   return None
        # if not self.update_title and not force:
        #     return None
        result = self.title_func(**self.title_func_args)
        if result:
            if not self.title_head.text:
                self.title_head.update(self.head_text)
            if not self.title_tail.text:
                self.title_tail.update(self.tail_text)
        elif self.inactive_disappear:
            self.title_head.update("")
            self.title_tail.update("")

        if force:
            self.title.update(result)
        else:
            return result

    def poll_body(self):
        result = self.body_func(**self.body_func_args)
        logger.warning("result = {}".format(result))
        if result:
            if self.update_title or self.title_head.text != self.head_text:
                logger.warning("update title")
                self.poll_title(force=True)
            if not self.body_tail.text:
                logger.warning("update tail")
                self.body_tail.update(self.tail_text)
        elif self.inactive_disappear:
            logger.warning("no result disappear")
            for w in [self.title_head, self.title, self.title_tail, self.body, self.body_tail]:
                if w.text:
                    w.update("")
        elif self.update_title:
            logger.warning("no result update title")
            self.poll_title(force=True)

        return result




