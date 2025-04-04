from setuptools import setup, find_packages

setup(
    name="polymarketbot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "py-clob-client>=0.20.0",
        "python-dotenv>=1.0.0",
        "aiohttp>=3.8.0",
        "websockets>=10.0",
        "structlog>=21.5.0",
        "asyncpg>=0.27.0",
        "SQLAlchemy>=2.0.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "pytest-mock>=3.10.0",
        ],
    },
) 