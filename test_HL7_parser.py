"""
Unit Tests for HL7 OBX Subsegment Parser

This module contains comprehensive tests for the HL7 OBX subsegment parser,
including positive tests, negative tests, and edge cases.

Author: [Your Name]
Created during Health Informatics Internship at MIHIN
"""

import pytest
import sys
import os

# Add the parent directory to path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from hl7_obx_parser import check_obx_subsegments, validate_obx_requirements, print_obx_results
from examples.sample_hl7_messages import (
    get_sample_message, 
    get_expected_results, 
    list_available_messages,
    SAMPLE_MESSAGES
)


class TestHL7OBXParser:
    """Test class for HL7 OBX subsegment parser functionality."""
    
    def test_complete_oru_message(self):
        """Test parsing of complete ORU message with all OBX subsegments."""
        message = get_sample_message('complete_oru')
        expected = get_expected_results('complete_oru')
        
        results = check_obx_subsegments(message)
        
        assert results['OBX.15.1'] == expected['OBX.15.1']
        assert results['OBX.15.2'] == expected['OBX.15.2']
        assert results['OBX.23.1'] == expected['OBX.23.1']
    
    def test_incomplete_oru_message(self):
        """Test parsing of ORU message missing OBX subsegments."""
        message = get_sample_message('incomplete_oru')
        expected = get_expected_results('incomplete_oru')
        
        results = check_obx_subsegments(message)
        
        assert results['OBX.15.1'] == expected['OBX.15.1']
        assert results['OBX.15.2'] == expected['OBX.15.2']
        assert results['OBX.23.1'] == expected['OBX.23.1']
        
        # Verify all lists are empty
        assert len(results['OBX.15.1']) == 0
        assert len(results['OBX.15.2']) == 0
        assert len(results['OBX.23.1']) == 0
    
    def test_complex_oru_message(self):
        """Test parsing of complex ORU message with varied content."""
        message = get_sample_message('complex_oru')
        expected = get_expected_results('complex_oru')
        
        results = check_obx_subsegments(message)
        
        assert results['OBX.15.1'] == expected['OBX.15.1']
        assert results['OBX.15.2'] == expected['OBX.15.2']
        assert results['OBX.23.1'] == expected['OBX.23.1']
    
    def test_international_message(self):
        """Test parsing of message with international characters."""
        message = get_sample_message('international')
        expected = get_expected_results('international')
        
        results = check_obx_subsegments(message)
        
        assert results['OBX.15.1'] == expected['OBX.15.1']
        assert results['OBX.15.2'] == expected['OBX.15.2']
        assert results['OBX.23.1'] == expected['OBX.23.1']
    
    def test_empty_message(self):
        """Test parsing of empty message."""
        with pytest.raises(Exception):  # Should raise parsing exception
            check_obx_subsegments("")
    
    def test_invalid_hl7_message(self):
        """Test parsing of invalid HL7 message."""
        invalid_message = "This is not a valid HL7 message"
        
        with pytest.raises(Exception):
            check_obx_subsegments(invalid_message)
    
    def test_message_without_obx(self):
        """Test parsing of valid HL7 message without OBX segments."""
        message = get_sample_message('adt_update')  # ADT message has no OBX
        
        results = check_obx_subsegments(message)
        
        # Should return empty lists for all OBX fields
        assert len(results['OBX.15.1']) == 0
        assert len(results['OBX.15.2']) == 0
        assert len(results['OBX.23.1']) == 0
    
    def test_malformed_obx_segment(self):
        """Test parsing of message with malformed OBX segment."""
        malformed_message = """MSH|^~\\&|TEST|TEST|TEST|TEST|20240815||ORU^R01|TEST|P|2.5.1|
OBX|1|TX|  # This OBX segment is incomplete
OBX|2|NM|1234||50|mg||||||F|||20240815||||LAB^REPORT|||||||||PROCESS^1|"""
        
        # Should not crash, should handle gracefully
        results = check_obx_subsegments(malformed_message)
        assert isinstance(results, dict)
        assert 'OBX.15.1' in results
        assert 'OBX.15.2' in results
        assert 'OBX.23.1' in results


