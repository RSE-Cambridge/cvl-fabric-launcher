import os
import sys
import glob

if len(sys.argv) < 3:
    print "Usage: package_windows_version.py <certificate.pfx> <password>"
    sys.exit(1)

code_signing_certificate = sys.argv[1]
code_signing_certificate_password = sys.argv[2]

os.system('del /Q dist\\*.*')

#os.system('C:\\Python27\\python.exe  .\\pyinstaller-2.1\\pyinstaller.py --icon MASSIVE.ico --console --debug --log-level=DEBUG launcher.py')
os.system('C:\\Python27\\python.exe  .\\pyinstaller\\pyinstaller.py --icon MASSIVE.ico --windowed launcher.py')

os.system('copy /Y MASSIVE.ico dist\\launcher\\')
os.system('copy /Y C:\\Python27\\Lib\\site-packages\\wx-2.8-msw-unicode\\wx\\gdiplus.dll dist\\launcher\\')
import shutil
shutil.copytree(r'openssh-cygwin-stdin-build', r'dist\launcher\openssh-cygwin-stdin-build')
tmpdir=r'dist\launcher\openssh-cygwin-stdin-build\tmp'
for subdir in os.listdir(tmpdir):
    subdirpath = os.path.join(tmpdir,subdir)
    if os.path.isdir(subdirpath):
        shutil.rmtree(subdirpath)

os.system('copy /Y GPL.txt dist\\launcher\\')

import requests
cacert = requests.certs.where()
os.system('copy /Y ' + cacert + ' dist\\launcher\\')

os.system('mkdir dist\\launcher\\help')
os.system('mkdir dist\\launcher\\help\\helpfiles')
os.system('copy /Y help\\helpfiles\\*.* dist\\launcher\\help\\helpfiles\\')
os.system('copy /Y help\\README.txt dist\\launcher\\help\\')

os.system('copy /Y kill-charade-processes.bat dist\\launcher\\')
os.system('copy /Y masterList.url dist\\launcher\\')

os.system("signtool sign -f \"" + code_signing_certificate + "\" -p " + code_signing_certificate_password + " dist\launcher\*.exe")
os.system("signtool sign -f \"" + code_signing_certificate + "\" -p " + code_signing_certificate_password + " dist\launcher\*.dll")

# Only one of these will work...
os.system(r""""C:\Program Files (x86)\Inno Setup 5\Compil32.exe" /cc .\\launcherWindowsSetupWizardScript.iss""")
os.system(r""""C:\Program Files\Inno Setup 5\Compil32.exe" /cc .\\launcherWindowsSetupWizardScript.iss""")
os.system("signtool sign -f \"" + code_signing_certificate + "\" -p " + code_signing_certificate_password + " setup.exe")

