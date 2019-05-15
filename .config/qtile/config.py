

import os
import subprocess
from typing import List

from libqtile import bar, layout, widget, hook
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen, Match

from my_scripts import getWlan, getVolumeIcon, getVolume, clickVolume
from my_scripts import FuncWithClick, GroupTextBox, getMpd, clickMpd
from my_scripts import getCapsNumLocks, getTemps, getUtilization
from my_scripts import toggleMuteVolume, changeVolume, CTextBox
from my_scripts import locksPressed

MOD = "mod4"
ALT = "mod1"
TERMINAL = "urxvt"
BROWSER = "firefox"
COLOR_ACT = '791c1c'
COLOR_ACC = 'a34a20'
COLOR_INA = '441500'
COLOR_TXT = '110808'
COLOR_BG = '0d0b0b'

widget_defaults = dict(
    font="Iosevka Nerd Font Medium Oblique",
    fontsize=15,
    padding=0
)
widget_border_defaults = dict(
    font="Iosevka Nerd Font Mono Medium",
    fontsize=20,
    padding=0
)

s = widget.TextBox(font="Iosevka Nerd Font Mono Medium",fontsize=20,
    padding=0, foreground=COLOR_ACC, text="S", background=COLOR_ACT)

capslock_header = widget.TextBox(text="", **widget_border_defaults, foreground=COLOR_ACT)
capslock_text = widget.TextBox(text="", **widget_defaults, foreground=COLOR_TXT,
    background=COLOR_ACT)
capslock_footer = widget.TextBox(text="", **widget_border_defaults, foreground=COLOR_ACT)

numlock_header = widget.TextBox(text="", **widget_border_defaults, foreground=COLOR_ACT)
numlock_text = widget.TextBox(text="", **widget_defaults, foreground=COLOR_TXT,
    background=COLOR_ACT)
numlock_footer = widget.TextBox(text="", **widget_border_defaults, foreground=COLOR_ACT)


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

    Key([MOD], "Caps_Lock", lazy.function(lambda x:locksPressed(
                                                    widgets=[capslock_header,
                                                    capslock_text, capslock_footer],
                                                    ontexts=["", "A ", ""],
                                                    offtexts="1", numlock=False))),

    Key([MOD], "Num_Lock", lazy.function(lambda x:locksPressed([numlock_header,
                                                    numlock_text, numlock_footer],
                                                    ontexts=["", "1 ", ""],
                                                    offtexts="1", numlock=True))),

    Key([], "XF86AudioMute", lazy.function(lambda x:toggleMuteVolume())),
    Key([MOD, ALT], "Left", lazy.function(lambda x:toggleMuteVolume())),
    Key([], "XF86AudioLowerVolume", lazy.function(lambda x:changeVolume('-5%'))),
    Key([MOD, ALT], "Down", lazy.function(lambda x:changeVolume('-5%'))),
    Key([], "XF86AudioRaiseVolume", lazy.function(lambda x:changeVolume('+5%'))),
    Key([MOD, ALT], "XF86AudioRaiseVolume", lazy.function(lambda x:changeVolume('+5%'))),

    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    Key([MOD], "XF86AudioLowerVolume", lazy.spawn("mpc prev")),
    Key([MOD], "XF86AudioRaiseVolume", lazy.spawn("mpc next")),

    Key([MOD, "control"], "r", lazy.restart()),
    Key([MOD, "control"], "q", lazy.shutdown()),
    Key([MOD], "a", lazy.spawn("rofi -show drun -config /home/job/.config/rofi/conf")),
    Key([], "Print", lazy.spawn("gnome-screenshot"))
]

groups = [
    Group(name='1', label="1 "),
    Group(name='2', label="2 "),
    Group(name='3', label="3 ", matches=[Match(wm_class=["Code"])] ),
    Group(name='4', label="4 ", matches=[Match(wm_instance_class=["ranger"])],
        init=True, spawn="urxvt -name ranger -e ranger"),
    Group(name='5', label="5 ", matches=[Match(wm_instance_class=["ncmpcpp"])],
        init=True, spawn="urxvt -name ncmpcpp -e ncmpcpp -s visualizer"),
    Group(name='6', label="6 "),
    Group(name='7', label="7 ")
]

