from setuptools import setup, find_packages

setup(
    name='yuseful_prompts',
    version='2.7.1',
    packages=find_packages(),
    install_requires=[
        'langchain-core',
        'langchain-community',
        'pytest'
    ],
    author='yactouat',
    author_email='yactouat@yactouat.com',
    description='tested prompts for common use-cases of the Markets Agent using open LLMs with ollama and Langchain',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/markets-agent/yuseful_prompts',
    license='MIT',
)
