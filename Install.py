#!/usr/bin/env python
import os
import subprocess
import sys
from pathlib import Path

def hasMakeFile(P):
	if 'Makefile' in [f.name for f in [*P.glob('*')]]:
		ret = [*P.glob('*')][[f.name for f in [*P.glob('*')]].index('Makefile')]
	else:
		ret = None
	return ret


def getPkgPath():
	script = Path(subprocess.getoutput('basename $(dirname $(pwd))'))
	folder = script.parent
	return folder


def getPkgName():
	makefile = Path('Makefile')
	with open(makefile, 'r') as f:
		for line in f:
			if 'NAME' in line:
				nameline = line
				break
	name = nameline.split('=')[-1]
	return name


def ask_passwd(PKGNAME):
	cmd = 'zenity --password --title="{PKGNAME} --------------------\nInstaller Requires ROOT(sudo) Priveleges." --timeout=0'.format(
		PKGNAME=PKGNAME)
	password = subprocess.run(cmd, shell=True, capture_output=True, universal_newlines=True).stdout
	return password


def showzen():
	arguments={'install':{
		'forms': '',
		'title': '\t\t{PKGNAME} : Installer\t\t\n',
		'text' : ' Pick the installpath\n\n\t',
		'add-combo':'           Path:     ',
		'combo-values': '/opt/local | /usr/local/ ',
		'text' : '/fixNTFS\n\n'
		}
	}
	args=[]
	inst=arguments['install']
	for k in inst:
		arg=f'--{k}'
		if inst[k]=='':
			args+=[arg]
			continue
		arg+=f'="{inst[k]}"'
		args+=[arg]
	cmd=f'zenity {" ".join(args)}'.format(PKGNAME=pkgname)
	print(cmd)
	installdir=  subprocess.run(cmd, shell=True, capture_output=True, universal_newlines=True).stdout
	return installdir




pkgpath = getPkgPath()
pkgname = getPkgName()
pw = ask_passwd(pkgname)
idir=showzen()
os.chdir(pkgpath)
cmd = 'make install'
sudo = f'echo {pw} | / usr/bin/env bash sudo -S {cmd}'
su = f'echo {pw} | su -c {cmd}'

try:
	subprocess.run(pkexec, shell=True, capture_output=True, universal_newlines=True).stdout
except Exception as E1:
	try:
		subprocess.run(sudo, shell=True, capture_output=True, universal_newlines=True).stdout
	except Exception as E1:
		try:
			subprocess.run(su, shell=True, capture_output=True, universal_newlines=True).stdout
		except Exception as E2:
			fail = 'Failed: \n {first} \n {second} \n'
			cmd = 'zenity --error --title="{PKGNAME} --------------------\n" --text="{result}" '.format(PKGNAME=pkgname,
																																																result=fail)
			subprocess.run(cmd, shell=True, capture_output=True, universal_newlines=True)
			sys.exit()



# cmd = 'zenity --info --title="{PKGNAME}" --text="{result}" '.format(PKGNAME=pkgname, result=result)
# subprocess.run(cmd, shell=True, capture_output=True, universal_newlines=True)
sys.exit()
