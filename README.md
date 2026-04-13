# volunteer_clean_stage1_plus

## Quick start

```bash
docker compose down -v
docker compose up --build
```

Open:
- app: http://localhost:8000
- phpMyAdmin: http://localhost:8081

## Demo users

- admin: `admin` / `admin12345`
- org: `org_demo` / `org12345`
- volunteer: `volunteer_demo` / `vol12345`

## What is already included

- clean Django + MySQL + Docker base
- volunteer profile with structured languages, skills and availability
- organizer dashboard with event CRUD and role CRUD
- applications, assignments and notifications
- seeded dictionaries and demo users
- logout returns to the landing page

## damp create
docker exec volunteer-db-1 sh -c "mysqldump --default-character-set=utf8mb4 --no-tablespaces -uapp -papppass volunteers_db > /tmp/volunteers_dump.sql"

docker cp volunteer-db-1:/tmp/volunteers_dump.sql .\volunteers_dump.sql

docker exec volunteer-db-1 rm /tmp/volunteers_dump.sql

## damp use
cmd /c "docker exec -i volunteer-db-1 mysql --default-character-set=utf8mb4 -uapp -papppass volunteers_db < volunteers_dump.sql"