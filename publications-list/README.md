# publications-site

Generates a list of publications with collapsible inline abstracts from an ADS library and renders them into an HTML template. The publications site lives at https://magao-x.org/publications, which is served from `/srv/www/publications`.

The XWCL/MagAO-X ADS library is a collection of papers produced by members of the collaboration, and can be found here: https://ui.adsabs.harvard.edu/public-libraries/EctrgCz4QjagJOiSxQlAXg. Anyone can add a publication to it, just tell @logan-pearce the email you used for your ADS account.

If you want to attach slides or a poster PDF to a publication:

1. clone this repository
2. make a new folder under `media/` named with the ADS bibcode of the abstract it should attach to
3. place your files in that folder, named as you want them to appear on the site. (e.g. `manuscript.pdf` becomes a download button with the label "manuscript")
4. (optional) compress oversized PDFs, see below
5. add the files to git, commit, and push

## How it works

The file in [.github/workflows/build.yml](.github/workflows/build.yml) defines a workflow (like the magao-x/handbook one) that builds the final pages and copies them into place on the magao-x.org host.

Pushing new changes triggers an update of the public-facing website. Since changes to the library on ADS don't automatically trigger updates, this workflow also runs nightly at 03:51 UTC.

## Local testing

You will need to export two environment variables:

```
export ADS_API_TOKEN=yourtoken
export ADS_LIBRARY_ID=EctrgCz4QjagJOiSxQlAXg
```

where `yourtoken` is replaced with the token available here: https://ui.adsabs.harvard.edu/user/settings/token

Once you have exported these, type `make` to build the site into the `output/` directory (creating it if necessary).

This also creates a self-contained Python environment in `pyenv/` which contains the dependencies of this script.

## Compressing oversized PDFs

If you have `gs` (GhostScript) installed you can shrink PDF file sizes dramatically with this command:

```
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf
```

Where `input.pdf` is the file to shrink, and `output.pdf` will be created by GhostScript. This turned a 35.6 MB PDF from PowerPoint into a 2.1 MB file with minimal loss in quality.
