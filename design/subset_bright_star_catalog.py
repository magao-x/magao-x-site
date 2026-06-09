#!/usr/bin/env python
import json
import sys

class FormattedFloat(float):
    __repr__ = staticmethod(lambda x: format(x, '3.4f'))

json.encoder.c_make_encoder = None
json.encoder.float = FormattedFloat

class MissingValue(Exception):
    pass

def as_float(substring):
    if len(substring.strip()) == 0:
        raise MissingValue()
    else:
        return float(substring)

def parse_line(line):
    # Excerpt from http://tdc-www.harvard.edu/catalogs/bsc5.readme:
    #
    # Byte-by-byte Description of file: catalog
    # --------------------------------------------------------------------------------
    #    Bytes Format  Units   Label    Explanations
    # --------------------------------------------------------------------------------
    #    1-  4  I4     ---     HR       [1/9110]+ Harvard Revised Number
    #                                     = Bright Star Number
    #    5- 14  A10    ---     Name     Name, generally Bayer and/or Flamsteed name
    # ...
    #   76- 77  I2     h       RAh      ?Hours RA, equinox J2000, epoch 2000.0 (1)
    #   78- 79  I2     min     RAm      ?Minutes RA, equinox J2000, epoch 2000.0 (1)
    #   80- 83  F4.1   s       RAs      ?Seconds RA, equinox J2000, epoch 2000.0 (1)
    #       84  A1     ---     DE-      ?Sign Dec, equinox J2000, epoch 2000.0 (1)
    #   85- 86  I2     deg     DEd      ?Degrees Dec, equinox J2000, epoch 2000.0 (1)
    #   87- 88  I2     arcmin  DEm      ?Minutes Dec, equinox J2000, epoch 2000.0 (1)
    #   89- 90  I2     arcsec  DEs      ?Seconds Dec, equinox J2000, epoch 2000.0 (1)
    # ...
    #  103-107  F5.2   mag     Vmag     ?Visual magnitude (1)
    id_num = int(line[:4])
    name = line[4:14]
    ra_hour = as_float(line[75:77])
    ra_min = as_float(line[77:79])
    ra_sec = as_float(line[79:83])
    ra = 360 * (ra_hour / 24 + ra_min / 24 / 60 + ra_sec / 24 / 60 / 60)

    dec_sgn = -1 if line[83] == '-' else 1
    dec_deg = as_float(line[84:86])
    dec_arcmin = as_float(line[86:88])
    dec_arcsec = as_float(line[88:90])
    dec = dec_sgn * (dec_deg + dec_arcmin / 60 + dec_arcsec / 60 / 60)
    v_mag = as_float(line[102:107])
    return {
        'id': id_num,
        'name': ''.join(name.strip().split()),
        'ra': ra,
        'dec': dec,
        'vmag': v_mag,
    }

def main(args):
    stars = []
    total = 0
    skipped = 0
    with open(args.CATALOG_FILE) as f:
        for line in f:
            total += 1
            try:
                star = parse_line(line)
            except MissingValue:
                skipped += 1
                continue
            if star['vmag'] < args.MAG_CUTOFF:
                stars.append(star)
    json.dump(stars, sys.stdout, separators=(',', ':'))
    print()
    print(f"Visited {total}, skipped {skipped}", file=sys.stderr)
    return 0

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('CATALOG_FILE')
    parser.add_argument('MAG_CUTOFF', type=float)
    args = parser.parse_args()
    sys.exit(main(args))