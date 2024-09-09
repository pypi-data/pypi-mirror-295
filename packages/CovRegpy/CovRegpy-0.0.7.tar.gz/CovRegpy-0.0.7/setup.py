
from setuptools import setup

setup(
  name = 'CovRegpy',
  packages = ['CovRegpy'],
  version = '0.0.7',
  license='cc-by-nc-4.0',
  description = 'Regularised covariance regression software based on Hoff and Niu (2012).',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  author = 'Cole van Jaarsveldt',
  author_email = 'colevj0303@gmail.com',
  url = 'https://github.com/Cole-vJ/CovRegpy.git',
  download_url = 'https://github.com/Cole-vJ/CovRegpy/archive/refs/tags/0.0.7.tar.gz',
  keywords = ['Portfolio Optimisation', 'Regularised Covariance Regression (RCR)', 'Empirical Mode Decomposition (EMD)', 'Singular Spectrum Analysis (SSA)', 'Singular Spectrum Decomposition (SSD)', 'X11', 'Implicit Factors', 'Risk Premia Parity', 'Risk Parity', 'Long\Short Equity'],
  install_requires=[
          'numpy',
          'seaborn',
	  'group-lasso',
	  'AdvEMDpy',
	  'pandas',
	  'matplotlib',
	  'yfinance',
  	  'mdlp-discretization',
	  'arch',
  	  'notebook',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: Free for non-commercial use',
    'Programming Language :: Python :: 3.11',
  ],
)
