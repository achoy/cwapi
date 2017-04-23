drop table if exists metaphotos;
drop index if exists photo_index;
create table metaphotos (
  id integer primary key autoincrement,
  pkey text not null,
  fname text not null,
  floc text not null,
  size integer,
  w integer,
  h integer,
  title text,
  datetime text
);
create index photo_src_index on metaphotos(pkey, fname, floc);
