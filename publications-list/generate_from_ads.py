import io
from glob import glob
import os
import json
import requests
import dateutil.parser
from jinja2 import Environment, FileSystemLoader
from os.path import exists, dirname, join, isdir, basename, splitext
from os import makedirs
import shutil
import datetime

project_dir = dirname(__file__)
repo_dir = dirname(project_dir)
output_dir = os.environ.get('PUBLICATIONS_OUTPUT_DIR', join(project_dir, 'output'))

PREFERRED_LINK_TYPES = [
    ('journal', 'PUB_HTML'),
    ('journal PDF', 'PUB_PDF'),
    ('arXiv', 'EPRINT_HTML'),
    ('arXiv PDF', 'EPRINT_PDF'),
]

MAX_ENTRIES = 1000

PUBLICATIONS_COUNT_PLACEHOLDER = 'NUMBER_OF_MAGAOX_PUBLICATIONS'

def main():
    templates_dir = join(repo_dir, 'templates')
    env = Environment(loader=FileSystemLoader([
        templates_dir,
        project_dir,
    ]))
    publications_template = env.get_template('list_template.html')
    makedirs(output_dir, exist_ok=True)
    media_dir, styles_dir = join(output_dir, 'media'), join(output_dir, 'styles')
    if isdir(media_dir):
        shutil.rmtree(media_dir)
    if isdir(styles_dir):
        shutil.rmtree(styles_dir)

    token = os.environ.get('ADS_API_TOKEN')
    if token is None:
        raise RuntimeError("Export ADS_API_TOKEN in your environment with the API key you get from the ADS web interface: https://ui.adsabs.harvard.edu/user/settings/token")

    library_id = os.environ.get('ADS_LIBRARY_ID')
    if library_id is None:
        raise RuntimeError("Export ADS_LIBRARY_ID in your environment with the value from the last segment of the URL. E.g. for https://ui.adsabs.harvard.edu/public-libraries/EctrgCz4QjagJOiSxQlAXg you would export ADS_LIBRARY_ID=EctrgCz4QjagJOiSxQlAXg")

    headers = {'Authorization': 'Bearer ' + token}
    response_payload = requests.get(f"https://api.adsabs.harvard.edu/v1/biblib/libraries/{library_id}?fl=bibcode&rows={MAX_ENTRIES}&start=0", headers=headers).json()
    bibcodes = response_payload['documents']

    export_payload = {
        'bibcode': bibcodes,
        'sort': 'date desc',
    }
    export_text = requests.post("https://api.adsabs.harvard.edu/v1/export/refabsxml",
                                headers=headers,
                                data=json.dumps(export_payload)).json()['export']

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(export_text, 'xml')

    publications = []
    for rec in soup.find_all('record'):
        extracted = {}
        extracted['title'] = rec.find('title').text
        extracted['authors'] = []
        for author in rec.find_all('author'):
            last_name, first_names = author.text.split(',', 1)
            name = first_names.strip() + ' ' + last_name.strip()
            extracted['authors'].append(name)
        extracted['kind'] = rec.attrs.get('type', 'article')
        extracted['bibcode'] = rec.find('bibcode').text
        extracted['journal'] = rec.find('journal').text
        extracted['abstract'] = rec.find('abstract').text
        extracted['links'] = []
        for label, kind in PREFERRED_LINK_TYPES:
            if rec.find('link', type=kind) is None:
                continue
            url = rec.find('link', type=kind).find('url').text
            extracted['links'].append({'label': label, 'url': url})
        extracted['publication_date'] = dateutil.parser.parse(rec.find('pubdate').text)
        extracted['attachments'] = []

        publications.append(extracted)


    publications_html = publications_template.render({
        'publications': publications,
        'today': datetime.datetime.today(),
        'library_id': library_id,
    })
    with open(join(output_dir, 'publications.html'), 'w') as f:
        f.write(publications_html)

    # The landing page carries a NUMBER_OF_MAGAOX_PUBLICATIONS literal placeholder
    # (baked into the SSR output of App.vue); replace it with the actual count
    # from the ADS library now that we have it.
    #
    # If main.ts ever starts hydrating App.vue again, the same literal will
    # reappear inside the client JS bundle's static-hoisted template and we'll
    # need to patch that too — otherwise hydration would swap the substituted
    # text back to the placeholder. With the current "islands" entrypoint
    # (main.ts mounts StarGlobe/TelescopeModel only) the bundle is tree-shaken
    # of App.vue's render function, so we opportunistically patch index.js when
    # the marker appears and stay silent when it doesn't.
    pub_count = str(len(publications))
    index_template_path = join(templates_dir, 'index.html')
    index_html = open(index_template_path).read()
    if PUBLICATIONS_COUNT_PLACEHOLDER not in index_html:
        raise RuntimeError(
            f"Expected placeholder {PUBLICATIONS_COUNT_PLACEHOLDER!r} not found in "
            f"{index_template_path}. Did the App.vue marker get renamed?"
        )
    with open(join(output_dir, 'index.html'), 'w') as f:
        f.write(index_html.replace(PUBLICATIONS_COUNT_PLACEHOLDER, pub_count))

    index_js_path = join(output_dir, 'index.js')
    if exists(index_js_path):
        index_js = open(index_js_path).read()
        if PUBLICATIONS_COUNT_PLACEHOLDER in index_js:
            with open(index_js_path, 'w') as f:
                f.write(index_js.replace(PUBLICATIONS_COUNT_PLACEHOLDER, pub_count))

if __name__ == "__main__":
    main()
