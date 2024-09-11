from setuptools import setup

requirements = ["colorama<=0.4.6", "qrcode<=6.1", "Image<=1.5.33"]

setup(name='PorkofQRCode',
      version='1.4',
      description='',
      packages=['PorkofQRCode'],
      author_email='porkof@mail2tor.com',
      zip_safe=False,
      install_requires=requirements)
