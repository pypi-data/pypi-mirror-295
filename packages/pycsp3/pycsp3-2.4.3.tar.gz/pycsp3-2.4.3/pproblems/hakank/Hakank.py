import os
import sys
import re

if sys.argv:
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1]) as f:
                s = f.read()
                m = re.findall(r'<span>Problem: (.*?)</span>', s)
                for v in m:
                    print(v)
        except Exception as e:
            print("pb")
