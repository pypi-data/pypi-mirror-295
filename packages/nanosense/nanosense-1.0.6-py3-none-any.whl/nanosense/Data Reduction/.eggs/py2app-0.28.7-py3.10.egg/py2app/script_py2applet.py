"""
Create an applet from a Python script.

You can drag in packages, Info.plist files, icons, etc.

It's expected that only one Python script is dragged in.
"""
from __future__ import print_function 

try :
    import imp 
except ImportError :
    from modulegraph import _imp as imp 
import os 
import plistlib 
import pprint 
import shutil 
import sys 
import tempfile 
from distutils .core import setup 

import py2app 
from py2app import build_app 
from py2app .util import copy_tree 

try :
    set 
except NameError :
    from sets import Set as set 

if sys .version_info [0 ]==3 :
    raw_input =input 

HELP_TEXT ="""
usage: py2applet --make-setup [options...] script.py [data files...]
   or: py2applet [options...] script.py [data files...]
   or: py2applet --help
"""

SETUP_TEMPLATE ='''"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = %s
DATA_FILES = %s
OPTIONS = %s

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
'''


def get_option_map ():
    optmap ={}
    for option in build_app .py2app .user_options :
        opt_long ,opt_short =option [:2 ]
        if opt_short :
            optmap ["-"+opt_short ]=opt_long .rstrip ("=")
    return optmap 


def get_cmd_options ():
    options =set ()
    for option in build_app .py2app .user_options :
        opt_long ,opt_short =option [:2 ]
        if opt_long .endswith ("=")and opt_short :
            options .add ("-"+opt_short )
    return options 


def main ():
    if not sys .argv [1 :]:
        print (HELP_TEXT )
        return 

    scripts =[]
    data_files =[]
    packages =[]
    args =[]
    plist ={}
    iconfile =None 
    parsing_options =True 
    next_is_option =False 
    cmd_options =get_cmd_options ()
    is_make_setup =False 
    for fn in sys .argv [1 :]:
        if parsing_options :
            if next_is_option :
                args .append (fn )
                next_is_option =False 
                continue 
            elif fn =="--make-setup":
                is_make_setup =True 
                continue 
            elif fn .startswith ("-"):
                args .append (fn )
                if fn in cmd_options :
                    next_is_option =True 
                continue 
            parsing_options =False 
        if not is_make_setup :
            fn =os .path .abspath (fn )
        if fn .endswith (".py"):
            if scripts :
                data_files .append (fn )
            else :
                scripts .append (fn )
        elif os .path .basename (fn )=="Info.plist":
            with open (fn ,"rb")as fp :
                if hasattr (plistlib ,"load"):
                    plist =plistlib .load (fp )
                else :
                    plist =plistlib .readPlist (fp )
        elif fn .endswith (".icns")and not iconfile :
            iconfile =os .path .abspath (fn )
        elif os .path .isdir (fn ):
            sys .path .insert (0 ,os .path .dirname (fn ))
            try :
                path =imp .find_module (os .path .basename (fn ))[0 ]
            except ImportError :
                path =""
            del sys .path [0 ]
            if os .path .realpath (path )==os .path .realpath (fn ):
                packages .append (os .path .basename (fn ))
            else :
                data_files .append (fn )
        else :
            data_files .append (fn )

    options ={"packages":packages ,"plist":plist ,"iconfile":iconfile }
    for k ,v in list (options .items ()):
        if not v :
            del options [k ]
    if is_make_setup :
        make_setup (args ,scripts ,data_files ,options )
    else :
        build (args ,scripts ,data_files ,options )


def make_setup (args ,scripts ,data_files ,options ):
    optmap =get_option_map ()
    cmd_options =get_cmd_options ()

    while args :
        cmd =args .pop (0 )
        if cmd in cmd_options :
            cmd =optmap [cmd ]
            options [cmd .replace ("-","_")]=args .pop (0 )
        elif "="in cmd :
            cmd ,val =cmd .split ("=",1 )
            options [cmd .lstrip ("-").replace ("-","_")]=val 
        else :
            cmd =optmap .get (cmd ,cmd )
            options [cmd .lstrip ("-").replace ("-","_")]=True 

    if os .path .exists ("setup.py"):
        res =""
        while res .lower ()not in ("y","n"):
            res =raw_input ("Existing setup.py detected, replace? [Y/n] ")
            if not res :
                break 
        if res =="n":
            print ("aborted!")
            return 
    f =open ("setup.py","w")
    tvars =tuple (map (pprint .pformat ,(scripts ,data_files ,options )))
    f .write (SETUP_TEMPLATE %tvars )
    f .flush ()
    f .close ()
    print ("Wrote setup.py")


def build (args ,scripts ,data_files ,options ):
    old_argv =sys .argv 
    sys .argv =[sys .argv [0 ],"py2app"]+args 
    old_path =sys .path 
    path_insert =set ()
    for script in scripts :
        path_insert .add (os .path .dirname (script ))
    sys .path =list (path_insert )+old_path 
    old_dir =os .getcwd ()
    tempdir =tempfile .mkdtemp ()
    os .chdir (tempdir )
    try :
        d =setup (
        app =scripts ,
        data_files =data_files ,
        options ={"py2app":options },
        )
        for target in d .app :
            copy_tree (
            target .appdir ,
            os .path .join (
            os .path .dirname (target .script ),
            os .path .basename (target .appdir ),
            ),
            preserve_symlinks =True ,
            )

    finally :
        os .chdir (old_dir )
        shutil .rmtree (tempdir ,ignore_errors =True )
        sys .argv =old_argv 
        sys .path =old_path 


if __name__ =="__main__":
    main ()
