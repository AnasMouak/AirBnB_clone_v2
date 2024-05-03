#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers"""
from fabric.api import local, env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['100.26.218.180', '35.168.8.95']

def do_pack():
    """Create a .tgz archive of the web_static folder"""
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = 'versions/web_static_' + now + '.tgz'
    local('mkdir -p versions')
    result = local('tar -cvzf {} web_static'.format(file_name))
    if result.succeeded:
        return file_name
    else:
        return None

def do_deploy(archive_path):
    """Deploy the archive to the web servers"""
    if not exists(archive_path):
        return False
    file_name = archive_path.split('/')[-1]
    folder_name = file_name.replace('.tgz', '')
    put(archive_path, '/tmp/')
    run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
    run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(file_name, folder_name))
    run('rm /tmp/{}'.format(file_name))
    run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(folder_name, folder_name))
    run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_name))
    run('rm -rf /data/web_static/current')
    run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_name))
    return True

def deploy():
    """Deploy the web_static archive"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
