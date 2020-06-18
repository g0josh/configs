from libqtile import widget

from my_widgets import ComboWidget

from my_scripts import getVolume, getVolumeIcon, volumePressed
from my_scripts import getGroupColors, getGroupLabel
from my_scripts import getMpd, clickMpd
from my_scripts import getTime, getlocksStatus, getTemps, getUtilization
from my_scripts import getInterfaces, getWlan, getLan
from my_scripts import powerClicked, POWER_BUTTONS, MOUSE_BUTTONS

DEFAULT_FONT = dict(
    font="Iosevka Nerd Font Medium",
    # font="JetBrainsMono Nerd Font Mono Regular",
    fontsize=14,
)

BORDER_FONT = dict(
    font="Iosevka Nerd Font Mono",
    fontsize=18,
)

ICON_FONT = dict(
    font="Font Awesome 5 Free Solid",
    fontsize=13,
)

common_widgets = {}
group_widgets = {}


def prepareCommonWidgets(theme):
    global common_widgets, group_widgets
    global DEFAULT_FONT, BORDER_FONT, ICON_FONT

    common_widgets['mpd'] = ComboWidget(title_poll_func=lambda: "", body_poll_func=getMpd, poll_interval=5,
                                        title_fg=theme['titlefg'], title_bg=theme['titlebg'],
                                        title_padding=theme['titlepadding'], body_padding=theme['bodypadding'],
                                        body_fg=theme['bodyfg'], body_bg=theme['bodybg'],
                                        title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
                                        border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                                        body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'],
                                        head_text=theme['leftmoduleprefix'], center_text=theme['leftmodulesuffix'],
                                        tail_text=theme['leftmodulesuffix'],
                                        update_title=False, click_func=clickMpd, update_after_click=True)

    common_widgets['local_time'] = ComboWidget(title_poll_func=lambda: "", body_poll_func=getTime, poll_interval=30,
                                               title_fg=theme['titlefg'], title_bg=theme['titlebg'],
                                               body_fg=theme['bodyfg'], body_bg=theme['bodybg'],
                                               title_padding=theme['titlepadding'], body_padding=theme['bodypadding'],

                                               title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
                                               border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                                               body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'],
                                               head_text=theme['leftmoduleprefix'], center_text=theme['leftmodulesuffix'],
                                               tail_text=theme['rightmodulesuffix'],
                                               update_title=False)

    common_widgets['india_time'] = ComboWidget(title_poll_func=getTime, poll_interval=30,
                                               title_poll_func_args={
                                                   'format': '%I:%M %p', 'timezone': 'Asia/Kolkata'},
                                               title_fg=theme['bodyfg'], title_bg=theme['bodybg'],
                                               title_padding=theme['titlepadding'], body_padding=theme['bodypadding'],

                                               title_font=DEFAULT_FONT['font'], title_font_size=DEFAULT_FONT['fontsize'],
                                               border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                                               head_text=theme['rightmoduleprefix'], tail_text=theme['rightmodulesuffix'],
                                               update_title=True)

    common_widgets['locks'] = ComboWidget(title_poll_func=lambda: "", body_poll_func=getlocksStatus, poll_interval=2,
                                          title_fg=theme['titlefg'], title_bg=theme['gradient1title'],
                                          body_fg=theme['titlefg'], body_bg=theme['gradient1body'],
                                          title_padding=theme['titlepadding'], body_padding=theme['bodypadding'],

                                          title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
                                          border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                                          body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'],
                                          head_text=theme['rightmoduleprefix'], center_text=theme['rightmodulesuffix'],
                                          tail_text=theme['rightmodulesuffix'],
                                          update_title=True, click_func=getlocksStatus, update_after_click=True)

    common_widgets['temperature'] = ComboWidget(title_poll_func=lambda: "", body_poll_func=getTemps, poll_interval=5,
                                                title_fg=theme['titlefg'], title_bg=theme['gradient2title'],
                                                body_fg=theme['titlefg'], body_bg=theme['gradient2body'],
                                                title_padding=theme['titlepadding'], body_padding=theme['bodypadding'],

                                                title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
                                                border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                                                body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'],
                                                head_text=theme['rightmoduleprefix'], center_text=theme['rightmodulesuffix'],
                                                tail_text=theme['rightmodulesuffix'],
                                                update_title=False, click_func=getTemps, update_after_click=True)

    common_widgets['utilization'] = ComboWidget(title_poll_func=lambda: "", body_poll_func=getUtilization, poll_interval=5,
                                                title_fg=theme['titlefg'], title_bg=theme['gradient3title'],
                                                body_fg=theme['titlefg'], body_bg=theme['gradient3body'],
                                                title_padding=theme['titlepadding'], body_padding=theme['bodypadding'],

                                                title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
                                                border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                                                body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'],
                                                head_text=theme['rightmoduleprefix'], center_text=theme['rightmodulesuffix'],
                                                tail_text=theme['rightmodulesuffix'],
                                                update_title=False, click_func=getUtilization, update_after_click=True)

    common_widgets['volume'] = ComboWidget(title_poll_func=getVolumeIcon, body_poll_func=getVolume, poll_interval=None,
                                           title_fg=theme['titlefg'], title_bg=theme['gradient4title'],
                                           body_fg=theme['titlefg'], body_bg=theme['gradient4body'],
                                           title_padding=theme['titlepadding'], body_padding=theme['bodypadding'],

                                           title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
                                           border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                                           body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'],
                                           head_text=theme['rightmoduleprefix'], center_text=theme['rightmodulesuffix'],
                                           tail_text=theme['rightmodulesuffix'],
                                           update_title=True, click_func=volumePressed, update_after_click=True, inactive_hide=False)

    # Since computers can have multiple net interfaces
    common_widgets['wlan'] = []
    common_widgets['lan'] = []
    for interface in getInterfaces():
        title = (lambda: "") if 'wl' in interface else (lambda: "")
        func = getWlan if 'wl' in interface else getLan
        i_list = common_widgets['wlan'] if 'wl' in interface else common_widgets['lan']
        i_list.append(ComboWidget(title_poll_func=title, body_poll_func=func, poll_interval=5,
                                  body_poll_func_args={'interface': interface},
                                  title_fg=theme['titlefg'], title_bg=theme['gradient5title'],
                                  body_fg=theme['titlefg'], body_bg=theme['gradient5body'],
                                  title_padding=theme['titlepadding'], body_padding=theme['bodypadding'],

                                  title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
                                  border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                                  body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'],
                                  head_text=theme['rightmoduleprefix'], center_text=theme['rightmodulesuffix'],
                                  tail_text=theme['rightmodulesuffix'],
                                  update_title=False))

    common_widgets['screen_lock'] = ComboWidget(title_poll_func=lambda: "", body_poll_func=None, poll_interval=None,
                                                title_fg=theme['titlefg'], title_bg=theme['gradient6title'],
                                                title_padding=theme['titlepadding'], body_padding=theme['bodypadding'],

                                                title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
                                                border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                                                head_text=theme['rightmoduleprefix'], center_text=theme['rightmodulesuffix'],
                                                tail_text=theme['rightmodulesuffix'], update_title=True, hide=True,
                                                click_func=powerClicked, click_func_args={'power_button': POWER_BUTTONS['LOCK_SCREEN']}, inactive_hide=False)

    common_widgets['shut'] = ComboWidget(title_poll_func=lambda: "", body_poll_func=None, poll_interval=None,
                                         title_fg=theme['titlefg'], title_bg=theme['gradient6title'],
                                         title_padding=theme['titlepadding'], body_padding=theme['bodypadding'],

                                         title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
                                         border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                                         head_text=theme['rightmoduleprefix'], center_text=theme['rightmodulesuffix'],
                                         tail_text=theme['rightmodulesuffix'], update_title=True, hide=True,
                                         click_func=powerClicked, click_func_args={'power_button': POWER_BUTTONS['SHUT_DOWN']}, inactive_hide=False)

    common_widgets['toggle_power'] = ComboWidget(title_poll_func=lambda: " ", body_poll_func=None, poll_interval=None,
                                                 title_fg=theme['titlefg'], title_bg=theme['gradient7title'],
                                                 title_padding=theme['titlepadding'], body_padding=theme['bodypadding'],

                                                 title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
                                                 border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                                                 head_text=theme['rightmoduleprefix'],
                                                 update_title=True, click_func=show_hide_power_widgets, click_func_args={}, inactive_hide=False)


