from setuptools import setup,find_packages

setup(
    name='HyperTech-STT',
    version='0.1',
    author='Priyanshu Pal',
    author_email='samarendranathpal46@gmail.com',
    description='This is Speech To Text package created by Priyanshu Pal'
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver_manager'
]
