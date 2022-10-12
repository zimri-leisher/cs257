CREATE TABLE nocs (id integer, noc text);
CREATE TABLE games (id integer, name text, location text, season text, year integer);
CREATE TABLE people (id integer, name text, sex text);
CREATE TABLE performances (id integer, person integer, noc integer, game integer);
CREATE TABLE medals (id integer, performance integer, sport text, event text, medal_type text);
