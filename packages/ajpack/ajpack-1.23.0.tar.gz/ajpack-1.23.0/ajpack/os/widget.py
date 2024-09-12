from pystray import Icon, Menu, MenuItem  #type:ignore
from PIL import Image

def show_status_icon(iconPath: str, title: str, addMenuItems: list[MenuItem] = [], useDefault: bool = True) -> None:
    """
    Show a status icon in the system tray.

    :param iconPath (str): The image path to use as icon.
    :param title (str): The title of the icon.
    :param addMenuItems (list[pystray.MenuItem]): A list of menu items to add to the default list.
    :param useDefault (bool): Whether to use the default menu items or not. (addMenuItems won't be removed)
    """

    # Load the icon image
    image = Image.open(iconPath)

    # Create the icon
    icon = Icon(title, image, title, Menu())

    # Create a menu
    def exit_icon():
        icon.stop()

    if useDefault:
        menuItems = [
            MenuItem("Open", lambda: print("Open clicked")),
            MenuItem("Exit", exit_icon)
        ] + addMenuItems
    else:
        menuItems = addMenuItems

    icon.menu = Menu(*menuItems)

    # Run the icon in the background
    icon.run()

# Example usage:
if __name__ == "__main__":
    iconPath = "C:/Users/aholz/Downloads/terminal.png"
    title = "My Status Icon"

    show_status_icon(iconPath, title, [MenuItem("Test", lambda: print("Test clicked"))], useDefault=False)