for i in groups:
    keys.extend([
        # MOD1 + letter of group = switch to group
        Key([MOD], i.name, lazy.group[i.name].toscreen()),

        # MOD1 + shift + letter of group = switch to & move focused window to group
        Key([MOD, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

configs={
    "margin":10
}

layouts = [
    layout.Columns(**configs),
    layout.MonadTall(**configs, ratio=0.6),
    layout.MonadWide(**configs, ratio=0.6),
    layout.Zoomy(**configs),
    layout.Max(),
    layout.Stack(**configs)
]

extension_defaults = widget_defaults.copy()

def getGroupBoxWidgets(border_text_l, border_text_r,active_fg, active_bg,
    inactive_fg, inactive_bg, urgent_fg, urgent_bg, not_empty_fg, not_empty_bg):
    w = []
    for g in groups:
        w += [
            GroupTextBox(track_group=g.name, label=border_text_l, center_aligned=True, borderwidth=0,
                active_fg=active_bg, active_bg=COLOR_BG, not_empty_fg=inactive_bg, not_empty_bg=COLOR_BG,
                inactive_fg=inactive_bg, inactive_bg=COLOR_BG,
                urgent_fg=urgent_bg, urgent_bg=COLOR_BG, **widget_border_defaults),
            GroupTextBox(track_group=g.name, label=g.label, center_aligned=True, borderwidth=0,
                active_fg=active_fg, active_bg=active_bg,not_empty_fg=not_empty_fg, not_empty_bg=not_empty_bg,
                inactive_fg=inactive_fg, inactive_bg=inactive_bg,
                urgent_fg=urgent_fg, urgent_bg=urgent_bg, **widget_defaults),
            GroupTextBox(track_group=g.name, label=border_text_r, center_aligned=True, borderwidth=0,
                active_fg=active_bg, active_bg=COLOR_BG,not_empty_fg=inactive_bg, not_empty_bg=COLOR_BG,
                inactive_fg=inactive_bg, inactive_bg=COLOR_BG,
                urgent_fg=urgent_bg, urgent_bg=COLOR_BG, **widget_border_defaults),
        ]
    return w

def getWidgets():
    widgets = [
        # Group box
        widget.CurrentLayoutIcon(background=COLOR_ACT, scale=0.6, foreground=COLOR_INA),
        widget.TextBox(
            **widget_border_defaults,background=COLOR_BG,
            text="", foreground=COLOR_ACT,
        )
    ]

    widgets += getGroupBoxWidgets(border_text_l="", border_text_r="", active_fg=COLOR_TXT, active_bg=COLOR_ACC,
        inactive_fg=COLOR_INA, inactive_bg=COLOR_TXT, urgent_fg=COLOR_TXT, urgent_bg=COLOR_ACT,
        not_empty_fg=COLOR_ACC, not_empty_bg=COLOR_TXT)

    widgets += [
        # Music
        widget.TextBox(
            **widget_border_defaults,
            text="", foreground=COLOR_ACT,
        ),
        widget.TextBox(
            **widget_defaults,
            foreground=COLOR_TXT, background=COLOR_ACT, text="",
        ),
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACT, text="",  background=COLOR_ACC
        ),
        FuncWithClick(func=getMpd, click_func=clickMpd, update_interval=2.0,
            **widget_defaults, foreground=COLOR_TXT, background=COLOR_ACC),
        widget.TextBox(
            **widget_border_defaults,
            text="", foreground=COLOR_ACC,
        ),

        widget.Spacer(length=400),

        # time
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACT, text=""),
        widget.TextBox(
            **widget_defaults,
            background=COLOR_ACT, text="",foreground=COLOR_TXT),
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACT, text="", background=COLOR_ACC),
        widget.Clock(format='%b %d, %a, %I:%M %p',
            **widget_defaults,
            foreground=COLOR_TXT, background=COLOR_ACC),
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACC, text=""),
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACC, text=""),
        widget.Clock(format='%I:%M %p ', timezone='Asia/Kolkata',
            **widget_defaults,
            foreground=COLOR_TXT, background=COLOR_ACC),
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACC, text=""),

        widget.Spacer(),

        widget.Systray(),
        # s,

        # Caps & Num Lock
        capslock_header,
        capslock_text,
        capslock_footer,
        numlock_header,
        numlock_text,
        numlock_footer,
        # FuncWithClick(func=lambda:"" if getCapsNumLocks() else "", update_interval=0.5,
        #     **widget_border_defaults, foreground=COLOR_ACT, background=None),

        # FuncWithClick(func=lambda:"" if getCapsNumLocks() else "", update_interval=0.5,
        #     **widget_defaults, foreground=COLOR_TXT, background=COLOR_ACT),

        # FuncWithClick(func=lambda:"" if getCapsNumLocks() else "", update_interval=0.5,
        #     **widget_border_defaults, foreground=COLOR_ACT, background=COLOR_ACC),

        # FuncWithClick(func=getCapsNumLocks, func_args={'num_text': 'Num', 'caps_text': 'Caps'},
        #     update_interval=0.5, **widget_defaults, foreground=COLOR_TXT, background=COLOR_ACC),

        # FuncWithClick(func=lambda:"" if getCapsNumLocks() else "", update_interval=0.5,
        #     **widget_border_defaults, foreground=COLOR_ACC, background=None),

        # Temperature
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACT, text=""),
        widget.TextBox(
            **widget_defaults,
            foreground=COLOR_TXT, background=COLOR_ACT, text=""),
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACT, text="", background=COLOR_ACC),
        FuncWithClick(func=getTemps, update_interval=5.0, **widget_defaults,
            foreground=COLOR_TXT, background=COLOR_ACC),
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACC, text="", background=None),

        # Utilization
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACT, text=""),
        widget.TextBox(
            **widget_defaults,
            foreground=COLOR_TXT, background=COLOR_ACT, text=""),
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACT, text="", background=COLOR_ACC),
        FuncWithClick(func=getUtilization, update_interval=3.0,
            background=COLOR_ACC, foreground=COLOR_TXT, **widget_defaults),

        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACC, text="", background=None),

        # Volume
        FuncWithClick(func=lambda: "", foreground=COLOR_ACT, click_func=clickVolume,
            update_interval=0.5, **widget_border_defaults),
        FuncWithClick(func=getVolumeIcon, click_func=clickVolume, update_interval=0.5,
            **widget_defaults, foreground=COLOR_TXT, background=COLOR_ACT),
        FuncWithClick(func=lambda: "", foreground=COLOR_ACT, background=COLOR_ACC,
            click_func=clickVolume, update_interval=0.5, **widget_border_defaults),
        FuncWithClick(func=getVolume, click_func=clickVolume, update_interval=0.5,
            background=COLOR_ACC, foreground=COLOR_TXT, **widget_defaults),
        FuncWithClick(func=lambda: "", foreground=COLOR_ACC, click_func=clickVolume,
            update_interval=0.5, **widget_border_defaults),

        # wifi
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACT, text=""),
        widget.TextBox(
            **widget_defaults,
            foreground=COLOR_TXT, background=COLOR_ACT, text="", ),
        widget.TextBox(
            **widget_border_defaults,
            foreground=COLOR_ACT, text="", background=COLOR_ACC),
        FuncWithClick(func=getWlan, func_args={'interface':'wlp4s0'}, update_interval=3.0,
            background=COLOR_ACC, foreground=COLOR_TXT, **widget_defaults),
        # widget.TextBox(
        #     **widget_border_defaults,
        #     foreground=COLOR_ACC, text="", background=None)
    ]
    return widgets

screens = [
    Screen(
        top=bar.Bar(
            getWidgets(),
            size=widget_border_defaults['fontsize'] - 1,
            background=COLOR_BG,
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
])
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
def autostart():
    start = os.path.expanduser('~/.config/qtile/autostart_once.sh')
    subprocess.call([start])

@hook.subscribe.startup
def autostart():
    start = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([start])


