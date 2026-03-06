CREATE SCHEMA IF NOT EXISTS volunteer_shema;

-- Users
CREATE TABLE volunteer_shema.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(30) NOT NULL,
    surname VARCHAR(30) NOT NULL,
    sex VARCHAR(10),
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events
CREATE TABLE volunteer_shema.events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    event_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Many-to-many таблица связи
CREATE TABLE volunteer_shema.event_member_table (
    user_id UUID NOT NULL,
    event_id UUID NOT NULL,

    PRIMARY KEY (user_id, event_id),

    CONSTRAINT fk_event_member_user
        FOREIGN KEY (user_id)
        REFERENCES volunteer_shema.users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_event_member_event
        FOREIGN KEY (event_id)
        REFERENCES volunteer_shema.events(id)
        ON DELETE CASCADE
);

-- Forms (1:1 с пользователем)
CREATE TABLE volunteer_shema.forms (
    user_id UUID PRIMARY KEY,
    form_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_form
        FOREIGN KEY(user_id)
        REFERENCES volunteer_shema.users(id)
        ON DELETE CASCADE
);