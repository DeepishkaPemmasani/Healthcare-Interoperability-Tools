# Healthcare Interoperability Tools

A collection of healthcare data interoperability tools developed during my Health Informatics internship at MIHIN (Michigan Health Information Network). This repository contains utilities for processing HL7 V2 messages and CCD (Continuity of Care Document) data mapping.

## 🏥 About

This project demonstrates practical applications of healthcare data standards and interoperability protocols, focusing on:
- HL7 V2 message parsing and validation
- CCD/C-CDA document data extraction
- Healthcare data mapping and transformation

## 🛠️ Tools & Technologies

- **Python**: Primary development language
- **HL7 Library**: For HL7 V2 message processing
- **XPath**: For CCD/XML document parsing
- **Healthcare Standards**: HL7 V2, C-CDA, FHIR concepts

## 📁 Project Structure

```
healthcare-interoperability-tools/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── hl7-tools/
│   ├── hl7_obx_parser.py
│   ├── examples/
│   │   └── sample_hl7_messages.py
│   └── tests/
│       └── test_hl7_parser.py
├── ccd-tools/
│   ├── ccd_mapping_guide.md
│   ├── ccd_xpath_examples.py
│   └── examples/
│       └── sample_ccd_extracts.xml
└── docs/
    ├── hl7_documentation.md
    └── ccd_documentation.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip package manager

### Installation
1. Clone the repository:
```bash
git clone https://github.com/DeepishkaPemmasani/healthcare-interoperability-tools.git
cd healthcare-interoperability-tools
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### HL7 V2 OBX Segment Parser
```python
from hl7_tools.hl7_obx_parser import check_obx_subsegments

# Parse HL7 message for specific OBX subsegments
results = check_obx_subsegments(your_hl7_message)
print(results)
```

#### CCD Data Mapping
Refer to `ccd-tools/ccd_mapping_guide.md` for comprehensive XPath patterns for extracting data from CCD documents.

## 📚 Documentation

- [HL7 V2 Message Processing](docs/hl7_documentation.md)
- [CCD Data Mapping Guide](ccd-tools/ccd_mapping_guide.md)

## 🔍 Features

### HL7 V2 Tools
- **OBX Subsegment Parser**: Extract specific observation subsegments (OBX.15.1, OBX.15.2, OBX.23.1)
- **Message Validation**: Verify presence of required segments and fields
- **Error Handling**: Robust parsing with graceful error management

### CCD Tools
- **XPath Pattern Library**: Pre-built patterns for common CCD data extraction
- **Data Mapping Templates**: Structured approaches for UI data mapping
- **Best Practices Guide**: Tips for handling CCD parsing edge cases

## 🏥 Healthcare Standards Compliance

This project works with industry-standard healthcare interoperability formats:
- **HL7 V2.x**: Health Level Seven International messaging standard
- **C-CDA**: Consolidated Clinical Document Architecture
- **LOINC Codes**: Logical Observation Identifiers Names and Codes

## 🤝 Contributing

This repository represents work completed during a Health Informatics internship. While not actively seeking contributions, feedback and suggestions are welcome.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MIHIN (Michigan Health Information Network)** for providing the internship opportunity
- **HL7 International** for healthcare interoperability standards
- **Healthcare IT Community** for continuous innovation in health informatics

## 📧 Contact

Feel free to reach out for questions about healthcare interoperability or this project:
- LinkedIn: [https://www.linkedin.com/in/deepishka-pemmasani/]
- Email: [deepupemmasani@gmail.com]

---
*Developed during Health Informatics Internship at MIHIN | 2024*
