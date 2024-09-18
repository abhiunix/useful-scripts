import os
import argparse
import gzip
import shutil
import json
from warcio.archiveiterator import ArchiveIterator

# Function to extract and save all HTML responses and line numbers
def extract_responses_with_line_numbers(warc_file, target_uri, output_html_dir, output_json_file):
    response_instances = []  # To store instances of the URI along with line numbers
    line_counter = 0  # To track the current line number

    # Ensure the output directory exists
    if not os.path.exists(output_html_dir):
        os.makedirs(output_html_dir)

    with open(warc_file, 'rb') as stream:
        for record in ArchiveIterator(stream, arc2warc=True):
            line_counter += 1  # Increment line number for each record

            if record.rec_headers.get_header('WARC-Type') == 'response':
                uri = record.rec_headers.get_header('WARC-Target-URI')

                # Check if this is the desired URI
                if uri == target_uri:
                    # Read and decode the response content
                    payload = record.content_stream().read()

                    # Generate a unique filename for each response
                    response_filename = f"{output_html_dir}/response_{len(response_instances) + 1}.html"

                    # Save the response content to an HTML file
                    with open(response_filename, 'wb') as html_file:
                        html_file.write(payload)

                    # Append the response information to the list with the line number
                    response_instances.append({
                        "uri": uri,
                        "line_number": line_counter,
                        "html_file": response_filename
                    })

    # Save the JSON file with the instances
    with open(output_json_file, 'w') as json_file:
        json.dump(response_instances, json_file, indent=4)

    print(f"Extracted {len(response_instances)} instances of {target_uri}.")
    print(f"JSON file with line numbers saved to {output_json_file}.")

# Function to decompress .gz files
def decompress_warc_gz(warc_gz_file):
    warc_file = warc_gz_file.replace('.gz', '')
    print(f"Decompressing {warc_gz_file} to {warc_file}...")
    with gzip.open(warc_gz_file, 'rb') as f_in:
        with open(warc_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Decompression complete: {warc_file}")
    return warc_file

# Main function to handle arguments
def main():
    parser = argparse.ArgumentParser(description="Extract responses from a WARC or WARC.GZ file.")

    # Add the WARC file argument
    parser.add_argument('warc_file', help='Path to the WARC or WARC.GZ file')

    # Add optional output directory and JSON file
    parser.add_argument('--output_html_dir', default='responses', help='Directory to save HTML responses')
    parser.add_argument('--output_json_file', default='response_instances.json', help='File to save response instances in JSON format')
    parser.add_argument('--target_uri', required=True, help='Target URI to filter responses')

    args = parser.parse_args()

    warc_file = args.warc_file

    # Check if the file is a .gz file and decompress if necessary
    if warc_file.endswith('.gz'):
        warc_file = decompress_warc_gz(warc_file)

    # Run the extraction with the (possibly decompressed) WARC file
    extract_responses_with_line_numbers(warc_file, args.target_uri, args.output_html_dir, args.output_json_file)

    # Clean up the decompressed WARC file if it was originally a .gz file
    if args.warc_file.endswith('.gz'):
        os.remove(warc_file)
        print(f"Deleted decompressed file: {warc_file}")

if __name__ == "__main__":
    main()
