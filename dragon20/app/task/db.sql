CREATE TABLE IF NOT EXISTS images (
  id int NOT NULL AUTO_INCREMENT,
  status int,
  name varchar(255),
  owner varchar(255),
  PRIMARY KEY (id)
);
