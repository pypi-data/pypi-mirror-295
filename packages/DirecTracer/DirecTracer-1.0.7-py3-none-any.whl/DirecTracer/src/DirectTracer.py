import os
import urllib.parse
import time


def _print_with_loading(message, delay=0.005):
    """ Print a message with a loading animation.

    Args:
        message (str): The message to print.
        delay (float, optional): The delay between each character. Defaults to 0.005.
    """

    for char in message:
        print(char, end='', flush=True)
        time.sleep(delay)
    print("", flush=True)


def save_directory_structure(root_dir=os.getcwd(),
                             text_output_file="directory_structure.txt",
                             markdown_output_file="directory_structure.md",
                             ignored_directories=[
                                 ".git", ".vscode", "venv", ".venv", ".idea", "out"],
                             ignored_extensions=[".exe"],
                             animation=False):
    """
    Save the directory structure to text and Markdown files.

    Args:
        root_dir (str): The root directory to start scanning from. Defaults to the current working directory.
        text_output_file (str): The name of the text output file. Defaults to "directory_structure.txt".
        markdown_output_file (str): The name of the Markdown output file. Defaults to "directory_structure.md".
        ignored_directories (list, optional): List of directories to ignore. Defaults to [".git", ".vscode", "venv", ".venv", ".idea", "out"].
        ignored_extensions (list, optional): List of file extensions to ignore. Defaults to [".exe"].
        animation (bool, optional): Enable/Disable the loading animation. Defaults to False.
    """

    with open(text_output_file, 'w', encoding='utf-8') as text_f, open(markdown_output_file, 'w', encoding='utf-8') as md_f:

        # Write the Markdown header
        md_f.write("# Directory Structure\n\n")

        # Write the format template
        md_f.write("Format:\n\n")
        md_f.write("```md\n")
        md_f.write("📂 Directory\n")
        md_f.write("  - File\n")
        md_f.write("```\n\n")

        is_first_directory = True  # Flag to check if the current directory is the first one

        print("Reading directory structure...")

        # Result parameters
        total_folders = 0
        total_files = 0

        # Walk through the directory tree
        for root, dirs, files in os.walk(root_dir):

            # Remove ignored directories from the list
            if ignored_directories:
                dirs[:] = [d for d in dirs if d not in ignored_directories]

            # Get the relative path and indentation level
            relative_path = os.path.relpath(root, root_dir)
            depth = relative_path.count(os.path.sep)
            indentation = "\t" * depth

            # Write folder information to both text and Markdown files
            if is_first_directory:
                text_f.write(
                    f"{indentation}📂 {os.path.basename(root)} (Current Directory)\n")
                md_f.write(
                    f"{'  ' * depth}- 📂 **{os.path.basename(root)} (Current Directory)**\n")
                is_first_directory = False
            else:
                text_f.write(f"{indentation}📂 {os.path.basename(root)}\n")
                md_f.write(f"{'  ' * depth}- 📂 **{os.path.basename(root)}**\n")

            print(f"✅ Read {relative_path} contents")

            # Update the folder count
            total_folders += 1

            # Loop through the files in the current directory
            for file in files:

                # Get the file extension
                _, file_extension = os.path.splitext(file)

                # Skip ignored file extensions
                if ignored_extensions and file_extension in ignored_extensions:
                    continue

                # Write file information to text file
                text_f.write(f"{indentation}  - {file}\n")

                # Generate relative file path with forward slashes
                file_path = os.path.join(
                    relative_path, file).replace(os.path.sep, '/')

                # Encode spaces in the filename for Markdown link
                encoded_file_path = urllib.parse.quote(file_path)

                # Write clickable file link to Markdown file
                md_f.write(
                    f"{'  ' * (depth + 1)}- [{file}]({encoded_file_path})\n")

                # Update the file count
                total_files += 1

        if animation:
            _print_with_loading("\n🌲 Directory structure read successfully.")
            _print_with_loading(f"Total folders: {total_folders}")
            _print_with_loading(f"Total files: {total_files}", 0.02)
        else:
            print("\n🌲 Directory structure read successfully.")
            print(f"Total folders: {total_folders}")
            print(f"Total files: {total_files}")

    # Print the output file paths
    if animation:
        _print_with_loading("\nDirectory structure saved to:")
        _print_with_loading(f"📄 {text_output_file}")
        _print_with_loading(f"📘 {markdown_output_file}")
    else:
        print("\nDirectory structure saved to:")
        print(f"📄 {text_output_file}")
        print(f"📘 {markdown_output_file}")


