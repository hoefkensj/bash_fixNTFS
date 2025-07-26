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
	zens={
		'installer'  :zenity --forms --title='{PKGNAME}: Installer' --text=' Pick the installpath\n\n\t FixNTFS will be installed to:\t\t $DIR/local/scripts/\n\n\t And Symlinked in:\t\t\t\t $DIR/bin ' --add-combo='           Path:     '  --combo-values=' /opt/local/fixNTFS/ | /usr/local/fixNTFS/ '


		}


pkgpath = getPkgPath()
pkgname = getPkgName()
pw = ask_passwd(pkgname)
os.chdir(pkgpath)
cmd = 'make install'
sudo = f'echo {pw} | / usr/bin/env bash sudo -S {cmd}'
su = f'echo {pw} | su -c {cmd}'
result = 'Install Successfull:\n - findexe :\n\tFind cmd with letters \n -lsexe :\n\tList all known commands'
try:
	subprocess.run(pkexec, shell=True, capture_output=True, universal_newlines=True).stdout
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

cmd = 'zenity --info --title="{PKGNAME}" --text="{result}" '.format(PKGNAME=pkgname, result=result)
subprocess.run(cmd, shell=True, capture_output=True, universal_newlines=True)
sys.exit()
