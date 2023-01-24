FILE_PATH = "../resources/fixed-length/users.txt"

### Plain Python

class User:
  def __init__(self, id: int, name: str, city: str, school: str) -> None:
    self.id = id
    self.name = name
    self.city = city
    self.school = school

  def __repr__(self) -> str:
    return f"[{self.id}] {self.name} at {self.school} in {self.city}"


new_user = User(1, "John Doe", "New York", "NYU")
print(new_user)

def parse_user(line: str) -> User:
  id = int(line[0:4])
  name = line[4:30].rstrip()
  city = line[30:60].rstrip()
  school = line[60:90].rstrip()
  return User(id, name, city, school)

with open(FILE_PATH, "r") as f:
  users = [parse_user(line) for line in f.readlines()]



for user in users:
  print(user)


## With dataclasses
from dataclasses import dataclass

@dataclass
class DataUser:
  id: int
  name: str
  city: str
  school: str

def parse_data_user(line: str) -> DataUser:
  id = int(line[0:4])
  name = line[4:30].rstrip()
  city = line[30:60].rstrip()
  school = line[60:90].rstrip()
  return DataUser(id, name, city, school)

with open(FILE_PATH, "r") as f:
  data_users = [parse_data_user(line) for line in f.readlines()]

for user in data_users:
  print(user)
