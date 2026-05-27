from setuptools import setup, find_packages

setup(
    name="ironclad",
    version="2.0.0",
    description="Advanced Face Detective & OSINT Investigation Engine",
    author="Ironclad Team",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "streamlit>=1.28.0",
        "langchain>=0.1.0",
        "insightface>=0.7.3",
        "faiss-cpu>=1.7.4",
        "opencv-python-headless>=4.8.0",
        "duckduckgo-search>=4.0.0",
        "numpy>=1.24.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ironclad=app:main",
        ],
    },
)
