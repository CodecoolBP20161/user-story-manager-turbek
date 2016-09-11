create table if not EXISTS entries (
  id integer primary key autoincrement,
  title text not null,
  story text not null,
  criteria text not null,
  value integer not null,
  estimation integer not null,
  status text not null
);