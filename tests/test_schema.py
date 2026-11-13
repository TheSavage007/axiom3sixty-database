import sqlite3

import pytest

from src.run_queries import build_db, load_queries, run_all


@pytest.fixture()
def con():
    c = build_db()
    c.execute("PRAGMA foreign_keys = ON")
    return c


def test_seed_loads_with_no_foreign_key_violations(con):
    assert con.execute("PRAGMA foreign_key_check").fetchall() == []
    assert con.execute("SELECT COUNT(*) FROM leads").fetchone()[0] == 420


def test_render_cache_rejects_duplicates(con):
    p, s, v = con.execute("SELECT plan_id, style_id, view_id FROM adu_renders LIMIT 1").fetchone()
    with pytest.raises(sqlite3.IntegrityError):
        con.execute(
            "INSERT INTO adu_renders (plan_id, style_id, view_id, image_url) VALUES (?, ?, ?, 'x')", (p, s, v)
        )


def test_contact_before_submission_is_rejected(con):
    with pytest.raises(sqlite3.IntegrityError):
        con.execute(
            "INSERT INTO leads (full_name, email, street, city, zip, submitted_at, first_contacted_at, status)"
            " VALUES ('Test', 't@example.com', '1 Main', 'Mesa', '85203',"
            " '2026-05-02 10:00:00', '2026-05-01 10:00:00', 'contacted')"
        )


def test_unknown_status_is_rejected(con):
    with pytest.raises(sqlite3.IntegrityError):
        con.execute(
            "INSERT INTO leads (full_name, email, street, city, zip, submitted_at, status)"
            " VALUES ('Test', 't@example.com', '1 Main', 'Mesa', '85203', '2026-05-02 10:00:00', 'maybe')"
        )


def test_lead_to_missing_plan_is_rejected(con):
    with pytest.raises(sqlite3.IntegrityError):
        con.execute(
            "INSERT INTO leads (full_name, email, street, city, zip, submitted_at, plan_id)"
            " VALUES ('Test', 't@example.com', '1 Main', 'Mesa', '85203', '2026-05-02 10:00:00', 999)"
        )


def test_every_query_runs_and_returns_rows(con):
    results = run_all(con)
    assert set(results) == set(load_queries())
    assert all(len(df) > 0 for df in results.values())


def test_seed_contains_no_real_contact_domains(con):
    domains = {row[0].split("@")[1] for row in con.execute("SELECT email FROM leads UNION SELECT email FROM contact_messages")}
    assert domains == {"example.com"}
