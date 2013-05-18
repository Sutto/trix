import tempfile
import shutil
import subprocess
import sys

side   = 20
width  = 11
wts    = width * side
height = 50
hts    = height * side

pieces = [[(0,0),(1,0),(2,0),(3,0)]
         ,[(0,0),(0,1),(1,0),(1,1)]
         ,[(0,0),(1,0),(2,0),(1,1)]
         ,[(0,0),(1,0),(2,0),(2,1)]
         ,[(0,1),(1,1),(2,1),(2,0)]
         ,[(1,0),(2,0),(0,1),(1,1)]
         ,[(0,0),(1,0),(1,1),(2,1)]]

colours = [(0,0,0),     (255,0,0),   (255,0,255), (255,165,0),
#          black        red          pink,        orange
           (255,255,0), (50,177,65), (0,255,255), (0,0,255)]
#          yellow       green        cyan         blue

edges = [(colours[0], [(0, wts), (0, wts + 2), (hts + 2, wts + 2), (hts + 2, wts), (0, wts)])
        ,(colours[0], [(hts, 0), (hts + 2, 0), (hts + 2, wts + 2), (hts, wts + 2), (hts, 0)])]

def rotate(k, xs):
    for i in range(k):
        xs = [(y, max([a for (a, b) in xs]) - x) for (x, y) in xs]
    return xs

def sqs(piece):
    [p, r, d] = piece
    ss = [(x, y + d) for (x, y) in rotate(r, pieces[p - 1])]
    adj = min([width - 1 - y for (x, y) in ss])
    return ([(x, y + min(0, adj)) for (x, y) in ss], colours[p])

def place(p, h, xs, b):
    (zs, c) = p
    ns = [(h + x * side, y * side, c) for (x, y) in zs]
    #if at height h the piece overlaps with the board, return b; o/w try one spot further down
    if h < 0 or any([(x1, y1) == (x2, y2) for (x1, y1, c1) in ns for (x2, y2, c2) in xs]):
        return b
    else:
        return place(p, h - side, xs, ns)

def slide(x, h):
    if x > h:
        return x - side
    else:
        return x

def elimLines(xs, hs):
    for h in hs:
        if all([any([(x, y) == (h, k) for (x, y, z) in xs]) for k in range(0, wts, side)]):
            xs = [(slide(x, h), y, c) for (x, y, c) in xs if x != h]
    return xs

def history(h, xs, ps):
    if ps == []:
        return []
    else:
        #slide ps[0] down until it hits something
        ys = place (ps[0], h + side, xs, [])
        hs = [x for (x, y, z) in ys]
        hs.sort()
        hs.reverse()
        #check for completed lines, highest first
        zs = elimLines(xs + ys, hs)
        hl = history(max([x for (x, y, z) in zs] + [0]), zs, ps[1:])
        hl.insert(0, zs)
        return hl

def mksq(p):
    (x, y, c) = p
    return (c, [(x, y), (x + side, y), (x + side, y + side), (x, y + side), (x, y)])

def writeColor(c):
    (r, g, b) = c
    return "".join(["rgb(", str(r), ",", str(g), ",", str(b), ")"])

def writePolygons(f, ps):
    f.write("<svg xmlns=\"http://www.w3.org/2000/svg\">\n")
    for (c, p) in ps:
        f.write("<polygon points=\"")
        for (x, y) in p:
            f.write("".join([str(x), ",", str(y), " "]))
        f.write("\" style=\"fill:")
        f.write(writeColor(c))
        f.write(";stroke:")
        f.write(writeColor(colours[0]))
        f.write(";stroke-width:2\"/>\n")
    f.write("</svg>\n")

# Generator version of the item. Takes a file name
def generate(input_file, output_file):
    with open(input_file) as f:
        ps = [sqs([int(x) for x in l.split(" ")]) for l in f.read().split("\n") if l.strip() != ""]
    # build the history of the placement: each entry h[k] describes the board after k+1 pieces
    h = history(0, [], ps)

    directory   = tempfile.mkdtemp("frames")
    frame_files = []
    size = "%dx%d" % (hts, wts)
    for k in range(len(h)):
        frame_name = str(k)
        frame_file = directory + "/" + frame_name
        svg = frame_file + ".svg"
        png = frame_file + ".png"
        with open(svg, 'w+') as f:
            writePolygons(f, edges + [mksq(p) for p in h[k]])
        subprocess.call(['convert', '-size', size, svg, png])
        frame_files.append(png)
    subprocess.call(["convert", "-delay", "20", "-loop", "0"] + frame_files + [output_file])
    shutil.rmtree(directory)

def main():
    if len(sys.argv) < 3:
        print("Usage: ", sys.argv[0], " result-file gif-name", file=sys.stdout)
        sys.exit(2)
    generate(sys.argv[1], sys.argv[2])

if __name__ == '__main__': main()