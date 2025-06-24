# CCD to UI Data Mapping Guide

## Overview

This guide provides comprehensive XPath patterns and best practices for extracting structured data from Continuity of Care Documents (CCD) for use in user interfaces and healthcare applications.

## Table of Contents

1. [Common CCD XPath Patterns](#common-ccd-xpath-patterns)
2. [Patient Demographics](#patient-demographics)
3. [Clinical Data Sections](#clinical-data-sections)
4. [Best Practices](#best-practices)
5. [Common Gotchas](#common-gotchas)
6. [Template Structure](#template-structure)

## Common CCD XPath Patterns

### Patient Demographics

#### Basic Patient Information
```xpath
# Patient name components
/ClinicalDocument/recordTarget/patientRole/patient/name/given
/ClinicalDocument/recordTarget/patientRole/patient/name/family

# Full name (concatenated)
concat(/ClinicalDocument/recordTarget/patientRole/patient/name/given, ' ', 
       /ClinicalDocument/recordTarget/patientRole/patient/name/family)

# Gender
/ClinicalDocument/recordTarget/patientRole/patient/administrativeGenderCode/@code
/ClinicalDocument/recordTarget/patientRole/patient/administrativeGenderCode/@displayName

# Date of Birth
/ClinicalDocument/recordTarget/patientRole/patient/birthTime/@value
```

#### Contact Information
```xpath
# Address components
/ClinicalDocument/recordTarget/patientRole/addr/streetAddressLine
/ClinicalDocument/recordTarget/patientRole/addr/city
/ClinicalDocument/recordTarget/patientRole/addr/state
/ClinicalDocument/recordTarget/patientRole/addr/postalCode

# Phone numbers and email
/ClinicalDocument/recordTarget/patientRole/telecom[@use='HP']/@value  # Home phone
/ClinicalDocument/recordTarget/patientRole/telecom[@use='WP']/@value  # Work phone
/ClinicalDocument/recordTarget/patientRole/telecom[starts-with(@value, 'mailto:')]/@value
```

## Clinical Data Sections

### Problems/Conditions

#### Active Problems Section
```xpath
# Section identifier
/ClinicalDocument/component/structuredBody/component/section[code/@code='11450-4']

# Active problem entries
/ClinicalDocument/component/structuredBody/component/section[code/@code='11450-4']/entry/act/entryRelationship/observation[statusCode/@code='active']

# Problem details
./value/@displayName                    # Condition name
./value/@code                          # Condition code
./effectiveTime/low/@value             # Onset date
./effectiveTime/high/@value            # Resolution date (if resolved)
./entryRelationship/observation[code/@code='SEV']/value/@displayName  # Severity
```

#### Problem Status Filtering
```xpath
# Active problems only
//observation[statusCode/@code='active']

# Resolved problems
//observation[statusCode/@code='completed']

# All problems regardless of status
//observation[code/@codeSystem='2.16.840.1.113883.6.96']  # SNOMED CT problems
```

### Medications

#### Active Medications Section
```xpath
# Medications section
/ClinicalDocument/component/structuredBody/component/section[code/@code='10160-0']

# Active medication entries
/ClinicalDocument/component/structuredBody/component/section[code/@code='10160-0']/entry/substanceAdministration[statusCode/@code='active']

# Medication details
./consumable/manufacturedProduct/manufacturedMaterial/code/@displayName  # Drug name
./consumable/manufacturedProduct/manufacturedMaterial/code/@code         # Drug code
./doseQuantity/@value                                                    # Dose amount
./doseQuantity/@unit                                                     # Dose unit
./rateQuantity/@value                                                    # Frequency
./routeCode/@displayName                                                 # Route (oral, IV, etc.)
./effectiveTime[@xsi:type='IVL_TS']/low/@value                          # Start date
./effectiveTime[@xsi:type='IVL_TS']/high/@value                         # End date
```

### Allergies and Adverse Reactions

#### Allergy Section
```xpath
# Allergies section
/ClinicalDocument/component/structuredBody/component/section[code/@code='48765-2']

# Allergy entries
/ClinicalDocument/component/structuredBody/component/section[code/@code='48765-2']/entry/act/entryRelationship/observation

# Allergy details
./participant/participantRole/playingEntity/code/@displayName     # Allergen name
./participant/participantRole/playingEntity/code/@code           # Allergen code
./value/@displayName                                              # Reaction type
./entryRelationship/observation[code/@code='SEV']/value/@displayName  # Severity level
./effectiveTime/low/@value                                        # First occurrence
```

### Vital Signs

#### Vital Signs Section
```xpath
# Vital signs section
/ClinicalDocument/component/structuredBody/component/section[code/@code='8716-3']

# Individual vital sign observations
/ClinicalDocument/component/structuredBody/component/section[code/@code='8716-3']/entry/organizer/component/observation

# Vital sign details
./code/@displayName                     # Type of vital (BP, Temp, etc.)
./code/@code                           # LOINC code
./value/@value                         # Measurement value
./value/@unit                          # Unit of measure
./effectiveTime/@value                 # Time recorded
./interpretationCode/@code             # Normal/High/Low flag
```

#### Specific Vital Signs
```xpath
# Blood Pressure (Systolic)
//observation[code/@code='8480-6']/value/@value

# Blood Pressure (Diastolic)  
//observation[code/@code='8462-4']/value/@value

# Temperature
//observation[code/@code='8310-5']/value/@value

# Heart Rate
//observation[code/@code='8867-4']/value/@value

# Weight
//observation[code/@code='29463-7']/value/@value
```

### Laboratory Results

#### Lab Results Section
```xpath
# Lab results section
/ClinicalDocument/component/structuredBody/component/section[code/@code='30954-2']

# Individual lab result observations
/ClinicalDocument/component/structuredBody/component/section[code/@code='30954-2']/entry/organizer/component/observation

# Lab result details
./code/@displayName                              # Test name
./code/@code                                     # LOINC code
./value/@value                                   # Result value
./value/@unit                                    # Unit
./referenceRange/observationRange/value/low/@value   # Normal range low
./referenceRange/observationRange/value/high/@value  # Normal range high
./interpretationCode/@code                       # H/L/N interpretation
./effectiveTime/@value                           # Result date
./statusCode/@code                               # Result status
```

## Best Practices

### 1. Null/Missing Value Handling
```xpath
# Check if element exists and has content
count(./value/@value) > 0

# Check for non-empty text content
string-length(normalize-space(./text())) > 0

# Conditional extraction with fallback
//observation[value/@value][1]/value/@value | //observation[text()][1]/text()
```

### 2. Handling Multiple Entries
```xpath
# Get first entry
(//observation)[1]

# Get last entry
(//observation)[last()]

# Get all entries (for iteration)
//observation

# Get entries with position
//observation[position() <= 5]  # First 5 entries
```

### 3. Date Range Filtering
```xpath
# Filter by date range (YYYYMMDD format)
//observation[effectiveTime/@value >= '20240101' and effectiveTime/@value <= '20241231']

# Filter by partial date (year only)
//observation[starts-with(effectiveTime/@value, '2024')]

# Most recent entries first (requires sorting in application)
//observation[effectiveTime/@value]
```

### 4. Data Sorting and Grouping
```xpath
# Group by status code
//observation[statusCode/@code='active']
//observation[statusCode/@code='completed']

# Group by code system
//observation[code/@codeSystem='2.16.840.1.113883.6.1']      # LOINC
//observation[code/@codeSystem='2.16.840.1.113883.6.96']     # SNOMED CT
```

## Common Gotchas

### 1. Case Sensitivity
```xpath
# CCD XML is case-sensitive - this will fail
//observation vs //Observation

# Correct approach
//observation
```

### 2. Namespace Handling
```xpath
# When dealing with different namespaces, use local-name()
//*[local-name()='observation']
//*[local-name()='ClinicalDocument']

# Register namespaces in your XPath processor when possible
```

### 3. Coded Values
```xpath
# Always check both @code and @displayName
./code/@displayName    # Human-readable name
./code/@code          # Machine-readable code

# Some systems only populate one or the other
./code/@displayName | ./code/@code
```

### 4. Date Format Variations
```xpath
# Handle different date formats
effectiveTime/@value                    # Full timestamp: 20240815143000
substring(effectiveTime/@value, 1, 8)   # Date only: 20240815
effectiveTime/low/@value                # Start date in range
effectiveTime/high/@value               # End date in range
```

### 5. Text vs Structured Content
```xpath
# Structured data (preferred)
./value/@value

# Fallback to narrative text
./text/content/text()

# Combined approach
./value/@value | ./text/content/text()
```

## Template Structure

Most CCD sections follow this hierarchical pattern:

```
ClinicalDocument
└── component
    └── structuredBody
        └── component
            └── section
                ├── code (@code, @displayName)          # Section identifier
                ├── title                               # Human-readable title
                ├── text                               # Narrative content
                └── entry                             # Structured data
                    └── [clinical statements]         # Observations, procedures, etc.
                        ├── statusCode
                        ├── effectiveTime
                        ├── value
                        └── [relationships]
```

### Section Code Reference

| Section | LOINC Code | Description |
|---------|------------|-------------|
| Problems | 11450-4 | Problem List |
| Medications | 10160-0 | Medication List |
| Allergies | 48765-2 | Allergies and Adverse Reactions |
| Vital Signs | 8716-3 | Vital Signs |
| Lab Results | 30954-2 | Relevant Diagnostic Tests |
| Procedures | 47519-4 | History of Procedures |
| Immunizations | 11369-6 | Immunization History |
| Social History | 29762-2 | Social History |

## Advanced Patterns

### Conditional Logic
```xpath
# If-then-else logic (XPath 2.0+)
if (count(./value/@value) > 0) then ./value/@value else 'Not specified'

# Using XPath 1.0 alternatives
./value/@value[string-length(.) > 0] | 'Not specified'[not(../value/@value)]
```

### Complex Filtering
```xpath
# Multiple conditions
//observation[statusCode/@code='active' and effectiveTime/@value >= '20240101']

# Exclude certain codes
//observation[not(code/@code='exclude-this-code')]

# Pattern matching
//observation[contains(code/@displayName, 'Blood')]
```

This guide provides a foundation for extracting meaningful data from CCD documents. Always test XPath expressions against your specific CCD implementations, as variations in structure and content are common across different healthcare systems.
