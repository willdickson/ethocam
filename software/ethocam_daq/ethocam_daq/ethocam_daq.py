import os

BASE_DATA_DIR = os.path.join(os.environ['HOME'],'data')

def check_base_data_dir(create=True):
    """
    Checks to see whether or not the base data director exists. If it
    doesn't exist it creates it when the create flag is true.
    """
    if not os.path.exists(BASE_DATA_DIR) and create:
        os.makedirs(BASE_DATA_DIR)

def test():
    check_base_data_dir()
    count = len(os.listdir(BASE_DATA_DIR))
    filename = f'test_file_{count}.txt'
    filepath = os.path.join(BASE_DATA_DIR, filename)
    with open(filepath,'w') as f:
        f.write('hello there!\n')


# ----------------------------------------------------------------------------- 
if __name__ == '__main__': 
    test()


