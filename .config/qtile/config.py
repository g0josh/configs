#!/usr/bin/python3

import os, time
import subprocess
from typing import List

from libqtile import bar, layout, widget, hook
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen, Match, ScratchPad, DropDown
from libqtile.log_utils import logger

from my_scripts import getVolumeIcon, getVolume, volumePressed
from my_widgets import FuncWithClick, GroupTextBox, ComboWidget
from my_scripts import getTemps, getUtilization, getMpd, clickMpd
from my_scripts import getlocksStatus, MOUSE_BUTTONS, POWER_BUTTONS
from my_scripts import powerClicked, getNumScreens, getTime
from my_scripts import getInterfaces, getLan, getWlan, setupMonitors

MOD = "mod4"
ALT = "mod1"
TERMINAL = "urxvt"
BROWSER = "firefox"
COLR_TITLE_BG = 'a42f2b'
COLR_BODY_BG = '1c5d87'
COLR_INACTIVE = '15232b'
COLR_TEXT = '110808'
COLR_BAR_BG = '090e36'

NUM_SCREENS = getNumScreens()

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
    Group(name='1', label="1 ", layout='treetab'),
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

def show_hide_power_widgets(x=0, y=0, button=1, widgets=[]):
    if button != MOUSE_BUTTONS['LEFT_CLICK']:
        return
    for w in widgets:
        if not isinstance(w, ComboWidget):
            logger.warning("Cannot hide {} type widget".format(type(w)))
            continue
        w.show(w.isHidden())

    global power_widgets
    for w in power_widgets:
        if widgets[0].isHidden():
            w.update(title_text=" ")
        else:
            w.update(title_text=" ")

# Create widgets for all screens
vol_widgets = []
capslock_widgets = []
power_widgets = []
lock_widgets = []
shut_widgets = []
wifi_widgets = []
lan_widgets = []
for n in range(NUM_SCREENS):
    vol_widgets.append( ComboWidget(title_poll_func=getVolumeIcon, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
        body_poll_func=getVolume, click_func=volumePressed, poll_interval=None, body_bg=COLR_BODY_BG,
        body_fg=COLR_TEXT, title_font=icon_font['font'],title_font_size=icon_font['fontsize'],
        border_font=border_font['font'],border_font_size=border_font['fontsize'], body_font=default_font['font'],
        body_font_size=default_font['fontsize'], update_after_click=True, inactive_hide=False, update_title=True)
    )

    # Since computers can have multiple net interfaces
    _wifi_widgets = []
    _lan_widgets = []
    for interface in getInterfaces():
        title = (lambda:"") if 'wl' in interface else (lambda:"")
        func = getWlan if 'wl' in interface else getLan
        w_list = _wifi_widgets if 'wl' in interface else _lan_widgets
        w_list.append( ComboWidget(title_poll_func=title, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT, body_poll_func=func,
            body_poll_func_args={'interface':interface}, poll_interval=5, body_bg=COLR_BODY_BG, body_fg=COLR_TEXT,
            title_font=icon_font['font'], title_font_size=icon_font['fontsize'], border_font=border_font['font'],
            border_font_size=border_font['fontsize'], body_font=default_font['font'], body_font_size=default_font['fontsize'])
        )
    wifi_widgets.append(_wifi_widgets)
    lan_widgets.append(_lan_widgets)

    capslock_widgets.append( ComboWidget(title_poll_func=lambda:"", title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
        title_font=icon_font['font'], title_font_size=icon_font['fontsize'], update_title=False, poll_interval=None,
        body_poll_func=getlocksStatus, body_bg=COLR_BODY_BG, body_fg=COLR_TEXT, body_font=default_font['font'],
        body_font_size=default_font['fontsize'],border_font=border_font['font'],border_font_size=border_font['fontsize'])
    )

    lock_widget = ComboWidget(title_poll_func=lambda:"", update_title=False, title_bg=COLR_TITLE_BG,
        title_fg=COLR_TEXT, title_font=icon_font['font'], title_font_size=icon_font['fontsize'],hide=True,
        poll_interval=None, border_font=border_font['font'],border_font_size=border_font['fontsize'],
        click_func=powerClicked, click_func_args={'power_button': POWER_BUTTONS['LOCK_SCREEN']},body_bg=COLR_BAR_BG)
    shut_widget = ComboWidget(title_poll_func=lambda:"", update_title=False, title_bg=COLR_TITLE_BG,
        title_fg=COLR_TEXT, title_font=icon_font['font'], title_font_size=icon_font['fontsize'],hide=True,
        poll_interval=None, border_font=border_font['font'],border_font_size=border_font['fontsize'],
        click_func=powerClicked, click_func_args={'power_button': POWER_BUTTONS['SHUT_DOWN']})
    power_widget = ComboWidget(title_poll_func=lambda:" ", update_title=False, title_bg=COLR_TITLE_BG,
        title_fg=COLR_TEXT, title_font=icon_font['font'], title_font_size=icon_font['fontsize'], tail_text="",
        poll_interval=None, border_font=border_font['font'],border_font_size=border_font['fontsize'],
        click_func=show_hide_power_widgets, click_func_args={'widgets':[lock_widget, shut_widget]},body_bg=COLR_BAR_BG)
    lock_widgets.append(lock_widget)
    shut_widgets.append(shut_widget)
    power_widgets.append(power_widget)

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
    global floating_windows
    floating_windows = []
    for window in qtile.currentGroup.windows:
        if window.floating:
            window.cmd_bring_to_front()
            floating_windows.append(window)
    floating_windows[-1].cmd_focus()

