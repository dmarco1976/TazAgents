# Test Coverage Analysis

## Executive Summary

**Current Test Coverage: 0%**

This codebase has **no tests whatsoever**. The entire parsing logic in `scripts/parse_registry.py` is untested, which poses significant risk to data integrity and maintainability.

---

## Codebase Overview

| Metric | Value |
|--------|-------|
| Source Files | 1 |
| Lines of Code | 155 |
| Functions | 1 (`parse_name_agency_address`) |
| Test Files | 0 |
| Test Coverage | 0% |

---

## Areas Requiring Test Coverage

### 1. Critical: `parse_name_agency_address()` Function (Priority: HIGH)

**Location:** `scripts/parse_registry.py:41-99`

This is the core parsing function containing complex conditional logic. It handles:

- Address extraction using state pattern matching
- Name parsing (surname/given names)
- Agency detection using known patterns
- Business word heuristics for unknown agencies

**Recommended Tests:**

```python
# Test cases for parse_name_agency_address()

# Basic parsing
("Smith, John Harcourts 123 Main St, Tasmania 7000",
 ("Smith, John", "Harcourts", "123 Main St, Tasmania 7000"))

# Multiple given names
("Jones, Mary Anne Roberts Real Estate 45 Beach Rd, Tasmania 7010",
 ("Jones, Mary Anne", "Roberts Real Estate", "45 Beach Rd, Tasmania 7010"))

# No agency detected
("Brown, James 78 River Ave, Tasmania 7250",
 ("Brown, James", "", "78 River Ave, Tasmania 7250"))

# No address present
("White, Sarah First National",
 ("White, Sarah", "First National", ""))

# Edge case: No comma in name
("InvalidFormat 123 Street, Tasmania 7000",
 ("InvalidFormat 123 Street, Tasmania 7000", "", ""))

# Complex agency names
("Lee, David Knight Frank Tasmania 500 Collins St, Victoria 3000",
 ("Lee, David", "Knight Frank Tasmania", "500 Collins St, Victoria 3000"))

# Business word heuristics
("Taylor, Emma Unknown Real Estate Group 10 Park Lane, Tasmania 7001",
 ("Taylor, Emma", "Unknown Real Estate Group", "10 Park Lane, Tasmania 7001"))
```

**Risk if Untested:** Incorrect agent data extraction leads to invalid records, incomplete agencies, or corrupted names.

---

### 2. High Priority: Regex Pattern Matching (Priority: HIGH)

**Location:** `scripts/parse_registry.py:35`

```python
pattern = re.compile(r'^(.+?)\s+(P1D2|P2D2|P3D2|P4)\s+(\d{1,2}\s+\w{3}\s+\d{4})\s+(Yes|No)$')
```

**Recommended Tests:**

```python
# Valid P1D2 licence (should match)
"Smith, John Harcourts 123 Main St P1D2 15 Jan 2025 Yes"

# Valid P4 licence (should match)
"Jones, Mary Roberts Ltd 45 Beach Rd P4 1 Dec 2024 Yes"

# Invalid licence type P2D2 (should match but be filtered)
"Brown, James Some Agency P2D2 20 Mar 2024 Yes"

# Invalid licence (No) - should match but be filtered
"White, Sarah Agency P1D2 10 Feb 2025 No"

# Malformed lines (should NOT match)
"Random text without licence info"
"Name only P1D2"  # Missing date/validity
"Complete P1D2 15 Jan 2025"  # Missing Yes/No

# Edge cases
"O'Brien, Patrick Agency P1D2 5 Sep 2025 Yes"  # Apostrophe in name
"Van Der Berg, Jan Agency P4 25 Oct 2024 Yes"  # Multi-part surname
```

**Risk if Untested:** Malformed data could slip through or valid records could be incorrectly rejected.

---

### 3. High Priority: Licence Type Filtering (Priority: HIGH)

**Location:** `scripts/parse_registry.py:119`

```python
if lic_type not in ('P1D2', 'P4') or valid != 'Yes':
    continue
```

**Recommended Tests:**

| Licence Type | Valid | Expected Outcome |
|--------------|-------|------------------|
| P1D2 | Yes | Include |
| P1D2 | No | Exclude |
| P4 | Yes | Include |
| P4 | No | Exclude |
| P2D2 | Yes | Exclude |
| P2D2 | No | Exclude |
| P3D2 | Yes | Exclude |
| P3D2 | No | Exclude |

**Risk if Untested:** Wrong agent types could be included or valid agents excluded.

---

### 4. Medium Priority: Role Assignment (Priority: MEDIUM)

**Location:** `scripts/parse_registry.py:123`

```python
role = 'Real Estate Agent' if lic_type == 'P1D2' else 'Sales Representative'
```

**Recommended Tests:**

```python
# P1D2 -> Real Estate Agent
assert get_role('P1D2') == 'Real Estate Agent'

# P4 -> Sales Representative
assert get_role('P4') == 'Sales Representative'
```

