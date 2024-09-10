import unittest
from generate_sample_structure import generate_sample_directory_structure
from DirecTracer import save_directory_structure
import os


class TestDirecTracer(unittest.TestCase):
    def test_save_directory_structure(self):

        # Generate sample directory structure
        generate_sample_directory_structure()

        # Call save_directory_structure function
        save_directory_structure(os.getcwd(), text_output_file="test_output.txt",
                                 markdown_output_file="test_output.md", animation=False)

    def test_save_directory_structure_with_animation(self):

        # Generate sample directory structure
        generate_sample_directory_structure()

        # Call save_directory_structure function
        save_directory_structure(os.getcwd(), text_output_file="test_output2.txt",
                                 markdown_output_file="test_output2.md", animation=True)


if __name__ == '__main__':
    unittest.main()
