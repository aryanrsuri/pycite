## Python Citation manager library 
                
buffer >> dict --> export to: format or template
                 

formats: ris, bibtex, json, csljson, enw, refworks,xml

template: apa,chicago,mla,vancouver,harvard

How it works
```
    c = Cite(buffer, extension)
    c.templ("apa")
    c.format("ris")
```
