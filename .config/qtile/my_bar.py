from functools import partial
from libqtile.lazy import lazy

from libqtile.config import Group
from libqtile import widget
from libqtile.core.manager import Qtile
from libqtile.log_utils import logger
from psutil import net_connections

from my_scripts import getGroupLabel, getVolume, getVolumeIcon, updateWallpaper, volumeClicked
from my_scripts import getGroupColors
from my_scripts import getMpd, clickMpd
from my_scripts import getTime, getlocksStatus, getTemps, getUtilization
from my_scripts import getNetworkInterfaces, getWlan, getLan
from my_scripts import powerClicked, POWER_BUTTONS, MOUSE_BUTTONS
from my_scripts import getBatteryCapacity, getBatteryStatusIcon

from my_widgets import ComboWidget
from icons import getIcons


DEFAULT_FONT = dict(
    # font="Iosevka Nerd Font Medium",
    font="JetBrainsMono Medium Nerd Font Mono",
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

# These are stored to update colors dynamically when interacted with
common_widgets: dict[str, list[any]] = {}
group_widgets: dict[int, list[list[any]]] = {}


def prepareWidgets(theme: dict):
    '''
    This function creates widgets common to all the screens
    '''

    global common_widgets

    common_widgets['module_separator'] = [widget.TextBox(
            **BORDER_FONT, text=theme['moduleseparator'], padding=0)]

    # Mpd
    mpdClick = {
        'Button1': partial(clickMpd, 1),
        'Button2': partial(clickMpd, 2),
        'Button3': partial(clickMpd, 3),
        'Button4': partial(clickMpd, 4),
        'Button5': partial(clickMpd, 5)
    }
    common_widgets['mpd'] = [
        widget.TextBox(
            **BORDER_FONT, foreground=theme['titlebg'], text=theme['leftmoduleprefix'], padding=0, mouse_callbacks=mpdClick),
        widget.TextBox(
            **ICON_FONT, foreground=theme['titlefg'], background=theme['titlebg'],
            text=getIcons()['music'], padding=theme['titlepadding'], mouse_callbacks=mpdClick),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['titlebg'], background=theme['bodybg'], text=theme['leftmodulesuffix'], padding=0, mouse_callbacks=mpdClick),
        widget.GenPollText(
            **DEFAULT_FONT, foreground=theme['bodyfg'], background=theme['bodybg'],
            func=getMpd, mouse_callbacks=mpdClick,
            padding=theme['bodypadding'], update_interval=3),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['bodybg'], text=theme['leftmodulesuffix'], padding=0, mouse_callbacks=clickMpd)
    ]

    # Prompt
    common_widgets['prompt'] = [
        widget.TextBox(
            **BORDER_FONT, foreground=theme['titlebg'], text=theme['leftmoduleprefix'], padding=0),
        widget.Prompt(
            **DEFAULT_FONT, foreground=theme['titlefg'], background=theme['titlebg'], prompt=getIcons()['launch']+" "),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['titlebg'], text=theme['leftmodulesuffix'], padding=0),
    ]

    # Locks
    common_widgets['locks'] = [
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient1title'], text=theme['rightmoduleprefix'], padding=0),
        widget.TextBox(
            **ICON_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient1title'],
            text=getIcons()['locks'], padding=theme['titlepadding']),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient1title'], background=theme['gradient1body'], text=theme['rightmodulesuffix'], padding=0),
        widget.GenPollText(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'], background=theme['gradient1body'],
            func=partial(updateLockWidget, theme), padding=theme['bodypadding'], update_interval=0.5),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient1body'], text=theme['rightmodulesuffix'], padding=0)
    ]

    # Volume
    volumeClick = {
        'Button1': partial(updateVolume, 1),
        'Button2': partial(updateVolume, 2),
        'Button3': partial(updateVolume, 3),
        'Button4': partial(updateVolume, 4),
        'Button5': partial(updateVolume, 5)
    }
    common_widgets['volume'] = [
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient2title'], text=theme['rightmoduleprefix'], padding=0, mouse_callbacks=volumeClick),
        widget.GenPollText(
            **ICON_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient2title'],
            func=getVolumeIcon, padding=theme['titlepadding'], mouse_callbacks=volumeClick, update_interval=5),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient2title'], background=theme['gradient2body'], text=theme['rightmodulesuffix'], padding=0, mouse_callbacks=volumeClick),
        widget.GenPollText(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'], background=theme['gradient2body'],
            func=getVolume, padding=theme['bodypadding'], mouse_callbacks=volumeClick, update_interval=5),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient2body'], text=theme['rightmodulesuffix'], padding=0, mouse_callbacks=volumeClick)
    ]

    # Utilization
    common_widgets['utilization'] = [
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient3title'], text=theme['rightmoduleprefix'], padding=0),
        widget.TextBox(
            **ICON_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient3title'],
            text=getIcons()['utilization'], padding=theme['titlepadding']),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient3title'], background=theme['gradient3body'], text=theme['rightmodulesuffix'], padding=0),
        widget.GenPollText(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'], background=theme['gradient3body'],
            func=getUtilization, padding=theme['bodypadding'], update_interval=3),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient3body'], text=theme['rightmodulesuffix'], padding=0)
    ]

    # Temperature
    common_widgets['temperature'] = [
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient4title'], text=theme['rightmoduleprefix'], padding=0),
        widget.TextBox(
            **ICON_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient4title'],
            text=getIcons()['temperature'], padding=theme['titlepadding']),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient4title'], background=theme['gradient4body'], text=theme['rightmodulesuffix'], padding=0),
        widget.GenPollText(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'], background=theme['gradient4body'],
            func=getTemps, padding=theme['bodypadding'], update_interval=3),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient4body'], text=theme['rightmodulesuffix'], padding=0)
    ]

    # Network
    common_widgets['network'] = []
    for interface in getNetworkInterfaces():
        icon = getIcons()['wlan' if 'wl' in interface else 'lan']
        common_widgets[interface] = [
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient5title'], text=theme['rightmoduleprefix'], padding=0),
            widget.TextBox(
                **ICON_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient5title'],
                text=icon, padding=theme['titlepadding']),
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient5title'], background=theme['gradient5body'], text=theme['rightmodulesuffix'], padding=0),
            widget.GenPollText(
                **DEFAULT_FONT, foreground=theme['gradientbodyfg'], background=theme['gradient5body'],
                func=partial(updateNetworkWidgets, theme, interface), padding=theme['bodypadding'], update_interval=3),
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient5body'], text=theme['rightmodulesuffix'], padding=0)
        ]
        if not common_widgets['network']:
            common_widgets['network'] += common_widgets['module_separator']
        common_widgets['network'] += common_widgets[interface]

    # Time
    common_widgets['time'] = [
        # Local time
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient6title'], text=theme['rightmoduleprefix'], padding=0),
        widget.TextBox(
            **ICON_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient6title'],
            text=getIcons()['clock'], padding=theme['titlepadding']),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient6title'], background=theme['gradient6body'], text=theme['rightmodulesuffix'], padding=0),
        widget.GenPollText(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'], background=theme['gradient6body'],
            func=getTime, padding=theme['bodypadding'], update_interval=30),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient6body'], text=theme['rightmodulesuffix'], padding=0),

        # Indian time
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient6title'], text=theme['rightmoduleprefix'], padding=0),
        widget.GenPollText(
            **DEFAULT_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient6title'],
            func=partial(getTime, format='%I:%M %p', timezone='Asia/Kolkata'), padding=theme['bodypadding'], update_interval=30),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient6body'], text=theme['rightmodulesuffix'], padding=0),
    ]

    # Battery
    if getBatteryStatusIcon():
        common_widgets['battery'] = [
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient7title'], text=theme['rightmoduleprefix'], padding=0),
            widget.GenPollText(
                **ICON_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient7title'],
                func=getBatteryStatusIcon, padding=theme['titlepadding']),
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient7title'], background=theme['gradient7body'], text=theme['rightmodulesuffix'], padding=0),
            widget.GenPollText(
                **DEFAULT_FONT, foreground=theme['gradientbodyfg'], background=theme['gradient7body'],
                func=getBatteryCapacity, padding=theme['bodypadding'], update_interval=3),
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient7body'], text=theme['rightmodulesuffix'], padding=0)
        ]

    # Power/Logout/Screen lock
    common_widgets['power'] = [
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient7body'], text=theme['rightmoduleprefix'], padding=0),
        widget.WidgetBox(background=theme['gradient7body'], foreground=theme['gradienttitlefg'], close_button_location='right',
                         text_closed=getIcons()['power'], text_open=getIcons()['cancel'], **ICON_FONT,
                         widgets=[
            # screen lock
            widget.TextBox(
                **ICON_FONT, background=theme['gradient7body'], foreground=theme['gradienttitlefg'], padding=theme['titlepadding'],
                text=getIcons()['screen_lock'], mouse_callbacks={'Button1': partial(powerClicked, 1, 2)}),
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient7body'], text=theme['rightmodulesuffix'], padding=0),

            # Logout
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient7body'], text=theme['rightmoduleprefix'], padding=0),
            widget.TextBox(
                **ICON_FONT, background=theme['gradient7body'], foreground=theme['gradienttitlefg'], padding=theme['titlepadding'],
                text=getIcons()['logout'], mouse_callbacks={'Button1': partial(powerClicked, 1, 1)}),
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient7body'], text=theme['rightmodulesuffix'], padding=0),

            # shutdown
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient7body'], text=theme['rightmoduleprefix'], padding=0),
            widget.TextBox(
                **ICON_FONT, background=theme['gradient7body'], foreground=theme['gradienttitlefg'], padding=theme['titlepadding'],
                text=getIcons()['power'], mouse_callbacks={'Button1': partial(powerClicked, 1, 0)}),
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient7body'], text=theme['rightmodulesuffix'], padding=0),

            # prefix for the cancel button when box is opened
            widget.TextBox(
                **BORDER_FONT, foreground=theme['gradient7body'], text=theme['rightmoduleprefix'], padding=0)
        ]),
        widget.TextBox(
            **BORDER_FONT, foreground=theme['gradient7body'], text=theme['rightmodulesuffix'], padding=0),
    ]



