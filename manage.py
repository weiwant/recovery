import os
import re
import sys

from config import USE_GPU
from src import app

if __name__ == '__main__':
    print(os.listdir(os.path.dirname(os.path.realpath(__file__))))
    for dir_name in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        if re.match(r'openpose.*', dir_name):
            build_dir = 'build_GPU' if USE_GPU else 'build_CPU'
            bin_dir = os.path.join(dir_name, build_dir, 'bin')
            dll_dir = os.path.join(dir_name, build_dir, 'x64', 'Release')
            os.environ['PATH'] = os.environ['PATH'] + ';' + bin_dir + ';' + dll_dir
            sys.path.append(os.path.join(dir_name, build_dir, 'python', 'openpose', 'Release'))
            break
    app.run()
