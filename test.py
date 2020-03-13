import random
bottomXs = []
try:
    a = random.sample(bottomXs, 1)[0]
except ValueError:
    print("Booom", len(bottomXs))
    raise Exception('spam', 'eggs')
