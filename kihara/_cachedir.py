import sys
import os

from .version import VERSION

APPNAME = 'kihara' + str(VERSION[0])

if sys.platform.startswith('java'):
	import platform
	os_name = platform.java_ver()[3][0]
	if os_name.startswith('Windows'):
		system = 'win32'
	elif os_name.startswith('Mac'):
		system = 'darwin'
	else:
		system = 'linux2'
else:
	system = sys.platform

def user_cache_path(filename):
	if system == "win32":
		path = os.path.normpath(_get_win_folder("CSIDL_LOCAL_APPDATA"))
		path = os.path.join(path, 'kihara', APPNAME)
	elif system == 'darwin':
		path = os.path.expanduser('~/Library/Caches')
		path = os.path.join(path, APPNAME)
	else:
		path = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
		path = os.path.join(path, APPNAME)
	ensure_dir_exists(path)
	return os.path.join(path, filename)

def ensure_dir_exists(d):
	if not os.path.isdir(d):
		os.makedirs(d)

def _get_win_folder_from_registry(csidl_name):
	import winreg as _winreg

	shell_folder_name = {
		"CSIDL_APPDATA": "AppData",
		"CSIDL_COMMON_APPDATA": "Common AppData",
		"CSIDL_LOCAL_APPDATA": "Local AppData",
	}[csidl_name]

	key = _winreg.OpenKey(
		_winreg.HKEY_CURRENT_USER,
		r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
	)
	dir, type = _winreg.QueryValueEx(key, shell_folder_name)
	return dir


def _get_win_folder_with_pywin32(csidl_name):
	from win32com.shell import shellcon, shell
	dir = shell.SHGetFolderPath(0, getattr(shellcon, csidl_name), 0, 0)

	has_high_char = False
	for c in dir:
		if ord(c) > 255:
			has_high_char = True
			break
	if has_high_char:
		try:
			import win32api
			dir = win32api.GetShortPathName(dir)
		except ImportError:
			pass

	return dir


def _get_win_folder_with_ctypes(csidl_name):
	import ctypes

	csidl_const = {
		"CSIDL_APPDATA": 26,
		"CSIDL_COMMON_APPDATA": 35,
		"CSIDL_LOCAL_APPDATA": 28,
	}[csidl_name]

	buf = ctypes.create_unicode_buffer(1024)
	ctypes.windll.shell32.SHGetFolderPathW(None, csidl_const, None, 0, buf)

	has_high_char = False
	for c in buf:
		if ord(c) > 255:
			has_high_char = True
			break
	if has_high_char:
		buf2 = ctypes.create_unicode_buffer(1024)
		if ctypes.windll.kernel32.GetShortPathNameW(buf.value, buf2, 1024):
			buf = buf2

	return buf.value

def _get_win_folder_with_jna(csidl_name):
	import array
	from com.sun import jna
	from com.sun.jna.platform import win32

	buf_size = win32.WinDef.MAX_PATH * 2
	buf = array.zeros('c', buf_size)
	shell = win32.Shell32.INSTANCE
	shell.SHGetFolderPath(None, getattr(win32.ShlObj, csidl_name), None, win32.ShlObj.SHGFP_TYPE_CURRENT, buf)
	dir = jna.Native.toString(buf.tostring()).rstrip("\0")

	has_high_char = False
	for c in dir:
		if ord(c) > 255:
			has_high_char = True
			break
	if has_high_char:
		buf = array.zeros('c', buf_size)
		kernel = win32.Kernel32.INSTANCE
		if kernel.GetShortPathName(dir, buf, buf_size):
			dir = jna.Native.toString(buf.tostring()).rstrip("\0")

	return dir

if system == "win32":
	try:
		import win32com.shell
		_get_win_folder = _get_win_folder_with_pywin32
	except ImportError:
		try:
			from ctypes import windll
			_get_win_folder = _get_win_folder_with_ctypes
		except ImportError:
			try:
				import com.sun.jna
				_get_win_folder = _get_win_folder_with_jna
			except ImportError:
				_get_win_folder = _get_win_folder_from_registry