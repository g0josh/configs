from functools import partial
from libqtile.lazy import lazy

from libqtile.config import Group
from qtile_extras import widget 
from qtile_extras.widget.decorations import RectDecoration
from libqtile.core.manager import Qtile
from libqtile.log_utils import logger
from psutil import net_connections

from my_scripts import getGroupLabel, getVolume, getVolumeIcon, updateWallpaper, volumeClicked
from my_scripts import getGroupColors
from my_scripts import getMpd, clickMpd
from my_scripts import getLocksStatus, getBluetoothStatus
from my_scripts import getNetworkInterfaces, getWlan, getLan
from my_scripts import powerClicked, POWER_BUTTONS, MOUSE_BUTTONS
from my_scripts import isBatteryPresent

# from my_widgets import ComboWidget
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
    module_separator_length = 2
    if 'modulepadding' in theme:
        module_separator_length = theme['modulepadding']

    common_widgets['module_separator'] = [widget.Spacer(length=module_separator_length)]

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
            **ICON_FONT, foreground=theme['titlefg'], padding=theme['titlepadding'], background=theme['titlebg'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            text=getIcons()['music'], mouse_callbacks=mpdClick),
        widget.GenPollText(
            **DEFAULT_FONT, foreground=theme['bodyfg'],padding=theme['bodypadding'], background=theme['bodybg'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            func=getMpd, mouse_callbacks=mpdClick,
            update_interval=1)
    ]

    # Prompt
    common_widgets['prompt'] = [
        widget.Prompt(
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            **DEFAULT_FONT, padding=theme['titlepadding'],background=theme['titlebg'],
            foreground=theme['titlefg'], prompt=getIcons()['launch']+" ")
    ]

    # Locks
    common_widgets['locks'] = [
        widget.TextBox(
            **ICON_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient1title'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True,group=True)],
            text=getIcons()['locks'], padding=theme['titlepadding']),
        widget.GenPollText(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'],background=theme['gradient1title'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            func=partial(updateLockWidget, theme), padding=theme['bodypadding'], update_interval=0.5),
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
        widget.GenPollText(
            **ICON_FONT, foreground=theme['gradienttitlefg'], padding=theme['titlepadding'], background=theme['gradient2title'],
            func=getVolumeIcon, mouse_callbacks=volumeClick, update_interval=1,
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            ),
        widget.GenPollText(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'], background=theme['gradient2title'],
            func=getVolume, padding=theme['bodypadding'], mouse_callbacks=volumeClick, update_interval=1,
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            )
    ]

    # Bluetooth
    common_widgets['bluetooth'] = [
        widget.TextBox(
            **ICON_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient1title'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True,group=True)],
            text=getIcons()['bluetooth'], padding=theme['titlepadding']),
        widget.GenPollText(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'],background=theme['gradient1title'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            func=partial(updateBluetoothWidget, theme), padding=theme['bodypadding'], update_interval=2,
        )
    ]

    # Utilization
    common_widgets['utilization'] = [
        widget.TextBox(
            **ICON_FONT, foreground=theme['gradienttitlefg'], padding=theme['titlepadding'],
            text=getIcons()['utilization'], background=theme['gradient3title'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)]
            ),
        widget.CPU(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'], padding=theme['bodypadding'], background=theme['gradient3body'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            format='{load_percent:.0f}%', update_interval=5
        ),
        widget.NvidiaSensors(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'],background=theme['gradient3body'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            padding=theme['bodypadding'],
            format='| {perf}'
        )
    ]

    # Temperature
    common_widgets['temperature'] = [
        widget.TextBox(
            **ICON_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient4title'],
            text=getIcons()['temperature'], padding=theme['titlepadding'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            ),
        widget.ThermalSensor(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'],background=theme['gradient4body'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            padding=theme['bodypadding'], format='{temp:.0f}' 
        ),
        widget.NvidiaSensors(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'],background=theme['gradient4body'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            padding=theme['bodypadding'],
            format='| {temp}'
        )
    ]

    # Network
    common_widgets['network'] = []
    for interface in getNetworkInterfaces():
        common_widgets[interface] = [
            widget.TextBox(
                **ICON_FONT, foreground=theme['gradienttitlefg'],background=theme['gradient5title'],
                decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
                text=getIcons()['wlan'] if 'wl' in interface else getIcons()['lan'], padding=theme['titlepadding']),
            widget.GenPollText(
                **DEFAULT_FONT, foreground=theme['gradientbodyfg'],background=theme['gradient5body'],
                decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
                func=partial(updateNetworkWidgets, theme, interface), padding=theme['bodypadding'], update_interval=3)
        ]
        if not common_widgets['network']:
           common_widgets['network'] += common_widgets['module_separator']
        common_widgets['network'] += common_widgets[interface]


    # Time
    common_widgets['time'] = [
        widget.TextBox(
            **ICON_FONT, foreground=theme['gradienttitlefg'],background=theme['gradient6title'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            text=getIcons()['clock'], padding=theme['titlepadding']),
        widget.Clock(
            **DEFAULT_FONT, foreground=theme['gradientbodyfg'], background=theme['gradient6body'],
            decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
            format='%b %d, %A, %I:%M %p', update_interval=30, padding=theme['bodypadding']
        )
    ]

    # Battery
    battery_icons = getIcons()['battery']
    if isBatteryPresent():
        common_widgets['battery'] = [
            widget.Battery(
                **ICON_FONT, foreground=theme['gradienttitlefg'], background=theme['gradient7title'],
                decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
                format='{char}', padding=theme['bodypadding'], charge_char=getIcons()['charging'],
                discharge_char=battery_icons[len(battery_icons)-2], empty_char=battery_icons[0],
                unknown_char=battery_icons[len(battery_icons)-2],
                full_char=battery_icons[-1], show_short_text=False
            ),
            widget.Battery(
                **DEFAULT_FONT, foreground=theme['gradientbodyfg'],background=theme['gradient7body'],
                decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
                format='{percent:2.0%}', padding=theme['bodypadding'], show_short_text=False
            )
        ]

    # Backlight
    #common_widgets['backlight'] = [
    #    widget.TextBox(
    #        **ICON_FONT, foreground=theme['gradienttitlefg'],background=theme['gradient7title'],
    #        decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
    #        text=getIcons()['backlight'], padding=theme['titlepadding']),
    #    widget.Backlight(
    #        **DEFAULT_FONT, foreground=theme['gradientbodyfg'], background=theme['gradient7body'],
    #        decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
    #        backlight_name='intel_backlight', change_command='light -Set {0}',
    #        padding=theme['bodypadding'] 
    #    )
    #]

    # Power/Logout/Screen lock
    common_widgets['power'] = [
        widget.WidgetBox(foreground=theme['gradienttitlefg'], close_button_location='right', padding=theme['titlepadding'],
                        decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
                        text_closed=f" {getIcons()['power']} ", text_open=f" {getIcons()['cancel']} ", **ICON_FONT,
                        background=theme['gradient7title'], widgets=[
            # screen lock
            widget.TextBox(
                **ICON_FONT, foreground=theme['gradienttitlefg'], padding=module_separator_length, background=theme['gradient7body'],
                decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
                text=getIcons()['screen_lock'], mouse_callbacks={'Button1': partial(powerClicked, 1, 2)}),
            widget.TextBox(
                **ICON_FONT, foreground=theme['gradienttitlefg'], padding=module_separator_length, background=theme['gradient7body'],
                decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
                text=getIcons()['logout'], mouse_callbacks={'Button1': partial(powerClicked, 1, 1)}),
            widget.TextBox(
                **ICON_FONT, foreground=theme['gradienttitlefg'], padding=module_separator_length,background=theme['gradient7body'],
                decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True, group=True)],
                text=getIcons()['power'], mouse_callbacks={'Button1': partial(powerClicked, 1, 0)}),
        ]),
    ]



