"""
PyInstaller Packaging Script.
Generates standalone Windows Executable TouchlessBrightnessControl.exe
"""
import os
import sys
import subprocess

def build():
    print("=" * 60)
    print("  PyInstaller Automated Build - TouchlessBrightnessControl.exe")
    print("=" * 60)

    # Ensure pyinstaller is installed
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_script = os.path.join(root_dir, "backend", "app", "main.py")
    task_model = os.path.join(root_dir, "hand_landmarker.task")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--name=TouchlessBrightnessControl",
        f"--add-data={task_model};.",
        "--collect-all=mediapipe",
        "--collect-all=screen_brightness_control",
        main_script
    ]

    print("Running PyInstaller command:")
    print(" ".join(cmd))
    subprocess.run(cmd, cwd=root_dir, check=True)
    print("\n[✓] Executable build complete!")
    print(f"Dist location: {os.path.join(root_dir, 'dist', 'TouchlessBrightnessControl')}")

if __name__ == "__main__":
    build()
