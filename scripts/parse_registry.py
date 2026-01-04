import pdfplumber
import re
import csv

pdf_path = "individual_agents_dec2025.pdf"
all_agents = []

# Known agency names/patterns to help with parsing
KNOWN_AGENCIES = [
    'Harcourts', 'First National', 'Ray White', 'LJ Hooker', 'Roberts Real Estate',
    'Elders', 'Raine & Horne', 'PRDnationwide', 'PRD', 'Knight Frank', 'View Real Estate',
    'Saunders Property', 'The Agency', 'Professionals', 'Century 21', 'Petrusma Property',
    'Charlotte Peterswald', 'Fall & Associates', 'Ripple', 'McGrath', 'Belle Property',
    'Homelands Property', 'Harrison Agents', 'Nest Property', '4one4', '4 One 4',
    'Curo Property', 'RWC', 'Jones Lang LaSalle', 'JLL', 'CBRE', 'Colliers', 'Savills',
    'Halliwell', 'EIS Property', 'Downton Property', 'Key2 Property', 'Bushby Property',
    'Peterswald', 'Eves', 'Jennings Real Estate', 'Lees Real Estate', 'Peter Lees',
    'Future Assist', 'One Agency', 'Hodgman', 'Lifestyle Property', 'Crowther',
    'Alan Cole', 'Area Specialist', 'Barry Plant', 'Biggin Scott', 'Coastal Property',
    'Complete Real Estate', 'Country Real Estate', 'Drummond', 'Dutton', 'Edwards Windsor',
    'Elphinstone', 'Emms Mooney', 'Ewart', 'Feature Property', 'Felmingham', 'Fiducia',
    'Foley', 'Fox & Hounds', 'Gourlay', 'Graham', 'Gunns', 'Haldane', 'Harmers',
    'Harrison Humphreys', 'Hayden', 'Hinton', 'Huon Real Estate', 'Ian Read', 'Iles',
    'Kathryn Clifton', 'Key Tasmanian', 'Latitude Real Estate', 'Libra',
    'Living Here', 'Living in Tasmania', 'Louwrens', 'Macquarie', 'Max Fry',
    'McElwaine', 'McEwan', 'Miller', 'Mitchell Rowe', 'Momentum', 'Morris', 'NAI Harcourts',
    'Pacific Coast', 'Paul McEvoy', 'Performance', 'Place Estate',
    'Price Property', 'Property Plus', 'Realty', 'Redland', 'Reed Property', 'Richardson',
    'Roberts Ltd', 'Rural', 'Sims', 'Smith Bros', 'Specialty', 'St Andrews', 'Stanley',
    'Strata', 'Tamar Property', 'Think Property', 'Turners', 'Walter Brinckman',
    'Waran', 'Whitley', 'Zing'
]

# Pattern to match licence info at end of line
pattern = re.compile(r'^(.+?)\s+(P1D2|P2D2|P3D2|P4)\s+(\d{1,2}\s+\w{3}\s+\d{4})\s+(Yes|No)$')

# Australian states
STATES = ['Tasmania', 'Victoria', 'New South Wales', 'Queensland', 'South Australia',
          'Western Australia', 'Northern Territory', 'ACT']

def parse_name_agency_address(raw):
    """Parse raw string into name, agency, and address components."""

    # First, try to find address by looking for state + postcode pattern
    address = ''
    remaining = raw

    for state in STATES:
        state_pattern = re.compile(rf'(.+?)\s+(\d+[A-Za-z/]*\s+.+?,\s+{state}\s+\d{{4}})$')
        match = state_pattern.match(raw)
        if match:
            remaining = match.group(1).strip()
            address = match.group(2).strip()
            break

    # Now parse name and agency from remaining
    # Name format: "[Maiden] Surname, Given1 [Given2] [Given3]"

    # Find the comma that separates surname from given names
    comma_idx = remaining.find(',')

    if comma_idx <= 0:
        # No comma - unusual format, return as name
        return remaining, '', address

    surname = remaining[:comma_idx].strip()
    after_surname = remaining[comma_idx + 1:].strip()

    # Try to find where given names end and agency begins
    # Strategy: look for known agency patterns
    agency = ''
    given_names = after_surname

    for agency_name in KNOWN_AGENCIES:
        idx = after_surname.find(agency_name)
        if idx > 0:  # Found agency name, and it's not at the start
            given_names = after_surname[:idx].strip()
            agency = after_surname[idx:].strip()
            break

    # If no known agency found, try heuristics
    if not agency:
        # Look for common business words
        business_starters = ['Real Estate', 'Property', 'Pty Ltd', 'Ltd', 'Group', 'Agency', 'Agents']
        for starter in business_starters:
            idx = after_surname.find(starter)
            if idx > 0:
                # Walk back to find where agency name might start
                before = after_surname[:idx].strip()
                words = before.split()
                if len(words) >= 2:
                    # Assume last 1-2 words before business word are part of agency name
                    given_names = ' '.join(words[:-2]) if len(words) > 2 else words[0] if len(words) > 1 else ''
                    agency = ' '.join(words[-2:]) + ' ' + after_surname[idx:].strip() if len(words) >= 2 else after_surname[idx:].strip()
                    break

    name = f"{surname}, {given_names}".strip().rstrip(',')

    return name, agency, address

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue

        for line in text.split('\n'):
            line = line.strip()
            if not line or 'Property Agents Board' in line or 'Name Business Name' in line or 'Individuals Property' in line:
                continue

            match = pattern.match(line)
            if match:
                raw = match.group(1).strip()
                lic_type = match.group(2)
                valid = match.group(4)

                # Only process sales roles (P1D2 and P4) with valid licences
                if lic_type not in ('P1D2', 'P4') or valid != 'Yes':
                    continue

                name, agency, location = parse_name_agency_address(raw)
                role = 'Real Estate Agent' if lic_type == 'P1D2' else 'Sales Representative'

                all_agents.append({
                    'Name': name.lstrip(', '),
                    'Agency': agency,
                    'Role': role,
                    'Phone': '',  # Not in registry
                    'Email': '',  # Not in registry
                    'Location': location
                })

# Write to CSV
output_file = 'tasmania-agents-official-registry.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Name', 'Agency', 'Role', 'Phone', 'Email', 'Location'])
    writer.writeheader()
    writer.writerows(all_agents)

print(f"Total sales agents: {len(all_agents)}")
print(f"Saved to: {output_file}")

print(f"\nRole breakdown:")
from collections import Counter
role_counts = Counter(a['Role'] for a in all_agents)
for role, count in sorted(role_counts.items()):
    print(f"  {role}: {count}")

print(f"\nSample records:")
for a in all_agents[:15]:
    print(f"\n  Name: {a['Name']}")
    print(f"  Agency: {a['Agency']}")
    print(f"  Location: {a['Location']}")
