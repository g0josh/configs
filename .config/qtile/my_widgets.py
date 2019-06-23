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

class FuncWithClick(base.ThreadPoolText):
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

# class ComboWidget(object):
#     def __init__(self, title_poll_func, title_poll_func_args, title_bg, title_fg, poll_title=False,
#                 body_poll_func, body_poll_func_args, body_fg, body_bg, click_func, click_func_args,
#                 border_font, border_font_size, title_font, title_font_size,
#                 body_font, body_font_size, collapsible=True, inactive_disappear=True,
#                 poll_interval=1000, head="", tail="", ):
#         self.body_func = body_poll_func
#         self.body_func_args = body_poll_func_args
#         self.inactive_disappear = inactive_disappear
#         self.ontexts = [head, "", "", ""],
#         'offtexts' : ["", "", "", ""] }
#         self.title_head = FuncWithClick(func=lambda:head, click_func=click_func, click_func_args=click_func_args,
#             foreground=title_bg, update_interval=10000, font=border_font, fontsize=border_font_size)
#         self.title = FuncWithClick(func=title_poll_func, func_args=title_poll_func_args,
#             click_func=click_func, click_func_args=click_func_args, foreground=title_fg, background=title_bg,
#             update_interval=10000, font=title_font, fontsize=title_font_size)
#         self.title_tail = FuncWithClick(func=lambda:tail, click_func=click_func, click_func_args=click_func_args,
#             foreground=title_bg, background=body_bg, update_interval=10000, font=border_font, fontsize=border_font_size)
#         self.body =  FuncWithClick(func=self._poll, func_args={},
#             click_func=click_func, click_func_args=click_func_args, foreground=body_fg, background=body_bg,
#             update_interval=poll_interval, font=body_font, fontsize=body_font_size)
#         self.body_tail = FuncWithClick(func=lambda:tail, click_func=click_func, click_func_args=click_func_args,
#             foreground=body_bg, update_interval=10000, font=border_font, fontsize=border_font_size)

#     def _poll(self):
#         body_result = self.body_func(**self.body_func_args)
#         if self.inactive_disappear and not body_result:
#             self.title_head.update("")
#             self.title.update("")
#             self.title_tail.update("")
#             self.body_tail

#         for w in [self.title_head, self.title, self.title_tail, self.body, self.body_tail]:
