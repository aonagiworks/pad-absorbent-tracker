#!/usr/bin/env python3
import subprocess, sys, os
def run(cmd):
    print(f"$ {cmd}")
    r=subprocess.run(cmd,shell=True,capture_output=True,text=True)
    print(r.stdout)
    if r.stderr: print(r.stderr)
    return r.returncode==0

os.chdir(os.path.dirname(os.path.abspath(__file__)))
ok = run("python3 build_data.py")
if not ok: sys.exit(1)
# git ops
run("git add data.json index.html")
# check staged diff
r=subprocess.run("git diff --cached --quiet",shell=True)
if r.returncode==0:
    print("no diff, skip commit")
    sys.exit(0)
run('git commit -m "auto update data.json"')
run("git push origin gh-pages")