def getWidgets(theme: dict, screen: int, groups: list[Group]):
    global group_widgets, common_widgets 

    if not common_widgets:
        prepareWidgets(theme)

    # Layout icon
    widgets = [
        widget.CurrentLayoutIcon(
            decorations=[RectDecoration(colour=theme['titlebg'], radius=5, filled=True)],
            scale=0.6, foreground=theme['titlefg'],
            padding=theme['titlepadding'] if theme['titlepadding'] else 4),
    ] + common_widgets['module_separator']

    # Group widgets
    group_widgets[screen] = []
    for group in groups:
        if group.name == 'scratchpad':
            continue

        _group_widgets = [
            widget.TextBox(
                **ICON_FONT, text=group.label,
                decorations=[RectDecoration(radius=5, filled=True, clip=True, use_widget_background=True)],
                foreground=theme['bodyfg'], padding=theme['titlepadding'], background=theme['bodybg'],
                mouse_callbacks={'Button1': lazy.function(clickGroup, group.name, theme)})
        ] + common_widgets['module_separator']
        group_widgets[screen].append(_group_widgets)
        widgets += _group_widgets

    widgets += common_widgets['mpd'] + common_widgets['module_separator'] + common_widgets['prompt']
    widgets.append(widget.Spacer())
    widgets += common_widgets['locks'] + common_widgets['module_separator'] + common_widgets['volume'] + common_widgets['module_separator'] 
    widgets += common_widgets['bluetooth'] + common_widgets['module_separator']
    widgets += common_widgets['temperature'] + common_widgets['module_separator'] + common_widgets['utilization'] + common_widgets['module_separator'] 
    widgets += common_widgets['network'] + common_widgets['module_separator'] 
    widgets += common_widgets['time'] + common_widgets['module_separator'] 
    if 'battery' in common_widgets:
        widgets += common_widgets['battery'] + common_widgets['module_separator'] 
    if 'backlight' in common_widgets:
        widgets += common_widgets['backlight'] + common_widgets['module_separator'] 
    widgets += common_widgets['power']

    return widgets


