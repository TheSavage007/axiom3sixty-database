# Physical Model

The physical model is the schema in [sql/schema.sql](../sql/schema.sql). It targets SQLite for portability and runs on PostgreSQL with one change: swap `INTEGER PRIMARY KEY` for `GENERATED ALWAYS AS IDENTITY`.

## Data Types

| Choice | Why |
|---|---|
| `DECIMAL(10,2)` for base_price | Money never goes in a floating point type |
| `DECIMAL(3,1)` for bathrooms | Plans list half baths (1.5) |
| `VARCHAR` lengths match the server side limits | The live lead function clamps name to 80, email to 120, street to 120, city to 80, zip to 12, and messages to 2,000 characters. The columns enforce the same limits |
| `TIMESTAMP` for submitted and contacted times | Speed to lead is measured in hours |

## Constraints

- **CHECK** on role, source, and status so only known values get in.
- **CHECK** that first contact cannot come before submission.
- **UNIQUE (plan_id, style_id, view_id)** on renders. This is what makes the app's fetch or generate logic safe: a second request for the same image finds the cached row instead of paying to generate a duplicate.
- **ON DELETE CASCADE** on plan features, so removing a plan cleans up its feature rows.
- Foreign keys from leads to plans and styles are nullable, because a contact form lead may not name a plan.

## Indexes

Indexes sit on the columns the business filters and groups by: `leads.submitted_at`, `status`, `city`, `plan_id`, and `assigned_user_id`, plus `contact_messages.submitted_at`. Renders need no extra index because the UNIQUE constraint already builds one on the lookup key.

## Security and Backup

1. **Least privilege.** Two roles: admin and user. Only admins read lead contact details; agents see leads assigned to them.
2. **Server side validation.** Lead and contact submissions are validated and length clamped in a server function before they touch storage, and a hidden honeypot field drops bot submissions silently.
3. **No real data in this repo.** Every person in `seed_synthetic.sql` is generated.
4. **Backups.** Nightly snapshot with 30 day retention, plus an export before any schema change.
