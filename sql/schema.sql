-- Axiom3Sixty Group database: physical schema
-- Standard SQL, tested on SQLite 3. Runs on PostgreSQL with INTEGER PRIMARY KEY
-- swapped for GENERATED ALWAYS AS IDENTITY.

PRAGMA foreign_keys = ON;

-- ---------- Product catalog ----------

CREATE TABLE floor_plans (
    plan_id        INTEGER PRIMARY KEY,
    plan_name      VARCHAR(60)   NOT NULL UNIQUE,
    sqft           INTEGER       NOT NULL CHECK (sqft > 0),
    base_price     DECIMAL(10,2) NOT NULL CHECK (base_price > 0),
    bedrooms       INTEGER       NOT NULL CHECK (bedrooms >= 0),
    bathrooms      DECIMAL(3,1)  NOT NULL CHECK (bathrooms > 0),
    width_ft       INTEGER       NOT NULL CHECK (width_ft > 0),
    depth_ft       INTEGER       NOT NULL CHECK (depth_ft > 0),
    description    TEXT
);

CREATE TABLE plan_features (
    plan_id        INTEGER      NOT NULL REFERENCES floor_plans(plan_id) ON DELETE CASCADE,
    feature        VARCHAR(80)  NOT NULL,
    PRIMARY KEY (plan_id, feature)
);

CREATE TABLE architectural_styles (
    style_id       INTEGER PRIMARY KEY,
    style_name     VARCHAR(60)  NOT NULL UNIQUE
);

CREATE TABLE render_views (
    view_id        INTEGER PRIMARY KEY,
    view_code      VARCHAR(20)  NOT NULL UNIQUE,   -- exterior, living, kitchen, bedroom, bath
    view_label     VARCHAR(40)  NOT NULL
);

-- Cache of generated renders: one image per plan, style, and view.
-- The UNIQUE constraint is what makes "fetch or generate" safe to call repeatedly.
CREATE TABLE adu_renders (
    render_id      INTEGER PRIMARY KEY,
    plan_id        INTEGER      NOT NULL REFERENCES floor_plans(plan_id),
    style_id       INTEGER      NOT NULL REFERENCES architectural_styles(style_id),
    view_id        INTEGER      NOT NULL REFERENCES render_views(view_id),
    image_url      VARCHAR(500) NOT NULL,
    created_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (plan_id, style_id, view_id)
);

-- ---------- People ----------

CREATE TABLE app_users (
    user_id        INTEGER PRIMARY KEY,
    full_name      VARCHAR(80)  NOT NULL,
    email          VARCHAR(120) NOT NULL UNIQUE,
    role           VARCHAR(10)  NOT NULL CHECK (role IN ('admin', 'user')),
    is_agent       BOOLEAN      NOT NULL DEFAULT 0,
    created_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE advisory_board_members (
    member_id      INTEGER PRIMARY KEY,
    full_name      VARCHAR(80)  NOT NULL,
    board_role     VARCHAR(10)  NOT NULL CHECK (board_role IN ('chair', 'member')),
    title          VARCHAR(80),
    bio            TEXT,
    photo_url      VARCHAR(500),
    display_order  INTEGER      NOT NULL UNIQUE
);

-- ---------- Lead pipeline ----------

CREATE TABLE leads (
    lead_id             INTEGER PRIMARY KEY,
    full_name           VARCHAR(80)  NOT NULL,
    email               VARCHAR(120) NOT NULL,
    phone               VARCHAR(30),
    street              VARCHAR(120) NOT NULL,
    city                VARCHAR(80)  NOT NULL,
    zip                 VARCHAR(12)  NOT NULL,
    plan_id             INTEGER      REFERENCES floor_plans(plan_id),
    style_id            INTEGER      REFERENCES architectural_styles(style_id),
    source              VARCHAR(30)  NOT NULL DEFAULT 'property_check'
                        CHECK (source IN ('property_check', 'custom_design', 'chat', 'contact_form')),
    status              VARCHAR(20)  NOT NULL DEFAULT 'new'
                        CHECK (status IN ('new', 'contacted', 'site_visit', 'proposal', 'won', 'lost')),
    submitted_at        TIMESTAMP    NOT NULL,
    first_contacted_at  TIMESTAMP,
    assigned_user_id    INTEGER      REFERENCES app_users(user_id),
    CHECK (first_contacted_at IS NULL OR first_contacted_at >= submitted_at)
);

CREATE TABLE contact_messages (
    message_id     INTEGER PRIMARY KEY,
    full_name      VARCHAR(80)   NOT NULL,
    email          VARCHAR(120)  NOT NULL,
    interest       VARCHAR(120),
    message        VARCHAR(2000),
    submitted_at   TIMESTAMP     NOT NULL
);

-- ---------- Indexes for the questions the business asks most ----------

CREATE INDEX idx_leads_submitted   ON leads (submitted_at);
CREATE INDEX idx_leads_status      ON leads (status);
CREATE INDEX idx_leads_city        ON leads (city);
CREATE INDEX idx_leads_plan        ON leads (plan_id);
CREATE INDEX idx_leads_assigned    ON leads (assigned_user_id);
CREATE INDEX idx_contact_submitted ON contact_messages (submitted_at);
