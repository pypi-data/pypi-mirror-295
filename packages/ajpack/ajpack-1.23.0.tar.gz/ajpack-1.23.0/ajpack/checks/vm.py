import subprocess

def run_on_vm(additional_blacklist: list[str] = []) -> bool:
    """
    Checks if current script is running on a vm.
    
    :param additional_blacklists: Some additionional keywords for a vm from you side.
    :return: bool --> If running on vm
    """
    blacklist: list[str] = [
    "vm",
    "black",
    "box",
    "vbox",
    "sand",
    ]

    for item in additional_blacklist: blacklist.append(item)

    output: str = str(subprocess.check_output("wmic bios")).lower()

    for item in blacklist:
        if item.lower() in output:
            return True
        
    return False