"""Pull supplier room names, LiteAPI's room mapping and master room lists from the LiteAPI sandbox.

Run by .github/workflows/fetch.yml with the LITEAPI_KEY repository secret. Writes data/live.json.
For each hotel: the master rooms from /data/hotel and every rate name from /hotels/rates with roomMapping on,
with LiteAPI's mappedRoomId (or null when the rate was left unmapped).
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import date, timedelta, datetime, timezone

KEY = os.environ.get("LITEAPI_KEY", "").strip()
API = "https://api.liteapi.travel/v3.0"
CITIES = ["Paris", "Barcelona", "Rome", "London", "Kraków", "Dubai", "New York", "Bangkok"]
HOTELS_PER_CITY = int(os.environ.get("HOTELS_PER_CITY", "25"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "live.json")


def call(path, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None, method="POST" if body else "GET",
                                 headers={"X-API-Key": KEY, "accept": "application/json", "content-type": "application/json"})
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            print(f"{e.code} {path}", file=sys.stderr)
            if e.code in (400, 401, 403, 404):
                return {}
        except Exception as e:  # noqa: BLE001
            print(f"retry {i + 1} {path}: {e}", file=sys.stderr)
        time.sleep(2 * (i + 1))
    return {}


def main():
    if not KEY:
        print("LITEAPI_KEY secret is missing. Add it in Settings > Secrets and variables > Actions.", file=sys.stderr)
        sys.exit(1)
    checkin = date.today() + timedelta(days=30)
    checkout = checkin + timedelta(days=1)
    out = {"fetched": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "source": "LiteAPI sandbox",
           "checkin": checkin.isoformat(), "occupancy": "2 adults, 1 night", "hotels": []}
    for city in CITIES:
        places = (call(f"/data/places?textQuery={urllib.parse.quote(city)}&language=en").get("data") or [])
        if not places:
            print(f"no place for {city}", file=sys.stderr)
            continue
        pid = places[0].get("placeId")
        rates = call("/hotels/rates", {"placeId": pid, "checkin": checkin.isoformat(), "checkout": checkout.isoformat(), "currency": "EUR",
                                       "guestNationality": "GB", "occupancies": [{"adults": 2}], "roomMapping": True, "includeHotelData": True,
                                       "maxRatesPerHotel": 200, "limit": HOTELS_PER_CITY, "timeout": 30})
        info = {h.get("id"): h for h in rates.get("hotels") or []}
        for h in (rates.get("data") or [])[:HOTELS_PER_CITY]:
            hid = h.get("hotelId")
            seen = {}
            for rt in h.get("roomTypes") or []:
                for r in rt.get("rates") or []:
                    name = (r.get("name") or "").strip()
                    m = r.get("mappedRoomId")
                    m = str(m) if m not in (None, "", 0) else None
                    k = (name, m)
                    seen.setdefault(k, {"name": name, "mapped": m, "n": 0, "board": r.get("boardName") or ""})
                    seen[k]["n"] += 1
            if not seen:
                continue
            d = call(f"/data/hotel?hotelId={urllib.parse.quote(hid)}").get("data") or {}
            master = [{"id": str(x.get("id")), "name": x.get("roomName") or x.get("name") or "", "maxOccupancy": x.get("maxOccupancy"),
                       "beds": [f"{b.get('quantity', 1)} x {b.get('bedType', '')}" for b in x.get("bedTypes") or []],
                       "size": x.get("roomSizeSquare")} for x in d.get("rooms") or []]
            out["hotels"].append({"id": hid, "name": d.get("name") or info.get(hid, {}).get("name") or hid, "city": city,
                                  "stars": d.get("starRating") or info.get(hid, {}).get("stars"), "master": master, "rates": list(seen.values())})
            time.sleep(0.2)
        print(f"{city}: {sum(1 for x in out['hotels'] if x['city'] == city)} hotels")
    if not out["hotels"]:
        print("No hotels returned. Keeping the previous file.", file=sys.stderr)
        sys.exit(1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    n = sum(len(h["rates"]) for h in out["hotels"])
    print(f"OK {len(out['hotels'])} hotels, {n} distinct rate names")


if __name__ == "__main__":
    import urllib.parse  # noqa: F401
    main()
