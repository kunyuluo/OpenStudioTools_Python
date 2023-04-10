import os


def import_epw(file_path):
    assert os.path.isfile(file_path), 'Cannot find an epw file at {}'.format(file_path)
    assert file_path.lower().endswith('epw'), '{} is not an .epw file. \n' \
                                              'It does not possess the .epw file extension.'.format(file_path)

    try:
        with open(file_path, 'r') as epwin:
            line = epwin.readline()
            print(line)
    except ValueError:
        pass


epw_path_str = "D:\Projects\OpenStudioDev\CHN_Shanghai.Shanghai.583670_IWEC.epw"
import_epw(epw_path_str)
