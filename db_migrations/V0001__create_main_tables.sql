-- Заявки с формы
CREATE TABLE leads (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    phone       VARCHAR(50)  NOT NULL,
    company     VARCHAR(255),
    message     TEXT,
    status      VARCHAR(50)  NOT NULL DEFAULT 'new',  -- new, in_progress, done
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Товары / каталог
CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    price       NUMERIC(12, 2),
    category    VARCHAR(100),
    image_url   TEXT,
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    sort_order  INTEGER      NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Отзывы клиентов
CREATE TABLE reviews (
    id          SERIAL PRIMARY KEY,
    author      VARCHAR(255) NOT NULL,
    company     VARCHAR(255),
    text        TEXT         NOT NULL,
    rating      SMALLINT     CHECK (rating BETWEEN 1 AND 5),
    is_published BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Выполненные работы (портфолио)
CREATE TABLE projects (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    client      VARCHAR(255),
    location    VARCHAR(255),
    image_url   TEXT,
    completed_at DATE,
    is_published BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
