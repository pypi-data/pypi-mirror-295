#!/#usr/bin/env python
###############################################################################
# (c) Copyright 2000-2024 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import argparse
import xml.etree.ElementTree as ET

import apd

###########################################################
#                                                         #
# The function of this script is to add authentication    #
# tokens to the paths in the file catalog xml file.       #
# This is necessary for the CI to have access to the data #
#                                                         #
###########################################################


########################################################
# Functions to do all of the dirty authentication work #
########################################################


def append_token(pfn):
    print(f"Appending token for {pfn!r}")
    token = apd.auth(pfn)  # Replace the pfn with the tokened pfns.
    return token


# Use this guy to process the pfn, obstaining the mdf prepend for the xrootd protocol, and then putting it back
def process_pfn(string):
    if string.startswith("mdf:"):
        temp_string = string[4:]
    else:
        temp_string = string
    new_string = append_token(temp_string)
    if string.startswith("mdf:"):
        new_string = "mdf:" + new_string
    return new_string


def replace_elements_in_xml(file_path):
    # Load XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    # Iterate over each old element and its corresponding replacement
    for element in root.iter("pfn"):
        element.set("name", process_pfn(element.get("name")))

    # Modify the pool catalog file
    xml_string = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
        + '<!DOCTYPE POOLFILECATALOG SYSTEM "InMemory">\n'
        + ET.tostring(root).decode("utf-8")
    )
    with open(file_path, "wt") as fh:
        fh.write(xml_string)

    print(f"XML file {file_path!r} modified and saved as {file_path!r}.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pool_xml_fn")
    args = parser.parse_args()

    # Create a new XML file to use in the test
    replace_elements_in_xml(args.pool_xml_fn)


if __name__ == "__main__":
    main()
