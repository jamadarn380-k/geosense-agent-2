from src.phase1_ml.site_scorer import score_location

PUNE_LATITUDE = 18.500419
PUNE_LONGITUDE = 73.765995

def test_score_location_returns_dictionary():
    result = score_location(PUNE_LATITUDE, PUNE_LONGITUDE)

    assert isinstance(result, dict)

def test_score_location_has_required_keys():
    result = score_location(PUNE_LATITUDE, PUNE_LONGITUDE)

    required_keys = [
        "input_latitude",
        "input_longitude",
        "nearest_location_id",
        "nearest_latitude",
        "nearest_longitude",
        "zone_name",
        "opportunity_score",
        "risk_score",
        "probability_good_site",
        "features",
        "verdict",
    ]

    for key in required_keys:
        assert key in result

def test_scores_are_between_zero_and_ten():
    result = score_location(PUNE_LATITUDE, PUNE_LONGITUDE)

    assert 0 <= result["opportunity_score"] <= 10
    assert 0 <= result["risk_score"] <= 10

def test_verdict_is_valid():
    result = score_location(PUNE_LATITUDE, PUNE_LONGITUDE)

    assert result["verdict"] in ["GOOD SITE", "POOR SITE"]