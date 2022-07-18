import os
import subprocess

from libqtile import bar, layout, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger

from icons import getIcons
from my_scripts import MOUSE_BUTTONS, clickMpd, getTheme, setupMonitors, updateWallpaper, getNumScreens, volumeClicked
from my_bar import DEFAULT_FONT, BORDER_FONT, getWidgets, updateGroupWidgets, updateVolume
from my_audio import setActiveSink

MOD = "mod4"
ALT = "mod1"
TERMINAL = guess_terminal()
BROWSER = "firefox"
ALTBROWSER = "google-chrome-stable"
AUTOSTART_SCRIPT = os.path.expanduser("~/.config/autostart.sh")
THEME = getTheme(os.path.expanduser('~/.config/themes/.theme'))
NUM_SCREENS = getNumScreens()

groups = [
    Group(name='1', label=f'1 {getIcons()["user"]}'),
    Group(name='2', label=f'2 {getIcons()["terminal"]}'),
    Group(name='3', label=f'3 {getIcons()["code"]}'),
    Group(
        name='4', label=f'4 {getIcons()["folder"]}', spawn='nautilus'),
    Group(name='5', label=f'5 {getIcons()["music"]}',
          matches=[Match(title='mpd'), Match(wm_class="music")]),
    Group(name='6', label=f'6 {getIcons()["mail"]}', spawn=['geary', 'gnome-calendar'],
          layout='monadtall', matches=[Match(wm_class=['gnome-calendar', 'geary'])]),
    Group(name='7', label=f'7 {getIcons()["download"]}',
          matches=[Match(wm_class=['Transmission-gtk', 'Uget-gtk'])]),
    Group(name='8', label=f'8 {getIcons()["user"]}'),
    ScratchPad('scratchpad', [
        # define a drop down terminal.
        # it is placed in the upper third of screen by default.
        DropDown('term', TERMINAL,
                 x=0.7, y=0.008, width=0.297, height=0.4, opacity=0.8,
                 on_focus_lost_hide=True),
        DropDown('calc', f'{TERMINAL} -e python3',
                 x=0.7, y=0.008, width=0.297, height=0.4, opacity=0.8,
                 on_focus_lost_hide=True)
    ],
        label='')
]


def window_to_next_prev_group(qtile, next=True):
    if qtile.current_window is None:
        return
    i = qtile.groups.index(qtile.current_group)
    i = i+1 if next else i-1
    if i < 0 or i >= len(groups):
        return
    qtile.current_window.togroup(qtile.groups[i].name)
    updateGroupWidgets(qtile, THEME)


def next_prev_group(qtile, next=True):
    i = qtile.groups.index(qtile.current_group)
    i = i+1 if next else i-1
    if i < 0 or i >= len(groups):
        return
    qtile.groups[i].cmd_toscreen()
    updateWallpaper(qtile)
    updateGroupWidgets(qtile, THEME)

