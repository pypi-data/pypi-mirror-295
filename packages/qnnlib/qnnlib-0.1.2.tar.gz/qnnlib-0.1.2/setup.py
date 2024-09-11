import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'qnnlib',      
  packages = ['qnnlib'], 
  version = '0.1.2', 
  license='MIT', 
  description = 'This library is designed to help data scientists easily conduct experiments with Quantum Neural Networks (QNNs) without the need to manually construct quantum circuits. ',
  long_description=DESCRIPTION,
  # long_description_content_type='text/markdown',
  author = 'chinnapongpsu',                 
  author_email = 'chinnapong.a@psu.ac.th',     
  url = 'https://github.com/chinnapongpsu/qnnlib',  
  download_url = 'https://github.com/chinnapongpsu/qnnlib/archive/refs/tags/0.1.2.zip',  
  keywords = [
    'quantum neural networks',
    "quantum machine learning"
    "zzfeaturemap",
    "twolocal"
  ],

  install_requires=[            # I get to this in a second
          'scikit-learn==1.5.1',
          'tensorflow==2.15.0',
          'keras==2.15.0',
          'pennylane==0.37.0',
          'matplotlib',
          'pandas',
          'qiskit-ibm-provider==0.11.0',
          'pennylane-qiskit'
      ],

  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Education',     
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.11',
  ],
)