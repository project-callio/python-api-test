from apitist import random
from faker import Faker

from common.models import FullName, Password, Comment

rand = random.Randomer()
fake = Faker("en-US")

rand.add_predefined(locale="en-US")
rand.add_types({
    FullName: lambda: f"{fake.first_name()} {fake.last_name()}",
    Password: fake.password,
    Comment: fake.sentence,
})
