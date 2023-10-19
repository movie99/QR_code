#credit https://gitlab.eecs.umich.edu/wearhouse-bot/wearhouse-april/-/blob/master/apriltag_gen.py
"""
this code is just for generating the qr codes with color and other options
"""
import sys
import math

import numpy as np, svgwrite

def color_qr(filename , family , color, size):
    #filename = 'test.svg'  # Default filename (.svg, .png, .jpeg or .pgm)
    #family = 'tag16h5'   # Default tag family (see tag_families)
    NTAGS = 10          # Number of tags to create
    TAG_PITCH = 10          # Spacing of tags
    WHITE = 0         # White color (0 is black)

    #thic piece of code will convert str(int) in acually real int on dict 
    #dict cant store real int as keys cause of hash
    color = {int(key): value for key, value in color.items()}
    # this converts all list to tuples
    for key in color:
        color[key] = tuple(color[key])

    print("this is color: ",color)

    DEFAULT_COLOR = 'rgb(0, 0, 0)'  # Default color for QR codes

    tag16h5 =  16, 5, (0x231b, 0x2ea5, 0x346a, 0x45b9, 0x79a6,
                      0x7f6b, 0xb358, 0xe745, 0xfe59, 0x156d)
    tag25h9 = 25, 9, (0x155cbf1, 0x1e4d1b6, 0x17b0b68, 0x1eac9cd, 0x12e14ce,
                      0x3548bb, 0x7757e6, 0x1065dab, 0x1baa2e7, 0xdea688)
    tag36h11 = 36, 11, (0xd5d628584, 0xd97f18b49, 0xdd280910e, 0xe479e9c98, 0xebcbca822,
                       0xf31dab3ac, 0x056a5d085, 0x10652e1d4, 0x22b1dfead, 0x265ad0472)
    tag_families = {"tag16h5": tag16h5, "tag25h9": tag25h9, "tag36h11": tag36h11}

    def set_graphics(fname, family):
        global FTYPE, IMG_WD, IMG_HT, SCALE, DWG_SIZE, VIEW_BOX
        FTYPE = fname.split('.')[-1].upper()
        FTYPE = FTYPE.replace("PGM", "PPM").replace("JPG", "JPEG")
        IMG_HT = int(math.sqrt(family[0])) + 6
        IMG_WD = (NTAGS - 1) * TAG_PITCH + IMG_HT

        if FTYPE == "SVG":
            SCALE = size
            DWG_SIZE = "%umm" % (IMG_WD * SCALE), "%umm" % (IMG_HT * SCALE)
            VIEW_BOX = "0 0 %u %s" % (IMG_WD, IMG_HT)
        else:
            SCALE = 10

    #gen tag
    def gen_tag(tag, val):
        area, minham, codes = tag
        dim = int(math.sqrt(area))
        d = np.frombuffer(np.array(codes[val], ">i8"), np.uint8)
        bits = np.unpackbits(d)[-area:].reshape((-1, dim))
        bits = np.pad(bits, 1, 'constant', constant_values=0)
        return np.pad(bits, 2, 'constant', constant_values=1)

    #save bitmpa
    def save_bitmap(fname, arrays):
        img = Image.new('L', (IMG_WD, IMG_HT), WHITE)
        for i, a in enumerate(arrays):
            t = Image.fromarray(a * WHITE)
            img.paste(t, (i * TAG_PITCH, 0))
        img = img.resize((IMG_WD * SCALE, IMG_HT * SCALE))
        img.save(fname, FTYPE)

    def save_vector(fname, arrays):
        qr_codes = {}  # Dictionary to store QR codes and colors
        dwg = svgwrite.Drawing(fname, DWG_SIZE, viewBox=VIEW_BOX, debug=False)
        for i, a in enumerate(arrays):
            fill_color = color.get(i, DEFAULT_COLOR)
            qr_codes[i] = fill_color  # Store QR code index and color
            g = dwg.g(stroke='none', fill=f"rgb{fill_color}")
            for dy, dx in np.column_stack(np.where(a == 0)):
                g.add(dwg.rect((i * TAG_PITCH + dx, dy), (1, 1)))
            dwg.add(g)
        dwg.save(pretty=True)
        return qr_codes

    opt = None
    for arg in sys.argv[1:]:
        if arg[0] == "-":
            opt = arg.lower()
        else:
            if opt == '-f':
                family = arg
            else:
                filename = arg
            opt = None
    if family not in tag_families:
        print("Unknown tag family: '%s'" % family)
        sys.exit(1)
    tagdata = tag_families[family]
    set_graphics(filename, tagdata)
    print("Creating %s, file %s" % (family, filename))
    tags = [gen_tag(tagdata, n) for n in range(0, NTAGS)]
    qr_codes = {}  # Dictionary to store all QR codes and colors
    if FTYPE == "SVG":
        qr_codes = save_vector(filename, tags)
    else:
        save_bitmap(filename, tags)
