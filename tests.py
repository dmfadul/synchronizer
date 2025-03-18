import os
import pytest
import tempfile

from main import copy_file


def test_copy_file():
    with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
        source_file_path = source + '/test.txt'
        replica_file_path = replica + '/test.txt'

        with open(source_file_path, 'w') as f:
            f.write('test')
        
        copy_file(source_file_path, replica)

        assert os.path.exists(replica_file_path)
        with open(replica_file_path, 'r') as f:
            assert f.read() == 'test'
