from .get_drives import drives
from .processes import list_processes
from .kill import kill_process
from .ressources import get_system_resources
from .disk import get_disk_info
from .batt import get_battery_status
from .base_path import get_base_path
from .folders import get_paths, parent_folder
from .win import get_terminal_output
from .network import get_local_ip

__all__ = ["drives", "list_processes", "kill_process", "get_system_resources", "get_disk_info", "get_battery_status", "get_base_path", "get_paths", "parent_folder", "get_terminal_output", "get_local_ip"]