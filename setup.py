import setuptools.command.build_py
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

#custom post-installation steps go here:
class Install(_install):
    def run(self):
        _install.do_egg_install(self)
        #nothing else to do

setup(
    cmdclass={
        'install': Install,
    },
    name='twitterbot',
    description='twitterbot',
    url='https://github.com/sequencecentral/twitter-bot.git',
    # git+https://github.com/sequencecentral/twitter-bot.git@main#egg=twitterbot
    author='Steve Ayers, Ph.D.',
    author_email='steve@sequenccecentral.com',
    # install_requires=[],
    version='1.0.1',
    license='MIT',
    # packages=['synchronicity','synchronicity.quotewidget'],
    packages = find_packages(),
    include_package_data = True,
    package_data={'': ['config.json','sources.json']},
    # Needed to actually package something
    # Needed for dependencies
    # install_requires=[''],
    # *strongly* suggested for sharing
    long_description=open('README.md').read(),
    install_requires=open('REQUIREMENTS.txt').read(), #['click==7.1.2','joblib==1.0.1','nltk==3.6.1','regex==2021.4.4','tqdm==4.60.0'],
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)

#to make an egg:
#python setup.py bdist_egg
#egg-info added