###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from xml.etree import ElementTree as ET

import pytest

from apd.pool_xml import replace_elements_in_xml


@pytest.fixture
def sample_xml_file(tmp_path):
    # Create a temporary XML file with sample content in the pytest-provided temporary directory
    sample_xml_content = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
    <POOLFILECATALOG>
        <File ID="sample-id">
            <physical>
                <pfn filetype="ROOT_All" name="root://example.com//path/to/file" se="Example-SE"/>
            </physical>
            <logical>
                <lfn name="/path/to/logical/file"/>
            </logical>
        </File>
    </POOLFILECATALOG>
    """
    file_path = tmp_path / "sample.xml"
    file_path.write_text(sample_xml_content)
    return file_path


def test_replace_elements_in_xml(monkeypatch, sample_xml_file):
    # Mock the apd.pool_xml.apd.auth function to return a tokenized PFN
    monkeypatch.setattr("apd.pool_xml.apd.auth", lambda x: f"{x}?token=12345")

    replace_elements_in_xml(str(sample_xml_file))

    # Load the modified XML to verify changes
    tree = ET.parse(sample_xml_file)
    root = tree.getroot()

    # Assert that the PFN has been updated with a token
    pfn_element = root.find(".//pfn")
    assert pfn_element is not None
    assert pfn_element.get("name") == "root://example.com//path/to/file?token=12345"
