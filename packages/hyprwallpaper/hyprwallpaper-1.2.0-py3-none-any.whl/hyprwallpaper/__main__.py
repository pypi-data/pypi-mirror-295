#!/usr/bin/env python3
import os
import shutil
import sys
import subprocess

# Initial conditions
confirmed = False

# picture wallpaper function
def picture_wallpaper():
    try:
        chosen_wp = input('\033[94menter the path of the new wallpaper. you can drag and drop from a file manager if you like. write exit if you wish to stop the program\n\033[0m')
        if chosen_wp == 'exit':
            sys.exit('\033[91mprogram successfully stopped\033[0m')

        elif os.path.isfile(chosen_wp):
            want = input('\033[95mare you sure you want ' + chosen_wp + ' to be your wallpaper? \033[1my/n\033[22m\033[0m \n')

            if want == 'y':
                change_picture_wallpaper(chosen_wp)
                confirmed = True
                return chosen_wp
            else:
                sys.exit('\033[91mif you do not want this wallpaper, please restart the program and choose one to your preferring')
    except FileNotFoundError:
    	print('\033[91mfile not found, please try again\033[0m')

# video wallpaper function
def video_wallpaper():
    try:
        chosen_wp = input('\033[94menter the path of the new wallpaper. you can drag and drop from a file manager if you like. write exit if you wish to stop the program\n\033[0m')

        if chosen_wp == 'exit':
                sys.exit('\033[91mprogram successfully stopped\033[0m')

        elif os.path.isfile(chosen_wp):
                want = input('\033[95mare you sure you want ' + chosen_wp + ' to be your wallpaper? \033[1my/n\033[22m\033[0m \n')

                if want == 'y':
                    change_video_wallpaper(chosen_wp)
                    confirmed = True
                else:
                    sys.exit('\033[91mif you do not want this wallpaper, please restart the program and choose one to your preferring')
    except FileNotFoundError:
    	print('\033[91mfile not found, please try again\033[0m')

def change_picture_wallpaper(chosen_image_wallpaper):
    command_for_wallpaper = 'preload = ' + chosen_image_wallpaper + '\nwallpaper = ,' + chosen_image_wallpaper
    home_dir = os.path.expanduser('~')
    hyprpaper_conf_file = os.path.join(home_dir, '.config/hypr/hyprpaper.conf')

    with open(hyprpaper_conf_file,'w') as file:
        file.write(command_for_wallpaper)

    sys.exit(f"\033[92mwallpaper successfully changed to {chosen_image_wallpaper}\033[0m")


def change_video_wallpaper(chosen_video_wallpaper):

    command_for_wallpaper = ['mpvpaper ','-o ' ,'"no-audio --loop " ', 'eDP-1 ', ' ',chosen_video_wallpaper]


    home_dir= os.path.expanduser('~')
    hyprland_conf_file = os.path.join(home_dir,'.config/hypr/hyprland.conf')

    with open(hyprland_conf_file, 'r') as file:
        lines = file.readlines()

    conf_file_code = ''.join(command_for_wallpaper)

    modified = False
    for i,line in enumerate(lines):
        if line.strip().startswith('exec-once = mpvpaper'):
            lines[i] = f'exec-once = {conf_file_code}'
            modified = True
            break
        elif line.strip().startswith('exec-once'):
            lines.insert(i+1 , f'exec-once = {conf_file_code}\n')
            modified = True
            break

    with open(hyprland_conf_file, 'w') as file :
        file.writelines(lines)

    if modified:
        print(f'added new command in {hyprland_conf_file} : {conf_file_code}')
    else:
        print('fail')

    sys.exit(f"\033[92mwallpaper successfully changed to {chosen_video_wallpaper}\033[0m")

while confirmed == False:
    wallpaper_mode = input('do you want a video wallpaper or picture wallpaper? v/p')
    if wallpaper_mode  in ['v','video','Video','V']:
        video_wallpaper()
    elif wallpaper_mode in['p','picture','Picture','P']:
        picture_wallpaper()
    elif wallpaper_mode in ['quit','exit','stop']:
        sys.exit('\033[91mprogram successfully stopped\033[0m')
