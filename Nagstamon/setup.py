# encoding: utf-8

# Nagstamon - Nagios status monitor for your desktop
# Copyright (C) 2008-2016 Henri Wahl <h.wahl@ifw-dresden.de> et al.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

# from distutils.core import setup
import sys
import platform

from Nagstamon.Config import AppInfo

NAME = AppInfo.NAME
VERSION = AppInfo.VERSION


# workaround to get directory of Qt5 plugins to add missing 'mediaservice' folder needed for audio on OSX and Windows
import os.path
from PyQt5 import QtCore
if platform.system() == 'Windows':
    QTPLUGINS = os.path.join(os.path.dirname(QtCore.__file__), 'plugins')
elif platform.system() == 'Darwin':
    # works of course only with Fink-based Qt5-installation
    QTPLUGINS = '/sw/lib/qt5-mac/plugins'

if platform.system() in ('Windows', 'Darwin'):
    from cx_Freeze import setup, Executable
    os_dependent_include_files = ['Nagstamon/resources/qt.conf',
                                  'Nagstamon/resources',
                                  '{0}/mediaservice'.format(QTPLUGINS)]
else:
    from distutils.core import setup
    os_dependent_include_files = ['Nagstamon/resources']

if platform.system() == 'Windows':
    base = 'Win32GUI' if sys.platform == 'win32' else None

CLASSIFIERS = [
    'Intended Audience :: System Administrators',
    'Development Status :: 5 - Production/Stable',
    'Environment :: Win32 (MS Windows)',
    'Environment :: X11 Applications',
    'Environment :: MacOS X',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Operating System :: POSIX',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Topic :: System :: Monitoring',
    'Topic :: System :: Networking :: Monitoring'
]

# Dependencies are automatically detected, but it might need
# fine tuning.
build_exe_options = dict(packages=['PyQt5.QtNetwork',
    'keyring.backends.file',
    'keyring.backends.Gnome',
    'keyring.backends.Google',
    'keyring.backends.kwallet',
    'keyring.backends.multi',
    'keyring.backends.OS_X',
    'keyring.backends.pyfs',
    'keyring.backends.SecretService',
    'keyring.backends.Windows'],
    include_files=os_dependent_include_files,
    include_msvcr=True,
    excludes=[])

bdist_mac_options = dict(iconfile='Nagstamon/resources/nagstamon.icns',
        custom_info_plist='Nagstamon/resources/Info.plist')

bdist_dmg_options = dict(volume_label='{0} {1}'.format(NAME, VERSION),
        applications_shortcut=False)

executables = [
    Executable('nagstamon-qt.py',
               base=base,
               icon='Nagstamon/resources/nagstamon.ico')
]

setup(name=NAME,
      version=VERSION,
      license='GNU GPL v2',
      description='Nagios status monitor for desktop',
      long_description='Nagstamon is a Nagios status monitor which takes place in systray or on desktop (GNOME, KDE, Windows) as floating statusbar to inform you in realtime about the status of your Nagios and derivatives monitored network. It allows to connect to multiple Nagios, Icinga, Opsview, Op5Monitor, Check_MK/Multisite, Centreon and Thruk servers.',
      classifiers=CLASSIFIERS,
      author='Henri Wahl',
      author_email='h.wahl@ifw-dresden.de',
      url='https://nagstamon.ifw-dresden.de',
      download_url='https://nagstamon.ifw-dresden.de/download',
      scripts=['nagstamon.py'],
      packages=['Nagstamon', 'Nagstamon.Server', 'Nagstamon.thirdparty'],
      package_dir={'Nagstamon': 'Nagstamon'},
      package_data={'Nagstamon': ['resources/*']},
      data_files=[('%s/share/man/man1' % sys.prefix, ['Nagstamon/resources/nagstamon.1'])],
      options=dict(build_exe=build_exe_options,
          bdist_mac=bdist_mac_options,
          bdist_dmg=bdist_dmg_options),
      executables=executables
      )
