import os, shutil, winshell #type:ignore
from win32com.client import Dispatch #type:ignore

def create_shortcut(
        name: str = "Shortcut",
        target_path: str = "",
        description: str | None = None,
        icon_path: str | None = None,
        arguments: str | None = None,

) -> None:
    """
    Creates a shortcut.

    :param name: The name of the shortcut.
    :param target_path: The target for the shortcut.
    :param description: The description for the shortcut.
    :param icon_path: The icon for the shortcut.
    :param arguments: The arguments for the shortcut.
    """

    shortcut_path = os.path.join(winshell.desktop(), f"{name}.lnk")
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target_path
    if arguments:
        shortcut.Arguments = arguments
    if description:
        shortcut.Description = description
    if icon_path:
        shortcut.IconLocation = icon_path
    
    shortcut.save()