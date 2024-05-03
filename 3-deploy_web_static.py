#!/usr/bin/python3
'''Fabric script that distributes an archive to web servers, using the function deploy'''                            
from fabric.api import put, run, env
from fabric.api import local
from datetime import datetime
import os
env.hosts = ['100.26.218.180', '35.168.8.95']

def do_pack():
    """generates a tgz archive"""
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.exists("versions"):
        local("mkdir versions")
    archive_path = f"versions/web_static_{time}.tgz"
    local(f"tar -czvf {archive_path} web_static")
    if os.path.exists(archive_path):
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    no_ext_arch_path = archive_path.split("/")[-1].split(".")[0]
    if not os.path.exists(archive_path):
        return False
    put(archive_path, '/tmp/')
    run(f'mkdir -p /data/web_static/releases/{no_ext_arch_path}/')
    run(f'tar -xzf /tmp/{archive_path.split("/")[-1]} -C /data/web_static/releases/{no_ext_arch_path}/')
    run(f'rm /tmp/{archive_path.split("/")[-1]}')
    run(f'mv /data/web_static/releases/{no_ext_arch_path}/web_static/* /data/web_static/releases/{no_ext_arch_path}/')
    run(f'rm -rf /data/web_static/releases/{no_ext_arch_path}/web_static')
    run('rm -rf /data/web_static/current')
    run(f'ln -s /data/web_static/releases/{no_ext_arch_path}/ /data/web_static/current')

def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
