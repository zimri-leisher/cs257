SELECT nocs.noc FROM nocs ORDER BY nocs.noc;

SELECT people.name from people, performances, nocs where people.id = performances.person AND performances.noc = nocs.id AND nocs.noc = 'JAM';

SELECT games.year, medals.sport, medals.event, medals.medal_type FROM medals, games, people, performances WHERE people.name = 'Gregory Efthimios "Greg" Louganis' AND performances.person = people.id AND medals.performance = performances.id AND games.id = performances.game AND medals.medal_type != 'NA';

SELECT DISTINCT nocs.noc, COUNT(medals.medal_type) FROM performances, nocs, medals WHERE performances.noc = nocs.id AND medals.medal_type = 'Gold' AND medals.performance = performances.id GROUP BY nocs.noc ORDER BY COUNT(medals.medal_type) DESC;
