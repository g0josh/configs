/* 
Ubuntu-like Panel
Copyright fthx 2022
License: GPL v3
*/

const Main = imports.ui.main;
const Panel = Main.panel;

function init() {
}

function enable() {
    Panel.add_style_class_name('panel-normal-font');
    Panel.add_style_class_name('panel-transparent-reduced');
}

function disable() {
    Panel.remove_style_class_name('panel-normal-font');
    Panel.remove_style_class_name('panel-transparent-reduced');
}
