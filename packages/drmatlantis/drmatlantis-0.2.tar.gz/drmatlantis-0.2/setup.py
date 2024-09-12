from setuptools import setup, find_packages

setup(
    name='drmatlantis',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'anywidget',
        'traitlets',
        'ipylab',
        'IPython'
    ],
    description='Dr. MATLANTIS server tool that connects local chatbot to MATLANTIS server',
    author='Hristo Todorov',
    author_email='httodoroff@gmail.com',
    license='MIT',
)