def toggle_lock_widgets(caps=True):
    global capslock_widgets
    for w in capslock_widgets:
        locks = w.text.split()
        to_find = 'A' if caps else '0'
        if to_find in locks:
            locks[locks.index(to_find)] = ""
        else:
            locks.append(to_find)
        w.update(body_text=" ".join(locks).strip())

def update_volume(button):
    global vol_widgets
    volumePressed(x=0, y=0, button=button)
    for w in vol_widgets:
        w.update()

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

    Key([], "Caps_Lock", lazy.function(lambda x:toggle_lock_widgets(caps=True))),
    Key([], "Num_Lock", lazy.function(lambda x:toggle_lock_widgets(caps=False))),

    Key([MOD, "shift", "control"], "Up", lazy.prev_screen()),
    Key([MOD, "shift", "control"], "Down", lazy.next_screen()),
    Key([MOD, "shift", "control"], "Right", lazy.function(lambda x:next_prev_group(x, next=True))),
    Key([MOD, "shift", "control"], "Left", lazy.function(lambda x:next_prev_group(x, next=False))),
    Key([MOD, "shift", "control"], "k", lazy.prev_screen()),
    Key([MOD, "shift", "control"], "j", lazy.next_screen()),
    Key([MOD, "shift", "control"], "l", lazy.function(lambda x:next_prev_group(x, next=True))),
    Key([MOD, "shift", "control"], "h", lazy.function(lambda x:next_prev_group(x, next=False))),
    Key([MOD], "u", lazy.next_urgent()),

    Key([], "XF86AudioMute", lazy.function(lambda x:update_volume(button=MOUSE_BUTTONS['LEFT_CLICK']))),
    Key([MOD], "z", lazy.function(lambda x:update_volume(button=MOUSE_BUTTONS['LEFT_CLICK']))),
    Key([], "XF86AudioLowerVolume", lazy.function(lambda x:update_volume(button=MOUSE_BUTTONS['SCROLL_DOWN']))),
    Key([MOD, ALT], "Down", lazy.function(lambda x:update_volume(button=MOUSE_BUTTONS['SCROLL_DOWN']))),
    Key([MOD, ALT], "j", lazy.function(lambda x:update_volume(button=MOUSE_BUTTONS['SCROLL_DOWN']))),
    Key([], "XF86AudioRaiseVolume", lazy.function(lambda x:update_volume(button=MOUSE_BUTTONS['SCROLL_UP']))),
    Key([MOD, ALT], "Up", lazy.function(lambda x:update_volume(button=MOUSE_BUTTONS['SCROLL_UP']))),
    Key([MOD, ALT], "k", lazy.function(lambda x:update_volume(button=MOUSE_BUTTONS['SCROLL_UP']))),

    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    Key([MOD], "XF86AudioLowerVolume", lazy.spawn("mpc prev")),
    Key([MOD], "XF86AudioRaiseVolume", lazy.spawn("mpc next")),

    Key([MOD, ALT], "Right", lazy.spawn("mpc next")),
    Key([MOD, ALT], "Left", lazy.spawn("mpc prev")),
    Key([MOD, ALT], "l", lazy.spawn("mpc next")),
    Key([MOD, ALT], "h", lazy.spawn("mpc prev")),

    Key([MOD, ALT, "control"], "Right", lazy.function(lambda x:window_to_next_prev_group(x, next=True))),
    Key([MOD, ALT, "control"], "Left", lazy.function(lambda x:window_to_next_prev_group(x, next=False))),
    Key([MOD, ALT, "control"], "l", lazy.function(lambda x:window_to_next_prev_group(x, next=True))),
    Key([MOD, ALT, "control"], "h", lazy.function(lambda x:window_to_next_prev_group(x, next=False))),

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
    # Layout Icon
    widgets = [
        widget.CurrentLayoutIcon(background=COLR_TITLE_BG, scale=0.6, foreground=COLR_INACTIVE),
        widget.TextBox(
            **border_font,background=COLR_BAR_BG,
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
    widgets += ComboWidget(title_poll_func=lambda:"", update_title=False, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
        title_font=icon_font['font'], title_font_size=icon_font['fontsize'],body_poll_func=getTime,poll_interval=30.0,
        body_bg=COLR_BODY_BG, body_fg=COLR_TEXT,body_font=default_font['font'],body_font_size=default_font['fontsize'],
        border_font=border_font['font'], border_font_size=border_font['fontsize'],head_text="", tail_text="",center_text="").getWidgets()
    widgets += ComboWidget(title_poll_func=getTime, title_poll_func_args={'format':'%I:%M %p', 'timezone':'Asia/Kolkata'},
        update_title=True, title_bg=COLR_BODY_BG, title_fg=COLR_TEXT,poll_interval=30.0,
        title_font=default_font['font'], title_font_size=default_font['fontsize'],border_font=border_font['font'],
        border_font_size=border_font['fontsize'],head_text="", tail_text="", body_bg=COLR_BAR_BG).getWidgets()
    # Prompt
    if screen == 0:
        widgets += [
                widget.TextBox(**border_font,foreground=COLR_TITLE_BG, text=""),
                widget.Prompt(**default_font, foreground=COLR_TEXT, background=COLR_TITLE_BG, prompt=" "),
                widget.TextBox(**border_font,foreground=COLR_TITLE_BG, text="")
        ]
    # Systray
    widgets += [widget.Spacer(),widget.Systray()]
    # Caps and Numlock
    widgets += capslock_widgets[screen].getWidgets()
    # Temperature
    widgets += ComboWidget(title_poll_func=lambda:"", update_title=False, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
        title_font=icon_font['font'], title_font_size=icon_font['fontsize'],body_poll_func=getTemps, poll_interval=5.0,
        click_func=getTemps, update_after_click=True,body_bg=COLR_BODY_BG, body_fg=COLR_TEXT,body_font=default_font['font'],
        body_font_size=default_font['fontsize'], border_font=border_font['font'], border_font_size=border_font['fontsize']).getWidgets()
    # Utilization
    widgets += ComboWidget(title_poll_func=lambda:"", update_title=False, title_bg=COLR_TITLE_BG, title_fg=COLR_TEXT,
            title_font=icon_font['font'], title_font_size=icon_font['fontsize'],body_poll_func=getUtilization, poll_interval=5.0,
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
    widgets += shut_widgets[screen].getWidgets() + lock_widgets[screen].getWidgets()
    widgets += power_widgets[screen].getWidgets()

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
bring_front_click = True
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
    setupMonitors()
    qtile.cmd_restart()

@hook.subscribe.startup_once
def startOnce():
    start = os.path.expanduser('~/.config/qtile/autostart_once.sh')
    subprocess.call([start])
    setupMonitors()

@hook.subscribe.startup
def start():
    start = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([start])
