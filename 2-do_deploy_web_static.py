#!/usr/bin/python3
'''Fabric script that distributes an archive to web servers, using the function do_deploy'''

from fabric.api import put, run, env
from datetime import datetime
import os
env.hosts = ['100.26.218.180', '35.168.8.95']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    no_ext_arch_path = archive_path.split("/")[-1].split(".")[0]
    if not os.path.exists(archive_path):
        return False
    put(f'{archive_path}', '/tmp/')
    run(f'mkdir -p /data/web_static/releases/{no_ext_arch_path}')
    run(f'tar -xzf /tmp/{archive_path.split("/")[-1]} -C /data/web_static/releases/{no_ext_arch_path}')
    run(f'rm /tmp/{archive_path.split("/")[-1]}')
    run(f'mv /data/web_static/releases/{no_ext_arch_path}/web_static/* /data/web_static/releases/{no_ext_arch_path}')
    run(f'rm -rf /data/web_static/releases/{no_ext_arch_path}/web_static')
    run('rm -rf /data/web_static/current')
    run(f'ln -s /data/web_static/releases/{no_ext_arch_path} /data/web_static/current')
