#!/usr/bin/env python3
"""Start backend server"""
import subprocess
import sys
import os

os.chdir(os.path.dirname(__file__))
result = subprocess.run(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
    cwd=os.getcwd()
)
sys.exit(result.returncode)
