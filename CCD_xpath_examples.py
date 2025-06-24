"""
CCD XPath Examples and Utilities

This module provides practical examples and utility functions for extracting
data from Continuity of Care Documents (CCD) using XPath expressions.

Author: [Your Name]
Created during Health Informatics Internship at MIHIN
"""

from lxml import etree
from typing import Dict, List, Any, Optional
import xml.etree.ElementTree as ET
from datetime import datetime


class CCDParser:
    """
    A utility class for parsing CCD documents and extracting structured data.
    """
    
    def __init__(self, ccd_content: str):
        """
        Initialize the CCD parser with document content.
        
        Args:
            ccd_content (str): XML content of the CCD document
        """
        try:
            self.root = etree.fromstring(ccd_content.encode('utf-8'))
            self.namespaces = self._extract_namespaces()
        except etree.XMLSyntaxError as e:
            raise ValueError(f"Invalid XML content: {str(e)}")
    
    def _extract_namespaces(self) -> Dict[str, str]:
        """Extract namespaces from the CCD document."""
        namespaces = {
            'cda': 'urn:hl7-org:v3',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
        
        # Add any additional namespaces found in the document
        for _, ns in etree.iterwalk(self.root, events=['start-ns']):
            if ns[0] and ns[1]:
                namespaces[ns[0]] = ns[1]
        
        return namespaces
    
    def xpath_query(self, xpath_expression: str) -> List[etree._Element]:
        """
        Execute an XPath query on the CCD document.
        
        Args:
            xpath_expression (str): XPath expression to execute
            
        Returns:
            List[etree._Element]: List of matching elements
        """
        try:
            return self.root.xpath(xpath_expression, namespaces=self.namespaces)
        except etree.XPathEvalError as e:
            print(f"XPath Error: {str(e)}")
            return []
    
    def extract_patient_demographics(self) -> Dict[str, Any]:
        """
        Extract patient demographic information from CCD.
        
        Returns:
            Dict[str, Any]: Patient demographics data
        """
        demographics = {}
        
        # Patient name
        given_names = self.xpath_query("//cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:patient/cda:name/cda:given/text()")
        family_name = self.xpath_query("//cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:patient/cda:name/cda:family/text()")
        
        if given_names and family_name:
            demographics['full_name'] = f"{' '.join(given_names)} {family_name[0]}"
            demographics['first_name'] = given_names[0] if given_names else ""
            demographics['last_name'] = family_name[0] if family_name else ""
        
        # Gender
        gender_code = self.xpath_query("//cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:patient/cda:administrativeGenderCode/@code")
        gender_display = self.xpath_query("//cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:patient/cda:administrativeGenderCode/@displayName")
        
        if gender_code:
            demographics['gender_code'] = gender_code[0]
        if gender_display:
            demographics['gender'] = gender_display[0]
        
        # Date of birth
        birth_time = self.xpath_query("//cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:patient/cda:birthTime/@value")
        if birth_time:
            demographics['date_of_birth'] = self._format_hl7_date(birth_time[0])
        
        # Address
        address_parts = {
            'street': self.xpath_query("//cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:addr/cda:streetAddressLine/text()"),
            'city': self.xpath_query("//cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:addr/cda:city/text()"),
            'state': self.xpath_query("//cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:addr/cda:state/text()"),
            'postal_code': self.xpath_query("//cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:addr/cda:postalCode/text()")
        }
        
        address = {}
        for key, values in address_parts.items():
            if values:
                address[key] = values[0]
        
        if address:
            demographics['address'] = address
        
        # Phone number
        phone = self.xpath_query("//cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:telecom[@use='HP']/@value")
        if phone:
            demographics['phone'] = phone[0].replace('tel:', '')
        
        return demographics
    
    def extract_problems(self) -> List[Dict[str, Any]]:
        """
        Extract problem list from CCD.
        
        Returns:
            List[Dict[str, Any]]: List of problems/conditions
        """
        problems = []
        
        # Problem list section (LOINC code 11450-4)
        problem_observations = self.xpath_query(
            "//cda:section[cda:code/@code='11450-4']//cda:observation"
        )
        
        for observation in problem_observations:
            problem = {}
            
            # Problem name
            display_name = observation.xpath(".//cda:value/@displayName", namespaces=self.namespaces)
            if display_name:
                problem['condition'] = display_name[0]
            
            # Problem code
            code = observation.xpath(".//cda:value/@code", namespaces=self.namespaces)
            if code:
                problem['code'] = code[0]
            
            # Status
            status = observation.xpath(".//cda:statusCode/@code", namespaces=self.namespaces)
            if status:
                problem['status'] = status[0]
            
            # Onset date
            onset_date = observation.xpath(".//cda:effectiveTime/cda:low/@value", namespaces=self.namespaces)
            if onset_date:
                problem['onset_date'] = self._format_hl7_date(onset_date[0])
            
            # Resolution date
            resolution_date = observation.xpath(".//cda:effectiveTime/cda:high/@value", namespaces=self.namespaces)
            if resolution_date:
                problem['resolution_date'] = self._format_hl7_date(resolution_date[0])
            
            if problem:  # Only add if we found some data
                problems.append(problem)
        
        return problems
    
    def extract_medications(self) -> List[Dict[str, Any]]:
        """
        Extract medication list from CCD.
        
        Returns:
            List[Dict[str, Any]]: List of medications
        """
        medications = []
        
        # Medications section (LOINC code 10160-0)
        med_administrations = self.xpath_query(
            "//cda:section[cda:code/@code='10160-0']//cda:substanceAdministration"
        )
        
        for administration in med_administrations:
            medication = {}
            
            # Medication name
            med_name = administration.xpath(".//cda:manufacturedMaterial/cda:code/@displayName", namespaces=self.namespaces)
            if med_name:
                medication['medication'] = med_name[0]
            
            # Medication code
            med_code = administration.xpath(".//cda:manufacturedMaterial/cda:code/@code", namespaces=self.namespaces)
            if med_code:
                medication['code'] = med_code[0]
            
            # Dose
            dose_value = administration.xpath(".//cda:doseQuantity/@value", namespaces=self.namespaces)
            dose_unit = administration.xpath(".//cda:doseQuantity/@unit", namespaces=self.namespaces)
            if dose_value and dose_unit:
                medication['dose'] = f"{dose_value[0]} {dose_unit[0]}"
            
            # Route
            route = administration.xpath(".//cda:routeCode/@displayName", namespaces=self.namespaces)
            if route:
                medication['route'] = route[0]
            
            # Status
            status = administration.xpath(".//cda:statusCode/@code", namespaces=self.namespaces)
            if status:
                medication['status'] = status[0]
            
            # Start date
            start_date = administration.xpath(".//cda:effectiveTime[@xsi:type='IVL_TS']/cda:low/@value", namespaces=self.namespaces)
            if start_date:
                medication['start_date'] = self._format_hl7_date(start_date[0])
            
            if medication:  # Only add if we found some data
                medications.append(medication)
        
        return medications
    
    def extract_allergies(self) -> List[Dict[str, Any]]:
        """
        Extract allergy information from CCD.
        
        Returns:
            List[Dict[str, Any]]: List of allergies
        """
        allergies = []
        
        # Allergies section (LOINC code 48765-2)
        allergy_observations = self.xpath_query(
            "//cda:section[cda:code/@code='48765-2']//cda:observation"
        )
        
        for observation in allergy_observations:
            allergy = {}
            
            # Allergen
            allergen = observation.xpath(".//cda:participant/cda:participantRole/cda:playingEntity/cda:code/@displayName", namespaces=self.namespaces)
            if allergen:
                allergy['allergen'] = allergen[0]
            
            # Reaction
            reaction = observation.xpath(".//cda:value/@displayName", namespaces=self.namespaces)
            if reaction:
                allergy['reaction'] = reaction[0]
            
            # Severity
            severity = observation.xpath(".//cda:entryRelationship/cda:observation[cda:code/@code='SEV']/cda:value/@displayName", namespaces=self.namespaces)
            if severity:
                allergy['severity'] = severity[0]
            
            if allergy:  # Only add if we found some data
                allergies.append(allergy)
        
        return allergies
