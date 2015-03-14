.PHONY : all build install uninstall clean

SHELL = /bin/sh
 
PREFIX = $(DESTDIR)/usr
BINDIR = $(PREFIX)/bin
 
all: build
 
build:
	@pyinstaller -s -F bin/pkg

install:
	@install -D -m 755 dist/pkg $(BINDIR)/pkg
 
uninstall:
	@rm $(BINDIR)/pkg
 
clean:
	@rm -rf build dist
