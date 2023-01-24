import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from airflow.decorators import dag, task

@dataclass
class User:
  id: str
  name: str
  city: str
  school: str
  age: int
  is_teacher: bool

def build_user(input_dict) -> User:
  return User(
    id=input_dict["id"],
    name=input_dict["name"],
    city=input_dict["city"],
    school=input_dict["school"],
    age=input_dict["age"],
    is_teacher=input_dict["is_teacher"]
  )

@dag(
    schedule=None,
    start_date=datetime(2023, 1, 11),
    catchup=False
)
def exercise15():

    @task
    def read_users(path: str) -> str:
      with open(path, "r") as f:
         users = json.load(f)
      
      return json.dumps(users)
    
    @task
    def transform_users(raw_users: str) -> None:
      for user in json.loads(raw_users):
         print(build_user(user))

    users = read_users("./dags/data/users.json")
    transform = transform_users(users)

_ = exercise15()

