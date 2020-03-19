#!/usr/bin/python3

import apt
import subprocess
import argparse

PREDEFINED = {
        "python-wxtools" : None,
        "python-rosdep":"python3-rosdep2",
        "python3-rosdep":"python3-rosdep2",
        }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", default=None, help="path to the src folder")
    args = parser.parse_args()
    
    src = args.path if args.path is not None else "src"
    try:
        a = subprocess.check_output(["rosdep","check","--from-paths", src,"--ignore-src"])
    except subprocess.CalledProcessError as e:
        err, deps = e.stderr, e.stdout

    if err is not None:
        print("Error", err.decode())
        exit()
    elif deps is not None:
        print("Dependencies not satisfied")
        deps = deps.decode().split('\n')
        deps = deps[1:]
        cache = apt.cache.Cache()
        cache.update()
        cache.open()
        for dep in deps:
            dep = dep.replace('apt\t', "", 1)
            dep_f = PREDEFINED[dep] if dep in PREDEFINED else dep
            if dep_f in [None, ""]:
                print("-------------- '{}' not installed".format(dep))
                continue
            if 'python3' in dep_f or 'python' not in dep_f:
                print("Installing ", dep)
                cache[dep_f].mark_install()
                continue
            _dep_f = dep_f.replace('python-', 'python3-', 1)
            pkg = cache[_dep_f]
            if pkg.is_installed:
                continue
            confirm = input("Install {} instead of {}? (Y/n)".format(_dep_f, dep_f))
            if confirm in ['n','N']:
                continue
            pkg.mark_install()
        
        try:
            cache.commit()
        except Exception as e:
            print(e)

    print("Nothing to install")
