import string


def react_polymer(polymer: str) -> str:
    i = 1
    while i < len(polymer):
        if polymer[i].upper() == polymer[i-1].upper() and polymer[i] != polymer[i-1]:
            polymer = polymer[0:i-1] + polymer[i+1:]
            i -= 2
        i += 1
        if i < 1:
            i = 1
    return polymer


def length_with_removed_type(polymer: str, removed):
    polymer_with_removed = polymer.replace(removed, "").replace(removed.upper(), "")
    polymer_with_removed = react_polymer(polymer_with_removed)
    return len(polymer_with_removed)


with open("input.txt", "r") as puzzle_input:
    polymer = puzzle_input.read()

polymer = react_polymer(polymer)

print(len(polymer))  # part 1

# I tried to find a better solution than to just try react it
#  with every type removed, but I failed
best = len(polymer)
for c in string.ascii_lowercase:
    length = length_with_removed_type(polymer, c)
    if length < best:
        best = length

print(best)  # part 2
