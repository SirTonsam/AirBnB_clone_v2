#!/usr/bin/env bash
from fabric import task
from fabric.api import run, put, env

@task
def do_deploy(archive_path):
  """Deploys the given archive to the web servers.

  Args:
    archive_path: The path to the archive file.

  Returns:
    True if the deployment was successful, False otherwise.
  """

  env.hosts = ['18.234.129.239', '54.237.19.91'] 

  # Upload the archive to the /tmp/ directory of the web server
  run('put {archive_path} /tmp/'.format(archive_path=archive_path))

  # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
  run('mkdir -p /data/web_static/releases/{archive_filename_without_extension}'.format(
      archive_filename_without_extension=archive_path.split('/')[-1].split('.')[0]))
  run('tar -xzf /tmp/{archive_path} -C /data/web_static/releases/{archive_filename_without_extension}'.format(
      archive_path=archive_path))

  # Delete the archive from the web server
  run('rm /tmp/{archive_path}'.format(archive_path=archive_path))

  # Delete the symbolic link /data/web_static/current
  run('rm -rf /data/web_static/current')

  # Create a new the symbolic link /data/web_static/current on the web server, linked to the new version of your code
  run('ln -s /data/web_static/releases/{archive_filename_without_extension} /data/web_static/current'.format(
      archive_filename_without_extension=archive_path.split('/')[-1].split('.')[0]))

  return True