def getWidgets(theme: dict, screen: int, groups: list[Group]):
    global group_widgets, common_widgets 

    if not common_widgets:
        prepareWidgets(theme)

    # Layout icon
    widgets = [
        widget.TextBox(
            **BORDER_FONT, text=theme['leftmoduleprefix'], foreground=theme['titlebg'], padding=0),
        widget.CurrentLayoutIcon(
            background=theme['titlebg'], scale=0.6, foreground=theme['titlefg'],
            padding=theme['titlepadding'] if theme['titlepadding'] else 4),
        widget.TextBox(
            **BORDER_FONT, text=theme['leftmodulesuffix'], foreground=theme['titlebg'], padding=0)
    ]

    # Group widgets
    group_widgets[screen] = []
    for group in groups:
        if group.name == 'scratchpad':
            continue

        _group_widgets = [
            widget.TextBox(
                **BORDER_FONT, text=theme['leftmoduleprefix'], foreground=theme['bodybg'], padding=0),
            widget.TextBox(
                # **ICON_FONT, text=lazy.function(getGroupLabel, group.name),
                **ICON_FONT, text=group.label,
                foreground=theme['bodyfg'], background=theme['bodybg'], padding=1,
                mouse_callbacks={'Button1': lazy.function(clickGroup, group.name, theme)}),
            widget.TextBox(
                **BORDER_FONT, text=theme['leftmodulesuffix'], foreground=theme['bodybg'], padding=0)
        ]
        group_widgets[screen].append(_group_widgets)
        widgets += _group_widgets

    widgets += common_widgets['mpd'] + common_widgets['module_separator'] + common_widgets['prompt']
    widgets.append(widget.Spacer())
    widgets += common_widgets['locks'] + common_widgets['module_separator'] + common_widgets['volume'] + common_widgets['module_separator'] 
    widgets += common_widgets['temperature'] + common_widgets['module_separator'] + common_widgets['utilization'] + common_widgets['module_separator'] 
    widgets += common_widgets['network'] + common_widgets['module_separator'] 
    widgets += common_widgets['time'] + common_widgets['module_separator'] 
    if 'battery' in common_widgets:
        widgets += common_widgets['battery'] + common_widgets['module_separator'] 
    widgets += common_widgets['power']

    return widgets


