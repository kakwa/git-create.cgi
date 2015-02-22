PREFIX = /usr/local/
EXEC_PREFIX = $(PREFIX)/
LIBEXECDIR = $(EXEC_PREFIX)/libexec

install:
	mkdir -p $(DESTDIR)/$(LIBEXECDIR)/git-create/
	cp git-create.cgi $(DESTDIR)/$(LIBEXECDIR)/git-create/git-create.cgi
	chmod 755 $(DESTDIR)/$(LIBEXECDIR)/git-create/git-create.cgi
