from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='twitterbot',
    packages=['twitterbot'],
    description='twitterbot',
    url='https://github.com/sequencecentral/twitter-bot.git',
    # git+https://github.com/sequencecentral/twitter-bot.git@main#egg=twitterbot
    author='Steve Ayers',
    author_email='steve@sequenccecentral.com',
    # install_requires=[],
    version='0.1',
    license='',
    long_description=open('README.md').read(),
)