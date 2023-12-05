import os

def collect_files(parent_directory, output_file):
    with open(output_file, 'w') as output:
        for filename in os.listdir(parent_directory):
            if filename.endswith(".py"):  # Adjust the file extension if needed
                with open(os.path.join(parent_directory, filename), 'r') as file:
                    file_contents = file.read()
                    output.write(f"``` {filename} {file_contents} ```\n\n\n")

# Replace 'output.txt' with the desired output file name
# Use '..' to specify the parent directory
collect_files('./', './scripts/all_text.txt')