def getGroupWidgets(theme, screen, groups):
    result = []
    for group in groups:
        result.append(
            ComboWidget(title_poll_func=getGroupLabel, title_poll_func_args={'group': group.name},
                        poll_interval=None, title_bg=theme['bodybg'], title_fg=theme['bodyfg'],
                        title_color_func=getGroupColors, title_color_func_args={
                            'group': group.name, 'theme': theme, 'screen': screen},
                        click_func=clickGroup, click_func_args={
                            'group': group.name},
                        update_after_click=True, inactive_hide=True, update_title=True,
                        title_padding=theme['wspadding'], body_padding=theme['bodypadding'],
                        title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
                        border_font=BORDER_FONT['font'], border_font_size=BORDER_FONT['fontsize'],
                        head_text=theme['leftmoduleprefix'], tail_text=theme['leftmodulesuffix'])
        )
    return result


def getWidgets(theme, screen, groups):
    global common_widgets, group_widgets

    if len(common_widgets) < 1:
        prepareCommonWidgets(theme)

    # Layout Icon
    widgets = [
        widget.CurrentLayoutIcon(
            background=theme['titlebg'], scale=0.6, foreground=theme['titlefg'], padding=theme['titlepadding']),
        widget.TextBox(
            **BORDER_FONT, text=theme['leftmodulesuffix'], foreground=theme['titlebg'], padding=0)
    ]

    _groups_widgets = getGroupWidgets(theme, screen, groups)
    for w in _groups_widgets:
        widgets += w.getWidgets()
    group_widgets[screen] = _groups_widgets

    widgets += common_widgets['mpd'].getWidgets()
    
    # Prompt
    if screen == 0:
        widgets += [
            widget.TextBox(
                **BORDER_FONT, foreground=theme['titlebg'], text=theme['leftmoduleprefix'], padding=0),
            widget.Prompt(
                **DEFAULT_FONT, foreground=theme['titlefg'], background=theme['titlebg'], prompt=" "),
            widget.TextBox(
                **BORDER_FONT, foreground=theme['titlebg'], text=theme['leftmodulesuffix'], padding=0),
        ]
    # Systray
    widgets += [widget.Spacer()]

    widgets += common_widgets['local_time'].getWidgets()
    widgets += common_widgets['india_time'].getWidgets()
    widgets += [widget.Spacer(length=675-theme['barrightborder'])]



    widgets += common_widgets['locks'].getWidgets()
    widgets += common_widgets['temperature'].getWidgets()
    widgets += common_widgets['utilization'].getWidgets()
    widgets += common_widgets['volume'].getWidgets()

    for k in ['wlan', 'lan']:
        for w in common_widgets[k]:
            widgets += w.getWidgets()

    widgets += common_widgets['screen_lock'].getWidgets()
    widgets += common_widgets['shut'].getWidgets()
    widgets += common_widgets['toggle_power'].getWidgets()

    return widgets


def updateGroupWidgets():
    global group_widgets
    for screen in group_widgets:
        for w in group_widgets[screen]:
            w.update()


def clickGroup(qtile, group, x=0, y=0, button=1):
    for _group in qtile.groups:
        if _group.name == group:
            _group.cmd_toscreen()
            break
    updateGroupWidgets()


def show_hide_power_widgets(x=0, y=0, button=1, qtile=None):
    if button != MOUSE_BUTTONS['LEFT_CLICK']:
        return

    global common_widgets
    common_widgets['screen_lock'].show(
        common_widgets['screen_lock'].isHidden())
    common_widgets['shut'].show(common_widgets['shut'].isHidden())

    if common_widgets['screen_lock'].isHidden():
        common_widgets['toggle_power'].update(title_text=" ")
    else:
        common_widgets['toggle_power'].update(title_text=" ")

def updateVolumeWidgets():
    global common_widgets
    common_widgets['volume'].update()