def clickGroup(qtile: Qtile, groupName: str, theme):
    for _group in qtile.groups:
        if _group.name == groupName:
            _group.cmd_toscreen()
            break
    updateGroupWidgets(qtile, theme)
    updateWallpaper(qtile)


def updateGroupWidgets(q: Qtile, theme: dict):
    global group_widgets

    for screen in group_widgets:
        for i, group in enumerate(group_widgets[screen], start=1):
            # group is an array of the form [TextBox(modulePrefix), TextBox(group.label), TextBox(moduleSuffix)]
            # label = getGroupLabel(q, str(i))
            # if not label:
            #     for g in group:
            #         g.update("")
            # else:
            (fgColor, bgColor) = getGroupColors(q, str(i), theme, screen)
            group[0].foreground = bgColor
            group[1].foreground = fgColor
            group[1].background = bgColor
            group[2].foreground = bgColor
            for g in group:
                g.update(g.text)


def updateVolume(button: int = 1, widget_only = False):
    global common_widgets
    if not widget_only:
        volumeClicked(button)
    # if button in [1, 2]:
    #     common_widgets['volume'][1].update(getIcons()['mute'])
    # else:
    common_widgets['volume'][1].update(getVolumeIcon())
    common_widgets['volume'][3].update(getVolume())


def updateNetworkWidgets(theme: dict, interface: str):
    global common_widgets
    wlan = 'wl' in interface
    widgets = common_widgets[interface] if interface in common_widgets else []
    if not widgets:
        return ""

    result = getWlan(interface, '') if wlan else getLan(interface, '')
    if not result:
        # hide all the widgets
        for _widget in widgets:
            _widget.update("")
    else:
        widgets[0].update(theme['rightmoduleprefix'])
        widgets[1].update(getIcons()['wlan' if wlan else 'lan'])
        widgets[2].update(theme['rightmodulesuffix'])
        widgets[4].update(theme['rightmodulesuffix'])

    return result

def updateLockWidget(theme: dict):
    global common_widgets

    widgets = common_widgets['locks']
    result = getlocksStatus()
    if not result:
        # hide all the widgets
        for _widget in widgets:
            _widget.update("")
    else:
        widgets[0].update(theme['rightmoduleprefix'])
        widgets[1].update(getIcons()['locks'])
        widgets[2].update(theme['rightmodulesuffix'])
        widgets[4].update(theme['rightmodulesuffix'])

    return result
