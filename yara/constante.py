#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author:       Ivan Fontarensky
@license:      GNU General Public License 3.0
@contact:      ivan.fontarensky_at_gmail.com
"""


import os

VERSION = "0.1"
DEBUG = 1
NAME = "yara-editor"
LOG_FILE = "./%s.log" % (NAME)

CONF_PATH = "%s/.yara/%s" %  (os.path.expanduser('~'),NAME)
CONF_FILE = "conf"
CONF_LANG = "lang"
CONF_LANG_PATH = "%s/i18n/i18n_en.qm" % (CONF_PATH)
CONF_PREFERENCE = "preference"
CONF_PATH_YARA = "path_yara_rules"
CONF_PATH_MALWARE = "path_malwares"

ERROR_LOADING_CONTROLLEUR = 1

#
# Message in log file
#
MSG_LAUNCH_APPLICATION = "Application start..."
MSG_INFO_READ_CONFIG_FILE = "Reading Configuration"
MSG_ITEM_DELETE = "Item deleted"
MSG_TRY_ITEM_DELETE = "Trying to delete"
MSG_COMPRESSION = "Compressed data with password 'infected'"
MSG_ERROR_WRITTING_CONFIG_FILE = "Error when writing configuration file"
MSG_ERROR_READING_CONFIG_FILE = "Error when reading configuration file"
MSG_ERROR_STOP_APPLICATION = "Error unknow, application stop now "
MSG_INFO_MALWARE_IDENTIFIED = "File identified"
MSG_TRY_ITEM_ADD = "Trying to add"
MSG_ITEM_ADD = "Item added "
MSG_ITEM_SET = "Item setted "
MSG_ORPHELIN = "Orphan detected "
MSG_ERROR_RUN_MODULE_FAILED = "Error during execution of the function run"
MSG_ERROR_REPORT = "Can't read report for this file"
MSG_WARNING_DELETE = "Are you really really sure you want to delete that project ? y@m be careful."
MSG_WARNING_DELETE_CLEAN = "Are you really really sure you want to delete that object ?"

# vim:ts=4:expandtab:sw=4