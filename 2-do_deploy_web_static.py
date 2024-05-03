#!/usr/bin/python3
'''Fabric script that distributes an archive to web servers, using the function do_deploy'''                            
from fabric.api import put, run, env
from datetime import datetime
from fabric.api import local
import os
env.hosts = ['100.26.218.180', '35.168.8.95']

def do_pack():
    """generates a tgz archive"""
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.exists("versions"):
        local("mkdir versions")
    local(f"tar -czvf versions/web_static_{time}.tgz web_static")
    if os.path.exists(f"versions/web_static_{time}.tgz"):
        return f"versions/web_static_{time}.tgz"
    else:
        return None
    
def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    no_ext_arch_path = archive_path.split("/")[-1].split(".")[0]
    archive_path = do_pack()
    if not os.path.exists(archive_path):
        return False
    put(archive_path, '/tmp/')
    run(f'mkdir -p /data/web_static/releases/{no_ext_arch_path}')
    run(f'tar -xzf /tmp/{archive_path.split("/")[-1]} -C/data/web_static/releases/{no_ext_arch_path}')
    run(f'rm /tmp/{archive_path.split("/")[-1]}')
    run(f'mv /data/web_static/releases/{no_ext_arch_path}/web_static/*/data/web_static/releases/{no_ext_arch_path}')
    run(f'rm -rf /data/web_static/releases/{no_ext_arch_path}/web_static')
    run('rm -rf /data/web_static/current')
    run(f'ln -s /data/web_static/releases/{no_ext_arch_path} /data/web_static/current')
