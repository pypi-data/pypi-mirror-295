import sys
import platform
from setuptools import setup, find_packages
import os

def rename_folder_if_exists(path, current_folder_name, new_folder_name):
    # Construct the full path of the current folder
    current_folder_path = os.path.join(path, current_folder_name)
    new_folder_path = os.path.join(path, new_folder_name)
    
    # Check if the current folder exists
    if os.path.exists(current_folder_path) and os.path.isdir(current_folder_path):
        # Rename the folder
        os.rename(current_folder_path, new_folder_path)
        print(f"Renamed folder '{current_folder_name}' to '{new_folder_name}'")
    else:
        print(f"Folder '{current_folder_name}' does not exist in '{path}'")

# 범용 dependencies
install_requires = [
]

# OS별로 설치 패키지 구분
if platform.system() == 'Windows':
    install_requires.append('pycryptodome')
    install_requires.append('crypto')

elif platform.system() == 'Linux':
    if sys.version_info >= (3, 7):
        install_requires.append('pycrypto==2.6')
    elif sys.version_info >= (3, 6):
        install_requires.append('crypto')

elif platform.system() == 'Darwin':  # macOS
    # install_requires.append('macos_specific_package')
    pass

setup(
    name='wipdevice',
    version='0.0.6', # 수정되면 꼭 version 업데이트하기
    description='Wow IoT Platform API libraries',
    author='wowsystem, nobu',
    author_email='contact@wowsystem.co.kr',
    url='https://github.com/WOWSYSTEM/WIP-Python',
    install_requires=install_requires,
    packages=find_packages(exclude=[]),
    keywords=['wowsystem', 'IoT', 'WIP', 'IoT Platform', 'IoT Server', 'wowsystem', 'WOW IoT Platform'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
