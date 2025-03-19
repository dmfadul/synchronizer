import os
import shutil

SOURCE = 'source'
REPLICA = 'replica'


def copy_files(path_to_source, path_to_replica):
    for root, dir, files in os.walk(path_to_source):
        folder_in_source = os.path.relpath(root, path_to_source)
        folder_in_replica = os.path.join(path_to_replica, folder_in_source)

        if not os.path.exists(folder_in_replica):
            os.makedirs(folder_in_replica)

        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(folder_in_replica, file)

            if not os.path.exists(replica_file):
                shutil.copy2(source_file, replica_file)


def delete_files():
    pass


if __name__ == '__main__':
    copy_files(SOURCE, REPLICA)
