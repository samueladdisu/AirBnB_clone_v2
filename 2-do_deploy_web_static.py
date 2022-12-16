#!/usr/bin/python3
"""
Generate .tgz files
"""
from os import path
from datetime import datetime as dt
from fabric.api import local, put, run, env
from fabric.context_managers import lcd


env.user = "ubuntu"
env.hosts = ["3.236.145.87", "3.236.223.114"]


def do_pack():
    """ generate .tgz file"""
    archived = dt.utcnow()
    if path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    p = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        archived.year, archived.month, archived.day,
        archived.hour, archived.minute, archived.second)
    if local("tar -cvzf {} web_static/".format(
            p)).failed is True:
        return None
    return p


def do_deploy(archive_path):
    """ Deploy files to servers"""
    print("archive_path")
    if path.isfile("{}".format(archive_path)) is False:
        return False
    result = put("{}".format(
        archive_path), "/tmp/{}".format(
            archive_path.split("/")[1]))
    if result.failed is True:
        return False
    extract_path = archive_path.split("/")[1].split(".")[0]
    if run("rm -rf /data/web_static/releases/{}/".format(
            extract_path)).failed is True:
        return False
    if run(
            "mkdir -p /data/web_static/releases/{}".format(
                extract_path)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(
            archive_path.split("/")[1], extract_path)).failed is True:
        return False
    if run("rm -rf /tmp/{}".format(archive_path.split("/")[1])).failed is True:
        return False
    part1 = "mv /data/web_static/releases/{}/web_static/*".format(extract_path)
    part2 = "/data/web_static/releases/{}/".format(extract_path)
    mv = "{} {}".format(part1, part2)
    if run(mv).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        pass
    if run(
        "ln -sf /data/web_static/releases/{}/ /data/web_static/current"
            .format(extract_path)).failed is True:
        return False
    return True
