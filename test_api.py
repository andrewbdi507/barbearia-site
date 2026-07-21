import requests
import json

BASE = "http://localhost:8000/api/v1"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwYWNhMmM4OC1jMWUxLTQ0YzAtOTMxNS0wZjJjMmRhZjFhMWIiLCJpYXQiOjE3ODQ1OTQ5MDEsImV4cCI6MTc4NDU5NTgwMSwidHlwZSI6ImFjY2VzcyIsImp0aSI6IjViMmE2ZTc0YTg5NzNjYjlmMzIzYWQwNGE3MmIxYWVkIiwidGVuYW50X2lkIjoiY2IzNTlhNTMtMDVhMy00NDM0LWI3Y2QtZmE3NWNiOTcwOTc1IiwicGVybWlzc2lvbnMiOltdLCJyb2xlIjoidW5rbm93biJ9.Ic0o_v456B7V-duKDf4_dtJdu9dEQYb8UBNGGaFl3uw"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Test services
print("=== GET /services ===")
r = requests.get(f"{BASE}/scheduling/services", headers=headers)
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2)[:500])

# Test create service
print("\n=== POST /services ===")
svc = {"name": "Corte Masculino", "description": "Corte tradicional", "price_cents": 4000, "duration_minutes": 30, "is_active": True}
r = requests.post(f"{BASE}/scheduling/services", headers=headers, json=svc)
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2)[:500])

# List again
print("\n=== GET /services (after create) ===")
r = requests.get(f"{BASE}/scheduling/services", headers=headers)
print(f"Status: {r.status_code}")
services = r.json()
print(f"Count: {len(services) if isinstance(services, list) else 'N/A'}")

# Test staff
print("\n=== GET /staff ===")
r = requests.get(f"{BASE}/staff", headers=headers)
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2)[:300])
