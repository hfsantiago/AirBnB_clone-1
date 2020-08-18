#!/usr/bin/python3
"""Fabric file for compress web static"""
from datetime import datetime as dt
from fabric.api import local


def do_pack():
    """Compress web_static"""
    now = dt.now()
    y, m, d = str(now.date()).split('-')
    hr, mn, sc = str(now.time()).split(':')
    sc = sc.split('.')[0]

    dest = 'web_static_{}{}{}{}{}{}.tgz'.format(y, m, d, hr, mn, sc)
    local('mkdir -p versions')

    result = local('tar -cvzf versions/{} web_static'.format(dest))

    return dest if not result.failed else None
