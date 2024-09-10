from setuptools import setup, find_packages

setup(
    name='mp4_extractor',
    version='0.1',
    packages=find_packages(),
    py_modules=['hello'],
    entry_points={
        'console_scripts': [
            'mp4_extractor=hello:main',
        ],
    },
    install_requires=[
        # 必要な依存関係があればここに記載
    ],
)
