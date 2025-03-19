import os
import pytest
import tempfile

from main import copy_files


def test_copy_files():
    with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
        source_file_path = source + '/test.txt'
        replica_file_path = replica + '/test.txt'

        with open(source_file_path, 'w') as f:
            f.write('test')
        
        copy_files(source, replica)

        # Perform checks
        assert os.path.exists(replica_file_path)
        with open(replica_file_path, 'r') as f:
            assert f.read() == 'test'


def test_inner_folders():
    with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
        inner_folder = source + '/inner_folder'
        os.makedirs(inner_folder)
        inner_file = inner_folder + '/test.txt'

        with open(inner_file, 'w') as f:
            f.write('inner test')
        
        copy_files(source, replica)

        # Perform checks
        assert os.path.exists(replica + '/inner_folder')
        assert os.path.exists(replica + '/inner_folder/test.txt')
        with open(replica + '/inner_folder/test.txt', 'r') as f:
            assert f.read() == 'inner test'


def test_delete_files():
    pass