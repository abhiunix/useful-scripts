#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 [-d directory] [-l file]"
    exit 1
}

# Parse flags
while getopts "d:l:" flag; do
    case "${flag}" in
        d) directory=${OPTARG} ;;
        l) file=${OPTARG} ;;
        *) usage ;;
    esac
done

# Check if both flags are provided
if [ -z "$directory" ] || [ -z "$file" ]; then
    usage
fi

# Create the root directory if it doesn't exist
mkdir -p "$directory"

# Function to download a file and handle duplication
download_file() {
    url=$1
    base_dir=$directory
    file_path="${base_dir}/$(echo "$url" | sed 's~http[s]*://~~')"
    file_dir=$(dirname "$file_path")
    file_name=$(basename "$file_path")

    # Create the necessary directories
    mkdir -p "$file_dir"

    # Check for file duplication and append a counter if necessary
    counter=1
    original_file_path="$file_path"
    while [[ -e "$file_path" ]]; do
        file_path="${original_file_path}-${counter}"
        counter=$((counter + 1))
    done

    # Download the file
    wget -q "$url" -O "$file_path"
}

# Extract the .js URLs, remove duplicates, and process each one
sort -u "$file" | while read -r url; do
    download_file "$url"
done
