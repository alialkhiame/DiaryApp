import itertools

array = ['v', 's', 's', 'i', 't', 'h', 'h', 'u', 'b', 'b', 'l', 'l', 'a']

# Generate all possible combinations of characters
combinations = []
for r in range(1, len(array) + 1):
    combinations.extend(itertools.combinations(array, r))

# Convert tuples to strings
combinations = [''.join(comb) for comb in combinations]

# Print all combinations
for combination in combinations:
    print(combination)
