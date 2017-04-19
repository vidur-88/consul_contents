from setuptools import setup

setup(name='consul-contents',
      version='1.0.0',
      description='This is for loading key-value stored on consul server',
      url='https://github.com/vidur-88/consul_contents.git',
      author='vikash gupta',
      author_email='vgupta840@gmail.com',
      license='',
      install_requires=['consulate==0.6.0'],
      packages=['consul_contents'],
      zip_safe=False)
