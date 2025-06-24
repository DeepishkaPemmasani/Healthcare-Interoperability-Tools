"""
Sample HL7 V2 Messages for Testing

This module contains sample HL7 V2 messages that can be used for testing
the OBX subsegment parser and other HL7 processing tools.

Author: [Your Name]
Created during Health Informatics Internship at MIHIN
"""

# Sample ORU^R01 (Observation Report) message with multiple OBX segments
SAMPLE_ORU_MESSAGE = """MSH|^~\\&|LAB_SYSTEM|HOSPITAL_LAB|EMR_SYSTEM|MAIN_HOSPITAL|20240815143000||ORU^R01|MSG001234|P|2.5.1|
PID|1||123456789^^^HOSPITAL^MR||DOE^JOHN^MIDDLE||19800101|M|||123 MAIN ST^^ANYTOWN^MI^48001||555-123-4567|||||123-45-6789|
OBR|1|ORDER123|RESULT456|1234^COMPLETE BLOOD COUNT^L|||20240815140000|||||||||DR^SMITH^ATTENDING|||||||20240815143000|||F|
OBX|1|NM|718-7^HEMOGLOBIN^LN||14.5|g/dL|12.0-16.0|N|||F|||20240815143000||||LAB_TECH^TECHNICIAN_NAME|||||||||PROCESS_ID_001^1|
OBX|2|NM|4544-3^HEMATOCRIT^LN||42.5|%|36.0-46.0|N|||F|||20240815143000||||LAB_TECH^TECHNICIAN_NAME|||||||||PROCESS_ID_002^2|
OBX|3|NM|6690-2^WBC^LN||7.2|10*3/uL|4.5-11.0|N|||F|||20240815143000||||CENTRAL_LAB^MAIN_LABORATORY|||||||||CBC_PROCESS^3|"""

# Sample ORU message with missing OBX subsegments (for negative testing)
SAMPLE_INCOMPLETE_MESSAGE = """MSH|^~\\&|LAB_SYSTEM|HOSPITAL_LAB|EMR_SYSTEM|MAIN_HOSPITAL|20240815143000||ORU^R01|MSG001235|P|2.5.1|
PID|1||123456790^^^HOSPITAL^MR||SMITH^JANE^||19750515|F|||456 OAK AVE^^SOMEWHERE^MI^48002||555-987-6543|||||987-65-4321|
OBR|1|ORDER124|RESULT457|2345^BASIC METABOLIC PANEL^L|||20240815140000|||||||||DR^JONES^ATTENDING|||||||20240815143000|||F|
OBX|1|NM|2345-7^GLUCOSE^LN||95|mg/dL|70-100|N|||F|||20240815143000|||||||||||||||||
OBX|2|NM|2160-0^CREATININE^LN||1.0|mg/dL|0.6-1.2|N|||F|||20240815143000|||||||||||||||||"""

# Sample message with complex OBX subsegments
SAMPLE_COMPLEX_MESSAGE = """MSH|^~\\&|RADIOLOGY|HOSPITAL_RAD|PACS_SYSTEM|MAIN_HOSPITAL|20240815150000||ORU^R01|MSG001236|P|2.5.1|
PID|1||123456791^^^HOSPITAL^MR||BROWN^MICHAEL^A||19650320|M|||789 PINE ST^^CITYVILLE^MI^48003||555-555-5555|||||555-44-3333|
OBR|1|ORDER125|RESULT458|36554-4^CHEST X-RAY^LN|||20240815145000|||||||||DR^RADIOLOGIST^CHIEF|||||||20240815150000|||F|
OBX|1|TX|36554-4^CHEST X-RAY^LN||IMPRESSION: Normal chest x-ray. No acute cardiopulmonary abnormalities.||||F|||20240815150000||||RADIOLOGY_DEPT^IMAGING_CENTER|||||||||RAD_QC_001^QUALITY_CONTROL|
OBX|2|TX|18782-3^RADIOLOGY REPORT^LN||TECHNIQUE: PA and lateral chest radiographs||||F|||20240815150000||||RAD_TECH^TECHNOLOGIST_NAME|||||||||IMAGE_PROC_002^FINAL|"""

# Sample ADT^A08 (Update Patient Information) message
SAMPLE_ADT_MESSAGE = """MSH|^~\\&|ADT_SYSTEM|MAIN_HOSPITAL|REGISTRATION|MAIN_HOSPITAL|20240815160000||ADT^A08|MSG001237|P|2.5.1|
EVN||20240815160000|||USER123|20240815160000|
PID|1||123456792^^^HOSPITAL^MR||WILSON^SARAH^ELIZABETH||19901205|F|||321 ELM ST^^NEWTOWN^MI^48004||555-111-2222|||||111-22-3333|
PV1|1|I|ICU^101^A|||||||||||||||123456792^^^HOSPITAL^VN|||||||||||||||||||||||||20240815160000|"""

