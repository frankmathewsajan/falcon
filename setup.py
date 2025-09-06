"""
Setup script for creating Falcon Team Tracker executable
Run with: python setup.py build
"""

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules may need to be included manually
build_exe_options = {
    "packages": ["os", "sys", "subprocess", "webbrowser", "time", "threading", "tkinter", "pathlib", "shutil"],
    "excludes": ["unittest", "test", "distutils"],
    "include_files": [],
    "zip_include_packages": ["encodings", "PySide6", "shiboken6"],
}

# Base for GUI applications on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="FalconTeamTracker",
    version="1.0.0",
    description="Falcon Team Tracker - Automated Installer and Server",
    author="Frank Mathew Sajan",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "falcon.py",
            base=base,
            target_name="FalconInstaller.exe",
            icon=None  # Add icon path here if you have one
        )
    ],
)
