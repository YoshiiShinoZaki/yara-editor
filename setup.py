#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author:       Ivan Fontarensky
@license:      GNU General Public License 3.0
@contact:      ivan.fontarensky_at_gmail.com
"""


import os, re, sys
import platform

from distutils.core import setup
from distutils.cmd import Command
from distutils.log import error, info, warn


class Uninstall(Command):
    description = "Attempt an uninstall from an install --record file"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def get_command_name(self):
        return 'uninstall'

    def run(self):
        try:
            f = open("uninstall.list")
            files = [file.strip() for file in f]
            f.close()
        except:
            raise DistutilsFileError("Unable to open uninstall.list. Did you try an uninstall without install before ?\nPlease do a 'python setup.py install' and then restart me.")


        for file in files:
            if os.path.isfile(file) or os.path.islink(file):
                info("removing %s" % repr(file))
                if not self.dry_run:

                    try:
                        os.unlink(file)
                    except OSError, e:
                        warn("could not delete: %s: %s" % (repr(file), e))

            elif not os.path.isdir(file):
                info("skipping %s" % repr(file))

        dirs = set()

        for file in reversed(sorted(files)):
            dir = os.path.dirname(file)

            if dir not in dirs and os.path.isdir(dir) and len(os.listdir(dir)) == 0:

                dirs.add(dir)

                if dir.find("site-packages/") > 0:
                    info("removing %s" % repr(dir))

                    if not self.dry_run:

                        try:
                            os.rmdir(dir)

                        except OSError, e:
                            warn("could not remove directory: %s" % str(e))

                else:
                    info("skipping empty directory %s" % repr(dir))



def extract_version():
  if not os.path.exists("VERSION"):
      subprocess.call(["make", "version"])
      if os.path.exists("VERSION"):
	  f = open("VERSION")
	  version = f.read()[0:-3]
	  f.close()
	  return version
      else:
	  print "ERROR: Unable to read the VERSION file."

if len(sys.argv)<1:
    usage

if sys.argv[1] == "install" and not "--record" in sys.argv:
      sys.argv.append("--record")
      sys.argv.append("uninstall.list")

man_dir = 'man' if platform.system() == 'FreeBSD' else 'share/man'
config_dir = '/etc/' if platform.system() == 'FreeBSD' else '/etc/'

data_files = [
        (os.path.join(man_dir, 'fr/man8'), ['man/fr/yara-editor.8']),
        (os.path.join(man_dir, 'man8'), ['man/fr/yara-editor.8']),
        (os.path.join(man_dir, 'en/man8'), ['man/en/yara-editor.8']),
        (os.path.join(config_dir, 'yaraeditor/yara-editor'), ['config/yara-editor.cfg'])
      ]



setup(
    name = 'yara-editor',
    version = '0.1.4',
    packages=['yaraeditor','yaraeditor/ui','yaraeditor/core/'],
    scripts = ['bin/yara-editor'],
    data_files=data_files,
    # Metadata
    author = 'Ivan Fontarensky',
    author_email = 'ivan.fontarensky_at_gmail.com',
    description = 'yara-editor is a free editor for yara in python.',
    license = 'GPLv3',
#    requires=["somepackage (>1.0, !=1.5)"],
    # keywords = '',
    cmdclass={'uninstall': Uninstall},

)



# vim:ts=4:expandtab:sw=4
