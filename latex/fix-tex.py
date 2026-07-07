#!/usr/bin/env python3
"""Post-pandoc LaTeX fixups (run inside the container, where book.tex is writable)."""
import sys
p = sys.argv[1]
s = open(p).read()
# code spans in table cells escape pipes as `\|\|`; pandoc leaks "\textbackslash|"
s = s.replace(r"\textbackslash{}\textbar{}", r"\textbar{}")
open(p, "w").write(s)
