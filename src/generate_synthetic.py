"""Generate synthetic seed data for the Axiom3Sixty database.

Every person, email, phone number, and street address here is invented.
Emails use the reserved example.com domain and phone numbers use the
fictional 555-01xx range, so nothing can reach a real person.

Usage:
    python src/generate_synthetic.py
"""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 360

# Public catalog, as listed on the live site
PLANS = [
    # name, sqft, price, beds, baths, width, depth, description
    ("Casa Mia", 710, 145000, 1, 1.0, 26, 28, "Compact one bedroom casita for a home office, guest suite, or rental."),
    ("Casa Mio", 710, 150000, 1, 1.5, 28, 31, "One bedroom casita with a powder room for guests."),
    ("Casa Lunita", 875, 160000, 2, 1.5, 28, 34, "Two bedroom layout sized for small lots."),
    ("Casa Reinita", 915, 170000, 2, 1.0, 32, 42, "Two bedroom plan with an open living core."),
    ("Casa Reina", 988, 180000, 2, 2.0, 34, 46, "Two bedroom, two bath plan with a split floor layout."),
    ("Casa Luna", 995, 195000, 2, 2.0, 30, 38, "Largest two bedroom, two bath casita in the line."),
]
COMMON_FEATURES = ["SIPs construction", "Permitting included", "Concrete tile roofing"]
STYLES = ["Contemporary Farmhouse", "Craftsman", "Modern Farmhouse", "Desert Modern"]
VIEWS = [("exterior", "Exterior"), ("living", "Living Room"), ("kitchen", "Kitchen"),
         ("bedroom", "Bedroom"), ("bath", "Bathroom")]

# Service area named on the live site, weighted toward the East Valley
CITIES = {
    "Mesa": ("85203", 16), "Gilbert": ("85234", 15), "Chandler": ("85225", 14),
    "Queen Creek": ("85142", 11), "San Tan Valley": ("85140", 9), "Scottsdale": ("85251", 10),
    "Tempe": ("85281", 9), "Phoenix (Ahwatukee)": ("85044", 10), "Phoenix": ("85016", 6),
}

FIRST = ["Avery", "Marcus", "Elena", "Jordan", "Priya", "Darnell", "Sofia", "Tobias", "Keisha",
         "Mateo", "Hannah", "Rashid", "Lucia", "Grant", "Imani", "Wesley", "Nadia", "Colton",
         "Yesenia", "Brennan", "Talia", "Quentin", "Marisol", "Dante", "Celeste", "Hector",
         "Brooke", "Andre", "Lena", "Felix", "Renata", "Silas", "Monique", "Arturo", "Joelle"]
LAST = ["Whitaker", "Delgado", "Okafor", "Brennan", "Castillo", "Hargrove", "Nguyen", "Pruitt",
        "Valdez", "Ashford", "Mbeki", "Lindqvist", "Serrano", "Holloway", "Banerjee", "Crowe",
        "Fontaine", "Ibarra", "Kessler", "Montoya", "Rourke", "Sandoval", "Tillman", "Vasquez",
        "Yarbrough", "Zeller", "Abernathy", "Calloway", "Duarte", "Ellison"]
STREETS = ["Saguaro Bloom Way", "Copper Mesa Dr", "Ironwood Ridge Ln", "Desert Lark Ave",
           "Palo Verde Crest St", "Sunstone Trail", "Mesquite Hollow Rd", "Quail Run Ct",
           "Agave Point Pl", "Ocotillo Shadow Dr", "Red Rock Vista Ln", "Cholla Canyon Way"]
INTERESTS = ["Backyard casita", "Rental income unit", "Space for aging parents", "Home office",
             "Financing options", "Custom design", "SIPs construction"]


def person(rng: random.Random, used: set[str]) -> tuple[str, str]:
    while True:
        first, last = rng.choice(FIRST), rng.choice(LAST)
        name = f"{first} {last}"
        if name not in used:
            used.add(name)
            return name, f"{first}.{last}{rng.randint(1, 99)}@example.com".lower()


def phone(rng: random.Random) -> str:
    return f"(480) 555-01{rng.randint(0, 99):02d}"


def sql_value(v) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def insert(table: str, cols: list[str], rows: list[tuple]) -> str:
    body = ",\n".join("  (" + ", ".join(sql_value(v) for v in r) + ")" for r in rows)
    return f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n{body};\n"


