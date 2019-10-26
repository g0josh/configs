#!/usr/bin/python

import sys
import os
import yaml

ALACRITTY_CONF_PATH = os.path.expanduser('~/.config/alacritty/alacritty.yml')
NAMES = ["Sea Shells", "Crayon Pony Fish", "Royal",
        "Gooey", "Gotham", "Wryan", "Wild Cherry", "Grape",
        "Spacedust", "Oceanic Next", "Fistank", "One Half Black",
        "Elio", "Dracula", "Cobalt", "Ciapre", "feathers",
        "Pencil Light", "One Light", "Hemisu Light"]
def get_colors(name="Sea Shells"):
    if name == "Sea Shells":
        COLOR_01="#17384c"           # HOST
        COLOR_02="#d15123"           # SYNTAX_STRING
        COLOR_03="#027c9b"           # COMMAND
        COLOR_04="#fca02f"           # COMMAND_COLOR2
        COLOR_05="#1e4950"           # PATH
        COLOR_06="#68d4f1"           # SYNTAX_VAR
        COLOR_07="#50a3b5"           # PROMP
        COLOR_08="#deb88d"           #

        COLOR_09="#434b53"           #
        COLOR_10="#d48678"           # COMMAND_ERROR
        COLOR_11="#628d98"           # EXEC
        COLOR_12="#fdd39f"           #
        COLOR_13="#1bbcdd"           # FOLDER
        COLOR_14="#bbe3ee"           #
        COLOR_15="#87acb4"           #
        COLOR_16="#fee4ce"           #

        BACKGROUND_COLOR="#09141b"   # Background Color
        FOREGROUND_COLOR="#deb88d"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Sea Shells"
    elif name == "feathers":
        COLOR_01= "#011234"
        COLOR_02= "#cf3d38"
        COLOR_03= "#a85a57"
        COLOR_04= "#c85537"
        COLOR_05= "#004588"
        COLOR_06= "#933e3e"
        COLOR_07= "#0b8191"
        COLOR_08= "#707880"
                 
        COLOR_09= "#002459"
        COLOR_10= "#fd6c67"
        COLOR_11= "#fd6c67"
        COLOR_12= "#ef8455"
        COLOR_13= "#29a4c0"
        COLOR_14= "#b76f6f"
        COLOR_15= "#00c6cf"
        COLOR_16= "#c5c8c6"
        BACKGROUND_COLOR="#000212"   # Background Color
        FOREGROUND_COLOR="#fcd7cf"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="feathers"
    elif name == "Cobalt":
        COLOR_01="#000000"           # HOST
        COLOR_02="#ff0000"           # SYNTAX_STRING
        COLOR_03="#38de21"           # COMMAND
        COLOR_04="#ffe50a"           # COMMAND_COLOR2
        COLOR_05="#1460d2"           # PATH
        COLOR_06="#ff005d"           # SYNTAX_VAR
        COLOR_07="#00bbbb"           # PROMP
        COLOR_08="#bbbbbb"           #

        COLOR_09="#555555"           #
        COLOR_10="#f40e17"           # COMMAND_ERROR
        COLOR_11="#3bd01d"           # EXEC
        COLOR_12="#edc809"           #
        COLOR_13="#5555ff"           # FOLDER
        COLOR_14="#ff55ff"           #
        COLOR_15="#6ae3fa"           #
        COLOR_16="#ffffff"           #

        BACKGROUND_COLOR="#132738"   # Background Color
        FOREGROUND_COLOR="#ffffff"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Cobalt 2"
    elif name =="Ciapre":
        COLOR_01="#181818"           # HOST
        COLOR_02="#810009"           # SYNTAX_STRING
        COLOR_03="#48513b"           # COMMAND
        COLOR_04="#cc8b3f"           # COMMAND_COLOR2
        COLOR_05="#576d8c"           # PATH
        COLOR_06="#724d7c"           # SYNTAX_VAR
        COLOR_07="#5c4f4b"           # PROMP
        COLOR_08="#aea47f"           #

        COLOR_09="#555555"           #
        COLOR_10="#ac3835"           # COMMAND_ERROR
        COLOR_11="#a6a75d"           # EXEC
        COLOR_12="#dcdf7c"           #
        COLOR_13="#3097c6"           # FOLDER
        COLOR_14="#d33061"           #
        COLOR_15="#f3dbb2"           #
        COLOR_16="#f4f4f4"           #

        BACKGROUND_COLOR="#191c27"   # Background Color
        FOREGROUND_COLOR="#aea47a"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Ciapre"
    elif name == "Pencil Light":
        COLOR_01="#212121"           # HOST
        COLOR_02="#c30771"           # SYNTAX_STRING
        COLOR_03="#10a778"           # COMMAND
        COLOR_04="#a89c14"           # COMMAND_COLOR2
        COLOR_05="#008ec4"           # PATH
        COLOR_06="#523c79"           # SYNTAX_VAR
        COLOR_07="#20a5ba"           # PROMP
        COLOR_08="#d9d9d9"           #

        COLOR_09="#424242"           #
        COLOR_10="#fb007a"           # COMMAND_ERROR
        COLOR_11="#5fd7af"           # EXEC
        COLOR_12="#f3e430"           #
        COLOR_13="#20bbfc"           # FOLDER
        COLOR_14="#6855de"           #
        COLOR_15="#4fb8cc"           #
        COLOR_16="#f1f1f1"           #

        BACKGROUND_COLOR="#f1f1f1"   # Background Color
        FOREGROUND_COLOR="#424242"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Pencil Light"
    elif name == "One Light":
        COLOR_01="#000000"
        COLOR_02="#DA3E39"
        COLOR_03="#41933E"
        COLOR_04="#855504"
        COLOR_05="#315EEE"
        COLOR_06="#930092"
        COLOR_07="#0E6FAD"
        COLOR_08="#8E8F96"

        COLOR_09="#2A2B32"
        COLOR_10="#DA3E39"
        COLOR_11="#41933E"
        COLOR_12="#855504"
        COLOR_13="#315EEE"
        COLOR_14="#930092"
        COLOR_15="#0E6FAD"
        COLOR_16="#FFFEFE"

        BACKGROUND_COLOR="#F8F8F8"
        FOREGROUND_COLOR="#2A2B32"
        CURSOR_COLOR="#2A2B32"
        PROFILE_NAME="One Light"
    elif name == "Hemisu Light":
        COLOR_01="#777777"
        COLOR_02="#FF0055"
        COLOR_03="#739100"
        COLOR_04="#503D15"
        COLOR_05="#538091"
        COLOR_06="#5B345E"
        COLOR_07="#538091"
        COLOR_08="#999999"

        COLOR_09="#999999"
        COLOR_10="#D65E76"
        COLOR_11="#9CC700"
        COLOR_12="#947555"
        COLOR_13="#9DB3CD"
        COLOR_14="#A184A4"
        COLOR_15="#85B2AA"
        COLOR_16="#BABABA"

        BACKGROUND_COLOR="#EFEFEF"
        FOREGROUND_COLOR="#444444"
        CURSOR_COLOR="#FF0054"
        PROFILE_NAME="Hemisu Light"
    elif name  == "One Half Black":
        COLOR_01="#282c34"           # HOST
        COLOR_02="#e06c75"           # SYNTAX_STRING
        COLOR_03="#98c379"           # COMMAND
        COLOR_04="#e5c07b"           # COMMAND_COLOR2
        COLOR_05="#61afef"           # PATH
        COLOR_06="#c678dd"           # SYNTAX_VAR
        COLOR_07="#56b6c2"           # PROMP
        COLOR_08="#dcdfe4"           #

        COLOR_09="#282c34"           #
        COLOR_10="#e06c75"           # COMMAND_ERROR
        COLOR_11="#98c379"           # EXEC
        COLOR_12="#e5c07b"           #
        COLOR_13="#61afef"           # FOLDER
        COLOR_14="#c678dd"           #
        COLOR_15="#56b6c2"           #
        COLOR_16="#dcdfe4"           #

        BACKGROUND_COLOR="#000000"   # Background Color
        FOREGROUND_COLOR="#dcdfe4"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="One Half Black"
    elif name == "Crayon Pony Fish":
        COLOR_01="#2b1b1d"           # HOST
        COLOR_02="#91002b"           # SYNTAX_STRING
        COLOR_03="#579524"           # COMMAND
        COLOR_04="#ab311b"           # COMMAND_COLOR2
        COLOR_05="#8c87b0"           # PATH
        COLOR_06="#692f50"           # SYNTAX_VAR
        COLOR_07="#e8a866"           # PROMP
        COLOR_08="#68525a"           #

        COLOR_09="#3d2b2e"           #
        COLOR_10="#c5255d"           # COMMAND_ERROR
        COLOR_11="#8dff57"           # EXEC
        COLOR_12="#c8381d"           #
        COLOR_13="#cfc9ff"           # FOLDER
        COLOR_14="#fc6cba"           #
        COLOR_15="#ffceaf"           #
        COLOR_16="#b0949d"           #

        BACKGROUND_COLOR="#150707"   # Background Color
        FOREGROUND_COLOR="#68525a"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Crayon Pony Fish"
    elif name == "Gooey":
        COLOR_01="#000009"           # Black
        COLOR_02="#BB4F6C"           # Red
        COLOR_03="#72CCAE"           # Green
        COLOR_04="#C65E3D"           # Yellow
        COLOR_05="#58B6CA"           # Blue
        COLOR_06="#6488C4"           # Cyan
        COLOR_07="#8D84C6"           # Magenta
        COLOR_08="#858893"           # Light gray

        COLOR_09="#1f222d"           # Dark gray
        COLOR_10="#ee829f"           # Light Red
        COLOR_11="#a5ffe1"           # Light Green
        COLOR_12="#f99170"           # Light Yellow
        COLOR_13="#8be9fd"           # Light Blue
        COLOR_14="#97bbf7"           # Light Cyan
        COLOR_15="#c0b7f9"           # Light Magenta
        COLOR_16="#ffffff"           # White

        BACKGROUND_COLOR="#0D101B"   # Background Color
        FOREGROUND_COLOR="#EBEEF9"   # Foreground Color (text)
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor color
        PROFILE_NAME="gooey"
    elif name == "Gotham":
        COLOR_01="#0a0f14" # Base 00 - Black
        COLOR_02="#c33027" # Base 08 - Red
        COLOR_03="#26a98b" # Base 0B - Green
        COLOR_04="#edb54b" # Base 0A - Yellow
        COLOR_05="#195465" # Base 0D - Blue
        COLOR_06="#4e5165" # Base 0E - Magenta
        COLOR_07="#33859d" # Base 0C - Cyan
        COLOR_08="#98d1ce" # Base 05 - White

        COLOR_09="#10151b" # Base 03 - Bright Black
        COLOR_10="#d26939" # Base 08 - Bright Red
        COLOR_11="#081f2d" # Base 0B - Bright Green
        COLOR_12="#245361" # Base 0A - Bright Yellow
        COLOR_13="#093748" # Base 0D - Bright Blue
        COLOR_14="#888ba5" # Base 0E - Bright Magenta
        COLOR_15="#599caa" # Base 0C - Bright Cyan
        COLOR_16="#d3ebe9" # Base 07 - Bright White

        FOREGROUND_COLOR="#98d1ce" # Base 05
        BACKGROUND_COLOR="#0a0f14" # Base 00
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="gotham"
    elif name == "Lavandula":
        COLOR_01="#230046"           # HOST
        COLOR_02="#7d1625"           # SYNTAX_STRING
        COLOR_03="#337e6f"           # COMMAND
        COLOR_04="#7f6f49"           # COMMAND_COLOR2
        COLOR_05="#4f4a7f"           # PATH
        COLOR_06="#5a3f7f"           # SYNTAX_VAR
        COLOR_07="#58777f"           # PROMP
        COLOR_08="#736e7d"           #

        COLOR_09="#372d46"           #
        COLOR_10="#e05167"           # COMMAND_ERROR
        COLOR_11="#52e0c4"           # EXEC
        COLOR_12="#e0c386"           #
        COLOR_13="#8e87e0"           # FOLDER
        COLOR_14="#a776e0"           #
        COLOR_15="#9ad4e0"           #
        COLOR_16="#8c91fa"           #

        BACKGROUND_COLOR="#050014"   # Background Color
        FOREGROUND_COLOR="#736e7d"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Lavandula"
    elif name == "Wryan":
        COLOR_01="#333333"           # HOST
        COLOR_02="#8c4665"           # SYNTAX_STRING
        COLOR_03="#287373"           # COMMAND
        COLOR_04="#7c7c99"           # COMMAND_COLOR2
        COLOR_05="#395573"           # PATH
        COLOR_06="#5e468c"           # SYNTAX_VAR
        COLOR_07="#31658c"           # PROMP
        COLOR_08="#899ca1"           #

        COLOR_09="#3d3d3d"           #
        COLOR_10="#bf4d80"           # COMMAND_ERROR
        COLOR_11="#53a6a6"           # EXEC
        COLOR_12="#9e9ecb"           #
        COLOR_13="#477ab3"           # FOLDER
        COLOR_14="#7e62b3"           #
        COLOR_15="#6096bf"           #
        COLOR_16="#c0c0c0"           #

        BACKGROUND_COLOR="#101010"   # Background Color
        FOREGROUND_COLOR="#999993"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Wryan"
    elif name == "Royal":
        COLOR_01="#241f2b"           # HOST
        COLOR_02="#91284c"           # SYNTAX_STRING
        COLOR_03="#23801c"           # COMMAND
        COLOR_04="#b49d27"           # COMMAND_COLOR2
        COLOR_05="#6580b0"           # PATH
        COLOR_06="#674d96"           # SYNTAX_VAR
        COLOR_07="#8aaabe"           # PROMP
        COLOR_08="#524966"           #

        COLOR_09="#312d3d"           #
        COLOR_10="#d5356c"           # COMMAND_ERROR
        COLOR_11="#2cd946"           # EXEC
        COLOR_12="#fde83b"           #
        COLOR_13="#90baf9"           # FOLDER
        COLOR_14="#a479e3"           #
        COLOR_15="#acd4eb"           #
        COLOR_16="#9e8cbd"           #

        BACKGROUND_COLOR="#100815"   # Background Color
        FOREGROUND_COLOR="#514968"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Royal"
    elif name == "Wild Cherry":
        COLOR_01="#000507"           # HOST
        COLOR_02="#d94085"           # SYNTAX_STRING
        COLOR_03="#2ab250"           # COMMAND
        COLOR_04="#ffd16f"           # COMMAND_COLOR2
        COLOR_05="#883cdc"           # PATH
        COLOR_06="#ececec"           # SYNTAX_VAR
        COLOR_07="#c1b8b7"           # PROMP
        COLOR_08="#fff8de"           #

        COLOR_09="#009cc9"           #
        COLOR_10="#da6bac"           # COMMAND_ERROR
        COLOR_11="#f4dca5"           # EXEC
        COLOR_12="#eac066"           #
        COLOR_13="#308cba"           # FOLDER
        COLOR_14="#ae636b"           #
        COLOR_15="#ff919d"           #
        COLOR_16="#e4838d"           #

        BACKGROUND_COLOR="#1f1726"   # Background Color
        FOREGROUND_COLOR="#dafaff"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Wild Cherry"
    elif name == "Grape":
        COLOR_01="#2d283f"           # HOST
        COLOR_02="#ed2261"           # SYNTAX_STRING
        COLOR_03="#1fa91b"           # COMMAND
        COLOR_04="#8ddc20"           # COMMAND_COLOR2
        COLOR_05="#487df4"           # PATH
        COLOR_06="#8d35c9"           # SYNTAX_VAR
        COLOR_07="#3bdeed"           # PROMP
        COLOR_08="#9e9ea0"           #

        COLOR_09="#59516a"           #
        COLOR_10="#f0729a"           # COMMAND_ERROR
        COLOR_11="#53aa5e"           # EXEC
        COLOR_12="#b2dc87"           #
        COLOR_13="#a9bcec"           # FOLDER
        COLOR_14="#ad81c2"           #
        COLOR_15="#9de3eb"           #
        COLOR_16="#a288f7"           #

        BACKGROUND_COLOR="#171423"   # Background Color
        FOREGROUND_COLOR="#9f9fa1"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Grape"
    elif name == "Spacedust":
        COLOR_01="#6e5346"           # HOST
        COLOR_02="#e35b00"           # SYNTAX_STRING
        COLOR_03="#5cab96"           # COMMAND
        COLOR_04="#e3cd7b"           # COMMAND_COLOR2
        COLOR_05="#0f548b"           # PATH
        COLOR_06="#e35b00"           # SYNTAX_VAR
        COLOR_07="#06afc7"           # PROMP
        COLOR_08="#f0f1ce"           #

        COLOR_09="#684c31"           #
        COLOR_10="#ff8a3a"           # COMMAND_ERROR
        COLOR_11="#aecab8"           # EXEC
        COLOR_12="#ffc878"           #
        COLOR_13="#67a0ce"           # FOLDER
        COLOR_14="#ff8a3a"           #
        COLOR_15="#83a7b4"           #
        COLOR_16="#fefff1"           #

        BACKGROUND_COLOR="#0a1e24"   # Background Color
        FOREGROUND_COLOR="#ecf0c1"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Spacedust"
    elif name == "Oceanic Next":
        COLOR_01="#121C21"           # HOST
        COLOR_02="#E44754"           # SYNTAX_STRING
        COLOR_03="#89BD82"           # COMMAND
        COLOR_04="#F7BD51"           # COMMAND_COLOR2
        COLOR_05="#5486C0"           # PATH
        COLOR_06="#B77EB8"           # SYNTAX_VAR
        COLOR_07="#50A5A4"           # PROMP
        COLOR_08="#FFFFFF"           #

        COLOR_09="#52606B"           #
        COLOR_10="#E44754"           # COMMAND_ERROR
        COLOR_11="#89BD82"           # EXEC
        COLOR_12="#F7BD51"           #
        COLOR_13="#5486C0"           # FOLDER
        COLOR_14="#B77EB8"           #
        COLOR_15="#50A5A4"           #
        COLOR_16="#FFFFFF"           #

        BACKGROUND_COLOR="#121b21"   # Background Color
        FOREGROUND_COLOR="#b3b8c3"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Oceanic Next"
    elif name == "Fishtank":
        COLOR_01="#03073c"           # HOST
        COLOR_02="#c6004a"           # SYNTAX_STRING
        COLOR_03="#acf157"           # COMMAND
        COLOR_04="#fecd5e"           # COMMAND_COLOR2
        COLOR_05="#525fb8"           # PATH
        COLOR_06="#986f82"           # SYNTAX_VAR
        COLOR_07="#968763"           # PROMP
        COLOR_08="#ecf0fc"           #

        COLOR_09="#6c5b30"           #
        COLOR_10="#da4b8a"           # COMMAND_ERROR
        COLOR_11="#dbffa9"           # EXEC
        COLOR_12="#fee6a9"           #
        COLOR_13="#b2befa"           # FOLDER
        COLOR_14="#fda5cd"           #
        COLOR_15="#a5bd86"           #
        COLOR_16="#f6ffec"           #

        BACKGROUND_COLOR="#232537"   # Background Color
        FOREGROUND_COLOR="#ecf0fe"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Fishtank"
    elif name == "Elio":
        COLOR_01="#303030"           # HOST
        COLOR_02="#e1321a"           # SYNTAX_STRING
        COLOR_03="#6ab017"           # COMMAND
        COLOR_04="#ffc005"           # COMMAND_COLOR2
        COLOR_05="#729FCF"           # PATH
        COLOR_06="#ec0048"           # SYNTAX_VAR
        COLOR_07="#2aa7e7"           # PROMP
        COLOR_08="#f2f2f2"           #

        COLOR_09="#5d5d5d"           #
        COLOR_10="#ff361e"           # COMMAND_ERROR
        COLOR_11="#7bc91f"           # EXEC
        COLOR_12="#ffd00a"           #
        COLOR_13="#0071ff"           # FOLDER
        COLOR_14="#ff1d62"           #
        COLOR_15="#4bb8fd"           #
        COLOR_16="#a020f0"           #

        BACKGROUND_COLOR="#041A3B"   # Background Color
        FOREGROUND_COLOR="#f2f2f2"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Elio"
    elif name == "Dracula":
        COLOR_01="#44475a"           # HOST
        COLOR_02="#ff5555"           # SYNTAX_STRING
        COLOR_03="#50fa7b"           # COMMAND
        COLOR_04="#ffb86c"           # COMMAND_COLOR2
        COLOR_05="#8be9fd"           # PATH
        COLOR_06="#bd93f9"           # SYNTAX_VAR
        COLOR_07="#ff79c6"           # PROMP
        COLOR_08="#94A3A5"           #

        COLOR_09="#000000"           #
        COLOR_10="#ff5555"           # COMMAND_ERROR
        COLOR_11="#50fa7b"           # EXEC
        COLOR_12="#ffb86c"           #
        COLOR_13="#8be9fd"           # FOLDER
        COLOR_14="#bd93f9"           #
        COLOR_15="#ff79c6"           #
        COLOR_16="#ffffff"           #

        BACKGROUND_COLOR="#282a36"   # Background Color
        FOREGROUND_COLOR="#94A3A5"   # Text
        CURSOR_COLOR=FOREGROUND_COLOR # Cursor
        PROFILE_NAME="Dracula"
    else:
        print("Unknown color scheme")
        return False
    colors = dict(
            black = COLOR_01,
            red = COLOR_02,
            green = COLOR_03,
            yellow = COLOR_04,
            blue = COLOR_05,
            magenta = COLOR_06,
            cyan = COLOR_07,
            white = COLOR_08,
            bright_black = COLOR_09,
            bright_red = COLOR_10,
            bright_green = COLOR_11,
            bright_yellow = COLOR_12,
            bright_blue = COLOR_13,
            bright_magenta = COLOR_14,
            bright_cyan = COLOR_15,
            bright_white = COLOR_16,
            background = BACKGROUND_COLOR,
            foreground = FOREGROUND_COLOR,
            cursor = CURSOR_COLOR
            )
    return colors

def main():
    global COLORS
    if len(sys.argv) < 2:
        print("Please enter a theme name")
        sys.exit(1)

    colors = get_colors(sys.argv[1].strip())
    if not colors:
        print("Unknown theme, Acceptable ones are - ", NAMES)
        sys.exit(1)
    with open(ALACRITTY_CONF_PATH, 'r') as fh:
        ala_conf = yaml.safe_load(fh)
    for key in colors:
        if 'ground' in key:
            ala_conf['colors']['primary'][key] = colors[key]
        elif 'bright' in key:
            ala_conf['colors']['bright'][key.split('_')[1]] = colors[key]
        else:
            ala_conf['colors']['normal'][key] = colors[key]
    with open(ALACRITTY_CONF_PATH, 'w') as fh:
        yaml.dump(ala_conf, fh, default_flow_style=False)

if __name__ == '__main__':
    main()

