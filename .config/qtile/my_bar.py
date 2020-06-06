from my_scripts import getNumScreens

from my_widgets import ComboWidget, GroupTextBox

NUM_SCREENS = getNumScreens()

def getBar(theme):
    pass

# Create widgets for all screens
vol_widgets = []
capslock_widgets = []
power_widgets = []
lock_widgets = []
shut_widgets = []
wifi_widgets = []
lan_widgets = []

for n in range(NUM_SCREENS):
    vol_widgets.append(ComboWidget(title_poll_func=getVolumeIcon, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
                                   body_poll_func=getVolume, click_func=volumePressed, poll_interval=None, body_bg=COLR_BODY_BG,
                                   body_fg=COLR_TEXT, title_font=icon_font[
                                       'font'], title_font_size=icon_font['fontsize'],
                                   border_font=border_font['font'], border_font_size=border_font[
                                       'fontsize'], body_font=default_font['font'],
                                   body_font_size=default_font['fontsize'], update_after_click=True, inactive_hide=False, update_title=True)
                       )

    # Since computers can have multiple net interfaces
    _wifi_widgets = []
    _lan_widgets = []
    for interface in getInterfaces():
        title = (lambda: "") if 'wl' in interface else (lambda: "")
        func = getWlan if 'wl' in interface else getLan
        w_list = _wifi_widgets if 'wl' in interface else _lan_widgets
        w_list.append(ComboWidget(title_poll_func=title, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT, body_poll_func=func,
                                  body_poll_func_args={'interface': interface}, poll_interval=5, body_bg=COLR_BODY_BG, body_fg=COLR_TEXT,
                                  title_font=icon_font['font'], title_font_size=icon_font[
                                      'fontsize'], border_font=border_font['font'],
                                  border_font_size=border_font['fontsize'], body_font=default_font['font'], body_font_size=default_font['fontsize'])
                      )
    wifi_widgets.append(_wifi_widgets)
    lan_widgets.append(_lan_widgets)

    capslock_widgets.append(ComboWidget(title_poll_func=lambda: "", title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
                                        title_font=icon_font['font'], title_font_size=icon_font['fontsize'], update_title=False, poll_interval=None,
                                        body_poll_func=getlocksStatus, body_bg=COLR_BODY_BG, body_fg=COLR_TEXT, body_font=default_font[
                                            'font'],
                                        body_font_size=default_font['fontsize'], border_font=border_font['font'], border_font_size=border_font['fontsize'])
                            )

    lock_widget = ComboWidget(title_poll_func=lambda: "", update_title=False, title_bg=COLR_TITLE_BG,
                              title_fg=COLR_TEXT, title_font=icon_font[
                                  'font'], title_font_size=icon_font['fontsize'], hide=True,
                              poll_interval=None, border_font=border_font['font'], border_font_size=border_font['fontsize'],
                              click_func=powerClicked, click_func_args={'power_button': POWER_BUTTONS['LOCK_SCREEN']}, body_bg=COLR_BAR_BG)
    shut_widget = ComboWidget(title_poll_func=lambda: "", update_title=False, title_bg=COLR_TITLE_BG,
                              title_fg=COLR_TEXT, title_font=icon_font[
                                  'font'], title_font_size=icon_font['fontsize'], hide=True,
                              poll_interval=None, border_font=border_font['font'], border_font_size=border_font['fontsize'],
                              click_func=powerClicked, click_func_args={'power_button': POWER_BUTTONS['SHUT_DOWN']})
    power_widget = ComboWidget(title_poll_func=lambda: " ", update_title=False, title_bg=COLR_TITLE_BG,
                               title_fg=COLR_TEXT, title_font=icon_font[
                                   'font'], title_font_size=icon_font['fontsize'], tail_text="",
                               poll_interval=None, border_font=border_font['font'], border_font_size=border_font['fontsize'],
                               click_func=show_hide_power_widgets, click_func_args={'widgets': [lock_widget, shut_widget]}, body_bg=COLR_BAR_BG)
    lock_widgets.append(lock_widget)
    shut_widgets.append(shut_widget)
    power_widgets.append(power_widget)


def getGroupBoxWidgets(border_text_l, border_text_r, active_fg, active_bg,
                       inactive_fg, inactive_bg, urgent_fg, urgent_bg, not_empty_fg, not_empty_bg):
    w = []
    for g in groups:
        if g.name == 'scratchpad':
            continue
        w += [
            GroupTextBox(track_group=g.name, label=border_text_l, center_aligned=True, borderwidth=0,
                         active_fg=active_bg, active_bg=COLR_BAR_BG, not_empty_fg=not_empty_bg, not_empty_bg=COLR_BAR_BG,
                         inactive_fg=inactive_bg, inactive_bg=COLR_BAR_BG,
                         urgent_fg=urgent_bg, urgent_bg=COLR_BAR_BG, **border_font),
            GroupTextBox(track_group=g.name, label=g.label, center_aligned=True, borderwidth=0,
                         active_fg=active_fg, active_bg=active_bg, not_empty_fg=not_empty_fg, not_empty_bg=not_empty_bg,
                         inactive_fg=inactive_fg, inactive_bg=inactive_bg,
                         urgent_fg=urgent_fg, urgent_bg=urgent_bg, **icon_font),
            GroupTextBox(track_group=g.name, label=border_text_r, center_aligned=True, borderwidth=0,
                         active_fg=active_bg, active_bg=COLR_BAR_BG, not_empty_fg=not_empty_bg, not_empty_bg=COLR_BAR_BG,
                         inactive_fg=inactive_bg, inactive_bg=COLR_BAR_BG,
                         urgent_fg=urgent_bg, urgent_bg=COLR_BAR_BG, **border_font),
        ]
    return w


