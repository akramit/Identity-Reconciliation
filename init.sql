CREATE DATABASE identity_db;

USE identity_db;

CREATE TABLE Contact (
  id INT PRIMARY KEY AUTO_INCREMENT,
  phoneNumber VARCHAR(255) default NULL,
  email VARCHAR(255) default NULL,
  linkedId INT default NULL,
  linkPrecedence VARCHAR(255) NOT NULL,
  createdAt datetime NOT NULL,
  updatedAt datetime NOT NULL,
  deletedAt datetime default NULL,
  constraint two_type check (linkPrecedence in ('primary','secondary'))
);

CREATE TABLE Components(
  id INT NOT NULL,
  componentId INT default NULL,
  primary key (id),
  constraint foreign_key_cascade foreign key (id) references Contact (id) on delete
  cascade on update cascade
);