def clickGroup(qtile: Qtile, groupName: str, theme):
    for _group in qtile.groups:
        if _group.name == groupName:
            _group.cmd_toscreen()
            break
    updateGroupWidgets(qtile, theme)
    updateWallpaper(qtile, theme=theme)


def updateGroupWidgets(q: Qtile, theme: dict):
    global group_widgets

    for screen in group_widgets:
        for i, group in enumerate(group_widgets[screen], start=1):
            # group is an array of the form [TextBox(modulePrefix), TextBox(group.label), TextBox(moduleSuffix)]
            # label = getGroupLabel(q, str(i))
            # if not label:
            #     for g in group:
            #         g.update("")
            # else:]
            (fgColor, bgColor) = getGroupColors(q, str(i), theme, screen)
            group[0].foreground = fgColor
            group[0].background = bgColor
            group[0].update(group[0].text)


def updateVolume(button: int = 1, widget_only = False):
    global common_widgets
    if not widget_only:
        volumeClicked(button)
    # if button in [1, 2]:
    #     common_widgets['volume'][1].update(getIcons()['mute'])
    # else:
    common_widgets['volume'][0].update(getVolumeIcon())
    common_widgets['volume'][1].update(getVolume())


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
        # widgets[0].update(theme['rightmoduleprefix'])
        widgets[0].update(getIcons()['wlan' if wlan else 'lan'])
        # widgets[2].update(theme['rightmodulesuffix'])
        # widgets[4].update(theme['rightmodulesuffix'])

    return result

def updateLockWidget(theme: dict):
    global common_widgets

    widgets = common_widgets['locks']
    result = getLocksStatus()
    if not result:
        # hide all the widgets
        for _widget in widgets:
            _widget.update("")
    else:
        widgets[0].update(getIcons()['locks'])

    return result

def updateBluetoothWidget(theme: dict):
    global common_widgets

    widgets = common_widgets['bluetooth']
    result = getBluetoothStatus()
    if not result:
        # hide all the widgets
        for _widget in widgets:
            _widget.update("")
    else:
        widgets[0].update(getIcons()['bluetooth'])

    return result
