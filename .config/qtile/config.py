#!/usr/bin/python3

import os
import subprocess
from typing import List

from libqtile import bar, layout, widget, hook
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen, Match, ScratchPad, DropDown

from my_scripts import getWlan, getVolumeIcon, getVolume, volumePressed
from my_scripts import FuncWithClick, GroupTextBox
from my_scripts import getTemps, getUtilization, getMpd, clickMpd
from my_scripts import getlocksStatus, MOUSE_BUTTONS, POWER_BUTTONS
from my_scripts import showPowerClicked, powerClicked

MOD = "mod4"
ALT = "mod1"
TERMINAL = "urxvt"
BROWSER = "opera"
COLR_TITLE_BG = 'a42f2b'
COLR_BODY_BG = '1c5d87'
COLR_INACTIVE = '15232b'
COLR_TEXT = '110808'
COLR_BAR_BG='090e36'

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

# Volume widgets
vol_icon_widget = FuncWithClick(func=getVolumeIcon, click_func=volumePressed,
        update_interval=1000,foreground=COLR_TEXT, background=COLR_TITLE_BG, **icon_font)
vol_widget = FuncWithClick(func=getVolume, click_func=volumePressed, update_interval=1000,
        background=COLR_BODY_BG, foreground=COLR_TEXT, **default_font)
vol_icon_widget.click_func_args = {'value_widget':vol_widget, 'icon_widget':vol_icon_widget}
vol_widget.click_func_args = {'value_widget':vol_widget, 'icon_widget':vol_icon_widget}

# Lock widgets
caps_lock_widget = widget.TextBox(text="A" if getlocksStatus()['Caps'] else "", **default_font, foreground=COLR_TEXT,
                background=COLR_BODY_BG)
num_lock_widget = widget.TextBox(text=" 0" if getlocksStatus()['Num'] else "", **default_font, foreground=COLR_TEXT,
                background=COLR_BODY_BG)

# power widgets
power_widget = FuncWithClick(func=lambda:" ", click_func=showPowerClicked,
                **icon_font, foreground=COLR_TEXT, background=COLR_TITLE_BG, update_interval=1000)
power_widget_footer = FuncWithClick(func=lambda:"", **border_font, foreground=COLR_TITLE_BG, update_interval=1000)

shut_widget_header = FuncWithClick(func=lambda:"", **border_font, foreground=COLR_TITLE_BG, update_interval=1000)
shut_widget = FuncWithClick(func=lambda:"", click_func=powerClicked, click_func_args={'widget_button':POWER_BUTTONS['SHUT']},
                **icon_font, foreground=COLR_TEXT, background=COLR_TITLE_BG, update_interval=1000)

logout_widget_header = FuncWithClick(func=lambda:"", **border_font, foreground=COLR_TITLE_BG, update_interval=1000)
logout_widget_footer = FuncWithClick(func=lambda:"", **border_font, foreground=COLR_TITLE_BG, update_interval=1000)
logout_widget = FuncWithClick(func=lambda:"", click_func=powerClicked, click_func_args={'widget_button':POWER_BUTTONS['LOGOUT']},
                **icon_font, foreground=COLR_TEXT, background=COLR_TITLE_BG, update_interval=1000)

lock_screen_widget_header = FuncWithClick(func=lambda:"", **border_font, foreground=COLR_TITLE_BG, update_interval=1000)
lock_screen_widget_footer = FuncWithClick(func=lambda:"", **border_font, foreground=COLR_TITLE_BG, update_interval=1000)
lock_screen_widget = FuncWithClick(func=lambda:"", click_func=powerClicked, click_func_args={'widget_button':POWER_BUTTONS['LOCK_SCREEN']},
                **icon_font, foreground=COLR_TEXT, background=COLR_TITLE_BG, update_interval=1000)
