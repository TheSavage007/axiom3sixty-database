# Data Dictionary

Every table and column in the schema.

## floor_plans

| Column | Type | Description |
|---|---|---|
| plan_id | INTEGER | Floor plan key |
| plan_name | VARCHAR(60) | Marketing name of the plan |
| sqft | INTEGER | Conditioned square footage |
| base_price | DECIMAL(10,2) | Starting price in dollars |
| bedrooms | INTEGER | Bedroom count |
| bathrooms | DECIMAL(3,1) | Bathroom count, half baths as .5 |
| width_ft | INTEGER | Footprint width in feet |
| depth_ft | INTEGER | Footprint depth in feet |
| description | TEXT | Plan summary |

## plan_features

| Column | Type | Description |
|---|---|---|
| plan_id | INTEGER | Floor plan key |
| feature | VARCHAR(80) | One selling point |

## architectural_styles

| Column | Type | Description |
|---|---|---|
| style_id | INTEGER | Style key |
| style_name | VARCHAR(60) | Finish package name |

## render_views

| Column | Type | Description |
|---|---|---|
| view_id | INTEGER | View key |
| view_code | VARCHAR(20) | Machine code for the view |
| view_label | VARCHAR(40) | Display label |

## adu_renders

| Column | Type | Description |
|---|---|---|
| render_id | INTEGER | Render key |
| plan_id | INTEGER | Floor plan key |
| style_id | INTEGER | Style key |
| view_id | INTEGER | View key |
| image_url | VARCHAR(500) | Location of the generated image |
| created_at | TIMESTAMP | When the row was created |

## app_users

| Column | Type | Description |
|---|---|---|
| user_id | INTEGER | User key |
| full_name | VARCHAR(80) | Person name |
| email | VARCHAR(120) | Email address |
| role | VARCHAR(10) | admin or user |
| is_agent | BOOLEAN | True if the user works leads |
| created_at | TIMESTAMP | When the row was created |

## advisory_board_members

| Column | Type | Description |
|---|---|---|
| member_id | INTEGER | Board member key |
| full_name | VARCHAR(80) | Person name |
| board_role | VARCHAR(10) | chair or member |
| title | VARCHAR(80) | Displayed title |
| bio | TEXT | Displayed biography |
| photo_url | VARCHAR(500) | Displayed photo |
| display_order | INTEGER | Card order on the page, 1 is first |

## leads

| Column | Type | Description |
|---|---|---|
| lead_id | INTEGER | Lead key |
| full_name | VARCHAR(80) | Person name |
| email | VARCHAR(120) | Email address |
| phone | VARCHAR(30) | Phone number, optional |
| street | VARCHAR(120) | Property street address |
| city | VARCHAR(80) | Property city |
| zip | VARCHAR(12) | Property ZIP code |
| plan_id | INTEGER | Floor plan key |
| style_id | INTEGER | Style key |
| source | VARCHAR(30) | Form the lead came from |
| status | VARCHAR(20) | Pipeline stage |
| submitted_at | TIMESTAMP | Submission time |
| first_contacted_at | TIMESTAMP | Time of first contact by an agent |
| assigned_user_id | INTEGER | Agent working the lead |

## contact_messages

| Column | Type | Description |
|---|---|---|
| message_id | INTEGER | Message key |
| full_name | VARCHAR(80) | Person name |
| email | VARCHAR(120) | Email address |
| interest | VARCHAR(120) | Topic the visitor picked |
| message | VARCHAR(2000) | Message body |
| submitted_at | TIMESTAMP | Submission time |
