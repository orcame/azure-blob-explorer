from distutils.core import setup

setup(name='azurebe',
      version='1.0.0',
      description='Windows Azure Blob explorer',
      url='https://github.com/orcame/azure-blob-explorer',
      packages=['azurebe',
                'azurebe.client',
                'azurebe.cmd']
     )
