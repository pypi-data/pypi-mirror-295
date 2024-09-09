
from setuptools import setup

setup(
  name = 'CovRegpy',
  packages = ['CovRegpy'],
  version = '0.0.6',
  license='cc-by-nc-4.0',
  description = 'Regularised covariance regression software based on Hoff and Niu (2012).',
  long_description = 'Regularised covariance regression software based on Hoff and Niu (2012) - see https://arxiv.org/pdf/1102.5721. This package was developed out of research performed by Cole van Jaarsveldt, Gareth W. Peters, Matthew Ames, and Mike Chantler. This package was built entirely using Python 3.11.5 - Python guarantees backwards compatibility which should ensure that this software package functions as expected on all future Python versions. See:\\\\ van Jaarsveldt, C., Peters, G., Ames, M., & Chantler, M. (2024) Package CovRegpy: Regularized covariance regression and forecasting in Python. Annals of Actuarial Science, First View. doi:10.1017/S1748499524000101 url: https://dx.doi.org/10.1017/S1748499524000101',
  long_description_content_type='text/markdown',
  author = 'Cole van Jaarsveldt',
  author_email = 'colevj0303@gmail.com',
  url = 'https://github.com/Cole-vJ/CovRegpy.git',
  download_url = 'https://github.com/Cole-vJ/CovRegpy/archive/refs/tags/0.0.6.tar.gz',
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
