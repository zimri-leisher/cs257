import csv


# data from https://www.kaggle.com/code/heesoo37/olympic-history-data-a-thorough-analysis/report

# credit https://stackoverflow.com/questions/1151658/python-hashable-dicts
class HashableDict(dict):
    def __key(self):
        return tuple((k, self[k]) for k in sorted(self))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()


class Table:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
        self.rows = set()
        self.ids = {}
        self.next_id = 0

    def add(self, *row):
        row_dict = HashableDict({field: col for (field, col) in zip(self.fields, row)})
        if row_dict not in self.rows:
            self.next_id += 1
            self.ids[row_dict] = self.next_id - 1
            self.rows.add(row_dict)
            return self.next_id - 1
        else:
            # this row already exists. return its id
            return self.ids[row_dict]

    def write(self):
        with open(self.name + ".csv", "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["id"] + self.fields)
            writer.writeheader()
            for row in self.rows:
                row["id"] = self.ids[row]
                writer.writerow(row)


def create_tables():
    nocs = Table("nocs", ["noc"])
    games = Table("games", ["name", "location", "season", "year"])
    people = Table("people", ["name", "sex"])
    performances = Table("performances", ["person", "noc", "game"])
    medals = Table("medals", ["performance", "sport", "event", "medal_type"])
    return nocs, games, people, performances, medals


def process_data(rows):
    nocs, games, people, performances, medals = create_tables()
    i = 0
    for row in rows:
        i += 1
        if i % 1000 == 0:
            print(i)
        noc_id = nocs.add(row["NOC"])
        game_id = games.add(row["Games"], row["City"], row["Season"], row["Year"])
        person_id = people.add(row["Name"], row["Sex"])
        performance_id = performances.add(person_id, noc_id, game_id)
        medals.add(performance_id, row["Sport"], row["Event"], row["Medal"])
    return nocs, games, people, performances, medals


# credit https://stackoverflow.com/questions/312443/how-do-i-split-a-list-into-equally-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def convert():
    with open("athlete_events.csv", "r") as data:
        reader = csv.DictReader(data,
                                ["ID", "Name", "Sex", "Age", "Height", "Weight", "Team", "NOC", "Games", "Year",
                                 "Season",
                                 "City", "Sport", "Event", "Medal"])
        next(reader)
        rows = list(reader)
        tables = process_data(rows)

    for table in tables:
        table.write()


if __name__ == "__main__":
    convert()
