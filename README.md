# IS-211-Mandatory-Assignment – BUA Renting Service

A basic Python web application framework for the Norwegian equipment-lending service **BUA**.

## Stack

| Layer    | Technology            |
|----------|-----------------------|
| Web      | Flask 3               |
| ORM      | Flask-SQLAlchemy      |
| Database | PostgreSQL 16 (Docker)|
| Tests    | pytest + pytest-flask |

## Domain model

* **User** – a registered member of BUA
* **Item** – a piece of equipment available for loan
* **Loan** – records that a user has borrowed an item, and when it was returned

## API endpoints

| Method | Path                        | Description                    |
|--------|-----------------------------|--------------------------------|
| GET    | `/users/`                   | List all users                 |
| POST   | `/users/`                   | Register a new user            |
| GET    | `/users/<id>`               | Get a specific user            |
| DELETE | `/users/<id>`               | Delete a user                  |
| GET    | `/items/`                   | List all items (`?available=true` to filter) |
| POST   | `/items/`                   | Add a new item                 |
| GET    | `/items/<id>`               | Get a specific item            |
| PUT    | `/items/<id>`               | Update an item                 |
| DELETE | `/items/<id>`               | Delete an item                 |
| GET    | `/loans/`                   | List all loans (`?active=true` to filter) |
| POST   | `/loans/`                   | Create a new loan              |
| GET    | `/loans/<id>`               | Get a specific loan            |
| POST   | `/loans/<id>/return`        | Mark an item as returned       |

## Running with Docker Compose

```bash
docker compose up --build
```

The web application will be available at <http://localhost:5000>.

## Local development (without Docker)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env          # adjust DATABASE_URL if needed
flask --app app run --debug
```

For a local SQLite database (no Postgres required), leave `DATABASE_URL` unset –
the app defaults to `sqlite:///bua.db`.

## Running tests

```bash
pytest tests/ -v
```