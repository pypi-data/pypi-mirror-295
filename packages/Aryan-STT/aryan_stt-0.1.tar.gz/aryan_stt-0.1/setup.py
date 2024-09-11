from setuptools import setup,find_packages

setup(
    name='Aryan-STT',
    version='0.1',
    author='Aryan Sahani',
    author_email='sahaniaryan321@gmail.com',
    description='this is speech to text package created by Aryan Sahani'
)
packages = find_packages(), 
install_requirements = [
    'selenium'
    'webdriver_manager'
]