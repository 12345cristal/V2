#!/usr/bin/env python3
import py_compile
import sys

try:
    py_compile.compile(
        r"C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend\app\api\v1\endpoints\perfil.py",
        doraise=True
    )
    print("✅ Syntax OK: perfil.py")
    sys.exit(0)
except py_compile.PyCompileError as e:
    print(f"❌ Syntax Error:\n{e}")
    sys.exit(1)
