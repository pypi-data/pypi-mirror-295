import unittest
from FileHarvestor import read_files
import os
from file_maker import generate_sample_directory_structure


class TestFileHarvestor(unittest.TestCase):

    def test_read_files(self):

        generate_sample_directory_structure()

        file_list = ["SampleDirectory/FolderA/File1.txt",
                     "SampleDirectory/FolderB/File1.txt",
                     "SampleDirectory/FolderC/File1.txt",
                     "SampleDirectory/FolderA/File2.txt",
                     "SampleDirectory/FolderB/File2.txt",
                     "SampleDirectory/FolderC/File2.txt",
                     "SampleDirectory/FolderA/File3.txt",
                     "SampleDirectory/FolderB/File3.txt",
                     "SampleDirectory/FolderC/File3.txt",
                     ]

        read_files(file_list=file_list,
                   output_text_file='./output/contents.txt',
                   output_markdown_file='./output/contents.md')

        self.assertTrue(os.path.exists('./output/contents.txt'))
        self.assertTrue(os.path.exists('./output/contents.md'))


if __name__ == '__main__':
    unittest.main()
