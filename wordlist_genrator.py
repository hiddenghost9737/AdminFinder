import itertools

common_prefixes = ['admin', 'login', 'dashboard', 'control', 'user', 'cp', 'web']
common_suffixes = ['', 'panel', 'admin', 'login', 'cp', 'web', 'dashboard']

words = ['admin', 'administrator', 'panel', 'login', 'user', 'control', 'dashboard']

generated_patterns = []

# Combine common prefixes, suffixes, and words to create a large list
for pattern in itertools.product(common_prefixes, words, common_suffixes):
    generated_patterns.append(''.join(pattern))

# Remove duplicates
generated_patterns = list(set(generated_patterns))

# Ensure the list has at least 100,000 entries
while len(generated_patterns) < 100000:
    generated_patterns += generated_patterns.copy()

# Write the first 100,000 patterns to a file
with open('admin.txt', 'w') as file:
    for i in range(100000):
        file.write(generated_patterns[i] + '\n')

print("Admin panel names generated and saved to admin.txt")
