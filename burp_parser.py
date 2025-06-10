#!/usr/bin/env python3

import os
import base64
import re
from pathlib import Path

def parse_burp_xml(input_file_path):
    """
    Parses a Burp XML file, extracts all base64-encoded <request> elements,
    decodes them, saves each to a text file, removes any OPTIONS requests,
    and renumbers the remaining files sequentially.
    """
    # Create output directory if it doesn't exist
    output_dir = Path("./requests-from-extractedxml")
    output_dir.mkdir(exist_ok=True)
    
    # Read entire XML file
    with open(input_file_path, 'r') as f:
        content = f.read()
    
    # Find all base64 blocks inside <request base64="true"><![CDATA[...]]>
    base64_requests = re.findall(
        r'<request\s+base64="true"><!\[CDATA\[(.*?)\]\]>',
        content,
        re.DOTALL
    )
    
    decoded_files = []
    # Decode each and write to a numbered .txt
    for idx, encoded in enumerate(base64_requests, start=1):
        try:
            decoded = base64.b64decode(encoded).decode('utf-8', errors='replace')
        except Exception as e:
            decoded = f"[Decode Error]: {e}"
        file_path = output_dir / f"{idx}.txt"
        with open(file_path, "w") as out:
            out.write(decoded)
        decoded_files.append(file_path)
    
    # Remove any files whose first line starts with "OPTIONS "
    for file_path in decoded_files:
        with open(file_path, "r") as f:
            first_line = f.readline()
        if first_line.startswith("OPTIONS "):
            print(f"Removing {file_path} as it contains an OPTIONS request.")
            file_path.unlink()
    
    # Renumber the remaining files sequentially
    remaining = sorted(output_dir.glob("*.txt"))
    for new_idx, file_path in enumerate(remaining, start=1):
        target = output_dir / f"{new_idx}.txt"
        if file_path.name != target.name:
            file_path.rename(target)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <burp_xml_file>")
        sys.exit(1)
    parse_burp_xml(sys.argv[1])
