# test_site_scorer.py
# Run with: python -m pytest tests/ -v

import sys
import os

# Add src/phase1_ml to path so we can import site_scorer
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'phase1_ml'))

from site_scorer import score_location

def test_score_returns_dict():
    result = score_location(13.0827, 80.2707)  # Chennai
    assert isinstance(result, dict), "score_location should return a dict"

def test_score_has_required_keys():
    result = score_location(13.0827, 80.2707)
    required_keys = [
        'latitude', 'longitude', 'opportunity_score',
        'risk_score', 'features', 'shap_explanation', 'verdict'
    ]
    for key in required_keys:
        assert key in result, f"Missing key: {key}"

def test_scores_in_valid_range():
    result = score_location(13.0827, 80.2707)
    assert 0 <= result['opportunity_score'] <= 10, "opportunity_score must be 0-10"
    assert 0 <= result['risk_score'] <= 10, "risk_score must be 0-10"

def test_verdict_is_valid():
    result = score_location(13.0827, 80.2707)
    assert result['verdict'] in ['GOOD SITE', 'POOR SITE'], "verdict must be GOOD SITE or POOR SITE"