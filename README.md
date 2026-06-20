# Madinaty

A community complaint management system built with **Django 5.2** and **Django REST Framework 3.16**. Citizens can submit complaints with media, track their status, and receive push notifications. Administrators manage complaints, categories, and news announcements.

## Tech Stack

| Component     | Technology                                |
|---------------|-------------------------------------------|
| Framework     | Django 5.2 + DRF 3.16                     |
| Auth          | SimpleJWT (dual User/Admin token models)  |
| Database      | PostgreSQL (SQLite for local dev)         |
| Push Alerts   | Firebase Cloud Messaging (FCM)            |
| SMS           | Twilio (phone verification)               |
| Storage       | WhiteNoise (static), local media files    |

## Requirements

- Python 3.13+
- PostgreSQL (optional — SQLite is used when no DATABASE_URL is set)

## Installation

### 1. Clone and enter the project

```bash
git clone https://github.com/AmmarHabib27/Madinaty
cd Madinaty
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

Minimal local setup (defaults to SQLite):

```
SECRET_KEY=your-secret-key-here
ENVIRONMENT=staging
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Leave blank to use SQLite
DATABASE_URL=

TIME_ZONE=Africa/Cairo
```

For PostgreSQL, set `DATABASE_URL`:

```
DATABASE_URL=postgres://user:password@localhost:5432/madinaty_main
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create an admin account

```bash
python manage.py createsuperuser --phone 01000000000 --name "Admin Name"
```

### 7. Start the server

```bash
python manage.py runserver
```

The API is available at `http://localhost:8000/api/`.

## API Overview

All responses are wrapped in a standard envelope:

```json
{
  "code": 200,
  "message": "",
  "data": { ... }
}
```

Authentication is via **JWT Bearer tokens**. Two user types exist:
- **Admin** — manages complaints, categories, news
- **User** (Client) — regular citizens who submit complaints

### Client Endpoints (`/api/client/`)

#### Auth

| Method | Endpoint                          | Description              |
|--------|-----------------------------------|--------------------------|
| POST   | `auth/register/`                  | Register new account     |
| POST   | `auth/login/`                     | Login                    |
| POST   | `auth/resend-otp/`                | Resend verification OTP  |
| POST   | `auth/verify-otp/`                | Verify phone with OTP    |
| POST   | `auth/forget-password/`           | Request password reset   |
| POST   | `auth/forget-password/confirm/`   | Confirm reset with OTP   |
| POST   | `auth/reset-password/`            | Reset password           |
| POST   | `auth/token/refresh/`             | Refresh access token     |
| POST   | `auth/logout/`                    | Logout (blacklist token) |
| POST   | `auth/update-player-id/`          | Update FCM push token    |

#### Profile

| Method | Endpoint                            | Description            |
|--------|-------------------------------------|------------------------|
| GET    | `profile/`                          | Get profile            |
| PATCH  | `profile/`                          | Update profile         |
| DELETE | `profile/remove-profile-picture/`   | Remove profile picture |

#### Complaints

| Method | Endpoint                     | Description                    |
|--------|------------------------------|--------------------------------|
| GET    | `complaints/`                | List own complaints (paginated)|
| POST   | `complaints/`                | Create a complaint             |
| GET    | `complaints/<id>/`           | Get complaint detail           |
| DELETE | `complaints/<id>/`           | Delete own complaint           |

#### News & Categories

| Method | Endpoint              | Description            |
|--------|-----------------------|------------------------|
| GET    | `news/`               | List news (paginated)  |
| GET    | `news/<id>/`          | Get news detail        |
| GET    | `categories/`         | List active categories |

### Admin Endpoints (`/api/admin/`)

#### Auth

| Method | Endpoint                 | Description              |
|--------|--------------------------|--------------------------|
| POST   | `auth/login/`            | Admin login              |
| POST   | `auth/token/refresh/`    | Refresh admin token      |
| POST   | `auth/logout/`           | Logout (blacklist token) |
| POST   | `auth/change-password/`  | Change password          |

#### Profile

| Method | Endpoint   | Description    |
|--------|------------|----------------|
| GET    | `profile/` | Get profile    |
| PATCH  | `profile/` | Update profile |

#### Users

| Method | Endpoint                         | Description            |
|--------|----------------------------------|------------------------|
| GET    | `users/`                         | List all users         |
| POST   | `users/<id>/toggle-active/`      | Activate/deactivate    |

#### Complaints

| Method | Endpoint                     | Description                        |
|--------|------------------------------|------------------------------------|
| GET    | `complaints/`                | List all complaints (filterable)   |
| GET    | `complaints/map/`            | List complaints for map view       |
| GET    | `complaints/<id>/`           | Get complaint detail               |
| PATCH  | `complaints/<id>/`           | Update status, priority, comment   |

Query parameters for `GET /api/admin/complaints/`:

| Param         | Values                                          |
|---------------|-------------------------------------------------|
| `status`      | `placed`, `valid`, `on_hold`, `rejected`, `resolved` |
| `priority`    | `low`, `intermediate`, `high`                   |
| `category_id` | Category ID                                     |

PATCH body for `complaints/<id>/`:

```json
{
  "status": "valid",
  "priority": "high",
  "admin_comment": "We are working on it."
}
```

#### Categories

| Method | Endpoint                | Description          |
|--------|-------------------------|----------------------|
| GET    | `categories/`           | List all categories  |
| POST   | `categories/`           | Create category      |
| GET    | `categories/<id>/`      | Get category detail  |
| PATCH  | `categories/<id>/`      | Update category      |
| DELETE | `categories/<id>/`      | Delete category      |

#### News

| Method | Endpoint        | Description        |
|--------|-----------------|--------------------|
| GET    | `news/`         | List all news      |
| POST   | `news/`         | Create news post   |
| GET    | `news/<id>/`    | Get news detail    |
| PATCH  | `news/<id>/`    | Update news        |
| DELETE | `news/<id>/`    | Delete news        |

## Django Admin Panel

The standard Django admin panel is available at `/django-admin/`. Use the superuser credentials created during setup.

## Environment Variables

| Variable                          | Default          | Description                           |
|-----------------------------------|------------------|---------------------------------------|
| `SECRET_KEY`                      | —                | Django secret key (required)          |
| `ENVIRONMENT`                     | `production`     | `production` or `staging`             |
| `DEBUG`                           | `False`          | Debug mode                            |
| `ALLOWED_HOSTS`                   | `*`              | Comma-separated hosts                 |
| `DATABASE_URL`                    | —                | PostgreSQL DSN (blank = SQLite)       |
| `CORS_ALLOW_ALL_ORIGINS`          | `False`          | Allow all CORS origins                |
| `ACCESS_TOKEN_LIFETIME_MINUTES`   | `1440` (24h)     | JWT access token TTL                  |
| `REFRESH_TOKEN_LIFETIME_MINUTES`  | `43200` (30d)    | JWT refresh token TTL                 |
| `TIME_ZONE`                       | `Africa/Cairo`   | Server timezone                       |
| `FCM_SERVICE_ACCOUNT_JSON`        | —                | Base64-encoded Firebase service key   |
| `TWILIO_ACCOUNT_SID`              | —                | Twilio SID (phone verification)       |
| `TWILIO_AUTH_TOKEN`               | —                | Twilio auth token                     |
| `TWILIO_PHONE_NUMBER`             | —                | Twilio sender number                  |
| `EMAIL_*`                         | Console backend  | SMTP config for emails                |
