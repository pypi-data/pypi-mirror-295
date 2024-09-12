from setuptools import setup,find_packages

setup(
    name = 'ghost-stt',
    version='0.1',
    author='Sarthak',
    author_email='sangrohasarthak06@gmail.com',
    description='this is speech to text package created by sarthak'
)
packges = find_packages()
install_requirements = [
    'selenium',
    'webdriver_manager'
]