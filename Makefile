.PHONY: install uninstall tarball

PROJECT=colorize
VERSION=1.0
BUILD=2

DESTDIR_PLUGIN=/usr/lib64/gimp/2.0/plug-ins/
DESTDIR_SCRIPT=/usr/bin
DESTDIR_DOCS=/usr/share/doc/colorize
TAR_BALL=$(PROJECT)-$(VERSION)-$(BUILD).tar.bz2

FILE_LIST=gimp_colorize.py \
			colorize.py \
			README.md \
			LICENSE \
			Makefile

install: $(FILE_LIST)
	install gimp_colorize.py $(DESTDIR_PLUGIN)
	install colorize.py	$(DESTDIR_SCRIPT)
	mkdir -p $(DESTDIR_DOCS)
	install README.md LICENSE $(DESTDIR_DOCS)

uninstall: $(DESTDIR_PLUGIN)/gimp_colorize.py $(DESTDIR_SCRIPT)/colorize.py $(DESTDIR_DOCS)
	rm -rf $^

tarball: $(TAR_BALL)

$(TAR_BALL): $(FILE_LIST)
	cd ..; tar cvjf $@ colorize/{$(shell tr ' ' ',' <<< "$^")}
	mv ../$@ .	

ChangeLog:
	git log --pretty=format:"* %aD, %an <%ae> %s %n%b" --date=short | \
        sed -e 's/\[/\n\t[/' -e 's/^-/\t-/' > ChangeLog

