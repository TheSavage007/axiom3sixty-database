# Conceptual Model

The conceptual model names the things the business cares about and how they relate, with no attention yet to keys or data types.

## Entities

| Entity | What it represents |
|---|---|
| Floor Plan | A casita or ADU model the company sells, such as Casa Luna or Casa Mia |
| Plan Feature | A selling point attached to a plan, such as SIPs construction or permitting included |
| Architectural Style | A finish package a buyer can preview: Contemporary Farmhouse, Craftsman, Modern Farmhouse, Desert Modern |
| Render View | A room or angle in a preview image: exterior, living room, kitchen, bedroom, bathroom |
| ADU Render | A generated preview image for one plan, in one style, from one view |
| Lead | A homeowner who submitted the Property Check form or another lead form |
| Contact Message | A general inquiry from the Contact form |
| App User | A staff account; agents work leads from the agent dashboard |
| Advisory Board Member | A person shown on the Advisory Board page |

## Relationships

1. A floor plan has many features.
2. A floor plan, a style, and a view together identify exactly one render. Renders are a cache, so many combinations may not exist yet.
3. A lead may name a floor plan and a style they are interested in. Neither is required.
4. A lead may be assigned to one agent. An agent works many leads.
5. Contact messages and board members stand alone. They do not depend on other entities.

## Business Rules

1. Every lead needs a name, an email, and a property address, because the Property Check feature looks up the lot.
2. A lead cannot be contacted before it was submitted.
3. The board has exactly one chair, shown first.
