#!/usr/bin/env python3
"""Wrap the built fragment in a full HTML document and write ../five-houses.html."""
import os

D = os.path.dirname(os.path.abspath(__file__))
frag = os.path.join(D, "five-houses.fragment.html")
h = open(frag).read()
i = h.index("</style>") + len("</style>")
out = (
    "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
    + h[:i]
    + "\n<style>[hidden]{display:none!important}body{margin:0}</style>\n</head>\n<body>\n"
    + h[i:]
    + "\n</body>\n</html>\n"
)
open(os.path.join(D, "..", "five-houses.html"), "w").write(out)
os.remove(frag)
print("wrote five-houses.html")
