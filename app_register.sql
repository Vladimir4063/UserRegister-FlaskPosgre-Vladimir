CREATE table users (
  id SERIAL primary KEY,
  name varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  id_role int NOT NULL,
  password varchar(100) NOT NULL
)

CREATE table role_user (
  id int not null primary KEY,
  role varchar(100) NOT NULL
)

-- INSERT role_user
insert into role_user (id, role) values (1, 'Premium')
insert into role_user (id, role) values (2, 'Standard')