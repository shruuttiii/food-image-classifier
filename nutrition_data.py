"""
Nutrition lookup table for the food classifier.

Values are approximate, per STANDARD SERVING SIZE (not per 100g), sourced from
typical nutrition references (USDA / Indian Food Composition Tables) for common
preparations of each dish. Since a single 2D photo has no depth/scale
information, exact calorie estimation from an image alone isn't physically
possible without a reference object — so these are standard-serving estimates,
which the app lets the user scale up/down.
"""

NUTRITION_DB = {
    "Pavbhaji": {
        "serving_size": "1 plate (~250g, 2 pav + bhaji)",
        "calories": 400,
        "protein_g": 8,
        "carbs_g": 55,
        "fat_g": 16,
        "emoji": "🍛"
    },
    "biryani": {
        "serving_size": "1 plate (~300g)",
        "calories": 450,
        "protein_g": 18,
        "carbs_g": 58,
        "fat_g": 15,
        "emoji": "🍚"
    },
    "burger": {
        "serving_size": "1 regular burger (~220g)",
        "calories": 350,
        "protein_g": 15,
        "carbs_g": 35,
        "fat_g": 17,
        "emoji": "🍔"
    },
    "dosa": {
        "serving_size": "1 plain dosa (~150g) with chutney/sambar",
        "calories": 260,
        "protein_g": 6,
        "carbs_g": 40,
        "fat_g": 8,
        "emoji": "🥞"
    },
    "french fries": {
        "serving_size": "1 regular portion (~115g)",
        "calories": 340,
        "protein_g": 4,
        "carbs_g": 43,
        "fat_g": 17,
        "emoji": "🍟"
    },
    "fruits_salad": {
        "serving_size": "1 bowl (~200g)",
        "calories": 130,
        "protein_g": 2,
        "carbs_g": 32,
        "fat_g": 0.5,
        "emoji": "🥗"
    },
    "idli": {
        "serving_size": "2 pieces (~120g) with sambar/chutney",
        "calories": 150,
        "protein_g": 5,
        "carbs_g": 30,
        "fat_g": 1,
        "emoji": "⚪"
    },
    "noodles": {
        "serving_size": "1 plate (~250g)",
        "calories": 400,
        "protein_g": 10,
        "carbs_g": 60,
        "fat_g": 13,
        "emoji": "🍜"
    },
    "paneer_tikka": {
        "serving_size": "1 plate (~150g, ~6 pieces)",
        "calories": 320,
        "protein_g": 18,
        "carbs_g": 10,
        "fat_g": 23,
        "emoji": "🧀"
    },
    "pasta": {
        "serving_size": "1 bowl (~250g)",
        "calories": 380,
        "protein_g": 12,
        "carbs_g": 55,
        "fat_g": 12,
        "emoji": "🍝"
    },
    "pizza": {
        "serving_size": "2 slices (~200g, medium regular crust)",
        "calories": 480,
        "protein_g": 20,
        "carbs_g": 55,
        "fat_g": 20,
        "emoji": "🍕"
    },
    "samosa": {
        "serving_size": "2 pieces (~120g)",
        "calories": 330,
        "protein_g": 6,
        "carbs_g": 36,
        "fat_g": 18,
        "emoji": "🥟"
    },
    "sandwiches": {
        "serving_size": "1 sandwich, 2 slices (~150g)",
        "calories": 300,
        "protein_g": 11,
        "carbs_g": 35,
        "fat_g": 12,
        "emoji": "🥪"
    },
    "sushi": {
        "serving_size": "6 pieces (~180g)",
        "calories": 260,
        "protein_g": 9,
        "carbs_g": 45,
        "fat_g": 4,
        "emoji": "🍣"
    },
    "vegetable_salad": {
        "serving_size": "1 bowl (~200g)",
        "calories": 110,
        "protein_g": 4,
        "carbs_g": 15,
        "fat_g": 4,
        "emoji": "🥙"
    },
}


def get_nutrition(class_name, multiplier=1.0):
    """Return nutrition info scaled by a serving multiplier."""
    data = NUTRITION_DB.get(class_name)
    if data is None:
        return None
    return {
        "serving_size": data["serving_size"],
        "multiplier": multiplier,
        "calories": round(data["calories"] * multiplier),
        "protein_g": round(data["protein_g"] * multiplier, 1),
        "carbs_g": round(data["carbs_g"] * multiplier, 1),
        "fat_g": round(data["fat_g"] * multiplier, 1),
        "emoji": data["emoji"],
    }
