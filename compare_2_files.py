import argparse

def read_keywords_from_file(filename):
    with open(filename, 'r') as file:
        return set(line.strip() for line in file if line.strip())

def compare_files(file1, file2):
    keywords_file1 = read_keywords_from_file(file1)
    keywords_file2 = read_keywords_from_file(file2)
    
    only_in_file1 = keywords_file1 - keywords_file2
    only_in_file2 = keywords_file2 - keywords_file1
    
    return only_in_file1, only_in_file2

def print_unique_keywords(only_in_file1, only_in_file2, file1, file2):
    print(f"These keywords are present in {file1} but not in {file2}")
    for keyword in sorted(only_in_file1):
        print(keyword)
    
    print(f"\nThese keywords are present in {file2} but not in {file1}")
    for keyword in sorted(only_in_file2):
        print(keyword)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare keywords in two files.')
    parser.add_argument('file1', type=str, help='First input file')
    parser.add_argument('file2', type=str, help='Second input file')

    args = parser.parse_args()
    
    only_in_file1, only_in_file2 = compare_files(args.file1, args.file2)
    print_unique_keywords(only_in_file1, only_in_file2, args.file1, args.file2)


#Usage:
# python3 compare_2_files.py out2.txt output.txt
