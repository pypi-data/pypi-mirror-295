import os
import sys
import setuptools

with open('/tmp/2fa_decoder/requirements.txt') as f:
    requirements = f.readlines()

with open("/tmp/2fa_decoder/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name ='2fa_decoder',
        version ='1.0.2',
        author ='Nghia Handsome',
        author_email ='nghiahandsome@gmail.com',
        url ='https://www.nghiahl.cloud',
        description ='Decode QR Code & Generate OTP',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='GNU General Public License v3 (GPLv3)',
        packages=setuptools.find_packages(),
        entry_points ={
            'console_scripts': [
                '2fa_decoder = 2fa_decoder.2fa_decoder:main'
            ]
        },
        classifiers =[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
        ],
        keywords ='QR_Code OTP 2FA Secret-Code',
        install_requires = requirements,
        zip_safe = False
)
