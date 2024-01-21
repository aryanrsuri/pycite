import os
from cite import Cite
for fn in os.listdir("data"):
    file = open(os.path.join("data", fn))
    ext: str = fn.rsplit(".")[-1]
    try:
        c = Cite(file.read(), ext)
        if ext == "bib":
            mla = c.format("mla")
            apa = c.format("apa")
            print("-------%s------\nMLA:  %s \nAPA: %s\n" % (fn, mla, apa))
    except Exception:
        raise Exception

# d = Cite("10.1073/pnas.2214423119", rtype="doi")
# x = Cite("", rtype="doi")
