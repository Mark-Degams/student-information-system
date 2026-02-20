names = ["Mark", "Mary", "John", "Manny", "Marco", "emath"]

search = "ma"

results = [name for name in names if search.lower() in name.lower()]

print(results)