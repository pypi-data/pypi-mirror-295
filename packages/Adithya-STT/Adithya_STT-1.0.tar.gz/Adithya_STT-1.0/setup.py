from setuptools import setup, find_packages

setup(
    name='Adithya_STT',
    version='1.0',
    author='Adithya',
    author_email='adhithya6281@gmail.com',
    description='This is the speech to text package using selenium and webdriver-manager',
    
)
packages=find_packages(),
install_requirements = [
    'selenium','webdriver_manager','webdriver-manager'
]