def getWidgets(screen=0):
    # Layout Icon
    widgets = [
        widget.CurrentLayoutIcon(
            background=COLR_TITLE_BG, scale=0.6, foreground=COLR_INACTIVE),
        widget.TextBox(
            **border_font, background=COLR_BAR_BG,
            text="", foreground=COLR_TITLE_BG,
        )
    ]
    # Groups
    widgets += getGroupBoxWidgets(border_text_l="", border_text_r="", active_fg=COLR_TEXT, active_bg=COLR_TITLE_BG,
                                  inactive_fg=COLR_TEXT, inactive_bg=COLR_INACTIVE, urgent_fg=COLR_TEXT, urgent_bg=COLR_TITLE_BG,
                                  not_empty_fg=COLR_TEXT, not_empty_bg=COLR_BODY_BG)
    # Music
    # widgets += ComboWidget(title_poll_func=lambda:"", update_title=False, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
    #     title_font=icon_font['font'], title_font_size=icon_font['fontsize'],body_poll_func=getMpd, body_poll_func_args={'not_connected_text':""},
    #     poll_interval=2.0,click_func=clickMpd, update_after_click=True,body_bg=COLR_BODY_BG, body_fg=COLR_TEXT,body_font=default_font['font'],
    #     body_font_size=default_font['fontsize'], border_font=border_font['font'], border_font_size=border_font['fontsize'],
    #     head_text="", tail_text="").getWidgets()

    widgets += [widget.Spacer(length=400)]

    # Time
    widgets += ComboWidget(title_poll_func=lambda: "", update_title=False, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
                           title_font=icon_font['font'], title_font_size=icon_font[
                               'fontsize'], body_poll_func=getTime, poll_interval=30.0,
                           body_bg=COLR_BODY_BG, body_fg=COLR_TEXT, body_font=default_font[
                               'font'], body_font_size=default_font['fontsize'],
                           border_font=border_font['font'], border_font_size=border_font['fontsize'], head_text="", tail_text="", center_text="").getWidgets()
    widgets += ComboWidget(title_poll_func=getTime, title_poll_func_args={'format': '%I:%M %p', 'timezone': 'Asia/Kolkata'},
                           update_title=True, title_bg=COLR_BODY_BG, title_fg=COLR_TEXT, poll_interval=30.0,
                           title_font=default_font['font'], title_font_size=default_font[
                               'fontsize'], border_font=border_font['font'],
                           border_font_size=border_font['fontsize'], head_text="", tail_text="", body_bg=COLR_BAR_BG).getWidgets()
    # Prompt
    if screen == 0:
        widgets += [
            widget.TextBox(**border_font, foreground=COLR_TITLE_BG, text=""),
            widget.Prompt(**default_font, foreground=COLR_TEXT,
                          background=COLR_TITLE_BG, prompt=" "),
            widget.TextBox(**border_font, foreground=COLR_TITLE_BG, text="")
        ]
    # Systray
    widgets += [widget.Spacer(), widget.Systray()]
    # Caps and Numlock
    widgets += capslock_widgets[screen].getWidgets()
    # Temperature
    widgets += ComboWidget(title_poll_func=lambda: "", update_title=False, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
                           title_font=icon_font['font'], title_font_size=icon_font[
                               'fontsize'], body_poll_func=getTemps, poll_interval=5.0,
                           click_func=getTemps, update_after_click=True, body_bg=COLR_BODY_BG, body_fg=COLR_TEXT, body_font=default_font['font'],
                           body_font_size=default_font['fontsize'], border_font=border_font['font'], border_font_size=border_font['fontsize']).getWidgets()
    # Utilization
    widgets += ComboWidget(title_poll_func=lambda: "", update_title=False, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
                           title_font=icon_font['font'], title_font_size=icon_font[
                               'fontsize'], body_poll_func=getUtilization, poll_interval=5.0,
                           click_func=getUtilization, update_after_click=True, body_bg=COLR_BODY_BG, body_fg=COLR_TEXT, body_font=default_font['font'],
                           body_font_size=default_font['fontsize'], border_font=border_font['font'], border_font_size=border_font['fontsize']).getWidgets()
    # Volume
    widgets += vol_widgets[screen].getWidgets()

    # Ethernet/Wifi
    for w in wifi_widgets[screen]:
        widgets += w.getWidgets()
    for w in lan_widgets[screen]:
        widgets += w.getWidgets()

    # Power
    widgets += shut_widgets[screen].getWidgets() + \
        lock_widgets[screen].getWidgets()
    widgets += power_widgets[screen].getWidgets()

    return widgets

