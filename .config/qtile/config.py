#!/usr/bin/python3

import os
import subprocess
from typing import List

from libqtile import bar, layout, widget, hook
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen, Match, ScratchPad, DropDown
from libqtile.log_utils import logger

from my_scripts import getWlan, getVolumeIcon, getVolume, volumePressed
from my_widgets import FuncWithClick, GroupTextBox, ComboWidget
from my_scripts import getTemps, getUtilization, getMpd, clickMpd
from my_scripts import getlocksStatus, MOUSE_BUTTONS, POWER_BUTTONS
from my_scripts import showPowerClicked, powerClicked, getNumScreens


MOD = "mod4"
ALT = "mod1"
TERMINAL = "urxvt"
BROWSER = "opera"
COLR_TITLE_BG = 'a42f2b'
COLR_BODY_BG = '1c5d87'
COLR_INACTIVE = '15232b'
COLR_TEXT = '110808'
COLR_BAR_BG = '090e36'

# NUM_SCREENS = getNumScreens()
NUM_SCREENS = 2

default_font = dict(
    font="Iosevka Nerd Font Bold Italic",
    fontsize=15,
    padding=0
)
border_font = dict(
    font="Iosevka Nerd Font Mono",
    fontsize=20,
    padding=0
)
icon_font = dict(
    font="Font Awesome 5 Free Solid",
    fontsize=14,
    padding=0
)

groups = [
    Group(name='1', label="1 "),
    Group(name='2', label="2 "),
    Group(name='3', label="3 ", matches=[Match(wm_class=["Code"])], init=True, spawn="code", layout="monadtall" ),
    Group(name='4', label="4 ", init=True, spawn="urxvt -name ranger -e ranger", layout="columns"),
    Group(name='5', label="5 ", init=True, spawn="urxvt -name ncmpcpp -e ncmpcpp -s visualizer", layout="columns"),
    Group(name='6', label="6 ", matches=[Match(wm_class=["Thunderbird"])], init=True, spawn="thunderbird", layout="monadtall"),
    Group(name='7', label="7 "),
    ScratchPad("scratchpad", [
        # define a drop down terminal.
        # it is placed in the upper third of screen by default.
        DropDown("term", TERMINAL,
                x=0.05, y=0.008, width=0.9, height=0.5, opacity=0.9,
                on_focus_lost_hide=True),
        DropDown("calc", "{} -e python".format(TERMINAL),
                x=0.05, y=0.008, width=0.9, height=0.5, opacity=0.9,
                on_focus_lost_hide=True)
        ],
        label="")
]

