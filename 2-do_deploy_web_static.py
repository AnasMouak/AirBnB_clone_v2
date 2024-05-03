#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers.
"""

from fabric.api import put, run, env
from fabric.context_managers import hide
from os.path import exists

env.hosts = ['100.26.218.180', '35.168.8.95']


def do_deploy(archive_path):
    """
    Distribute an archive to web servers.

    Args:
        archive_path (str): The path of the archive to distribute.

    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        with hide('running'):
            put(archive_path, '/tmp/')

        # Get the filename without extension
        filename = archive_path.split('/')[-1].split('.')[0]

        # Uncompress the archive to the releases folder
        with hide('running'):
            run('mkdir -p /data/web_static/releases/{}/'.format(filename))
            run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'.format(
                filename, filename))

        # Remove the archive from the web server
        with hide('running'):
            run('rm /tmp/{}.tgz'.format(filename))

        # Move the contents of the web_static folder one level up
        with hide('running'):
            run('mv /data/web_static/releases/{}/web_static/* '
                '/data/web_static/releases/{}/'.format(filename, filename))
            run('rm -rf /data/web_static/releases/{}/web_static'.format(
                filename))

        # Remove the current symlink
        with hide('running'):
            run('rm -rf /data/web_static/current')

        # Create a new symlink pointing to the new release
        with hide('running'):
            run('ln -s /data/web_static/releases/{}/ '
                '/data/web_static/current'.format(filename))

        print("New version deployed!")
        return True

    except Exception:
        return False
