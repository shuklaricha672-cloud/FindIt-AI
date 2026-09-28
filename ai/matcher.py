def calculate_match(
    detected_objects,
    item_type,
    location,
    found_location,
    description="",
    found_description=""
):

    score = 0

    # -------------------------
    # Object / Category Match
    # -------------------------

    detected_names = [
        obj["name"].lower()
        for obj in detected_objects
    ]

    if item_type.lower() in detected_names:
        score += 60

    # -------------------------
    # Location Match
    # -------------------------

    if location.lower() == found_location.lower():
        score += 25

    # -------------------------
    # Description Match
    # -------------------------

    if description and found_description:

        words1 = set(description.lower().split())
        words2 = set(found_description.lower().split())

        common_words = words1.intersection(words2)

        if len(common_words) >= 2:
            score += 15

    return min(score, 100)