# Create widgets for all screens
# vol_icon_widgets = []
vol_widgets = []
numlock_widgets = []
capslock_widgets = []
power_widgets = []
power_tail_widgets = []
lock_head_widgets = []
lock_widgets = []
lock_tail_widgets = []
shut_head_widgets = []
shut_widgets = []
# wifi_icon_head_widgets = []
# wifi_icon_widgets = []
# wifi_icon_tail_widgets = []
wifi_widgets = []
# wifi_tail_widgets = []
# cb=ComboWidget(title_poll_func=lambda:"", title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT, body_poll_func=getWlan,
#         body_poll_func_args={'interface':'wlps0'}, body_bg=COLR_BODY_BG, body_fg=COLR_TEXT,
#         title_font=icon_font['font'], title_font_size=icon_font['fontsize'], border_font=border_font['font'],
#         border_font_size=border_font['fontsize'], body_font=default_font['font'], body_font_size=default_font['fontsize'])
# logger.warning(cb.getWidgets())
for n in range(NUM_SCREENS):
    # Volume widgets
    # vol_icon_widget = FuncWithClick(func=getVolumeIcon, click_func=volumePressed,
    #         update_interval=1000,foreground=COLR_TEXT, background=COLR_TITLE_BG, **icon_font)
    # vol_widget = FuncWithClick(func=getVolume, click_func=volumePressed, update_interval=1000,
    #         background=COLR_BODY_BG, foreground=COLR_TEXT, **default_font)
    # vol_icon_widget.click_func_args = {'value_widget':vol_widget, 'icon_widget':vol_icon_widget}
    # vol_widget.click_func_args = {'value_widget':vol_widget, 'icon_widget':vol_icon_widget}
    # vol_icon_widgets.append(vol_icon_widget)
    # vol_widgets.append(vol_widget)

    vol_widgets.append( ComboWidget(title_poll_func=getVolumeIcon, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
        body_poll_func=getVolume, click_func=volumePressed, poll_interval=None, body_bg=COLR_BODY_BG,
        body_fg=COLR_TEXT, title_font=icon_font['font'],title_font_size=icon_font['fontsize'],
        border_font=border_font['font'],border_font_size=border_font['fontsize'], body_font=default_font['font'],
        body_font_size=default_font['fontsize'])
    )
    # Wifi widgets
    # wifi_icon_head_widget = widget.TextBox(text="", **border_font,foreground=COLR_TITLE_BG)
    # wifi_icon_widget = widget.TextBox(text="", **icon_font,foreground=COLR_TEXT, background=COLR_TITLE_BG)
    # wifi_icon_tail_widget = widget.TextBox(text="", **border_font,foreground=COLR_TITLE_BG, background=COLR_BODY_BG)
    # wifi_widget = FuncWithClick(background=COLR_BODY_BG, foreground=COLR_TEXT, **default_font, func=getWlan, update_interval=3.0)
    # wifi_tail_widget = widget.TextBox(**border_font,foreground=COLR_BODY_BG, text="")
    # wifi_widget.func_args = {'interface': 'wlp2s0', 'error_text':'',
    #     'widgets': [wifi_icon_head_widget, wifi_icon_widget, wifi_icon_tail_widget, wifi_tail_widget],
    #     'ontexts': ["", "", "", ""],
    #     'offtexts' : ["", "", "", ""] }
    # wifi_icon_head_widgets.append(wifi_icon_head_widget)
    # wifi_icon_widgets.append(wifi_icon_widget)
    # wifi_icon_tail_widgets.append(wifi_icon_tail_widget)
    # wifi_widgets.append(wifi_widget)
    # wifi_tail_widgets.append(wifi_tail_widget)

    wifi_widgets.append( ComboWidget(title_poll_func=lambda:"", title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT, body_poll_func=getWlan,
        body_poll_func_args={'interface':'wlp2s0'}, poll_interval=5, body_bg=COLR_BODY_BG, body_fg=COLR_TEXT,
        title_font=icon_font['font'], title_font_size=icon_font['fontsize'], border_font=border_font['font'],
        border_font_size=border_font['fontsize'], body_font=default_font['font'], body_font_size=default_font['fontsize'])
    )
    # Lock widgets
    numlock_widgets.append( widget.TextBox(text="0" if getlocksStatus()['Num'] else "", **default_font, foreground=COLR_TEXT,
                    background=COLR_BODY_BG) )
    capslock_widgets.append( widget.TextBox(text=" A" if getlocksStatus()['Caps'] else "", **default_font, foreground=COLR_TEXT,
                    background=COLR_BODY_BG) )

    # power widgets
    power_widget = FuncWithClick(func=lambda:" ", click_func=showPowerClicked,
                    **icon_font, foreground=COLR_TEXT, background=COLR_TITLE_BG, update_interval=1000)
    power_tail_widget = FuncWithClick(func=lambda:"", **border_font, foreground=COLR_TITLE_BG, update_interval=1000)
    lock_head_widget = FuncWithClick(func=lambda:"", **border_font, foreground=COLR_TITLE_BG, update_interval=1000)
    lock_widget = FuncWithClick(func=lambda:"", click_func=powerClicked, click_func_args={'widget_button':POWER_BUTTONS['LOCK_SCREEN']},
                    **icon_font, foreground=COLR_TEXT, background=COLR_TITLE_BG, update_interval=1000)
    lock_tail_widget = FuncWithClick(func=lambda:"", **border_font, foreground=COLR_TITLE_BG, update_interval=1000)
    shut_head_widget = FuncWithClick(func=lambda:"", **border_font, foreground=COLR_TITLE_BG, update_interval=1000)
    shut_widget = FuncWithClick(func=lambda:"", click_func=powerClicked, click_func_args={'widget_button':POWER_BUTTONS['SHUT']},
                    **icon_font, foreground=COLR_TEXT, background=COLR_TITLE_BG, update_interval=1000)

    power_widget.click_func_args = {'widgets':[power_widget, power_tail_widget,
                                        lock_head_widget, lock_widget, lock_tail_widget,
                                        shut_head_widget, shut_widget],
                                    'ontexts':[" ","","","","", ""," "],
                                    'offtexts': ["", "", "", "", "", "", ""]}
    power_widgets.append(power_widget)
    power_tail_widgets.append(power_tail_widget)
    lock_head_widgets.append(lock_head_widget)
    lock_widgets.append(lock_widget)
    lock_tail_widgets.append(lock_tail_widget)
    shut_head_widgets.append(shut_head_widget)
    shut_widgets.append(shut_widget)

