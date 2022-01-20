--id
--hash
--original url

CREATE TABLE url(
  id int AUTO_INCREMENT UNIQUE,
  shortened_url varchar(7) UNIQUE,
  original_url varchar(1000) NOT NULL,
  PRIMARY KEY(id, shortened_url)
);