**Risk if Untested:** Incorrect role labels in output data.

---

### 5. Medium Priority: Address State Detection (Priority: MEDIUM)

**Location:** `scripts/parse_registry.py:38-39, 48-54`

Tests should verify all Australian states are properly detected:

```python
STATES = ['Tasmania', 'Victoria', 'New South Wales', 'Queensland',
          'South Australia', 'Western Australia', 'Northern Territory', 'ACT']
```

**Recommended Tests:**

```python
# Each state should be detected
("Name, Given Agency 123 St, Tasmania 7000", "123 St, Tasmania 7000")
("Name, Given Agency 456 Rd, Victoria 3000", "456 Rd, Victoria 3000")
("Name, Given Agency 789 Ave, New South Wales 2000", "789 Ave, New South Wales 2000")
# ... etc for all states

# Edge case: Multiple states in string (should match last one)
("Name, Given Victoria Real Estate 100 Main St, Tasmania 7000", "100 Main St, Tasmania 7000")
```

**Risk if Untested:** Addresses in certain states might not be detected.

---

### 6. Medium Priority: Known Agency Detection (Priority: MEDIUM)

**Location:** `scripts/parse_registry.py:9-32, 74-79`

With 60+ known agencies, this needs parametrized testing:

```python
# Sample agencies to test
test_agencies = [
    'Harcourts',
    'First National',
    'Ray White',
    'Roberts Real Estate',
    'Knight Frank',
    'Charlotte Peterswald',
    '4one4',
]

# Each known agency should be detected
for agency in test_agencies:
    input_str = f"Smith, John {agency} 123 Main St, Tasmania 7000"
    _, detected_agency, _ = parse_name_agency_address(input_str)
    assert detected_agency.startswith(agency)
```

**Risk if Untested:** New agencies added to the list might not be detected properly.

---

### 7. Low Priority: CSV Output (Priority: LOW)

**Location:** `scripts/parse_registry.py:134-139`

**Recommended Tests:**

```python
# Verify CSV has correct headers
headers = ['Name', 'Agency', 'Role', 'Phone', 'Email', 'Location']

# Verify special characters are properly escaped
# Verify empty fields are handled
# Verify encoding is UTF-8
```

**Risk if Untested:** Output file format issues.

---

### 8. Low Priority: Header/Footer Line Filtering (Priority: LOW)

**Location:** `scripts/parse_registry.py:109`

```python
if not line or 'Property Agents Board' in line or 'Name Business Name' in line or 'Individuals Property' in line:
    continue
```

**Recommended Tests:**

```python
# These lines should be skipped
skip_lines = [
    '',
    'Property Agents Board of Tasmania',
    'Name Business Name Address',
    'Individuals Property Agents',
]

# These lines should be processed
process_lines = [
    'Smith, John Harcourts P1D2 15 Jan 2025 Yes',
]
```

---

## Proposed Test Structure

```
TazAgents/
├── scripts/
│   └── parse_registry.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Pytest fixtures
│   ├── test_parse_name_agency.py      # Unit tests for parsing function
│   ├── test_pattern_matching.py       # Regex pattern tests
│   ├── test_filtering.py              # Licence filtering tests
│   └── test_integration.py            # End-to-end tests
├── pytest.ini                         # Pytest configuration
└── requirements-dev.txt               # Development dependencies
```

---

## Recommended Development Dependencies

```txt
# requirements-dev.txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.0.0
```

---

## Recommended pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short
```

---

## Priority Implementation Order

1. **Week 1: Critical Tests**
   - `parse_name_agency_address()` unit tests
   - Regex pattern matching tests
   - Licence type filtering tests

2. **Week 2: High Priority Tests**
   - State detection tests
   - Agency detection tests
   - Edge case coverage

3. **Week 3: Medium/Low Priority**
   - CSV output tests
   - Integration tests
   - Line filtering tests

---

## Expected Coverage After Implementation

| Component | Current | Target |
|-----------|---------|--------|
| `parse_name_agency_address()` | 0% | 95%+ |
| Pattern matching | 0% | 100% |
| Filtering logic | 0% | 100% |
| Agency detection | 0% | 90%+ |
| Overall | 0% | 85%+ |

---

## Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Incorrect name parsing | High | Medium | Unit tests for parse function |
| Missing agencies | Medium | Medium | Parametrized agency tests |
| Invalid licence filtering | High | Low | Explicit filter tests |
| Address detection failure | Medium | Low | State pattern tests |
| Output file corruption | Low | Low | CSV format tests |

---

## Conclusion

This codebase urgently needs test coverage, particularly for the `parse_name_agency_address()` function which contains complex string parsing logic. Without tests:

1. Refactoring is risky
2. Bug detection relies on manual verification
3. Data integrity cannot be verified
4. Adding new agencies or patterns is error-prone

Implementing the proposed test suite will significantly improve code reliability and maintainability.
