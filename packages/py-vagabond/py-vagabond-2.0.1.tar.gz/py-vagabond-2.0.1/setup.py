from setuptools import setup, find_packages

setup(
    name='py-vagabond',
    version='2.0.1',
    license="MIT License with attribution requirement",
    author="Ranit Bhowmick",
    author_email='bhowmickranitking@duck.com',
    description='''Vagabond is a comprehensive library for pathfinding, navigation, and environmental understanding in robotics and automation. It provides a range of algorithms and tools to help developers create efficient and sophisticated pathfinding solutions for robots and autonomous systems.''',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Kawai-Senpai/Vagabond',
    download_url='https://github.com/Kawai-Senpai/Vagabond',
    keywords=["Pathfinding", "Robotics", "Navigation", "A* Algorithm", "Graph Theory", "Automation", "Robotic Systems"],
    install_requires=['graphviz==0.20.1'],
)
