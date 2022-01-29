CREATE TABLE url(
  id int AUTO_INCREMENT UNIQUE,
  shortened_url varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci UNIQUE,
  original_url varchar(1000) NOT NULL,
  PRIMARY KEY(id, shortened_url)
);
CREATE TABLE url_stats(
  shortened_url varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci UNIQUE PRIMARY KEY,
  time_accessed mediumtext,
  datetime_created datetime,
  FOREIGN KEY (shortened_url) REFERENCES url(shortened_url) ON DELETE CASCADE
);