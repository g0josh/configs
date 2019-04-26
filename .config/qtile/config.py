import os
import subprocess
from typing import List

from libqtile import bar, layout, widget, hook
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen, Match

MOD = "mod4"
ALT = "mod1"
TERMINAL = "urxvt"
BROWSER = "firefox"
HOME = os.path.expanduser('~')
CONF_DIR = os.path.join(HOME, ".config/qtile/")

COLOR_ACT = '791c1c'
COLOR_ACC = 'a34a20'
COLOR_INA = '441500'
COLOR_TXT = '110808'

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

    # Toggle between different layouts as defined below
    Key([MOD], "Tab", lazy.next_layout()),
    Key([MOD], "w", lazy.window.kill()),
    
    Key([], "XF86AudioMute", lazy.spawn(CONF_DIR+"pulse_mute.sh toggle")),
    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(CONF_DIR+"pulse_vol.sh -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(CONF_DIR+"pulse_vol.sh +5%")),
    Key([MOD], "XF86AudioLowerVolume", lazy.spawn("mpc prev")),
    Key([MOD], "XF86AudioRaiseVolume", lazy.spawn("mpc next")),

    Key([MOD, "control"], "r", lazy.restart()),
    Key([MOD, "control"], "q", lazy.shutdown()),
    Key([MOD], "a", lazy.spawn("rofi -show drun -config /home/job/.config/rofi/conf")),
    Key([], "Print", lazy.spawn("gnome-screenshot"))
]

groups = [
    Group(name='1', label=" 1  "),
    Group(name='2', label=" 2  "),
    Group(name='3', label=" 3  ", matches=[Match(wm_class=["Code"])] ),
    Group(name='4', label=" 4  ", matches=[Match(wm_instance_class=["ranger"])],
        init=True, spawn="urxvt -name ranger -e ranger"),
    Group(name='5', label=" 5  ", matches=[Match(wm_instance_class=["ncmpcpp"])],
        init=True, spawn="urxvt -name ncmpcpp -e ncmpcpp -s visualizer"),
    Group(name='6', label=" 6  "),
    Group(name='7', label=" 7  ")
]

for i in groups:
    keys.extend([
        # MOD1 + letter of group = switch to group
        Key([MOD], i.name, lazy.group[i.name].toscreen()),

        # MOD1 + shift + letter of group = switch to & move focused window to group
        Key([MOD, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

configs={
    'margin':10
}

layouts = [
    layout.Columns(**configs),
    layout.MonadTall(**configs, ratio=0.6),
    layout.MonadWide(**configs, ratio=0.6),
    layout.Zoomy(**configs),
    layout.Max(),
    layout.Stack(**configs)
]

widget_defaults = dict(
    font="Iosevka Nerd Font Medium Oblique" ,
    fontsize=14, 
    padding=0,
)
widget_border_defaults = dict(
    font="Iosevka Nerd Font Medium Oblique" ,
    fontsize=20,
    padding=0,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [# Group box
                widget.TextBox(
                    **widget_border_defaults, background=COLOR_ACT,
                    foreground=COLOR_ACT, text="a"
                ),
                widget.CurrentLayoutIcon(background=COLOR_ACT, scale=0.6, foreground=COLOR_INA),
                widget.TextBox(
                    **widget_border_defaults,background=COLOR_ACC,
                    text="", foreground=COLOR_ACT,
                ),
                widget.GroupBox(active=COLOR_TXT, inactive=COLOR_INA, borderwidth=2, center_aligned=True,
                        foreground=COLOR_INA, background=COLOR_ACC, hide_unused=True,
                        highlight_color=[COLOR_ACT], highlight_method='line', disable_drag=True,
                        invert_mouse_wheel=False, markup=True, rounded=False, 
                        this_current_screen_border=COLOR_ACT, this_screen_border=COLOR_ACC, spacing=2,
                        urgent_alert_method='border', urgent_border=COLOR_INA, urgent_text=COLOR_INA,
                        use_mouse_wheel=True, font='Iosevka Nerd Font', font_size=15),
                widget.TextBox(
                    **widget_border_defaults,
                    text="", foreground=COLOR_ACC,
                ),

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
                widget.jMpd2(status_format='{artist}|{title} - {elapsed}/{duration}',
                    **widget_defaults,
                    background=COLOR_ACC, foreground=COLOR_TXT,
                    no_connection='', update_iterval=1
                ),    
                widget.TextBox(
                    **widget_border_defaults,
                    text="", foreground=COLOR_ACC,
                ),

                widget.Spacer(),
                
                # time
                widget.TextBox(
                    **widget_border_defaults,
                    foreground=COLOR_ACT, text=""),
                widget.TextBox(
                    **widget_defaults,
                    background=COLOR_ACT, text="",foreground=COLOR_TXT),
                widget.TextBox(
                    **widget_border_defaults,
                    foreground=COLOR_ACT, text="", background=COLOR_ACC),
                widget.Clock(format='%a %d-%m %I:%M %p',
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

                widget.Spacer(length=500),

                # Caps & Num Lock
                widget.TextBox(
                    **widget_border_defaults,
                    foreground=COLOR_ACT, text=""),
                widget.TextBox(
                    **widget_defaults,
                    foreground=COLOR_TXT, background=COLOR_ACT, text=""),
                widget.TextBox(
                    **widget_border_defaults,
                    foreground=COLOR_ACT,
                    text="", background=COLOR_ACC),
                widget.CapsNumLockIndicator(**widget_defaults, foreground=COLOR_TXT,
                    background=COLOR_ACC, update_interval=0.3),
                widget.TextBox(
                    **widget_border_defaults,
                    foreground=COLOR_ACC, text="", background=None),

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
                widget.BashCommand("~/.config/polybar/gettemp.sh",
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
                widget.BashCommand("~/.config/polybar/utilization.sh",
                    foreground=COLOR_TXT, background=COLOR_ACC),
                widget.TextBox(
                    **widget_border_defaults,
                    foreground=COLOR_ACC, text="", background=None),

                # Volume
                widget.TextBox(
                    **widget_border_defaults,
                    foreground=COLOR_ACT, text=""),
                widget.TextBox(
                    **widget_defaults,
                    foreground=COLOR_TXT, background=COLOR_ACT, text=""),
                widget.TextBox(
                    **widget_border_defaults,
                    foreground=COLOR_ACT, text="", background=COLOR_ACC),
                widget.jVolume(muted_label='',
                    **widget_defaults,
                    background=COLOR_ACC, foreground=COLOR_TXT),
                widget.TextBox(
                    **widget_border_defaults,
                    foreground=COLOR_ACC, text="", background=None),
                
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
                widget.jWlan(background=COLOR_ACC, foreground=COLOR_TXT,
                    disconnected_message='', interface='wlo1',
                    format='{essid}', **widget_defaults),
                widget.TextBox(
                    **widget_border_defaults,
                    foreground=COLOR_ACC, text="", background=None),

                
                widget.Systray()
            ],
            size=widget_border_defaults['fontsize'] - 2,
            background=(255, 0, 0, 0.0),
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


