PORT := 3322

.PHONY: all

all: output/index.html

DESIGN_SOURCES := design/src/App.vue \
           design/src/Base.vue \
           design/src/components/SiteHeader.vue \
           design/src/components/SiteFooter.vue \
           design/src/components/StarGlobe.vue \
           design/src/components/TelescopeModel.vue \
           design/src/components/VideoWrapper.vue \
           design/src/styles/global.scss \
           design/src/main.ts \
           design/src/entry-server.js \
           design/index.html \
           design/prerender.js

design/dist/static/index.html design/dist/static/base.html: $(DESIGN_SOURCES)
	cd design && yarn generate
	cd design && yarn js-beautify --type html -r ./dist/static/index.html
	cd design && yarn js-beautify --type html -r ./dist/static/base.html
	cd design && yarn js-beautify --type css -r ./dist/static/assets/index.css
	cd design && yarn js-beautify -r ./dist/static/index.js

templates/index.html: design/dist/static/index.html
	mkdir -p templates/
	cp design/dist/static/index.html templates/

templates/base.html: design/dist/static/base.html
	mkdir -p templates/
	cp design/dist/static/base.html templates/

# Stamp file: re-copies the design dist (assets, fonts, videos, etc.) into
# output/ whenever the design build changes. The generator overwrites
# output/index.html and writes output/publications.html on top of this.
output/.assets.stamp: design/dist/static/index.html design/dist/static/base.html
	mkdir -p output/
	cp -R design/dist/static/* ./output/
	touch output/.assets.stamp

# Override to point at a Python with beautifulsoup4/jinja2/lxml/python-dateutil/
# requests already installed (e.g. nix-built `python3.withPackages (...)`); the
# default uses an in-tree venv populated from requirements_loose.txt.
PUBLICATIONS_PYTHON ?= publications-list/pyenv/bin/python

publications-list/pyenv/bin/python:
	$(MAKE) -C publications-list pyenv
	publications-list/pyenv/bin/python -m pip install -r publications-list/requirements_loose.txt

output/index.html: templates/index.html templates/base.html publications-list/generate_from_ads.py publications-list/list_template.html $(PUBLICATIONS_PYTHON) output/.assets.stamp
	PUBLICATIONS_OUTPUT_DIR=output $(PUBLICATIONS_PYTHON) publications-list/generate_from_ads.py

# Both files come out of a single generator run; declaring this dep keeps
# `make output/publications.html` working without re-invoking the generator.
output/publications.html: output/index.html

.PHONY: dev
dev: output/index.html output/publications.html
	python -m http.server --bind 127.0.0.1 --directory ./output/ $(PORT)
	open http://localhost:$(PORT)
