import os
import subprocess

# os.system('echo $HOME')
# os.system('echo %s' %'$HOME')

# os.system('echo $HOME > outfile')
# f = open('outfile','r')
# print f.read()

# stream = os.popen('echo $HOME')
# print stream.read()

output = subprocess.check_output(['ls','-l'])
print output