from setuptools import setup, find_packages

setup(
    name="feizhu_chat_client",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "websocket-client",
    ],
    entry_points={
        "console_scripts": [
            "feizhu-start=feizhu_chat_client.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple WebSocket chat client",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/websocket-chat",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
