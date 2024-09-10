# DirecTracer

DirecTracer is a Python script that generates a directory structure in both text and Markdown formats. It can be used to visualize the hierarchy of folders and files in a given directory, while also excluding specific folders and file extensions.

## DirecTracer on PyPI

View the DirecTracer package on PyPI by clicking [here](https://pypi.org/project/DirecTracer/).

## Features

- `save_directory_structure()` function:

  - Generates a directory structure in text and Markdown formats.
  - Supports ignoring specific directories and file extensions.
  - Outputs clickable links in the Markdown file for easy navigation.
  - Text & loading animations while generating the directory structure.

- `generate_markdown_table()` function:

  - Generates a Markdown table from the given directory structure.
  - Includes columns of Serial Number and clickable links to the files through the file names.

## Demonstration Video

Click on the thumbnail below to watch the demonstration video on YouTube.

[![DirecTracer](./demo/thumbnail2.png)](https://youtu.be/FqMauKiTvVs?si=FJlBiQBwpZb7_IPm)

## Usage

Install the DirecTracer package using the following command:

```bash
pip install DirecTracer
```

OR

Clone this repository using the following command:

```bash
git clone https://github.com/Hardvan/DirecTracer
cd DirecTracer
pip install .
```

Call the `save_directory_structure` function from the `DirecTracer` module to generate the directory structure.

```python
from DirecTracer import save_directory_structure
import os


# Generate the directory structure in text and Markdown formats
save_directory_structure(
   root_dir=os.getcwd(),
   text_output_file="directory_structure.txt",
   markdown_output_file="directory_structure.md",
   animation=True
)
```

View the [`run.py`](./run.py) file for a complete example.

The `save_directory_structure()` function accepts the following parameters:

- **root_dir (str):** The root directory to start scanning from. Defaults to the current working directory.
- **text_output_file (str):** The name of the text output file. Defaults to "directory_structure.txt".
- **markdown_output_file (str):** The name of the Markdown output file. Defaults to "directory_structure.md".
- **ignored_directories (list, optional):** List of directories to ignore. Defaults to [".git", ".vscode", "venv", ".venv", ".idea", "out"].
- **ignored_extensions (list, optional):** List of file extensions to ignore. Defaults to [".exe"].
- **animation (bool, optional):** Enable/Disable the loading animation. Defaults to False.

The `generate_markdown_table()` function accepts the following parameters:

- **root_dir (str)**: The root directory to start scanning from. Defaults to the current working directory.
- **markdown_output_file (str)**: The name of the Markdown output file. Defaults to "markdown_table.md".
- **animation (bool, optional)**: Enable/Disable the loading animation. Defaults to False.
- **ignored_extensions (list, optional)**: List of file extensions to ignore. Defaults to [".exe"].

## Output Example

To have a look at the current directory structure of this repository, check out the [directory_structure.md](./directory_structure.md) file.

## Run the following commands to update the package (for maintainers)

1. Change version in `setup.py`
2. Run the following commands

   ```bash
   python setup.py bdist_wheel sdist
   twine check dist/*
   twine upload dist/*
   ```

   In case you forget to update the version in `setup.py`:

   - delete the `dist` folder
   - update version in `setup.py`
   - run the above commands again.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE.txt) file for details.

## Author

**Hardik Pawar** - [Hardvan](https://github.com/Hardvan)
