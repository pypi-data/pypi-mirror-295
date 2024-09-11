import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="knifes",
    version="0.9.19",
    author="knifes",
    author_email="author@example.com",
    description="Swiss Army Knife",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.0",
    install_requires=[
        'python-decouple',
        'prompt_toolkit',
        'attrs',
        'cattrs',
        'httpx[http2]'
        # 'cryptography',                       #  required by aes
        # 'tencentcloud-sdk-python==3.0.600',   #  required by sms
        # 'Pillow',                             #  required by luban
        # 'pillow-heif',                        #  required by luban
    ]
)
