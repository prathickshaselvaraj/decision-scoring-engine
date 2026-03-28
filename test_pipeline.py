from src.ranker import rank_alternatives

def test_ranking_order():
    sample = [
        {"alternative": "A", "final_score": 0.5, "contributions": {}, "normalized": {}},
        {"alternative": "B", "final_score": 0.8, "contributions": {}, "normalized": {}},
    ]

    result = rank_alternatives(sample)

    assert result[0]["alternative"] == "B"
    assert result[1]["alternative"] == "A"
