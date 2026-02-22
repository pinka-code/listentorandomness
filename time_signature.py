TIME_SIGNATURES = {
    "2/4": {"num": 2, "den": 4, "type": "binary"},
    "3/4": {"num": 3, "den": 4, "type": "binary"},
    "4/4": {"num": 4, "den": 4, "type": "binary"},
    "2/2": {"num": 2, "den": 2, "type": "binary"},
    "6/8": {"num": 6, "den": 8, "type": "ternary"},
    "9/8": {"num": 9, "den": 8, "type": "ternary"},
    "12/8": {"num": 12, "den": 8, "type": "ternary"},
}

def choose_time_signature(rng):
    """
    Returns:
    - name (e.g., "4/4")
    - numerator
    - denominator
    - type ("binary" or "ternary")
    """
    name, data = rng.choice(list(TIME_SIGNATURES.items()))
    return name, data["num"], data["den"], data["type"]