import random

banned_items = ["knife", "scissors", "explosives", "liquid", "gas", "weapon", "acid"]

def is_item_dangerous(item):
    return item.lower() in banned_items and random.random() < 0.5  # %50 risk