power_widget.click_func_args = {'widgets':[power_widget, power_widget_footer,
                                    lock_screen_widget_header, lock_screen_widget, lock_screen_widget_footer,
                                    logout_widget_header,logout_widget,logout_widget_footer,
                                    shut_widget_header, shut_widget],
                                'ontexts':[" ","","","","", "","","",""," "],
                                'offtexts':["","", "","","","","","","",""]}

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
    Key([MOD, "control"], "space", lazy.layout.flip()),


    # Switch window focus to other pane(s) of stack
    Key([MOD], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([MOD, "shift"], "space", lazy.layout.rotate()),

    # Toggle floating
    Key([MOD, "control"], "space", lazy.window.toggle_floating()),

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

    Key([], "Caps_Lock", lazy.function(lambda x:caps_lock_widget.update( "A" if caps_lock_widget.text == "" else "" ))),
    Key([], "Num_Lock", lazy.function(lambda x:num_lock_widget.update( " 0" if num_lock_widget.text == "" else "" ))),

    Key([], "XF86AudioMute", lazy.function(lambda x:volumePressed(x=0,y=0,mouse_click=MOUSE_BUTTONS['LEFT_CLICK'],
                                                     icon_widget=vol_icon_widget, value_widget=vol_widget))),
    Key([MOD, ALT], "Left", lazy.function(lambda x:volumePressed(x=0,y=0,mouse_click=MOUSE_BUTTONS['LEFT_CLICK'],
                                                     icon_widget=vol_icon_widget, value_widget=vol_widget))),

    Key([], "XF86AudioLowerVolume", lazy.function(lambda x:volumePressed(x=0,y=0,mouse_click=MOUSE_BUTTONS['SCROLL_DOWN'],
                                                    icon_widget=vol_icon_widget, value_widget=vol_widget))),
    Key([MOD, ALT], "Down", lazy.function(lambda x:volumePressed(x=0,y=0,mouse_click=MOUSE_BUTTONS['SCROLL_DOWN'],
                                                    icon_widget=vol_icon_widget, value_widget=vol_widget))),

    Key([], "XF86AudioRaiseVolume", lazy.function(lambda x:volumePressed(x=0,y=0,mouse_click=MOUSE_BUTTONS['SCROLL_UP'],
                                                icon_widget=vol_icon_widget, value_widget=vol_widget))),
    Key([MOD, ALT], "Up", lazy.function(lambda x:volumePressed(x=0,y=0,mouse_click=MOUSE_BUTTONS['SCROLL_UP'],
                                                icon_widget=vol_icon_widget, value_widget=vol_widget))),

    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    Key([MOD], "XF86AudioLowerVolume", lazy.spawn("mpc prev")),
    Key([MOD], "XF86AudioRaiseVolume", lazy.spawn("mpc next")),
    Key([MOD, ALT], "Right", lazy.spawn("mpc next")),

    Key([MOD, "control"], "r", lazy.restart()),
    Key([MOD, "control"], "q", lazy.shutdown()),
    # Key([MOD], "a", lazy.spawn("rofi -show drun -config {}".format(os.path.expanduser('~/.config/rofi/conf')))),
    Key([MOD], 'a', lazy.spawncmd()),
    Key([], "Print", lazy.spawn("gnome-screenshot")),
    Key([MOD], "x", lazy.spawn(os.path.expanduser('~/.config/qtile/lockscreen.sh')))
]