def build(seed: int = SEED) -> dict[str, list[tuple]]:
    rng = random.Random(seed)
    data: dict[str, list[tuple]] = {}

    data["floor_plans"] = [(i + 1, *p) for i, p in enumerate(PLANS)]
    feats = []
    for pid, p in enumerate(PLANS, start=1):
        feats.append((pid, f"{p[3]} Bed / {p[4]:g} Bath"))
        feats.append((pid, f"Approx. {p[1]} sq ft"))
        feats.extend((pid, f) for f in COMMON_FEATURES)
    data["plan_features"] = feats
    data["architectural_styles"] = [(i + 1, s) for i, s in enumerate(STYLES)]
    data["render_views"] = [(i + 1, code, label) for i, (code, label) in enumerate(VIEWS)]

    combos = [(p, s, v) for p in range(1, 7) for s in range(1, 5) for v in range(1, 6)]
    cached = sorted(rng.sample(combos, 78))
    start = datetime(2026, 6, 1)
    data["adu_renders"] = [
        (i + 1, p, s, v, f"https://renders.example.com/plan{p}/style{s}/view{v}.jpg",
         (start + timedelta(hours=rng.randint(0, 24 * 120))).strftime("%Y-%m-%d %H:%M:%S"))
        for i, (p, s, v) in enumerate(cached)
    ]

    used: set[str] = set()
    users = []
    for uid, (role, agent) in enumerate([("admin", False), ("user", True), ("user", True), ("user", True)], 1):
        name, email = person(rng, used)
        users.append((uid, name, email.replace("@", ".team@"), role, agent, "2026-01-05 09:00:00"))
    data["app_users"] = users

    board = []
    for order in range(1, 8):
        name, _ = person(rng, used)
        role = "chair" if order == 1 else "member"
        title = "Chair, Advisory Board" if order == 1 else "Board Member"
        board.append((order, name, role, title, "Synthetic bio for portfolio demonstration.", None, order))
    data["advisory_board_members"] = board

    cities = list(CITIES)
    weights = [CITIES[c][1] for c in cities]
    funnel = ["new", "contacted", "site_visit", "proposal", "won", "lost"]
    leads = []
    lead_start = datetime(2026, 1, 1)
    for lid in range(1, 421):
        name, email = person(rng, used)
        city = rng.choices(cities, weights)[0]
        submitted = lead_start + timedelta(minutes=rng.randint(0, 60 * 24 * 300))
        # Demand rises in spring and fall; trim a share of summer submissions
        if submitted.month in (6, 7, 8) and rng.random() < 0.35:
            submitted -= timedelta(days=rng.randint(60, 120))
        source = rng.choices(["property_check", "custom_design", "chat", "contact_form"], [62, 14, 14, 10])[0]
        status = rng.choices(funnel, [14, 30, 20, 14, 9, 13])[0]
        contacted = None
        if status != "new":
            hours = rng.lognormvariate(2.6, 0.9)  # median about 13 hours
            contacted = submitted + timedelta(hours=hours)
        plan = rng.choices(range(1, 7), [14, 10, 18, 12, 22, 24])[0] if source != "contact_form" else None
        style = rng.randint(1, 4) if plan and rng.random() < 0.8 else None
        agent = rng.choice([2, 3, 4]) if status != "new" else None
        leads.append((
            lid, name, email, phone(rng) if rng.random() < 0.85 else None,
            f"{rng.randint(100, 9899)} E {rng.choice(STREETS)}", city, CITIES[city][0],
            plan, style, source, status, submitted.strftime("%Y-%m-%d %H:%M:%S"),
            contacted.strftime("%Y-%m-%d %H:%M:%S") if contacted else None, agent,
        ))
    data["leads"] = sorted(leads, key=lambda r: r[11])
    data["leads"] = [(i + 1, *r[1:]) for i, r in enumerate(data["leads"])]

    msgs = []
    for mid in range(1, 121):
        name, email = person(rng, used)
        ts = lead_start + timedelta(minutes=rng.randint(0, 60 * 24 * 300))
        interest = rng.choice(INTERESTS)
        msgs.append((mid, name, email, interest, f"Interested in {interest.lower()}. Please reach out.",
                     ts.strftime("%Y-%m-%d %H:%M:%S")))
    data["contact_messages"] = sorted(msgs, key=lambda r: r[5])
    return data


COLUMNS = {
    "floor_plans": ["plan_id", "plan_name", "sqft", "base_price", "bedrooms", "bathrooms", "width_ft",
                    "depth_ft", "description"],
    "plan_features": ["plan_id", "feature"],
    "architectural_styles": ["style_id", "style_name"],
    "render_views": ["view_id", "view_code", "view_label"],
    "adu_renders": ["render_id", "plan_id", "style_id", "view_id", "image_url", "created_at"],
    "app_users": ["user_id", "full_name", "email", "role", "is_agent", "created_at"],
    "advisory_board_members": ["member_id", "full_name", "board_role", "title", "bio", "photo_url",
                               "display_order"],
    "leads": ["lead_id", "full_name", "email", "phone", "street", "city", "zip", "plan_id", "style_id",
              "source", "status", "submitted_at", "first_contacted_at", "assigned_user_id"],
    "contact_messages": ["message_id", "full_name", "email", "interest", "message", "submitted_at"],
}


def main() -> None:
    data = build()
    header = ("-- Synthetic seed data. Every name, email, phone, and address is invented.\n"
              "-- Generated by src/generate_synthetic.py (seed 360).\n\n")
    sql = header + "\n".join(insert(t, COLUMNS[t], data[t]) for t in COLUMNS)
    (ROOT / "sql" / "seed_synthetic.sql").write_text(sql)
    with open(ROOT / "data" / "synthetic_leads.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLUMNS["leads"])
        w.writerows(data["leads"])
    print({t: len(r) for t, r in data.items()})


if __name__ == "__main__":
    main()
