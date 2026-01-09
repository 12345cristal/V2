#!/usr/bin/env python3
"""Test backend endpoints"""
import requests
import time
import sys

time.sleep(3)  # Wait for backend to be ready

base = "http://localhost:8000/api/v1"

print("\n" + "="*70)
print("🧪 TESTING BACKEND ENDPOINTS")
print("="*70)

tests_passed = 0
tests_failed = 0

# Test 1: Estados Cita (public)
print("\n✅ TEST 1: GET /estados-cita (PUBLIC)")
try:
    r = requests.get(f"{base}/estados-cita", timeout=5)
    if r.status_code == 200:
        data = r.json()
        count = len(data) if isinstance(data, list) else len(str(data))
        print(f"   ✓ Status: {r.status_code} - Retorna {count} registros")
        tests_passed += 1
    else:
        print(f"   ✗ Status: {r.status_code} - {r.text[:80]}")
        tests_failed += 1
except Exception as e:
    print(f"   ✗ ERROR: {str(e)[:80]}")
    tests_failed += 1

# Test 2: Especialidades (public)
print("\n✅ TEST 2: GET /especialidades (PUBLIC)")
try:
    r = requests.get(f"{base}/especialidades", timeout=5)
    if r.status_code == 200:
        data = r.json()
        count = len(data) if isinstance(data, list) else len(str(data))
        print(f"   ✓ Status: {r.status_code} - Retorna {count} registros")
        tests_passed += 1
    else:
        print(f"   ✗ Status: {r.status_code} - {r.text[:80]}")
        tests_failed += 1
except Exception as e:
    print(f"   ✗ ERROR: {str(e)[:80]}")
    tests_failed += 1

# Test 3: Roles (public)
print("\n✅ TEST 3: GET /roles (PUBLIC)")
try:
    r = requests.get(f"{base}/roles", timeout=5)
    if r.status_code == 200:
        data = r.json()
        count = len(data) if isinstance(data, list) else len(str(data))
        print(f"   ✓ Status: {r.status_code} - Retorna {count} registros")
        tests_passed += 1
    else:
        print(f"   ✗ Status: {r.status_code} - {r.text[:80]}")
        tests_failed += 1
except Exception as e:
    print(f"   ✗ ERROR: {str(e)[:80]}")
    tests_failed += 1

# Test 4: Perfil/me (requires token)
print("\n✅ TEST 4: GET /perfil/me (REQUIRES JWT)")
try:
    r = requests.get(f"{base}/perfil/me", timeout=5)
    if r.status_code == 401:
        print(f"   ✓ Status: {r.status_code} - Correct: No token provided")
        tests_passed += 1
    else:
        print(f"   ✗ Status: {r.status_code} - Expected 401")
        tests_failed += 1
except Exception as e:
    print(f"   ✗ ERROR: {str(e)[:80]}")
    tests_failed += 1

# Test 5: Coordinador Dashboard (requires token)
print("\n✅ TEST 5: GET /coordinador/dashboard (REQUIRES JWT)")
try:
    r = requests.get(f"{base}/coordinador/dashboard", timeout=5)
    if r.status_code == 401:
        print(f"   ✓ Status: {r.status_code} - Correct: No token provided")
        tests_passed += 1
    else:
        print(f"   ✗ Status: {r.status_code} - Expected 401")
        tests_failed += 1
except Exception as e:
    print(f"   ✗ ERROR: {str(e)[:80]}")
    tests_failed += 1

# Summary
print("\n" + "="*70)
print(f"📊 RESULTS: {tests_passed} passed ✓ | {tests_failed} failed ✗")
print("="*70 + "\n")

sys.exit(0 if tests_failed == 0 else 1)
