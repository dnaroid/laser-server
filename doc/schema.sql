CREATE TABLE author
(
  author_id   INTEGER NOT NULL,
  author_name TEXT,
  expired     TEXT,
  PRIMARY KEY ("author_id)", "unique (author_name")
);
CREATE TABLE comments
(
  comment_id    INTEGER NOT NULL,
  news_id       INTEGER,
  comment_text  TEXT,
  creation_date TEXT,
  PRIMARY KEY ("comment_id)", "foreign key(news_id"),
  FOREIGN KEY (news_id) REFERENCES news (news_id)
    DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE migrate_version
(
  repository_id   TEXT PRIMARY KEY NOT NULL,
  repository_path TEXT,
  version         INTEGER
);
CREATE TABLE news
(
  news_id           INTEGER PRIMARY KEY NOT NULL,
  title             TEXT,
  short_text        TEXT,
  full_text         TEXT,
  creation_date     TEXT,
  modification_date TEXT
);
CREATE TABLE news_author
(
  author_id INTEGER,
  news_id   INTEGER,
  FOREIGN KEY (news_id) REFERENCES news (news_id)
    DEFERRABLE INITIALLY DEFERRED,
  FOREIGN KEY (author_id) REFERENCES author (author_id)
    DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE news_tag
(
  tag_id  INTEGER,
  news_id INTEGER,
  FOREIGN KEY (news_id) REFERENCES news (news_id)
    DEFERRABLE INITIALLY DEFERRED,
  FOREIGN KEY (tag_id) REFERENCES tag (tag_id)
    DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE roles
(
  user_id INTEGER NOT NULL,
  name    TEXT,
  PRIMARY KEY ("user_id)", "foreign key(user_id"),
  FOREIGN KEY (user_id) REFERENCES users (user_id)
    DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE tag
(
  tag_id   INTEGER NOT NULL,
  tag_name TEXT,
  PRIMARY KEY ("tag_id)", "unique (tag_name")
);
CREATE TABLE users
(
  user_id   INTEGER NOT NULL,
  user_name TEXT,
  password  TEXT,
  login     TEXT,
  PRIMARY KEY ("user_id)", "unique (user_name")
);