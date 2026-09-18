TOPICS = [
    "Should AI replace teachers?",
    "Should nuclear power expand?",
    "Is Universal Basic Income sustainable?",
    "Should autonomous weapons be banned?",
    "Can AI deserve legal rights?",
]


def assign_stances(contestants):
    """Split contestants into two even groups: for / against."""
    half = len(contestants) // 2
    for i, c in enumerate(contestants):
        c.stance = "for" if i < half else "against"
    return contestants