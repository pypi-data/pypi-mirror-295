from setuptools import find_packages, setup
import os
def get_version():
    with open('VERSION', 'r') as f:
        exec(compile(f.read(), 'VERSION', 'exec'))
    return locals()['__version__']

def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content

def get_requirements(filename='NWUcellsr/requirements.txt'):
    here = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(here, filename), 'r') as f:
        requires = [line.strip() for line in f.readlines()]
    return requires

if __name__ == '__main__':
    setup(
        name='NWUcellsr',
        version=get_version(),
        description='Your SDK description',
        long_description=readme(),
        long_description_content_type='text/markdown',
        author='Your Name',
        author_email='your.email@example.com',
        keywords='your, keywords, here',
        url='https://github.com/yourusername/yourrepo',
        packages=find_packages(),
        include_package_data=True,
        package_data={
            'NWUcellsr': ['models/sr.pth'],  # Ensure this matches the directory structure
        },
        install_requires=get_requirements(),
        zip_safe=False,
    )
