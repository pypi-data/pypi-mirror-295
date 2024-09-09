import os 
import subprocess
import sys 
this_folder=os.path.dirname(os.path.abspath(__file__))
relpaths = os.path.join(this_folder, "allmodules.py")
compilefile = os.path.join(this_folder, "joinall.py")
if os.path.exists(relpaths):
    from .allmodules import *
else:
    pr = subprocess.run(
        " ".join([sys.executable, compilefile]),
        shell=True,
        env=os.environ,
        capture_output=False,
    )
    from .allmodules import *