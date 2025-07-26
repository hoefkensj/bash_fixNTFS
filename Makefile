NAME=fixNTFS
SRC=src/bash_${NAME}
DSTOPT=/opt/local/scripts
BINOPT=/opt/local/shell
DSTUSR=/usr/local/scripts
BINUSR=/usr/local/bin

T1=fixNTFS

installcom:
	chmod 775   $(SRC)/$(T1).sh

install-opt:installcom
	install -vD $(SRC)/$(T1).sh $(DSTOPT)/$(NAME)/$(T1).sh
	ln -s $(DSTOPT)/$(NAME)/$(T1).sh $(BINOPT)/$(T1)
install-usr:installcom
	install -vD $(SRC)/$(T1).sh $(DSTUSR)/$(NAME)/$(T1).sh
	ln -s $(DSTUSR)/$(NAME)/$(T1).sh $(BINUSR)/$(T1)

uninstall-usr:
	rm -rvf $(DSTUSR)/$(NAME)/$(T1).sh
	rm -rvf $(BINUSR)/$(T1)

uninstall-opt:
	rm -rvf $(DSTOPT)/$(NAME)/$(T1).sh
	rm -rvf $(BINOPT)/$(T1)


install:install-usr
uninstall:uninstall-usr
