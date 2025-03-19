import os
import pytest
import tempfile

from main import sync_folders, gen_logger


def test_copy_files():
    with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
        logger = gen_logger(source + '/sync.log')

        source_file_path = source + '/test.txt'
        replica_file_path = replica + '/test.txt'

        with open(source_file_path, 'w') as f:
            f.write('test')
        
        sync_folders(source, replica, logger)

        # Perform checks
        assert os.path.exists(replica_file_path)
        with open(replica_file_path, 'r') as f:
            assert f.read() == 'test'


def test_inner_folders():
    with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
        logger = gen_logger(source + '/sync.log')

        inner_folder = source + '/inner_folder'
        os.makedirs(inner_folder)
        inner_file = inner_folder + '/test.txt'

        with open(inner_file, 'w') as f:
            f.write('inner test')
        
        sync_folders(source, replica, logger)

        # Perform checks
        assert os.path.exists(replica + '/inner_folder')
        assert os.path.exists(replica + '/inner_folder/test.txt')
        with open(replica + '/inner_folder/test.txt', 'r') as f:
            assert f.read() == 'inner test'


def test_delete_files():
    with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
        logger = gen_logger(source + '/sync.log')

        new_file = source + '/new_file.txt'
        with open(new_file, 'w') as f:
            f.write('new file')
        
        sync_folders(source, replica, logger)
        os.remove(new_file)

        sync_folders(source, replica, logger)

        # Perform checks
        assert not os.path.exists(replica + '/new_file.txt')


def test_replace_files():
    with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as replica:
        logger = gen_logger(source + '/sync.log')

        new_file = source + '/new_file.txt'
        with open(new_file, 'w') as f:
            f.write('new file')
        
        sync_folders(source, replica, logger)

        with open(new_file, 'w') as f:
            f.write('replaced content')
        
        sync_folders(source, replica, logger)

        # Perform checks
        with open(replica + '/new_file.txt', 'r') as f:
            assert f.read() == 'replaced content'


if __name__ == '__main__':
    pytest.main()