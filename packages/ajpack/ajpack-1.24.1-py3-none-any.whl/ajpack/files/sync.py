import os
import shutil
import time

from ..folder.env import create_env

global fileCounter
fileCounter: int
fileCounter = 0

def _get_files(path: str) -> dict[str, str]:
    """Gets all files of a path."""
    files: dict[str, str] = {}

    for dirpath, _, dirfiles in os.walk(path):
        for file in dirfiles:
            f: str = os.path.join(dirpath, file)
            if os.path.isfile(f):
                files[os.path.basename(f)] = f
    
    return files

def _compare_files(srcFile: str, tarFile: str) -> str:
    """Compares the source and target file."""
    try:
        if not os.path.exists(tarFile):
            return srcFile
        elif os.path.getmtime(srcFile) > os.path.getmtime(tarFile):
            return srcFile
    except FileNotFoundError:
        pass
    return ""

def _scan_files(srcDir: str, tarDir: str) -> dict[str, str]:
    """Returns all files of the source and target directory, which are different."""
    create_env([tarDir])

    filesSrc: dict[str, str] = _get_files(srcDir)
    filesTar: dict[str, str] = _get_files(tarDir)

    backupFiles: dict[str, str] = {}

    for srcFile in filesSrc.keys():
        srcFilePath: str = filesSrc[srcFile]
        srcFileDir: str = os.path.dirname(srcFilePath)

        relPath: str = os.path.relpath(srcFileDir, srcDir)
        tarFileDir: str = os.path.join(tarDir, relPath)

        if not os.path.exists(tarFileDir):
            os.makedirs(tarFileDir, exist_ok=True)

        tarFilePath: str = os.path.join(tarFileDir, srcFile)

        if srcFile in filesTar.keys():
            comparedFile: str = _compare_files(srcFilePath, filesTar[srcFile])

            if comparedFile:
                backupFiles[srcFilePath] = tarFilePath
        else:
            backupFiles[srcFilePath] = tarFilePath

    return backupFiles

def _backup_file(srcFile: str, tarFile: str) -> None:
    """Copies the files"""
    global fileCounter
    try:
        shutil.copy2(srcFile, tarFile)
        create_env([tarFile])
        fileCounter += 1
    except Exception:
        pass

def sync_files(srcDir: str, tarDir: str) -> tuple[dict[str, str], int, float]:
    """
    Syncs two directories (in one direction), acts like a backup.

    :param srcDir (str): The source directory to back up.
    :param tarDir (str): The target directory to sync.

    :return backupFiles, len(backupFiles.keys()), seconds (tuple[dict[str, str], int, float]): The synced files with their source paths as keys and their destination paths as values. Also the length of the dictionary. Also the time needed in seconds.
    """
    global fileCounter
    
    stamp1: float = time.time()

    backupFiles: dict[str, str] = _scan_files(srcDir, tarDir)
    
    for srcFileToBackup, tarFileToBackup in backupFiles.items():
        _backup_file(srcFileToBackup, tarFileToBackup)

    stamp2: float = time.time()

    return backupFiles, len(backupFiles.keys()), stamp2-stamp1