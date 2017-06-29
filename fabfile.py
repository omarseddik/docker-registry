from fabric.api import *
from fabric.operations import local,run
from fabric.contrib.project import rsync_project
import sys
env.basepath = '/'
env.config = 'config'

from config import dev_env

def login():
	local("docker login --username=%s --password=%s"%(env['docker']['username'],env['docker']['password']))

def build(image):
	login()
	result = local("cd images/%s && docker build -t php7-fpm ."%image)
	print result

def push(image):
	build(image)
	tag = env['docker']['username']+"/"+image
	local("docker tag %s %s"%(image,tag))
	result = local("docker push %s"%tag)
	print result
# Set environement

def dev():
	set_config(dev_env)

def set_config(env_config):
	for key in env_config:
		env[key] = env_config[key]