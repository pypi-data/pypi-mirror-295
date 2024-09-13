# setup.py
from setuptools import setup, find_packages

setup(
    name='hotmail-flask-mailer',
    version='0.1.0',
    description='A Flask module for sending emails via Hotmail using the mailer package',
    author='Prakhar Doneria',
    author_email='prakhardoneria3@gmail.com',
    url='https://github.com/prakhardoneria/hotmail-flask-mailer',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0',
        'quick-mailer'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Framework :: Flask',
    ],
    entry_points={
        'console_scripts': [
            'hotmail-flask-mailer=hotmail_flask_mailer.app:app.run',
        ],
    },
)
