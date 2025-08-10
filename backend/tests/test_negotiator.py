from app.ai_agents.negotiator import Negotiator


def test_generate_variants_default():
    negotiator = Negotiator()
    expected = [
        "red_steel_matte",
        "red_steel_gloss",
        "red_plastic_matte",
        "red_plastic_gloss",
        "blue_steel_matte",
        "blue_steel_gloss",
        "blue_plastic_matte",
        "blue_plastic_gloss",
    ]
    assert negotiator.generate_variants() == expected


def test_generate_variants_custom_options():
    negotiator = Negotiator()
    options = {"size": ["S", "L"], "color": ["green"]}
    assert negotiator.generate_variants(options) == [
        "S_green",
        "L_green",
    ]

