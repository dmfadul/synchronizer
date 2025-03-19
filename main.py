import os
import shutil
import hashlib

SOURCE = 'source'
REPLICA = 'replica'


def files_are_identical(path_file1, path_file2):
    hash_md5 = hashlib.md5()
    with open(path_file1, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    hash1 = hash_md5.hexdigest()

    hash_md5 = hashlib.md5()
    with open(path_file2, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    hash2 = hash_md5.hexdigest()

    return hash1 == hash2


def copy_files(path_to_source, path_to_replica):
    for root, _, files in os.walk(path_to_source):
        folder_in_source = os.path.relpath(root, path_to_source)
        folder_in_replica = os.path.join(path_to_replica, folder_in_source)

        if not os.path.exists(folder_in_replica):
            os.makedirs(folder_in_replica)

        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(folder_in_replica, file)

            if not os.path.exists(replica_file):
                shutil.copy2(source_file, replica_file)

            if not files_are_identical(source_file, replica_file):
                shutil.copy2(source_file, replica_file)


def delete_files(path_to_source, path_to_replica):
    for root, dirs, files in os.walk(path_to_replica, topdown=False):
        folder_in_replica = os.path.relpath(root, path_to_replica)
        folder_in_source = os.path.join(path_to_source, folder_in_replica)

        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(folder_in_source, file)

            if not os.path.exists(source_file):
                os.remove(replica_file)
        
        for dir in dirs:
            replica_folder = os.path.join(root, dir)
            source_folder = os.path.join(folder_in_source, dir)

            if not os.path.exists(source_folder):
                shutil.rmtree(replica_folder)


def sync_folders(path_to_source, path_to_replica):
    copy_files(path_to_source, path_to_replica)
    delete_files(path_to_source, path_to_replica)


if __name__ == '__main__':
    sync_folders(SOURCE, REPLICA)
