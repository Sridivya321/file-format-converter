from setuptools import setup

setup(name='ffconverter',
      version='0.1',
      description='file_format_conversion',
      url='https://github.com/Sridivya321/file-format-converter',
      author='Sridivya Bunga',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['ffconverter'],
      zip_safe=False,
      entry_points = {
        'console_scripts': ['ffconverter=ffconverter:main'],},
      install_requires=[
          'pandas<=1.5.10'
      ],
      )