def generate_markdown_table(root_dir=os.getcwd(), markdown_output_file="markdown_table.md", animation=False, ignored_extensions=[".exe"]):
    """
    Reads all the files in the given directory and generates a Markdown table with the following columns:
    - `#`: Serial number of the file starting from 1.
    - `File Name`: Contains [Title Case Name Of File](Relative File Path). The format of input file is "number_file_name.extension".

    Args
    ----
    - `root_dir` (str): The root directory to start scanning from. Defaults to the current working directory.
    - `markdown_output_file` (str): The name of the Markdown output file. Defaults to "markdown_table.md".
    - `animation` (bool, optional): Enable/Disable the loading animation. Defaults to False.
    - `ignored_extensions` (list, optional): List of file extensions to ignore. Defaults to [".exe"].
    """

    with open(markdown_output_file, 'w', encoding='utf-8') as md_f:

        # Write the Markdown header
        md_f.write("# Markdown Table\n\n")

        # Write the format template
        md_f.write("Format:\n\n")
        md_f.write("```md\n")
        md_f.write("| # | File Name |\n")
        md_f.write("|---|-----------|\n")
        md_f.write("| 1 | [Capitalized Name Of File](Relative File Path) |\n")
        md_f.write("```\n\n")

        # Write "#", "File Name" headers
        md_f.write("| # | File Name |\n")
        md_f.write("|---|-----------|\n")

        print("Reading directory structure...")

        # Result parameters
        total_files = 0

        # Walk through the directory tree
        for root, _, files in os.walk(root_dir):

            # Get the relative path
            relative_path = os.path.relpath(root, root_dir)

            # Loop through the files in the current directory
            for file in files:

                # Get the file extension
                _, file_extension = os.path.splitext(file)

                # Skip ignored file extensions
                if file_extension in ignored_extensions:
                    continue

                # Generate relative file path with forward slashes
                file_path = os.path.join(
                    relative_path, file).replace(os.path.sep, '/')

                # Encode spaces in the filename for Markdown link
                encoded_file_path = urllib.parse.quote(file_path)
                # Prefix the relative file path with root_dir
                encoded_file_path = os.path.join(
                    root_dir, encoded_file_path).replace(os.path.sep, '/')

                # file name is like this: "{number}_{file_name_with_under_scores}.{extension}"
                # Extract it into "{Capitalized Name Of File}" (i.e., Proper Case)
                new_name = file.split("_", 1)[1]
                new_name = new_name.split(".")[0]
                new_name = new_name.replace("_", " ")
                new_name = new_name.title()

                # Write file information to Markdown file
                md_f.write(
                    f"| {total_files + 1} | [{new_name}]({encoded_file_path}) |\n")

                # Update the file count
                total_files += 1

        if animation:
            _print_with_loading("\n🌲 Markdown table generated successfully.")
            _print_with_loading(f"Total files: {total_files}", 0.02)
        else:
            print("\n🌲 Markdown table generated successfully.")
            print(f"Total files: {total_files}")

    # Print the output file paths
    if animation:
        _print_with_loading("\nMarkdown table saved to:")
        _print_with_loading(f"📘 {markdown_output_file}")
    else:
        print("\nMarkdown table saved to:")
        print(f"📘 {markdown_output_file}")


if __name__ == "__main__":

    # ? animation = True/False: Enable/Disable the loading animation
    # save_directory_structure(root_dir=os.getcwd(), animation=True)
    generate_markdown_table(root_dir="../test/TestDir",
                            markdown_output_file="./test.md", animation=True)
