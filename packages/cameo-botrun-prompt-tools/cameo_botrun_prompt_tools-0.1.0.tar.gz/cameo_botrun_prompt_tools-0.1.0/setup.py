from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='cameo_botrun_prompt_tools',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='elantievs',
    author_email='elantievs@gmail.com',
    description='cameo_botrun_prompt_tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bohachu/cameo_botrun_prompt_tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)

