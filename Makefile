PREFIX ?= /usr/local

.SUFFIXES: .mo .po

all: wbui.mo wbui.bin

wbui.bin: *.py wbui/*.py
	python setup.py clean --all
	python setup.py bdist_wheel
	echo '#!/usr/bin/python' > $@
	cat dist/*.whl >> $@
	chmod 755 $@

clean:
	python setup.py clean --all
	rm -f *.mo *.bin
	rm -rf dist *.egg-info

.po.mo:
	msgfmt $< -o $@

install:
	install -Dm755 wbui.bin $(DESTDIR)$(PREFIX)/bin/wbui
