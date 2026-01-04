# Tasmania Real Estate Agents - Data Collection Project

Comprehensive database of all licensed real estate sales agents in Tasmania, Australia.

## Project Status: Complete

| Metric | Value |
|--------|-------|
| **Total Sales Agents** | 1,600 |
| **Data Source** | Property Agents Board of Tasmania (Official Government Registry) |
| **Last Updated** | December 2025 |
| **Coverage** | 100% of licensed agents |

---

## Data Summary

### Final Deliverable: `tasmania-agents-COMPLETE.csv`

| Field | Completeness | Notes |
|-------|--------------|-------|
| Name | 100% | Full legal name from official registry |
| Agency | 85.4% | Business/agency affiliation |
| Role | 100% | Real Estate Agent (P1D2) or Sales Representative (P4) |
| Phone | 21.1% | Direct or office phone |
| Email | 14.3% | Professional email |
| Location | 82.3% | City/suburb in Tasmania |

### Role Breakdown

| Licence Type | Role | Count | Description |
|--------------|------|-------|-------------|
| P1D2 | Real Estate Agent | 430 | Fully licensed agents who can operate independently |
| P4 | Sales Representative | 1,170 | Licensed representatives working under a P1D2 agent |

---

## Data Sources

### Primary Source: Property Agents Board of Tasmania
- **Authority**: Official government licensing body
- **URL**: https://www.propertyagentsboard.com.au/current-register.html
- **Registry Date**: December 19, 2025
- **Data Extracted**: Individual Property Agents register (PDF)

The Property Agents Board maintains the official register of all licensed property agents in Tasmania. This is the authoritative source for agent verification.

### Secondary Sources (Contact Enrichment)
Contact information was gathered from publicly available sources:
- Agency websites
- Real estate listing platforms (realestate.com.au, domain.com.au)
- Professional directories
- Allhomes Tasmania listings

---

## Methodology

### Phase 1: Official Registry Extraction
1. Downloaded official Individual Property Agents register from Property Agents Board
2. Parsed PDF to extract all licensed agents (1,624 total records)
3. Filtered for sales-related roles only:
   - **P1D2**: Real Estate Agent (included)
   - **P4**: Property Representative (included)
   - P2D2: Property Manager (excluded)
   - P3D2: General Auctioneer (excluded)
4. Removed invalid licences (8 records with "Valid: No")
5. Result: 1,600 valid sales agents

### Phase 2: Contact Information Enrichment
1. Web scraped major real estate agency websites
2. Collected agent profiles from listing platforms
3. Extracted: phone numbers, email addresses, office locations
4. Merged with official registry data using fuzzy name matching

### Phase 3: Data Quality & Deduplication
1. Normalized name formats for matching
2. Cross-referenced multiple sources for accuracy
3. Deduplicated based on name + agency combination
4. Validated against official registry as ground truth

---

## Files Included

### Data Files
| File | Records | Description |
|------|---------|-------------|
| `SAMPLE-tasmania-agents.csv` | 50 | Sample records with contact info (included) |
| `tasmania-agents-COMPLETE.csv` | 1,600 | Full dataset (not in repo - available upon request) |

### Source Documents
| File | Description |
|------|-------------|
| `individual_agents_dec2025.pdf` | Official registry PDF from Property Agents Board |
| `conducting_business_dec2025.pdf` | Business entities register |

### Scripts
| File | Description |
|------|-------------|
| `parse_registry.py` | PDF extraction and parsing script |

---

## Sample Data

```csv
Name,Agency,Role,Phone,Email,Location
"Abbott, Haylee Maree",Harcourts Huon Valley,Real Estate Agent,03 6264 0000,,Huonville
"Adams, Kristy May",4one4 Property Co,Sales Representative,0409 134 220,kristy@4one4.com.au,Hobart
"Alexander-Smith, Tahlia",Petrusma Property,Sales Representative,0467 950 234,talexander-smith@petrusma.com.au,Hobart
"Allie, Rose",Elders Real Estate Hobart,Sales Representative,0426 877 789,rose.allie@elders.com.au,Hobart
"Anderson, Craig William",Peterswald,Real Estate Agent,0428 449 843,craig@peterswald.com.au,Hobart
```

---

## Data Quality Notes

### Strengths
- **100% population coverage** - Every licensed sales agent in Tasmania is included
- **Official source** - Data verified against government registry
- **Current** - Registry dated December 2025
- **Structured** - Clean CSV format ready for import

### Limitations
- **Contact info gaps** - Phone (21%) and email (14%) coverage is partial
- **Name parsing** - Some names may include partial agency info due to PDF format
- **Point-in-time** - Licences expire/renew; registry should be refreshed periodically

### Recommendations for Contact Enrichment
To improve phone/email coverage:
1. Scrape individual agency "Our Team" pages
2. Use LinkedIn Sales Navigator for professional emails
3. Check RateMyAgent.com.au profiles
4. Contact agencies directly for team directories

---

## Licence Types Explained

| Code | Name | Description |
|------|------|-------------|
| P1D2 | Real Estate Agent | Can buy, sell, lease property; supervise P4 agents |
| P2D2 | Property Manager | Manages rental properties (excluded from this dataset) |
| P3D2 | General Auctioneer | Conducts property auctions (excluded from this dataset) |
| P4 | Property Representative | Works under P1D2 supervision; can sell/lease property |

---

## Usage

### Importing to Excel/Google Sheets
1. Open the CSV file directly, or
2. Use Data > Import > Upload CSV

### Importing to CRM
The CSV format is compatible with most CRM systems:
- HubSpot: Contacts > Import
- Salesforce: Data Import Wizard
- Zoho: Leads > Import

### Database Import
```sql
-- Example PostgreSQL
CREATE TABLE tasmania_agents (
    name VARCHAR(255),
    agency VARCHAR(255),
    role VARCHAR(50),
    phone VARCHAR(50),
    email VARCHAR(255),
    location VARCHAR(255)
);

COPY tasmania_agents FROM 'tasmania-agents-COMPLETE.csv'
WITH (FORMAT csv, HEADER true);
```

---

## Verification

To verify this data against the official source:
1. Visit: https://www.propertyagentsboard.com.au/current-register.html
2. Download "Individual" register PDF
3. Cross-reference any agent by name

---

## Project Statistics

| Metric | Value |
|--------|-------|
| Total Licensed Property Agents (all types) | 1,616 |
| Sales Agents (P1D2 + P4) | 1,600 |
| Property Managers (P2D2) - excluded | 5 |
| Auctioneers (P3D2) - excluded | 11 |
| Invalid Licences - excluded | 8 |

---

## Contact

For questions about this dataset or methodology, please open an issue in this repository.
