FILE_PATH = "../resources/plain/months.txt"

print()

with open(FILE_PATH, "r") as f:
  lines = [line.rstrip() for line in f.readlines()]

print(lines)

with open(FILE_PATH, "r") as f:
  lines2 = f.read().splitlines()

print(lines2)

