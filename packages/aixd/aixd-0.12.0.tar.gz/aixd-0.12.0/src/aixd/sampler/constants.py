import datetime


def seed_from_timestamp():
    return int(datetime.datetime.now().timestamp())


RANDOM_SEED_SAMPLING = seed_from_timestamp()  # Random seed for sampling
