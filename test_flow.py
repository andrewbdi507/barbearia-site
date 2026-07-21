import requests, json

BASE = "http://localhost:8000/api/v1"

print("=== Login ===")
r = requests.post(f"{BASE}/auth/login", json={"email": "admin@blackhouse.com", "password": "Admin123!", "tenant_id": "cb359a53-05a3-4434-b7cd-fa75cb970975"})
data = r.json()
TOKEN = data.get("access_token", "")
print(f"Status: {r.status_code} | Token: {TOKEN[:40]}...")

if not TOKEN:
    print(f"Error: {data}")
    exit()

headers = {"Authorization": f"Bearer {TOKEN}"}

# GET services
print("\n=== GET /services ===")
r = requests.get(f"{BASE}/scheduling/services", headers=headers)
print(f"Status: {r.status_code}")
result = r.json()
if isinstance(result, list):
    for s in result:
        print(f"  {s['name']}: R${s['price_cents']/100:.2f} ({s['duration_minutes']}min) {'ACTIVE' if s.get('is_active') else 'INACTIVE'}")
else:
    print(json.dumps(result, indent=2)[:400])

# POST service
print("\n=== POST Corte ===")
svc = {"name": "Corte Masculino", "description": "Corte tradicional", "price_cents": 4000, "duration_minutes": 30, "is_active": True}
r = requests.post(f"{BASE}/scheduling/services", headers=headers, json=svc)
print(f"Status: {r.status_code} | {json.dumps(r.json())[:200]}")

# POST barba
print("\n=== POST Barba ===")
r = requests.post(f"{BASE}/scheduling/services", headers=headers, json={"name": "Barba", "price_cents": 2500, "duration_minutes": 20, "is_active": True})
print(f"Status: {r.status_code} | {json.dumps(r.json())[:200]}")

# POST combo
print("\n=== POST Combo ===")
r = requests.post(f"{BASE}/scheduling/services", headers=headers, json={"name": "Corte + Barba", "price_cents": 6000, "duration_minutes": 50, "is_active": True})
print(f"Status: {r.status_code} | {json.dumps(r.json())[:200]}")

# Final list
print("\n=== Final services ===")
r = requests.get(f"{BASE}/scheduling/services", headers=headers)
for s in r.json():
    price = s.get('price_cents') or s.get('base_price') or s.get('effective_price', 0)
    name = s.get('name', s.get('id', '?'))
    print(f"  {name}: R${price/100:.2f} (id={s.get('id','?')[:8]}...)")
