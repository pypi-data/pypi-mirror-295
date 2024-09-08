from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='PySensor-MQTT',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        'paho-mqtt',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Biblioteca para simulação de sensores e publicação via MQTT',
    author='Raunick Vileforte Vieira Generoso',
    author_email='raunickbhdesign@gmail.com',
    url='https://github.com/raunick/sensor_library_mqtt',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