groups = [
    Group(name='1', label="1 "),
    Group(name='2', label="2 "),
    Group(name='3', label="3 ", matches=[Match(wm_class=["Code"])], init=True, spawn="code", layout="monadtall" ),
    Group(name='4', label="4 ", init=True, spawn="urxvt -name ranger -e ranger", layout="columns"),
    Group(name='5', label="5 ", init=True, spawn="urxvt -name ncmpcpp -e ncmpcpp -s visualizer", layout="columns"),
    Group(name='6', label="6 "),
    Group(name='7', label="7 "),
    ScratchPad("scratchpad", [
        # define a drop down terminal.
        # it is placed in the upper third of screen by default.
        DropDown("term", TERMINAL,
                x=0.05, y=0.008, width=0.9, height=0.7, opacity=0.9,
                on_focus_lost_hide=True),
        DropDown("calc", "{} -e python".format(TERMINAL),
                x=0.05, y=0.59, width=0.9, height=0.4, opacity=0.9,
                on_focus_lost_hide=True)
        ],
        label="")
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
    layout.Zoomy(**layout_configs),
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

def getWidgets():
    widgets = [
        # Group box
        widget.CurrentLayoutIcon(background=COLR_TITLE_BG, scale=0.6, foreground=COLR_INACTIVE),
        widget.TextBox(
            **border_font,background=COLR_BAR_BG,
            text="", foreground=COLR_TITLE_BG,
        )
    ]

    widgets += getGroupBoxWidgets(border_text_l="", border_text_r="", active_fg=COLR_TEXT, active_bg=COLR_BODY_BG,
        inactive_fg=COLR_TEXT, inactive_bg=COLR_INACTIVE, urgent_fg=COLR_TEXT, urgent_bg=COLR_TITLE_BG,
        not_empty_fg=COLR_BODY_BG, not_empty_bg=COLR_INACTIVE)

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

        widget.Spacer(length=470),

        # time
        widget.TextBox(**border_font,foreground=COLR_TITLE_BG, text=""),
        widget.TextBox(**icon_font,background=COLR_TITLE_BG, text="",foreground=COLR_TEXT),
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
        caps_lock_widget,
        num_lock_widget,
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
        FuncWithClick(func=lambda: "", click_func=volumePressed,
            click_func_args={'icon_widget':vol_icon_widget, 'value_widget':vol_widget},
            foreground=COLR_TITLE_BG, update_interval=1000, **border_font),
        vol_icon_widget,
        FuncWithClick(func=lambda: "", click_func=volumePressed,
            click_func_args={'icon_widget':vol_icon_widget, 'value_widget':vol_widget},
            foreground=COLR_TITLE_BG, background=COLR_BODY_BG, update_interval=1000,
            **border_font),
        vol_widget,
        FuncWithClick(func=lambda: "", click_func=volumePressed,
            click_func_args={'icon_widget':vol_icon_widget, 'value_widget':vol_widget},
            foreground=COLR_BODY_BG, update_interval=1000, **border_font),

        # wifi
        widget.TextBox(**border_font,foreground=COLR_TITLE_BG, text=""),
        widget.TextBox(
            **icon_font,
            foreground=COLR_TEXT, background=COLR_TITLE_BG, text="", ),
        widget.TextBox(
            **border_font,
            foreground=COLR_TITLE_BG, text="", background=COLR_BODY_BG),
        FuncWithClick(func=getWlan, func_args={'interface':'wlo1'}, update_interval=3.0,
            background=COLR_BODY_BG, foreground=COLR_TEXT, **default_font),
        widget.TextBox(**border_font,foreground=COLR_BODY_BG, text=""),

        # power
        widget.TextBox(**border_font,foreground=COLR_TITLE_BG, text=""),
        power_widget, power_widget_footer,
        lock_screen_widget_header, lock_screen_widget, lock_screen_widget_footer,
        logout_widget_header, logout_widget, logout_widget_footer,
        shut_widget_header, shut_widget
    ]
    return widgets

screens = [
    Screen(
        top=bar.Bar(
            getWidgets(),
            size=border_font['fontsize'] - 1,
            background=COLR_BAR_BG,
            opacity=0.9
        ),
    ),
]

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

# Autostart
@hook.subscribe.startup_once
def startOnce():
    start = os.path.expanduser('~/.config/qtile/autostart_once.sh')
    subprocess.call([start])

@hook.subscribe.startup
def start():
    start = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([start])