# 
def window_to_next_prev_group(qtile, next=True):
    if qtile.currentWindow is None:
        return
    i = qtile.groups.index(qtile.currentGroup)
    i = i+1 if next else i-1
    if i < 0 or i >= len(groups):
        return
    qtile.currentWindow.togroup(qtile.groups[i].name)

def next_prev_group(qtile, next=True):
    i = qtile.groups.index(qtile.currentGroup)
    i = i+1 if next else i-1
    if i < 0 or i >= len(groups):
        return
    qtile.groups[i].cmd_toscreen()

@lazy.function
def float_to_front(qtile):
    """
    Bring all floating windows of the group to front
    """
    for window in qtile.currentGroup.windows:
        if window.floating:
            window.cmd_bring_to_front()

def toggle_text_widgets(widgets=capslock_widgets, options=[" A", ""]):
    for _widget in widgets:
        if not isinstance(_widget, widget.TextBox):
            continue
        _widget.update(options[0] if _widget.text == options[1] else options[1])

# def update_volume_widgets(action=MOUSE_BUTTONS['LEFT_CLICK']):
#     global vol_icon_widgets, vol_widgets
#     for x, y in zip(vol_widgets, vol_icon_widgets):
#         volumePressed(x=0,y=0,mouse_click=action, icon_widget=y, value_widget=x)

