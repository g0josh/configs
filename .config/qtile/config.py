#!/usr/bin/python3

import os
import subprocess
from typing import List
import json

from libqtile import layout, hook
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Match, ScratchPad, DropDown
from libqtile.log_utils import logger

from my_scripts import changeVolume, toggleMuteVolume, getInterfaces
from my_scripts import getTheme, startPolybar
from my_scripts import LAYOUT_ICONS

MOD = "mod4"
ALT = "mod1"
TERMINAL = "alacritty"
BROWSER = "firefox"
THEME_PATH = os.path.expanduser("~/.config/themes/current.theme")
THEME = getTheme(THEME_PATH)
POLYBAR_INFO = {}

default_font = dict(
    font="Iosevka Medium Oblique",
    fontsize=14,
    padding=0
)
border_font = dict(
    font="Iosevka Nerd Font Mono",
    fontsize=16,
    padding=0
)

icon_font = dict(
    font="Font Awesome 5 Free Solid",
    fontsize=12,
    padding=0
)

groups = [
    Group(name='1', label="1 "),
    Group(name='2', label="2 "),
    Group(name='3', label="3 ", matches=[Match(wm_class=["code-oss"])], layout="columns" ),
    Group(name='4', label="4 "),
    Group(name='5', label="5 ", init=True, spawn=["franz", "{} -e ranger".format(TERMINAL)], layout="monadwide"),
    # Group(name='6', label="6 ", matches=[Match(wm_class=["Thunderbird"])], init=True, spawn="thunderbird", layout="monadtall"),
    Group(name='6', label="6 "),
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

def window_to_next_prev_group(qtile, next=True):
    if qtile.current_window is None:
        return
    i = qtile.groups.index(qtile.current_group)
    i = i+1 if next else i-1
    if i < 0 or i >= len(groups):
        return
    qtile.current_window.togroup(qtile.groups[i].name)

def next_prev_group(qtile, next=True):
    i = qtile.groups.index(qtile.current_group)
    i = i+1 if next else i-1
    if i < 0 or i >= len(groups):
        return
    qtile.groups[i].cmd_toscreen()

@lazy.function
def float_to_front(qtile):
    """
    Bring all floating windows of the group to front
    """
    global floating_windows
    floating_windows = []
    for window in qtile.current_group.windows:
        if window.floating:
            window.cmd_bring_to_front()
            floating_windows.append(window)
    floating_windows[-1].cmd_focus()

@lazy.function
def polybar_hook(qtile):
    try:
        subprocess.call(['polybar-msg','hook','qtileWs','1'])
    except subprocess.CalledProcessError as e:
        logger.warn(e)
        return

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
    Key([MOD, "control"], "m", lazy.spawn(os.path.expanduser('~/.config/qtile/autostart.sh'))),
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
    Key([MOD], "Tab", lazy.next_layout(), polybar_hook),

    Key([MOD], "q", lazy.window.kill()),

    Key([MOD, "shift", "control"], "Up", lazy.prev_screen(), polybar_hook),
    Key([MOD, "shift", "control"], "Down", lazy.next_screen(), polybar_hook),
    Key([MOD, "shift", "control"], "Right", lazy.function(lambda x:next_prev_group(x, next=True)), polybar_hook),
    Key([MOD, "shift", "control"], "Left", lazy.function(lambda x:next_prev_group(x, next=False)), polybar_hook),
    Key([MOD], "u", lazy.next_urgent(), polybar_hook),

    Key([], "XF86AudioMute", lazy.function(lambda x:toggleMuteVolume())),
    Key([MOD], "z", lazy.function(lambda x:toggleMuteVolume())),
    Key([], "XF86AudioLowerVolume", lazy.function(lambda x:changeVolume('-5%'))),
    Key([MOD, ALT], "Down", lazy.function(lambda x:changeVolume('-5%'))),
    Key([], "XF86AudioRaiseVolume", lazy.function(lambda x:changeVolume('+5%'))),
    Key([MOD, ALT], "Up", lazy.function(lambda x:changeVolume('+5%'))),

    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    Key([MOD], "XF86AudioLowerVolume", lazy.spawn("mpc prev")),
    Key([MOD], "XF86AudioRaiseVolume", lazy.spawn("mpc next")),

    Key([MOD, ALT], "Right", lazy.spawn("mpc next")),
    Key([MOD, ALT], "Left", lazy.spawn("mpc prev")),

    Key([MOD, ALT, "control"], "Right", lazy.function(lambda x:window_to_next_prev_group(x, next=True)), polybar_hook),
    Key([MOD, ALT, "control"], "Left", lazy.function(lambda x:window_to_next_prev_group(x, next=False)), polybar_hook),

    Key([MOD, "control"], "r", lazy.restart()),
    Key([MOD, "shift", "control"], "q", lazy.shutdown()),
    Key([MOD], "a", lazy.spawn("rofi -show drun")),
    # Key([MOD], 'a', lazy.spawncmd()),
    Key([], "Print", lazy.spawn("gnome-screenshot")),
    Key([MOD], "x", lazy.spawn(os.path.expanduser('~/.config/qtile/lockscreen.sh'))),
    
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
            Key([MOD], i.name, lazy.group[i.name].toscreen(), polybar_hook),
            # MOD1 + shift + letter of group = switch to & move focused window to group
            Key([MOD, "shift"], i.name, lazy.window.togroup(i.name), polybar_hook),
        ])

layout_configs={
    "margin":10,
    "border_width":2,
    "border_focus":THEME['focusedwindowborder'],
    "border_normal":THEME['windowborder']
}

layouts = [
    layout.Columns(num_columns=2, **layout_configs),
    layout.MonadTall(**layout_configs, ratio=0.65),
    layout.MonadWide(**layout_configs, ratio=0.65),
    layout.TreeTab(**layout_configs, active_bg=THEME['focusedwindowborder'], inactive_bg=THEME['windowborder'],
        active_fg=THEME['titlefg'], inactive_fg=THEME['bodyfg'], bg_color=THEME['windowborder'],
        padding_left=2, panel_width=100, font=default_font['font'], sections=['Sections'] ),
    layout.Max()
]

extension_defaults = default_font.copy()

#No bar as we are using polybar
screens = []

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
    border_focus=THEME['focusedwindowborder'],
    border_normal=THEME['windowborder']
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

def launch_polybar():
    global POLYBAR_INFO
    POLYBAR_INFO = startPolybar(THEME_PATH)
    for s in POLYBAR_INFO:
        if os.path.exists(POLYBAR_INFO[s]['ws_fifo_path']):
            os.remove(POLYBAR_INFO[s]['ws_fifo_path'])
        os.mkfifo(POLYBAR_INFO[s]['ws_fifo_path'])

@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    start = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([start])
    #launch_polybar()

@hook.subscribe.startup_once
def startOnce():
    start = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([start])
    #launch_polybar()

'''
@hook.subscribe.startup
def start():
    start = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([start])
'''
