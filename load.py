import os
from cite import Cite
for fn in os.listdir("data"):
    file = open(os.path.join("data", fn))
    try:
        c = Cite(file.read(), rtype="bibtex")
        print("%s and its parsed %s" % (fn,c.parts))
    except Exception:
        raise Exception

d = Cite("10.1073/pnas.2214423119", rtype="doi")
# will fail
x = Cite("", rtype="doi")



