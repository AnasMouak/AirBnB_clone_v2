#!/usr/bin/python3
'''script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack'''

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """generates a tgz archive"""
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.exists("versions"):
        local("mkdir versions")
    local(f"tar -czvf versions/web_static_{time}.tgz web_static")
    if os.path.exists("versions/web_static_{time}.tgz"):
        return "versions/web_static_{time}.tgz"
    else:
        return None
