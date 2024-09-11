from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="supabase-overleaf",
    version="0.1.0",
    author="Chen, Xingqiang",
    author_email="chen.xinqiang@iechor.com",
    description="A tool to crawl Overleaf templates and store data in Supabase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chenxingqiang/overleaf-templates-supabase",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "beautifulsoup4",
        "supabase",
    ],
    entry_points={
        "console_scripts": [
            "supabase-overleaf=supabase_overleaf.main:main",
        ],
    },
)