def cycle_audio_sink(qtile, next=True):
    setActiveSink('next' if next else 'prev')
    updateVolume(1, True)


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([MOD], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([MOD], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([MOD], "j", lazy.layout.down(), desc="Move focus down"),
    Key([MOD], "k", lazy.layout.up(), desc="Move focus up"),
    Key([MOD], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([ALT, "shift"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([ALT, "shift"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([ALT, "shift"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([ALT, "shift"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([MOD], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([MOD], "f", lazy.window.toggle_fullscreen(), desc="Toggle window fullscreen"),
    Key([MOD, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle window floating"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multile stack panes
    Key(
        [MOD, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([MOD], "Return", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([MOD], "b", lazy.spawn(BROWSER), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([MOD], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([MOD], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([MOD, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([MOD, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([MOD], "space", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    Key([MOD, ALT, "control"], "Up", lazy.prev_screen(), lazy.function(updateGroupWidgets, THEME)),
    Key([MOD, ALT, "control"], "k", lazy.prev_screen(), lazy.function(updateGroupWidgets, THEME)),
    Key([MOD, ALT, "control"], "h", lazy.prev_screen(), lazy.function(updateGroupWidgets, THEME)),
    Key([MOD, ALT, "control"], "Down", lazy.next_screen(), lazy.function(updateGroupWidgets, THEME)),
    Key([MOD, ALT, "control"], "j", lazy.next_screen(), lazy.function(updateGroupWidgets, THEME)),
    Key([MOD, ALT, "control"], "l", lazy.next_screen(), lazy.function(updateGroupWidgets, THEME)),

    # Move between groups
    Key([MOD, "control"], "Right", lazy.function(
        lambda x:next_prev_group(x, next=True))),
    Key([MOD, "control"], "l", lazy.function(
        lambda x:next_prev_group(x, next=True))),
    Key([MOD, "control"], "j", lazy.function(
        lambda x:next_prev_group(x, next=True))),
    Key([MOD, "control"], "Left", lazy.function(
        lambda x:next_prev_group(x, next=False))),
    Key([MOD, "control"], "h", lazy.function(
        lambda x:next_prev_group(x, next=False))),
    Key([MOD, "control"], "k", lazy.function(
        lambda x:next_prev_group(x, next=False))),
    Key([MOD], "u", lazy.next_urgent(), lazy.function(updateGroupWidgets, THEME)),

    # Move windows between groups
    Key([MOD, "control", "shift"], "Right", lazy.function(
        lambda x:window_to_next_prev_group(x, next=True))),
    Key([MOD, "control", "shift"], "l", lazy.function(
        lambda x:window_to_next_prev_group(x, next=True))),
    Key([MOD, "control", "shift"], "j", lazy.function(
        lambda x:window_to_next_prev_group(x, next=True))),
    Key([MOD, "control", "shift"], "Left", lazy.function(
        lambda x:window_to_next_prev_group(x, next=False))),
    Key([MOD, "control", "shift"], "h", lazy.function(
        lambda x:window_to_next_prev_group(x, next=False))),
    Key([MOD, "control", "shift"], "k", lazy.function(
        lambda x:window_to_next_prev_group(x, next=False))),

    Key([MOD, "control"], "m", lazy.function(setupMonitors)),
    
    # Audio
    Key([MOD, ALT], "k", lazy.function(lambda x: updateVolume(MOUSE_BUTTONS['SCROLL_UP'])), desc="Increase volume of active sink"),
    Key([MOD, ALT], "j", lazy.function(lambda x: updateVolume(MOUSE_BUTTONS['SCROLL_DOWN'])), desc="Decrease volume of active sink"),
    Key([MOD, ALT], "u", lazy.function(cycle_audio_sink), desc="Switch to next audio sink"),
    Key([MOD, ALT], "d", lazy.function(cycle_audio_sink, False), desc="Switch to previous audio sink"),
    Key([MOD, ALT], "Next", lazy.function(cycle_audio_sink), desc="Switch to next audio sink"),
    Key([MOD, ALT], "Prior", lazy.function(cycle_audio_sink, False), desc="Switch to previous audio sink"),

    # Music
    Key([MOD, ALT], "space", lazy.function(lambda x: clickMpd(MOUSE_BUTTONS['LEFT_CLICK'])), desc="Toggle music"),
    Key([MOD, ALT], "h", lazy.function(lambda x: clickMpd(MOUSE_BUTTONS['SCROLL_DOWN'])), desc="Decrease volume of active sink"),
    Key([MOD, ALT], "l", lazy.function(lambda x: clickMpd(MOUSE_BUTTONS['SCROLL_UP'])), desc="Decrease volume of active sink")
]

for i in groups:
    if i.name == 'scratchpad':
        keys.extend([
            Key([MOD], "w", lazy.group['scratchpad'].dropdown_toggle('term')),
            Key([MOD], "c", lazy.group['scratchpad'].dropdown_toggle('calc'))
        ])
    else:
        keys.extend(
            [
                # mod1 + letter of group = switch to group
                Key(
                    [MOD],
                    i.name,
                    lazy.group[i.name].toscreen(), lazy.function(updateWallpaper), lazy.function(updateGroupWidgets, THEME),
                    desc="Switch to group {}".format(i.name),
                ),
                # mod1 + shift + letter of group = switch to & move focused window to group
                Key(
                    [MOD, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True), lazy.function(updateWallpaper), lazy.function(updateGroupWidgets, THEME),
                    desc="Switch to & move focused window to group {}".format(
                        i.name),
                ),
            ]
        )

layout_configs = {
    "margin": 10,
    "border_width": 2,
    "border_focus": THEME['focusedwindowborder'],
    "border_normal": THEME['windowborder']
}

layouts = [
    layout.Columns(num_columns=2, **layout_configs),
    layout.MonadTall(**layout_configs, ratio=0.65),
    layout.MonadWide(**layout_configs, ratio=0.65),
    layout.TreeTab(**layout_configs, active_bg=THEME['focusedwindowborder'], inactive_bg=THEME['windowborder'],
                   active_fg=THEME['titlefg'], inactive_fg=THEME['bodyfg'], bg_color=THEME['windowborder'],
                   padding_left=2, panel_width=100, font=DEFAULT_FONT['font'], sections=['Sections']),
    layout.Max()
]

widget_defaults = dict(
    font=DEFAULT_FONT["font"],
    fontsize=DEFAULT_FONT["fontsize"],
    padding=0,
)
extension_defaults = widget_defaults.copy()

screens = []
for screen in range(NUM_SCREENS):
    screens.append(
        Screen(
              bottom=bar.Bar(
                  widgets=getWidgets(THEME, screen, groups),
                  size=BORDER_FONT['fontsize'] - 1,
                  margin=[THEME['bartopborder'], THEME['barleftborder'], THEME['barbottomborder'], THEME['barrightborder']],
                  background=THEME['background'], opacity=1
              ) if 'bottombar' in THEME and THEME['bottombar'] else None,
              top = bar.Bar(
                  widgets=getWidgets(THEME, screen, groups),
                  size=BORDER_FONT['fontsize'] - 1,
                  margin=[THEME['bartopborder'], THEME['barleftborder'], THEME['barbottomborder'], THEME['barrightborder']],
                  background=THEME['background'], opacity=1
              ) if 'bottombar' not in THEME or not THEME['bottombar'] else None
        )

    )

# Drag floating layouts.
mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    **layout_configs,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# @hook.subscribe.screen_change
@hook.subscribe.startup_once
def restart_on_randr():
    setupMonitors()
    subprocess.run(['bash', AUTOSTART_SCRIPT])


@hook.subscribe.client_killed
@hook.subscribe.client_focus
@hook.subscribe.client_new
def windowDeleted(c):
    if "blurwallpaper" in THEME and THEME["blurwallpaper"]:
        updateWallpaper(c.qtile, -1)
    updateGroupWidgets(c.qtile, THEME)


@hook.subscribe.startup_complete
def refreshWidgets():
    # setupMonitors()
    updateWallpaper(setSolid=True)