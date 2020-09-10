from functools import partial

from libqtile import widget
from libqtile.core.manager import Qtile
from libqtile.log_utils import logger

from my_scripts import getVolume, getVolumeIcon, volumeClicked
from my_scripts import getGroupColors, getGroupLabel
from my_scripts import getMpd, clickMpd
from my_scripts import getTime, getlocksStatus, getTemps, getUtilization
from my_scripts import getInterfaces, getWlan, getLan
from my_scripts import powerClicked, POWER_BUTTONS, MOUSE_BUTTONS
from my_scripts import getBatteryCapacity, getBatteryStatusIcon

from my_widgets import ComboWidget
from icons import getIcons

DEFAULT_FONT = dict(
    font="Iosevka Nerd Font Medium",
    #font="JetBrainsMonoMedium Nerd Font Mono",
    fontsize=14,
)

BORDER_FONT = dict(
    font="Iosevka Nerd Font Mono",
    fontsize=20,
)

ICON_FONT = dict(
    font="Font Awesome 5 Free Solid",
    fontsize=12,
)

common_widgets = {}
group_widgets = {}


def prepareCommonWidgets(theme):
    global common_widgets, group_widgets
    global DEFAULT_FONT, BORDER_FONT, ICON_FONT

    common_widgets['mpd'] = ComboWidget(title_func=lambda qtile: getIcons()['music'], title_bg=theme['titlebg'], title_fg=theme['titlefg'],
                                  title_padding=theme['titlepadding'], body_func=getMpd, body_bg=theme['bodybg'],
                                  body_fg=theme['bodyfg'], body_padding=theme['bodypadding'], poll_interval=30,
                                  title_head_text=theme['leftmoduleprefix'], title_tail_text=theme['leftmodulesuffix'],
                                  body_tail_text=theme['leftmodulesuffix'], head_tail_font=BORDER_FONT['font'],
                                  head_tail_font_size=BORDER_FONT['fontsize'], title_font=ICON_FONT['font'],
                                  title_font_size=ICON_FONT['fontsize'],
                                  body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'], 
                                  click_func=clickMpd, click_update=True,
                                  margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '')


    common_widgets['locks'] = ComboWidget(title_func=lambda qtile: getIcons()['locks'], title_bg=theme['gradient1title'], title_fg=theme['gradienttitlefg'],
                                  title_padding=theme['titlepadding'], body_func=getlocksStatus, body_bg=theme['gradient1body'],
                                  body_fg=theme['gradientbodyfg'], body_padding=theme['bodypadding'], poll_interval=2, title_head_text=theme['rightmoduleprefix'],
                                  title_tail_text=theme['rightmodulesuffix'], body_tail_text=theme['rightmodulesuffix'],
                                  head_tail_font=BORDER_FONT['font'],
                                  head_tail_font_size=BORDER_FONT['fontsize'], title_font=ICON_FONT['font'],
                                  title_font_size=ICON_FONT['fontsize'],
                                  body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'], 
                                  click_update=True, inactive_hide=True,
                                  margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '')

    common_widgets['temperature'] = ComboWidget(title_func=lambda qtile: getIcons()['temperature'], title_bg=theme['gradient2title'], title_fg=theme['gradienttitlefg'],
                                  title_padding=theme['titlepadding'], body_func=getTemps, body_bg=theme['gradient2body'],
                                  body_fg=theme['gradientbodyfg'], body_padding=theme['bodypadding'], poll_interval=5, title_head_text=theme['rightmoduleprefix'],
                                  title_tail_text=theme['rightmodulesuffix'], body_tail_text=theme['rightmodulesuffix'],
                                  head_tail_font=BORDER_FONT['font'],
                                  head_tail_font_size=BORDER_FONT['fontsize'], title_font=ICON_FONT['font'],
                                  title_font_size=ICON_FONT['fontsize'],
                                  body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'], click_update=True,
                                  margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '')

    common_widgets['utilization'] = ComboWidget(title_func=lambda qtile: getIcons()['utilization'], title_bg=theme['gradient3title'], title_fg=theme['gradienttitlefg'],
                                  title_padding=theme['titlepadding'], body_func=getUtilization, body_bg=theme['gradient3body'],
                                  body_fg=theme['gradientbodyfg'], body_padding=theme['bodypadding'], poll_interval=5, title_head_text=theme['rightmoduleprefix'],
                                  title_tail_text=theme['rightmodulesuffix'], body_tail_text=theme['rightmodulesuffix'],
                                  head_tail_font=BORDER_FONT['font'],
                                  head_tail_font_size=BORDER_FONT['fontsize'], title_font=ICON_FONT['font'],
                                  title_font_size=ICON_FONT['fontsize'],
                                  body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'], click_update=True,
                                  margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '')

    common_widgets['volume'] = ComboWidget(title_func=getVolumeIcon, title_bg=theme['gradient4title'], title_fg=theme['gradienttitlefg'],
                                  title_update=True, title_padding=theme['titlepadding'], body_func=getVolume, body_bg=theme['gradient4body'],
                                  body_fg=theme['gradientbodyfg'], body_padding=theme['bodypadding'], poll_interval=None, title_head_text=theme['rightmoduleprefix'],
                                  title_tail_text=theme['rightmodulesuffix'], body_tail_text=theme[
                                      'rightmodulesuffix'], head_tail_font=BORDER_FONT['font'],
                                  head_tail_font_size=BORDER_FONT['fontsize'], title_font=ICON_FONT[
                                      'font'], title_font_size=ICON_FONT['fontsize'],
                                  body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'], click_func=volumeClicked, click_update=True,
                                  margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '')

    # Since computers can have multiple net interfaces
    common_widgets['wlan'] = []
    common_widgets['lan'] = []
    for interface in getInterfaces():
        title = (lambda qtile: getIcons()['wifi']) if 'wl' in interface else (lambda qtile: getIcons()['lan'])
        func = getWlan if 'wl' in interface else getLan
        i_list = common_widgets['wlan'] if 'wl' in interface else common_widgets['lan']
        i_list.append(ComboWidget(title_func=title, title_fg=theme['gradienttitlefg'], title_bg=theme['gradient5title'],
                        title_padding=theme['titlepadding'], body_func=partial(func, interface=interface),
                        body_fg=theme['gradientbodyfg'], body_bg=theme['gradient5body'], body_padding=theme['bodypadding'],
                        poll_interval=5, title_head_text=theme['rightmoduleprefix'], title_tail_text=theme['rightmodulesuffix'],
                        body_tail_text=theme['rightmodulesuffix'], head_tail_font=BORDER_FONT['font'], head_tail_font_size=BORDER_FONT['fontsize'],
                        title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'], body_font=DEFAULT_FONT['font'],
                        body_font_size=DEFAULT_FONT['fontsize'], inactive_hide=True, click_update=True,
                        margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '' ))
        # Upload/download speeds as separate widgets. This is usefull if the default font does not contain
        # the Upload/download glymphs(and looks better), But since it will add the overhead of more widgets
        # and our default _font has these glymphs we are disabling it
        # i_list.append(ComboWidget(title_func=lambda qtile: "", title_fg=theme['titlefg'], title_bg=theme['gradient5title'],
        #                 title_padding=5, body_func=partial(getNetSpeed, interface=interface),
        #                 body_fg=theme['titlefg'], body_bg=theme['gradient5body'], body_padding=theme['bodypadding'],
        #                 poll_interval=5, title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'], body_font=DEFAULT_FONT['font'],
        #                 body_font_size=DEFAULT_FONT['fontsize'], inactive_hide=True, click_update=True,
        #                 margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '' ))
        # i_list.append(ComboWidget(title_func=lambda qtile: "", title_fg=theme['titlefg'], title_bg=theme['gradient5title'],
        #                 title_padding=5, body_func=partial(getNetSpeed, interface=interface, upload=True),
        #                 body_fg=theme['titlefg'], body_bg=theme['gradient5body'], body_padding=theme['bodypadding'],
        #                 poll_interval=5, title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'], body_font=DEFAULT_FONT['font'],
        #                 body_font_size=DEFAULT_FONT['fontsize'], inactive_hide=True, click_update=True,
        #                 margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '' ))
        # i_list.append(ComboWidget(title_func=partial(func, interface=interface), title_label=theme['rightmodulesuffix'], title_bg=theme['background'], title_fg=theme['gradient5body'],
        #                        title_padding=0, poll_interval=5, title_font=BORDER_FONT['font'],
        #                        title_font_size=BORDER_FONT['fontsize'], click_update=True, title_update=True))
    
    common_widgets['local_time'] = ComboWidget(title_func=lambda qtile: getIcons()['clock'], title_bg=theme['gradient6title'], title_fg=theme['gradienttitlefg'],
                                  title_padding=theme['titlepadding'], body_func=getTime, body_bg=theme['gradient6body'],
                                  body_fg=theme['gradientbodyfg'], body_padding=theme['bodypadding'], poll_interval=30,
                                  title_head_text=theme['rightmoduleprefix'], title_tail_text=theme['rightmodulesuffix'],
                                  body_tail_text=theme['rightmodulesuffix'], head_tail_font=BORDER_FONT['font'],
                                  head_tail_font_size=BORDER_FONT['fontsize'], title_font=ICON_FONT['font'],
                                  title_font_size=ICON_FONT['fontsize'],
                                  body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'], click_update=True,
                                  margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '')

    common_widgets['india_time'] = ComboWidget(title_func=partial(getTime, format='%I:%M %p', timezone='Asia/Kolkata'), 
                                title_bg=theme['gradient6body'], title_fg=theme['gradientbodyfg'],
                                title_padding=theme['bodypadding'], poll_interval=30, title_head_text=theme['rightmoduleprefix'],
                                title_tail_text=theme['rightmodulesuffix'], head_tail_font=BORDER_FONT['font'],
                                head_tail_font_size=BORDER_FONT['fontsize'], title_font=DEFAULT_FONT['font'],
                                title_font_size=DEFAULT_FONT['fontsize'], click_update=True, title_update=True,
                                margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '')

    common_widgets['battery'] = ComboWidget(title_func=getBatteryStatusIcon, title_bg=theme['gradient1title'], title_fg=theme['gradienttitlefg'],
                                  title_padding=theme['titlepadding'], body_func=getBatteryCapacity, body_bg=theme['gradient1body'],
                                  body_fg=theme['gradientbodyfg'], body_padding=theme['bodypadding'], poll_interval=5, title_head_text=theme['rightmoduleprefix'],
                                  title_tail_text=theme['rightmodulesuffix'], body_tail_text=theme['rightmodulesuffix'],
                                  head_tail_font=BORDER_FONT['font'],
                                  head_tail_font_size=BORDER_FONT['fontsize'], title_font=ICON_FONT['font'],
                                  title_font_size=ICON_FONT['fontsize'],
                                  body_font=DEFAULT_FONT['font'], body_font_size=DEFAULT_FONT['fontsize'], 
                                  click_update=True, inactive_hide=True, title_update=True,
                                  margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '')

    power_bg = theme['gradient7title'] if 'gradient7title' in theme else theme['titlebg']
    common_widgets['screen_lock'] = ComboWidget(title_func=lambda qtile: getIcons()['screen_lock'], title_bg=power_bg, title_fg=theme['gradienttitlefg'],
                                       title_update=True, title_padding=theme['titlepadding'], title_head_text=theme['rightmoduleprefix'],
                                       title_tail_text=theme['rightmodulesuffix'], head_tail_font=BORDER_FONT['font'],
                                       head_tail_font_size=BORDER_FONT['fontsize'], title_font=ICON_FONT['font'],
                                       title_font_size=ICON_FONT['fontsize'], hide=True,
                                       click_func=lambda qtile, buttton: powerClicked(qtile, buttton, POWER_BUTTONS['LOCK_SCREEN']),
                                       margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '')

    common_widgets['shut'] = ComboWidget(title_func=lambda qtile: getIcons()['power'], title_bg=power_bg, title_fg=theme['gradienttitlefg'],
                                title_update=True, title_padding=theme['titlepadding'], title_head_text=theme['rightmoduleprefix'],
                                title_tail_text=theme['rightmodulesuffix'], head_tail_font=BORDER_FONT['font'],
                                head_tail_font_size=BORDER_FONT['fontsize'], title_font=ICON_FONT['font'],
                                title_font_size=ICON_FONT['fontsize'], hide=True,
                                click_func=lambda qtile, buttton: powerClicked(qtile, buttton, POWER_BUTTONS['SHUT_DOWN']))

    common_widgets['toggle_power'] = ComboWidget(title_func=lambda qtile: getIcons()['power'], title_bg=power_bg, title_fg=theme['gradienttitlefg'],
                                title_update=True, 
                                title_padding=theme['titlepadding'] if theme['titlepadding'] else 4,
                                title_head_text=theme['rightmoduleprefix'], head_tail_font=BORDER_FONT['font'],
                                head_tail_font_size=BORDER_FONT['fontsize'], title_font=ICON_FONT['font'],
                                title_font_size=ICON_FONT['fontsize'], click_func=show_hide_power_widgets,
                                margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '')

