from setuptools import setup, find_packages

setup(
    name='linux_vm',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'docker',  # Docker Python SDK
        # Removed 'http', as it's part of the standard library
    ],
    entry_points={
        'console_scripts': [
            'create-linux-vm=linux.linux_vm:create_linux_vm',
            'start-linux-vm=linux.linux_vm:start_linux_vm',
            'stop-linux-vm=linux.linux_vm:stop_linux_vm',
            'start-webserver=linux.webserver:start_webserver',
        ],
    },
    description='A package to manage a Docker-based Linux VM and start a web server.',
    long_description=open('README.md').read(),  # Ensure this file exists
    long_description_content_type='text/markdown',
    author='Souporno Chakraborty',
    author_email='shrabanichakraborty83@gmail.com',
    url='https://github.com/Tirthaboss/linux_vm',
)
