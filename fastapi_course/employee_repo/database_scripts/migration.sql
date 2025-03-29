CREATE TABLE employees (
  id serial primary key,
  first_name text not null,
  last_name text not null,
  email text unique not null,
  salary numeric not null,
  image_url text,
  is_active boolean default true
)