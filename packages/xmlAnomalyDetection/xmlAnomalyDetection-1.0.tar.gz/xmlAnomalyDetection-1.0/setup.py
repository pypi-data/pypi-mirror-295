from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = [line.strip() for line in f.readlines()]

setup(
    name='xmlAnomalyDetection',
    version='1.0',
    packages=find_packages(),
    install_requires=install_requires,
    author='Talha Yousuf',
    author_email='th05691@gmail.com',
    entry_points="""
        [console_scripts]
        xml_anomaly_detection=xmlAnomalyDetection.cli:main
    """,
    include_package_data=True,
)
