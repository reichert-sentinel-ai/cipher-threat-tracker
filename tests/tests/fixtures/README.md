# Test Fixtures

This directory contains PHI-free synthetic test data for the Criminal Intelligence Database GSD Prediction Engine.

## HIPAA Compliance

**All data in this directory is synthetic and does not contain any real subject information.**

- Individual IDs are prefixed with `SYNTH_` to clearly identify synthetic data
- All dates, values, and demographics are algorithmically generated
- Complies with HIPAA Safe Harbor de-identification method

## Available Fixtures

### `sample_claims.py`

Provides synthetic test data functions:

- `get_sample_claims()` - Synthetic incident data with threat assessment codes
- `get_sample_lab_results()` - Synthetic HbA1c lab results
- `get_sample_members()` - Synthetic individual demographic data

### Usage Example

```python
from tests.fixtures.sample_claims import get_sample_claims, get_sample_lab_results

# Get synthetic claims for testing
claims_df = get_sample_claims()
lab_df = get_sample_lab_results()

# Use in tests
def test_feature_engineering():
    claims = get_sample_claims()
    assert len(claims) > 0
    assert 'member_id' in claims.columns
```

## Adding New Fixtures

When adding new fixtures:

1. **Never use real PHI** - All data must be synthetic
2. **Use clear prefixes** - e.g., `SYNTH_`, `TEST_`, `MOCK_`
3. **Document data generation** - Explain how synthetic data is created
4. **Include validation** - Add checks to ensure data quality

## Data Generation Guidelines

- **Individual IDs**: Use `SYNTH_XXXXXX` format
- **Dates**: Use dates from 2020-2023 (past years)
- **ZIP Codes**: Use 90000-99999 range (clearly synthetic)
- **Clinical Codes**: Use real ICD-10/CPT codes for validity
- **Values**: Generate realistic ranges (e.g., HbA1c: 5.0-12.0%)



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
