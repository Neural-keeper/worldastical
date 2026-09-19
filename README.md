# Worldastical

Worldastical is a worldbuilding and creative planning tool designed to help writers, game designers, and storytellers structure a fictional universe with clarity and consistency. The project started as a lightweight Streamlit application for local use and has been expanded into a deployable web-oriented version under the `web_deployable/` directory.

## Project Overview

The app is built around a structured, section-based authoring workflow. Instead of forcing users to write an entire world from scratch in one long document, it breaks the process into meaningful categories such as:

- Name and identity
- Inspiration and tone
- Geology and landscape
- Political geography
- Symbolism and iconography
- Religion and belief systems
- Government and politics
- Historical events and context
- Flora, fauna, and ecology
- Unique world-building quirks

This approach makes the system easier to use, easier to revisit, and more scalable as a creative planning tool.

## Tech Stack in Phases

### Phase 1: Interface and application shell

The original version uses Python and Streamlit for the front-end experience.

- `app.py` serves as the entry point for the main application.
- The project is split into a page-based interface using the `pages/` directory.
- Reusable UI components are centralized in `ui/`.
- This phase prioritizes rapid prototyping and user-friendly interaction without requiring a heavy front-end stack.

### Phase 2: World model and content architecture

The creative logic is organized around a structured schema instead of freeform text alone.

- `core/default_world.py` defines the default data model for a world.
- Sections are intentionally modular to support narrative consistency.
- Each category can contain nested values, arrays, and metadata for deeper worldbuilding.

This enables a more systematic authoring process and sets the foundation for a future database-backed system.

### Phase 3: Persistence and local storage

The prototype currently stores world data in local JSON files.

- `core/storage.py` handles loading, saving, and deleting world files.
- World states are written into a local `worlds/` directory.
- This keeps the prototype simple and portable during early development.

### Phase 4: User flow and state management

World-building sessions are managed using Streamlit session state.

- The active world is tracked during navigation between sections.
- The user can create, load, and update world data in a guided flow.
- This pattern creates a clean authoring experience for a single-user prototype.

## Project Structure

- `app.py` — main Streamlit app entry point
- `core/` — world schema and persistence logic
- `pages/` — individual worldbuilding sections
- `ui/` — shared layout and content components
- `web_deployable/` — deployment-ready web version built for broader hosting and scalability

## Screenshot
<img width="1669" height="912" alt="Screenshot 2025-12-28 204445" src="https://github.com/user-attachments/assets/aa863f6f-fcdb-4382-ac9a-2f99d6743f37" />
