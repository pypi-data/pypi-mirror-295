from setuptools import setup, find_packages

setup(
    name='mpsqd',
    version='0.1.4',    
    description='A Python package based on MPS to solve the TDSE and HEOM',
    url='https://github.com/qiangshi-group/MPSQD',
    author='Qiang Shi',
    author_email='qshi@iccas.ac.cn',
    license='MIT',
    packages=find_packages(),
    install_requires=['numpy',
                      'scipy',                     
                      ],

    classifiers=[
        'Development Status :: 4 - Beta ',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