keys = [
    # Switch between windows in current stack pane
    Key([MOD], "k", lazy.layout.up()),
    Key([MOD], "j", lazy.layout.down()),
    Key([MOD], "h", lazy.layout.left()),
    Key([MOD], "l", lazy.layout.right()),
    Key([MOD], "Up", lazy.layout.up()),
    Key([MOD], "Down", lazy.layout.down()),
    Key([MOD], "Left", lazy.layout.left()),
    Key([MOD], "Right", lazy.layout.right()),

    # Move windows up or down in current stack
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up()),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down()),
    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(), lazy.layout.swap_left()),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(), lazy.layout.swap_right()),
    Key([MOD, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([MOD, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([MOD, "shift"], "Left", lazy.layout.swap_left(), lazy.layout.shuffle_left()),
    Key([MOD, "shift"], "Right", lazy.layout.swap_right(), lazy.layout.shuffle_right()),

    Key([MOD, "control"], "k", lazy.layout.grow(), lazy.layout.grow_up()),
    Key([MOD, "control"], "j", lazy.layout.shrink(), lazy.layout.grow_down()),
    Key([MOD, "control"], "h", lazy.layout.grow_left()),
    Key([MOD, "control"], "l", lazy.layout.grow_right()),
    Key([MOD, "control"], "Up", lazy.layout.grow(), lazy.layout.grow_up()),
    Key([MOD, "control"], "Down", lazy.layout.shrink(), lazy.layout.grow_down()),
    Key([MOD, "control"], "Left", lazy.layout.grow_left()),
    Key([MOD, "control"], "Right", lazy.layout.grow_right()),

    Key([MOD, "control"], "n", lazy.layout.normalize()),
    Key([MOD, "control"], "m", lazy.layout.maximize()),
    Key([MOD, "shift"], "space", lazy.layout.flip()),


    # Switch window focus to other pane(s) of stack
    Key([MOD], "space", lazy.layout.next()),

    # Swap panes of split stack
    # Key([MOD, "shift"], "space", lazy.layout.rotate()),

    # Toggle floating n fullscreen
    Key([MOD, "shift"], "f", lazy.window.toggle_floating()),
    Key([MOD, "control"], "f", float_to_front),
    Key([MOD], "f", lazy.window.toggle_fullscreen()),


    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([MOD, "shift"], "Return", lazy.layout.toggle_split()),
    Key([MOD], "Return", lazy.spawn(TERMINAL)),
    Key([MOD], "b", lazy.spawn(BROWSER)),

    # Toggle between different layouts
    Key([MOD], "Tab", lazy.next_layout()),

    Key([MOD], "w", lazy.window.kill()),

    Key([], "Caps_Lock", lazy.function(lambda x:toggle_text_widgets(widgets=capslock_widgets, options=[" A", ""]))),
    Key([], "Num_Lock", lazy.function(lambda x:toggle_text_widgets(widgets=numlock_widgets, options=["0", ""]))),

    Key([MOD, "shift", "control"], "Up", lazy.prev_screen()),
    Key([MOD, "shift", "control"], "Down", lazy.next_screen()),
    Key([MOD, "shift", "control"], "Right", lazy.function(lambda x:next_prev_group(x, next=True))),
    Key([MOD, "shift", "control"], "Left", lazy.function(lambda x:next_prev_group(x, next=False))),
    Key([MOD], "u", lazy.next_urgent()),

    # Key([], "XF86AudioMute", lazy.function(lambda x:update_volume_widgets(action=MOUSE_BUTTONS['LEFT_CLICK']))),
    # Key([MOD], "z", lazy.function(lambda x:update_volume_widgets(action=MOUSE_BUTTONS['LEFT_CLICK']))),
    # Key([], "XF86AudioLowerVolume", lazy.function(lambda x:update_volume_widgets(action=MOUSE_BUTTONS['SCROLL_DOWN']))),
    # Key([MOD, ALT], "Down", lazy.function(lambda x:update_volume_widgets(action=MOUSE_BUTTONS['SCROLL_DOWN']))),
    # Key([], "XF86AudioRaiseVolume", lazy.function(lambda x:update_volume_widgets(action=MOUSE_BUTTONS['SCROLL_UP']))),
    # Key([MOD, ALT], "Up", lazy.function(lambda x:update_volume_widgets(action=MOUSE_BUTTONS['SCROLL_UP']))),

    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    Key([MOD], "XF86AudioLowerVolume", lazy.spawn("mpc prev")),
    Key([MOD], "XF86AudioRaiseVolume", lazy.spawn("mpc next")),

    Key([MOD, ALT], "Right", lazy.spawn("mpc next")),
    Key([MOD, ALT], "Left", lazy.spawn("mpc prev")),

    Key([MOD, ALT, "control"], "Right", lazy.function(lambda x:window_to_next_prev_group(x, next=True))),
    Key([MOD, ALT, "control"], "Left", lazy.function(lambda x:window_to_next_prev_group(x, next=False))),

    Key([MOD, "control"], "r", lazy.restart()),
    Key([MOD, "control"], "q", lazy.shutdown()),
    # Key([MOD], "a", lazy.spawn("rofi -show drun -config {}".format(os.path.expanduser('~/.config/rofi/conf')))),
    Key([MOD], 'a', lazy.spawncmd()),
    Key([], "Print", lazy.spawn("gnome-screenshot")),
    Key([MOD], "x", lazy.spawn(os.path.expanduser('~/.config/qtile/lockscreen.sh')))
]

for i in groups:
    if i.name == 'scratchpad':
            keys.extend([
                Key([MOD], "s", lazy.group['scratchpad'].dropdown_toggle('term')),
                Key([MOD, "shift"], "s", lazy.window.togroup("scratchpad")),
                Key([MOD], "c", lazy.group['scratchpad'].dropdown_toggle('calc'))
            ])
    else:
        keys.extend([
            # MOD1 + letter of group = switch to group
            Key([MOD], i.name, lazy.group[i.name].toscreen()),
            # MOD1 + shift + letter of group = switch to & move focused window to group
            Key([MOD, "shift"], i.name, lazy.window.togroup(i.name)),
        ])

layout_configs={
    "margin":10,
    "border_width":3,
    "border_focus":COLR_TITLE_BG,
    "border_normal":COLR_TEXT
}

layouts = [
    layout.Columns(**layout_configs),
    layout.MonadTall(**layout_configs, ratio=0.65),
    layout.MonadWide(**layout_configs, ratio=0.65),
    layout.TreeTab(**layout_configs, active_bg=COLR_TITLE_BG, inactive_bg=COLR_INACTIVE,
        active_fg=COLR_TEXT, inactive_fg=COLR_BODY_BG, bg_color=COLR_BAR_BG,
        padding_left=2, panel_width=100, font=default_font['font'], sections=['Sections'] ),
    layout.Max(),
]

extension_defaults = default_font.copy()

def getGroupBoxWidgets(border_text_l, border_text_r,active_fg, active_bg,
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
                active_fg=active_fg, active_bg=active_bg,not_empty_fg=not_empty_fg, not_empty_bg=not_empty_bg,
                inactive_fg=inactive_fg, inactive_bg=inactive_bg,
                urgent_fg=urgent_fg, urgent_bg=urgent_bg, **icon_font),
            GroupTextBox(track_group=g.name, label=border_text_r, center_aligned=True, borderwidth=0,
                active_fg=active_bg, active_bg=COLR_BAR_BG,not_empty_fg=not_empty_bg, not_empty_bg=COLR_BAR_BG,
                inactive_fg=inactive_bg, inactive_bg=COLR_BAR_BG,
                urgent_fg=urgent_bg, urgent_bg=COLR_BAR_BG, **border_font),
        ]
    return w

def getWidgets(screen=0):
    widgets = [
        # Group box
        widget.CurrentLayoutIcon(background=COLR_TITLE_BG, scale=0.6, foreground=COLR_INACTIVE),
        widget.TextBox(
            **border_font,background=COLR_BAR_BG,
            text="", foreground=COLR_TITLE_BG,
        )
    ]

    widgets += getGroupBoxWidgets(border_text_l="", border_text_r="", active_fg=COLR_TEXT, active_bg=COLR_TITLE_BG,
        inactive_fg=COLR_TEXT, inactive_bg=COLR_INACTIVE, urgent_fg=COLR_TEXT, urgent_bg=COLR_TITLE_BG,
        not_empty_fg=COLR_TEXT, not_empty_bg=COLR_BODY_BG)

    widgets += [
        # Music
        widget.TextBox(
            **border_font,
            text="", foreground=COLR_TITLE_BG,
        ),
        widget.TextBox(
            **icon_font,
            foreground=COLR_TEXT, background=COLR_TITLE_BG, text="",
        ),
        widget.TextBox(
            **border_font,
            foreground=COLR_TITLE_BG, text="",  background=COLR_BODY_BG
        ),
        FuncWithClick(func=getMpd, click_func=clickMpd, update_interval=2.0,
            **default_font, foreground=COLR_TEXT, background=COLR_BODY_BG),
        widget.TextBox(
            **border_font,
            text="", foreground=COLR_BODY_BG,
        ),

        widget.Spacer(length=370),

        # time
        widget.TextBox(**border_font,foreground=COLR_TITLE_BG, text=""),
        widget.TextBox(**icon_font, background=COLR_TITLE_BG, text="",foreground=COLR_TEXT),
        widget.TextBox(**border_font,foreground=COLR_TITLE_BG, text="", background=COLR_BODY_BG),
        widget.Clock(format='%b %d, %A, %I:%M %p',**default_font,
            foreground=COLR_TEXT, background=COLR_BODY_BG),
        widget.TextBox(**border_font,foreground=COLR_BODY_BG, text=""),
        widget.TextBox(**border_font,foreground=COLR_BODY_BG, text=""),
        widget.Clock(format='%I:%M %p', timezone='Asia/Kolkata',
            **default_font,
            foreground=COLR_TEXT, background=COLR_BODY_BG),
        widget.TextBox(
            **border_font,
            foreground=COLR_BODY_BG, text=""),

        widget.TextBox(**border_font,foreground=COLR_TITLE_BG, text=""),
        widget.Prompt(**default_font, foreground=COLR_TEXT, background=COLR_TITLE_BG, prompt=" "),
        widget.TextBox(**border_font,foreground=COLR_TITLE_BG, text=""),
        widget.Spacer(),

        widget.Systray(),

        # Caps & Num Lock
        widget.TextBox(text="" ,**border_font,  foreground=COLR_TITLE_BG, background=None),
        widget.TextBox(text="", **icon_font, foreground=COLR_TEXT, background=COLR_TITLE_BG),
        widget.TextBox(text="" , **border_font, foreground=COLR_TITLE_BG, background=COLR_BODY_BG),
        numlock_widgets[screen],
        capslock_widgets[screen],
        widget.TextBox(text="", **border_font, foreground=COLR_BODY_BG, background=None),

        # Temperature
        widget.TextBox(
            **border_font,
            foreground=COLR_TITLE_BG, text=""),
        widget.TextBox(
            **icon_font,
            foreground=COLR_TEXT, background=COLR_TITLE_BG, text=""),
        widget.TextBox(
            **border_font,
            foreground=COLR_TITLE_BG, text="", background=COLR_BODY_BG),
        FuncWithClick(func=getTemps, update_interval=5.0, **default_font,
            foreground=COLR_TEXT, background=COLR_BODY_BG),
        widget.TextBox(
            **border_font,
            foreground=COLR_BODY_BG, text="", background=None),

        # Utilization
        widget.TextBox(
            **border_font,
            foreground=COLR_TITLE_BG, text=""),
        widget.TextBox(
            **icon_font,
            foreground=COLR_TEXT, background=COLR_TITLE_BG, text=""),
        widget.TextBox(
            **border_font,
            foreground=COLR_TITLE_BG, text="", background=COLR_BODY_BG),
        FuncWithClick(func=getUtilization, update_interval=3.0,
            background=COLR_BODY_BG, foreground=COLR_TEXT, **default_font),

        widget.TextBox(
            **border_font,
            foreground=COLR_BODY_BG, text="", background=None),

        # Volume
        # FuncWithClick(func=lambda: "", click_func=volumePressed,
        #     click_func_args={'icon_widget':vol_icon_widget, 'value_widget':vol_widget},
        #     foreground=COLR_TITLE_BG, update_interval=1000, **border_font),
        # vol_icon_widgets[screen],
        # FuncWithClick(func=lambda: "", click_func=volumePressed,
        #     click_func_args={'icon_widget':vol_icon_widget, 'value_widget':vol_widget},
        #     foreground=COLR_TITLE_BG, background=COLR_BODY_BG, update_interval=1000,
        #     **border_font),
        # vol_widgets[screen],
        # FuncWithClick(func=lambda: "", click_func=volumePressed,
        #     click_func_args={'icon_widget':vol_icon_widget, 'value_widget':vol_widget},
        #     foreground=COLR_BODY_BG, update_interval=1000, **border_font),
        # wifi
        # wifi_icon_head_widgets[screen], wifi_icon_widgets[screen], wifi_icon_tail_widgets[screen],
        # wifi_widgets[screen], wifi_tail_widgets[screen],
    ]
    widgets += vol_widgets[screen].getWidgets()
    widgets += wifi_widgets[screen].getWidgets()
    widgets += [
        # power
        widget.TextBox(**border_font,foreground=COLR_TITLE_BG, text=""),
        power_widgets[screen], power_tail_widgets[screen],
        lock_head_widgets[screen], lock_widgets[screen], lock_tail_widgets[screen],
        shut_head_widgets[screen], shut_widgets[screen]
    ]
    return widgets

screens = []
for n in range(NUM_SCREENS):
    screens.append(
        Screen(
            top=bar.Bar(
                widgets=getWidgets(n),
                size=border_font['fontsize'] - 1,
                background=COLR_BAR_BG, opacity=0.9
            )
        )
    )

# Drag floating layouts.
mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules: List = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    ],
    border_width=2,
    border_focus=COLR_TITLE_BG,
    border_normal=COLR_INACTIVE
)
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# apps to groups
# @hook.subscribe.client_new
# def assignGroup(c):
#     with open('/home/job/.qlog', 'a') as f:
#         f.write("test {}, {}, {}\n".format(c.name, c.wm_instance_class, c.wm_class))
#     if c.wm_class == "Code":
#         c.togroup("3")
#     if c.wm_instance_class == "ranger_inst":
#         c.togroup("4")
#     if c.wm_instance_class == "ncmpcpp_inst":
#         c.togroup("5")

@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()

# Autostart
@hook.subscribe.startup_once
def startOnce():
    start = os.path.expanduser('~/.config/qtile/autostart_once.sh')
    subprocess.call([start])

@hook.subscribe.startup
def start():
    start = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([start])