class TestValidationFunctions:
    """Test class for validation helper functions."""
    
    def test_validate_all_present(self):
        """Test validation when all required fields are present."""
        results = {
            'OBX.15.1': ['LAB'],
            'OBX.15.2': ['LABORATORY'],
            'OBX.23.1': ['PROCESS_001']
        }
        
        validation = validate_obx_requirements(results)
        
        assert validation['is_valid'] is True
        assert len(validation['missing_fields']) == 0
        assert validation['total_present'] == 3
        assert validation['total_required'] == 3
    
    def test_validate_partial_present(self):
        """Test validation when some required fields are missing."""
        results = {
            'OBX.15.1': ['LAB'],
            'OBX.15.2': [],  # Missing
            'OBX.23.1': ['PROCESS_001']
        }
        
        validation = validate_obx_requirements(results)
        
        assert validation['is_valid'] is False
        assert 'OBX.15.2' in validation['missing_fields']
        assert validation['total_present'] == 2
        assert validation['total_required'] == 3
    
    def test_validate_custom_requirements(self):
        """Test validation with custom required fields."""
        results = {
            'OBX.15.1': ['LAB'],
            'OBX.15.2': [],
            'OBX.23.1': ['PROCESS_001']
        }
        
        # Only require OBX.15.1 and OBX.23.1
        validation = validate_obx_requirements(results, ['OBX.15.1', 'OBX.23.1'])
        
        assert validation['is_valid'] is True
        assert len(validation['missing_fields']) == 0
        assert validation['total_present'] == 2
        assert validation['total_required'] == 2
    
    def test_validate_none_present(self):
        """Test validation when no required fields are present."""
        results = {
            'OBX.15.1': [],
            'OBX.15.2': [],
            'OBX.23.1': []
        }
        
        validation = validate_obx_requirements(results)
        
        assert validation['is_valid'] is False
        assert len(validation['missing_fields']) == 3
        assert validation['total_present'] == 0


class TestUtilityFunctions:
    """Test class for utility functions."""
    
    def test_print_results_function(self, capsys):
        """Test the print_obx_results function output."""
        results = {
            'OBX.15.1': ['LAB_TECH', 'CENTRAL_LAB'],
            'OBX.15.2': ['TECHNICIAN'],
            'OBX.23.1': []
        }
        
        print_obx_results(results)
        captured = capsys.readouterr()
        
        assert "OBX SUBSEGMENT ANALYSIS RESULTS" in captured.out
        assert "OBX.15.1: Present" in captured.out
        assert "OBX.15.2: Present" in captured.out
        assert "OBX.23.1: Not present" in captured.out
        assert "LAB_TECH" in captured.out
        assert "CENTRAL_LAB" in captured.out


class TestIntegrationScenarios:
    """Integration tests for real-world scenarios."""
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from message to validation."""
        message = get_sample_message('complete_oru')
        
        # Parse the message
        results = check_obx_subsegments(message)
        
        # Validate results
        validation = validate_obx_requirements(results)
        
        # Assert end-to-end success
        assert isinstance(results, dict)
        assert validation['is_valid'] is True
        assert all(len(values) > 0 for values in results.values())
    
    def test_batch_processing(self):
        """Test processing multiple messages in batch."""
        batch_results = {}
        
        for msg_type in ['complete_oru', 'incomplete_oru', 'complex_oru']:
            message = get_sample_message(msg_type)
            results = check_obx_subsegments(message)
            batch_results[msg_type] = results
        
        # Verify all messages were processed
        assert len(batch_results) == 3
        assert all(isinstance(result, dict) for result in batch_results.values())
        
        # Verify different outcomes
        assert len(batch_results['complete_oru']['OBX.15.1']) > 0
        assert len(batch_results['incomplete_oru']['OBX.15.1']) == 0
        assert len(batch_results['complex_oru']['OBX.15.1']) > 0


# Pytest fixtures
@pytest.fixture
def sample_complete_message():
    """Fixture providing a complete HL7 message."""
    return get_sample_message('complete_oru')


@pytest.fixture
def sample_incomplete_message():
    """Fixture providing an incomplete HL7 message."""
    return get_sample_message('incomplete_oru')


# Performance tests
class TestPerformance:
    """Performance tests for the parser."""
    
    def test_large_message_performance(self):
        """Test performance with larger HL7 messages."""
        # Create a message with many OBX segments
        base_message = get_sample_message('complete_oru')
        obx_segment = "OBX|4|NM|TEST^TEST^L||100|mg||||||F|||20240815||||LAB^TECH|||||||||PROC^4|"
        
        # Add 100 additional OBX segments
        large_message = base_message + '\n' + '\n'.join([obx_segment] * 100)
        
        import time
        start_time = time.time()
        results = check_obx_subsegments(large_message)
        end_time = time.time()
        
        # Should complete within reasonable time (less than 1 second)
        assert (end_time - start_time) < 1.0
        assert len(results['OBX.15.1']) > 100  # Should find many entries


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v", "--tb=short"])
