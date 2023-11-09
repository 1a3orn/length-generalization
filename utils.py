import os


# make folder if it doesn't exist
def make_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def make_folder_at(*args):
    make_folder(os.path.join(*args))