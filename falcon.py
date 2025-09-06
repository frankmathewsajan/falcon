#!/usr/bin/env python3
"""
Falcon Team Tracker - Automated Installer and Server
Author: Frank Mathew Sajan
Description: Automated installation and server startup for the Falcon Django application
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import shutil

class FalconInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Falcon Team Tracker - Installer")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        self.root.minsize(500, 500)
        
        # Variables
        self.install_path = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Ready to install Falcon Team Tracker")
        
        # Setup UI
        self.setup_ui()
        
        # Default installation path
        default_path = os.path.join(os.path.expanduser("~"), "FalconTeamTracker")
        self.install_path.set(default_path)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2563eb", height=80)
        title_frame.pack(fill="x", pady=(0, 20))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="Falcon Team Tracker", 
            font=("Arial", 20, "bold"),
            fg="white", 
            bg="#2563eb"
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame, 
            text="Automated Installation & Server Startup", 
            font=("Arial", 10),
            fg="#93c5fd", 
            bg="#2563eb"
        )
        subtitle_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, padx=40, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Create a container for all content except buttons
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Installation path selection
        path_frame = tk.LabelFrame(content_frame, text="Installation Location", font=("Arial", 12, "bold"))
        path_frame.pack(fill="x", pady=(0, 20))
        
        path_entry_frame = tk.Frame(path_frame)
        path_entry_frame.pack(fill="x", padx=10, pady=10)
        
        self.path_entry = tk.Entry(
            path_entry_frame, 
            textvariable=self.install_path, 
            font=("Arial", 10),
            width=50
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            path_entry_frame, 
            text="Browse", 
            command=self.browse_folder,
            bg="#3b82f6",
            fg="white",
            font=("Arial", 10),
            padx=20
        )
        browse_btn.pack(side="right")
        
        # Requirements info
        info_frame = tk.LabelFrame(content_frame, text="Requirements", font=("Arial", 12, "bold"))
        info_frame.pack(fill="x", pady=(0, 20))
        
        requirements = [
            "Python 3.8+ (automatically detected)",
            "Git (for cloning repository)",
            "Internet connection (for downloading dependencies)",
            "500MB free disk space"
        ]
        
        for req in requirements:
            req_label = tk.Label(info_frame, text=req, font=("Arial", 10), anchor="w")
            req_label.pack(fill="x", padx=10, pady=2)
        
        # Progress section
        progress_frame = tk.LabelFrame(content_frame, text="Installation Progress", font=("Arial", 12, "bold"))
        progress_frame.pack(fill="x", pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.progress_var, 
            maximum=100,
            length=500
        )
        self.progress_bar.pack(pady=10, padx=10)
        
        self.status_label = tk.Label(
            progress_frame, 
            textvariable=self.status_text, 
            font=("Arial", 10),
            wraplength=500
        )
        self.status_label.pack(pady=(0, 10), padx=10)
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=20, side="bottom")
        
        self.install_btn = tk.Button(
            button_frame,
            text="Install & Run Falcon",
            command=self.start_installation,
            bg="#16a34a",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10,
            width=20
        )
        self.install_btn.pack(side="left", padx=(0, 10), expand=True)
        
        quit_btn = tk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit,
            bg="#dc2626",
            fg="white",
            font=("Arial", 12),
            padx=30,
            pady=10,
            width=15
        )
        quit_btn.pack(side="right", expand=True)
    
    def browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory(title="Select Installation Directory")
        if folder:
            self.install_path.set(os.path.join(folder, "FalconTeamTracker"))
    
    def update_progress(self, value, status):
        """Update progress bar and status"""
        self.progress_var.set(value)
        self.status_text.set(status)
        self.root.update()
    
    def run_command_with_progress(self, command, cwd=None, progress_callback=None):
        """Run a command with real-time output and progress updates"""
        try:
            process = subprocess.Popen(
                command, 
                shell=True, 
                cwd=cwd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True
            )
            
            output_lines = []
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    output_lines.append(output.strip())
                    if progress_callback:
                        progress_callback(output.strip())
            
            return_code = process.poll()
            return return_code == 0, '\n'.join(output_lines), ""
            
        except Exception as e:
            return False, "", str(e)
    
    def run_command(self, command, cwd=None):
        """Run a command and return success status"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd, 
                capture_output=True, 
                text=True,
                timeout=300  # 5 minute timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def check_requirements(self):
        """Check if required software is installed"""
        # Check Python
        try:
            python_version = sys.version_info
            if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
                return False, "Python 3.8+ is required"
        except:
            return False, "Python is not installed"
        
        # Check Git
        success, _, _ = self.run_command("git --version")
        if not success:
            return False, "Git is not installed. Please install Git from https://git-scm.com/"
        
        return True, "All requirements met"
    
    def create_shortcuts(self, install_dir):
        """Create shortcuts to run the application"""
        try:
            # Create shortcut in parent directory of installation
            parent_dir = os.path.dirname(install_dir)
            folder_name = os.path.basename(install_dir)
            
            if os.name == 'nt':  # Windows
                # Create batch file in parent directory
                batch_content = f'''@echo off
title Falcon Team Tracker
echo Starting Falcon Team Tracker...
cd /d "{install_dir}"
call venv\\Scripts\\activate
python manage.py runserver 127.0.0.1:8000
pause'''
                
                batch_path = os.path.join(parent_dir, "Run_Falcon.bat")
                with open(batch_path, 'w') as f:
                    f.write(batch_content)
                
                # Create uninstall batch file
                uninstall_content = f'''@echo off
title Falcon Team Tracker - Uninstaller
echo.
echo ============================================
echo   Falcon Team Tracker - Uninstaller
echo ============================================
echo.
echo This will completely remove Falcon Team Tracker and all its files.
echo.
set /p confirm="Are you sure you want to uninstall? (Y/N): "
if /i "%confirm%" NEQ "Y" (
    echo Uninstall cancelled.
    pause
    exit /b
)

echo.
echo Stopping Falcon Team Tracker processes...

REM Kill any Python processes running Django server
taskkill /f /im python.exe /fi "WINDOWTITLE eq Falcon Team Tracker*" 2>nul
taskkill /f /im python.exe /fi "COMMANDLINE eq *manage.py runserver*" 2>nul

REM Wait a moment for processes to close
timeout /t 2 /nobreak >nul

echo Removing installation directory...
if exist "{install_dir}" (
    rmdir /s /q "{install_dir}"
    if exist "{install_dir}" (
        echo Warning: Some files could not be deleted. Please close any open programs and try again.
        pause
        exit /b 1
    ) else (
        echo Installation directory removed successfully.
    )
) else (
    echo Installation directory not found.
)

echo Removing shortcuts...
if exist "%~dp0Run_Falcon.bat" del "%~dp0Run_Falcon.bat"
if exist "%USERPROFILE%\\Desktop\\Falcon Team Tracker.lnk" del "%USERPROFILE%\\Desktop\\Falcon Team Tracker.lnk"

echo.
echo ============================================
echo   Uninstall completed successfully!
echo ============================================
echo.
echo Falcon Team Tracker has been completely removed from your system.
echo.

REM Self-delete this uninstall script
echo Cleaning up uninstaller...
(goto) 2>nul & del "%~f0"'''

                uninstall_path = os.path.join(parent_dir, "Uninstall_Falcon.bat")
                with open(uninstall_path, 'w') as f:
                    f.write(uninstall_content)
                
                # Try to create desktop shortcut
                try:
                    import win32com.client
                    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
                    shortcut_path = os.path.join(desktop, "Falcon Team Tracker.lnk")
                    
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(shortcut_path)
                    shortcut.Targetpath = batch_path
                    shortcut.WorkingDirectory = install_dir
                    shortcut.IconLocation = batch_path
                    shortcut.save()
                    
                    return True, f"Desktop shortcut, run script, and uninstaller created at {parent_dir}"
                except:
                    return True, f"Run script and uninstaller created at {parent_dir} (desktop shortcut requires pywin32)"
                    
            else:  # Unix/Linux/Mac
                # Create shell script in parent directory
                script_content = f'''#!/bin/bash
echo "Starting Falcon Team Tracker..."
cd "{install_dir}"
source venv/bin/activate
python manage.py runserver 127.0.0.1:8000'''
                
                script_path = os.path.join(parent_dir, "run_falcon.sh")
                with open(script_path, 'w') as f:
                    f.write(script_content)
                
                # Create uninstall script
                uninstall_content = f'''#!/bin/bash
echo "============================================"
echo "  Falcon Team Tracker - Uninstaller"
echo "============================================"
echo
echo "This will completely remove Falcon Team Tracker and all its files."
echo
read -p "Are you sure you want to uninstall? (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo
echo "Stopping Falcon Team Tracker processes..."

# Kill any Python processes running Django server
pkill -f "manage.py runserver" 2>/dev/null
pkill -f "python.*runserver" 2>/dev/null

# Wait a moment for processes to close
sleep 2

echo "Removing installation directory..."
if [ -d "{install_dir}" ]; then
    rm -rf "{install_dir}"
    if [ -d "{install_dir}" ]; then
        echo "Warning: Some files could not be deleted. Please check permissions and try again."
        exit 1
    else
        echo "Installation directory removed successfully."
    fi
else
    echo "Installation directory not found."
fi

echo "Removing shortcuts..."
rm -f "$(dirname "$0")/run_falcon.sh"

echo
echo "============================================"
echo "  Uninstall completed successfully!"
echo "============================================"
echo
echo "Falcon Team Tracker has been completely removed from your system."
echo

# Self-delete this uninstall script
rm -f "$0"'''

                uninstall_path = os.path.join(parent_dir, "uninstall_falcon.sh")
                with open(uninstall_path, 'w') as f:
                    f.write(uninstall_content)
                
                # Make both scripts executable
                os.chmod(script_path, 0o755)
                os.chmod(uninstall_path, 0o755)
                return True, f"Run script and uninstaller created at {parent_dir}"
                
        except Exception as e:
            return False, f"Could not create shortcuts: {e}"
    
    def start_installation(self):
        """Start the installation process in a separate thread"""
        def install_thread():
            try:
                self.install_btn.config(state="disabled")
                
                # Check requirements
                self.update_progress(5, "Checking requirements...")
                req_ok, req_msg = self.check_requirements()
                if not req_ok:
                    messagebox.showerror("Requirements Error", req_msg)
                    return
                
                install_dir = self.install_path.get()
                
                # Create installation directory
                self.update_progress(10, "Creating installation directory...")
                try:
                    os.makedirs(install_dir, exist_ok=True)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not create directory: {e}")
                    return
                
                # Clone repository
                self.update_progress(20, "Cloning Falcon repository from GitHub...")
                success, stdout, stderr = self.run_command(
                    "git clone https://github.com/frankmathewsajan/falcon.git .", 
                    cwd=install_dir
                )
                if not success:
                    messagebox.showerror("Git Error", f"Failed to clone repository:\\n{stderr}")
                    return
                
                # Create virtual environment
                self.update_progress(40, "Creating Python virtual environment...")
                success, _, stderr = self.run_command(
                    f'"{sys.executable}" -m venv venv', 
                    cwd=install_dir
                )
                if not success:
                    messagebox.showerror("Virtual Environment Error", f"Failed to create virtual environment:\\n{stderr}")
                    return
                
                # Determine activate script path
                if os.name == 'nt':  # Windows
                    activate_script = os.path.join(install_dir, "venv", "Scripts", "activate")
                    python_exe = os.path.join(install_dir, "venv", "Scripts", "python.exe")
                    pip_exe = os.path.join(install_dir, "venv", "Scripts", "pip.exe")
                else:  # Unix/Linux/Mac
                    activate_script = os.path.join(install_dir, "venv", "bin", "activate")
                    python_exe = os.path.join(install_dir, "venv", "bin", "python")
                    pip_exe = os.path.join(install_dir, "venv", "bin", "pip")
                
                # Install dependencies
                self.update_progress(60, "Installing Python dependencies...")
                
                def dependency_progress(line):
                    if "Collecting" in line:
                        package = line.split("Collecting ")[-1].split(" ")[0] if "Collecting " in line else ""
                        self.update_progress(60, f"Installing dependencies... Collecting {package}")
                    elif "Installing" in line:
                        package = line.split("Installing ")[-1].split(" ")[0] if "Installing " in line else ""
                        self.update_progress(65, f"Installing dependencies... Installing {package}")
                    elif "Successfully installed" in line:
                        self.update_progress(70, "Dependencies installed successfully!")
                
                success, _, stderr = self.run_command_with_progress(
                    f'"{pip_exe}" install -r requirements.txt', 
                    cwd=install_dir,
                    progress_callback=dependency_progress
                )
                if not success:
                    messagebox.showerror("Dependencies Error", f"Failed to install dependencies:\\n{stderr}")
                    return
                
                # Run migrations
                self.update_progress(75, "Setting up database...")
                success, _, stderr = self.run_command(
                    f'"{python_exe}" manage.py migrate', 
                    cwd=install_dir
                )
                if not success:
                    messagebox.showerror("Database Error", f"Failed to setup database:\\n{stderr}")
                    return
                
                # Collect static files
                self.update_progress(85, "Collecting static files...")
                success, _, stderr = self.run_command(
                    f'"{python_exe}" manage.py collectstatic --noinput', 
                    cwd=install_dir
                )
                if not success:
                    # Non-critical error, continue anyway
                    print(f"Warning: collectstatic failed: {stderr}")
                
                # Start Django development server
                self.update_progress(95, "Starting Falcon Team Tracker server...")
                
                def start_server():
                    success, _, stderr = self.run_command(
                        f'"{python_exe}" manage.py runserver 127.0.0.1:8000', 
                        cwd=install_dir
                    )
                
                # Start server in background
                server_thread = threading.Thread(target=start_server, daemon=True)
                server_thread.start()
                
                # Wait a moment for server to start
                time.sleep(3)
                
                # Open browser
                self.update_progress(100, "Opening Falcon Team Tracker in browser...")
                webbrowser.open("http://127.0.0.1:8000")
                
                # Create shortcuts
                shortcut_success, shortcut_msg = self.create_shortcuts(install_dir)
                parent_dir = os.path.dirname(install_dir)
                
                # Show success message
                shortcut_info = ""
                if shortcut_success:
                    if os.name == 'nt':  # Windows
                        shortcut_info = f"""
EASY ACCESS:
- Desktop shortcut created (if available)
- Or double-click: {parent_dir}\\Run_Falcon.bat

UNINSTALL:
- To completely remove: {parent_dir}\\Uninstall_Falcon.bat"""
                    else:  # Unix/Linux/Mac
                        shortcut_info = f"""
EASY ACCESS:
- Run the script: {parent_dir}/run_falcon.sh

UNINSTALL:
- To completely remove: {parent_dir}/uninstall_falcon.sh"""
                else:
                    if os.name == 'nt':  # Windows
                        shortcut_info = f"""
TO RUN AGAIN LATER:
- Double-click: {parent_dir}\\Run_Falcon.bat

UNINSTALL:
- To completely remove: {parent_dir}\\Uninstall_Falcon.bat"""
                    else:  # Unix/Linux/Mac
                        shortcut_info = f"""
TO RUN AGAIN LATER:
- Navigate to: {parent_dir}
- Run: ./run_falcon.sh

UNINSTALL:
- Run: ./uninstall_falcon.sh"""
                
                success_msg = f"""
Falcon Team Tracker installed successfully!

Installation Location: {install_dir}
Web Interface: http://127.0.0.1:8000
Admin Interface: http://127.0.0.1:8000/admin

The application is now running in your browser.
To stop the server, close this installer window.
{shortcut_info}
"""
                
                messagebox.showinfo("Installation Complete!", success_msg)
                
            except Exception as e:
                messagebox.showerror("Installation Error", f"An unexpected error occurred:\\n{str(e)}")
            finally:
                self.install_btn.config(state="normal")
        
        # Start installation in separate thread
        threading.Thread(target=install_thread, daemon=True).start()
    
    def run(self):
        """Run the installer"""
        self.root.mainloop()

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        # Console mode for debugging
        print("Falcon Team Tracker - Console Mode")
        print("This would normally show the GUI installer")
        return
    
    try:
        # Create and run the installer GUI
        installer = FalconInstaller()
        installer.run()
    except ImportError as e:
        if "tkinter" in str(e):
            print("Error: tkinter is not available. Please install tkinter or run Python with tkinter support.")
            print("On Ubuntu/Debian: sudo apt-get install python3-tk")
            print("On CentOS/RHEL: sudo yum install tkinter")
        else:
            print(f"Import error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting Falcon installer: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
