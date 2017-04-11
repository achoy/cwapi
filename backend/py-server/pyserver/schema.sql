drop table if exists metaphotos;
create table metaphotos (
  id integer primary key autoincrement,
  url text not null,
  size integer,
  title text
);