# Sample message with international characters and special cases
SAMPLE_INTERNATIONAL_MESSAGE = """MSH|^~\\&|INTL_SYSTEM|GLOBAL_HOSPITAL|EMR_INTL|MAIN_HOSPITAL|20240815170000||ORU^R01|MSG001238|P|2.5.1|
PID|1||INT123456^^^HOSPITAL^MR||GARCÍA^MARÍA^JOSÉ||19851215|F|||555 INTERNATIONAL BLVD^^GLOBAL CITY^MI^48005||555-999-8888|||||999-88-7777|
OBR|1|INTL_ORDER|INTL_RESULT|3456^INTERNATIONAL TEST^L|||20240815165000|||||||||DR^INTERNATIONAL^SPECIALIST|||||||20240815170000|||F|
OBX|1|ST|INTL-001^SPECIAL TEST^L||Résultat spécial avec caractères accentués||||F|||20240815170000||||INTL_LAB^LABORATOIRE_INTERNATIONAL|||||||||INTL_PROC_001^SPÉCIAL|"""

# Dictionary containing all sample messages for easy access
SAMPLE_MESSAGES = {
    'complete_oru': SAMPLE_ORU_MESSAGE,
    'incomplete_oru': SAMPLE_INCOMPLETE_MESSAGE,
    'complex_oru': SAMPLE_COMPLEX_MESSAGE,
    'adt_update': SAMPLE_ADT_MESSAGE,
    'international': SAMPLE_INTERNATIONAL_MESSAGE
}

# Expected results for testing
EXPECTED_RESULTS = {
    'complete_oru': {
        'OBX.15.1': ['LAB_TECH', 'LAB_TECH', 'CENTRAL_LAB'],
        'OBX.15.2': ['TECHNICIAN_NAME', 'TECHNICIAN_NAME', 'MAIN_LABORATORY'],
        'OBX.23.1': ['PROCESS_ID_001', 'PROCESS_ID_002', 'CBC_PROCESS']
    },
    'incomplete_oru': {
        'OBX.15.1': [],
        'OBX.15.2': [],
        'OBX.23.1': []
    },
    'complex_oru': {
        'OBX.15.1': ['RADIOLOGY_DEPT', 'RAD_TECH'],
        'OBX.15.2': ['IMAGING_CENTER', 'TECHNOLOGIST_NAME'],
        'OBX.23.1': ['RAD_QC_001', 'IMAGE_PROC_002']
    },
    'international': {
        'OBX.15.1': ['INTL_LAB'],
        'OBX.15.2': ['LABORATOIRE_INTERNATIONAL'],
        'OBX.23.1': ['INTL_PROC_001']
    }
}


def get_sample_message(message_type: str) -> str:
    """
    Retrieve a sample HL7 message by type.
    
    Args:
        message_type (str): Type of message to retrieve
                          ('complete_oru', 'incomplete_oru', 'complex_oru', 
                           'adt_update', 'international')
    
    Returns:
        str: HL7 message string
        
    Raises:
        KeyError: If message_type is not found
    """
    if message_type not in SAMPLE_MESSAGES:
        available_types = ', '.join(SAMPLE_MESSAGES.keys())
        raise KeyError(f"Message type '{message_type}' not found. "
                      f"Available types: {available_types}")
    
    return SAMPLE_MESSAGES[message_type]


def get_expected_results(message_type: str) -> dict:
    """
    Get expected parsing results for a sample message.
    
    Args:
        message_type (str): Type of message
        
    Returns:
        dict: Expected results for OBX subsegment parsing
    """
    return EXPECTED_RESULTS.get(message_type, {})


def list_available_messages() -> list:
    """
    List all available sample message types.
    
    Returns:
        list: List of available message type keys
    """
    return list(SAMPLE_MESSAGES.keys())


# Example usage and testing functions
if __name__ == "__main__":
    print("Available Sample HL7 Messages:")
    print("=" * 40)
    
    for msg_type in list_available_messages():
        print(f"\n{msg_type.upper().replace('_', ' ')}:")
        print("-" * 30)
        
        # Show first few lines of each message
        message = get_sample_message(msg_type)
        lines = message.split('\n')
        for i, line in enumerate(lines[:3]):  # Show first 3 lines
            print(f"  {line}")
        
        if len(lines) > 3:
            print(f"  ... ({len(lines) - 3} more lines)")
        
        # Show expected results
        expected = get_expected_results(msg_type)
        if expected:
            print(f"\n  Expected OBX subsegments:")
            for field, values in expected.items():
                count = len(values) if values else 0
                print(f"    {field}: {count} values")
