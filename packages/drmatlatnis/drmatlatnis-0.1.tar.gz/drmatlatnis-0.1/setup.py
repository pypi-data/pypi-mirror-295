from setuptools import setup, find_packages

setup(
    name='drmatlatnis',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'anywidget',
        'traitlets',
        'ipylab',
        'IPython'
    ],
    description='Dr. MATLANTIS server tool that connects local chatbot to MATLANTIS server',
    author='Hristo Todorov',
    author_email='hristo@so-ti.com',
    license='MIT',
)
