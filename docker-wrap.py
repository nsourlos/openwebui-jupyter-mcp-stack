import subprocess, os, sys

# get the folder of the executable itself (not where it’s run from)
base_dir = os.path.dirname(os.path.abspath(sys.executable))

os.chdir(base_dir)

subprocess.run(["docker", "compose", "down"], check=True)
subprocess.run(["docker", "compose", "build"], check=True)
subprocess.run(["docker", "compose", "up", "-d"], check=True)
# for cmd in [
#     ["docker", "compose", "down"],
#     ["docker", "compose", "build"],
#     ["docker", "compose", "up", "-d"]
# ]:
#     subprocess.run(cmd, check=True)