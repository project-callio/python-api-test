from apitist import random
from faker import Faker

rand = random.Randomer()
fake = Faker("en-EN")

rand.add_predefined()
