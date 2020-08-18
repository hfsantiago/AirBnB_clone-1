#!/usr/bin/python3
"""Distributes an archive to your web servers, using the function do_deploy"""
from datetime import datetime as dt
from fabric.api import local, env, put, run
import os

env.hosts = ['34.74.57.2', '52.90.165.93']


def do_pack():
    """Compress web_static"""
    now = dt.now()
    y, m, d = str(now.date()).split('-')
    hr, mn, sc = str(now.time()).split(':')
    sc = sc.split('.')[0]

    dest = 'web_static_{}{}{}{}{}{}.tgz'.format(y, m, d, hr, mn, sc)
    local('mkdir -p versions')

    result = local('tar -cvzf versions/{} web_static'.format(dest))

    dest = 'versions/{}'.format(dest)
    return dest if not result.failed else None


def do_deploy(archive_path):
    """Function for deploy"""
    if not os.path.exists(archive_path):
        return False

    data_path = '/data/web_static/releases/'
    tmp = archive_path.split('.')[0]
    name = tmp.split('/')[1]
    dest = data_path + name

    try:
        put(archive_path, '/tmp')
        run('mkdir -p {}'.format(dest))
        run('tar -xzf /tmp/{}.tgz -C {}'.format(name, dest))
        run('rm -f /tmp/{}.tgz'.format(name))
        run('mv {}/web_static/* {}/'.format(dest, dest))
        run('rm -rf {}/web_static'.format(dest))
        run('rm -rf /data/web_static/current'.format(name))
        run('ln -s {} /data/web_static/current'.format(dest))
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to your web servers"""
    path = do_pack()
    print(path)
    if path is None:
        return False

    return do_deploy(path)

deploy()
