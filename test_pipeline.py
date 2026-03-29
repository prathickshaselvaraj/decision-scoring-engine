from src.ranker import rank_alternatives

# ✅ Test 1: Basic ranking order
def test_ranking_order():
    sample = [
        {"alternative": "A", "final_score": 0.5, "contributions": {}, "normalized": {}},
        {"alternative": "B", "final_score": 0.8, "contributions": {}, "normalized": {}},
    ]
    result = rank_alternatives(sample)
    assert result[0]["alternative"] == "B"
    assert result[1]["alternative"] == "A"

# ✅ Test 2: Rank assigned correctly
def test_rank_numbers_assigned():
    sample = [
        {"alternative": "X", "final_score": 0.3, "contributions": {}, "normalized": {}},
        {"alternative": "Y", "final_score": 0.9, "contributions": {}, "normalized": {}},
        {"alternative": "Z", "final_score": 0.6, "contributions": {}, "normalized": {}},
    ]
    result = rank_alternatives(sample)
    assert result[0]["rank"] == 1
    assert result[1]["rank"] == 2
    assert result[2]["rank"] == 3

# ✅ Test 3: Single alternative
def test_single_alternative():
    sample = [
        {"alternative": "Only", "final_score": 1.0, "contributions": {}, "normalized": {}},
    ]
    result = rank_alternatives(sample)
    assert result[0]["alternative"] == "Only"
    assert result[0]["rank"] == 1

# ✅ Test 4: Equal scores - both should be ranked
def test_equal_scores():
    sample = [
        {"alternative": "A", "final_score": 0.5, "contributions": {}, "normalized": {}},
        {"alternative": "B", "final_score": 0.5, "contributions": {}, "normalized": {}},
    ]
    result = rank_alternatives(sample)
    assert len(result) == 2

# ✅ Test 5: Empty list
def test_empty_alternatives():
    result = rank_alternatives([])
    assert result == []

# ✅ Integration Test: Full pipeline flow
def test_full_pipeline_integration():
    candidates = [
        {"alternative": "Candidate_A", "final_score": 0.72, "contributions": {}, "normalized": {}},
        {"alternative": "Candidate_B", "final_score": 0.88, "contributions": {}, "normalized": {}},
        {"alternative": "Candidate_C", "final_score": 0.65, "contributions": {}, "normalized": {}},
        {"alternative": "Candidate_D", "final_score": 0.91, "contributions": {}, "normalized": {}},
    ]
    result = rank_alternatives(candidates)

    # Top ranked should be D
    assert result[0]["alternative"] == "Candidate_D"
    # Last ranked should be C
    assert result[-1]["alternative"] == "Candidate_C"
    # All candidates returned
    assert len(result) == 4
    # Ranks are sequential
    for i, r in enumerate(result):
        assert r["rank"] == i + 1