def getGroupWidgets(theme, screen, groups):
    result = []
    for group in groups:
        result.append(
            ComboWidget(title_func=partial(getGroupLabel, group=group.name),
               title_bg=theme['bodybg'], title_fg=theme['bodyfg'], title_update=True,
               title_padding=theme['wspadding'], title_head_text=theme['leftmoduleprefix'],
               title_color_func=partial(
                   getGroupColors, group=group.name, theme=theme, screen=screen),
               title_tail_text=theme['leftmodulesuffix'], head_tail_font=BORDER_FONT[
                   'font'], head_tail_font_size=BORDER_FONT['fontsize'],
               title_font=ICON_FONT['font'], title_font_size=ICON_FONT['fontsize'],
               click_func=partial(clickGroup, group=group.name), inactive_hide=True,
               click_update=True, margin_text=theme['moduleseparator'] if 'moduleseparator' in theme else '')
        )
    return result


def getWidgets(theme, screen, groups):
    global common_widgets, group_widgets

    if len(common_widgets) < 1:
        prepareCommonWidgets(theme)

    # Layout Icon
    widgets = [
        widget.CurrentLayoutIcon(
            background=theme['titlebg'], scale=0.6, foreground=theme['titlefg'],
            padding=theme['titlepadding'] if theme['titlepadding'] else 4),
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
        if 'moduleseparator' in theme and theme['moduleseparator'] != "":
            widgets += [widget.TextBox(text=theme['moduleseparator'], padding=0)]
        widgets += [
            widget.TextBox(
                **BORDER_FONT, foreground=theme['titlebg'], text=theme['leftmoduleprefix'], padding=0),
            widget.Prompt(
                **DEFAULT_FONT, foreground=theme['titlefg'], background=theme['titlebg'], prompt=getIcons()['launch']+" "),
            widget.TextBox(
                **BORDER_FONT, foreground=theme['titlebg'], text=theme['leftmodulesuffix'], padding=0),
        ]

    # Auto spacer
    widgets += [widget.Spacer()]

    widgets += common_widgets['locks'].getWidgets()
    widgets += common_widgets['temperature'].getWidgets()
    widgets += common_widgets['utilization'].getWidgets()
    widgets += common_widgets['volume'].getWidgets()
    for k in ['wlan', 'lan']:
        for w in common_widgets[k]:
            widgets += w.getWidgets()

    widgets += common_widgets['local_time'].getWidgets()
    widgets += common_widgets['india_time'].getWidgets()
    widgets += common_widgets['battery'].getWidgets()
    widgets += common_widgets['screen_lock'].getWidgets()
    widgets += common_widgets['shut'].getWidgets()
    widgets += common_widgets['toggle_power'].getWidgets()

    return widgets


def updateGroupWidgets():
    global group_widgets
    for screen in group_widgets:
        for w in group_widgets[screen]:
            w.update()


def clickGroup(qtile: Qtile, button: int, group: str):
    for _group in qtile.groups:
        if _group.name == group:
            _group.cmd_toscreen()
            break
    updateGroupWidgets()


def show_hide_power_widgets(qtile, button):
    if button != MOUSE_BUTTONS['LEFT_CLICK']:
        return

    global common_widgets
    common_widgets['screen_lock'].show(
        common_widgets['screen_lock'].isHidden())
    common_widgets['shut'].show(common_widgets['shut'].isHidden())

    if common_widgets['screen_lock'].isHidden():
        common_widgets['toggle_power'].title.update(getIcons()['power'])
    else:
        common_widgets['toggle_power'].title.update(getIcons()['cancel'])


def updateVolumeWidgets():
    global common_widgets
    common_widgets['volume'].update()
