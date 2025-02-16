import os
import subprocess
import sys

venv_path = os.path.join(os.getcwd(), ".venv", "Scripts", "activate")

cmd_command = f'start cmd /k "{venv_path} && python -m streamlit run main.py"'

ps_command = f'start powershell -NoExit -Command "& {venv_path}; python -m streamlit run main.py"'

if sys.platform == "win32":
    subprocess.run(cmd_command, shell=True)
