from setuptools import setup
from io import open
test_requirements = ['pytest']
extras = {'test': test_requirements}

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lights',
    version='0.1.0',
    packages=['lights'],
    url='https://github.com/spyoungtech/lights',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author='Spencer Young',
    author_email='spencer.young@spyoung.com',
    install_requires=['phue', 'fire'],
    tests_require=test_requirements,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='Command Line Utility for controlling phillips hue lights',
    entry_points={
        'console_scripts': ['lights = lights.__init__:main']
    },
)