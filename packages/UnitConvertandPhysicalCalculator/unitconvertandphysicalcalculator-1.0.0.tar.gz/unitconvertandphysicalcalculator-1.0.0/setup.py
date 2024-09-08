# coding:UTF-8
import setuptools

setuptools.setup(
    name="Unit-Convert-Including",
    version="1.0.0",
    author="Chay",
    author_email="lichenyi_2020@qq.com",
    url="https://github.com/lichenyichay/Unit-Convert-Including/",
    description="A simple converter and a Physical quantity calculator.",
    long_description="单位转换器兼物理量计算器",
    python_requires=">=3.5",
    packages_dir={"": "src"},
    packages_data={"": ["*.txt", "*.info", "*.properties"], "": ["data/*.*"]},
    exclude=["*.test", "*.test.*", "test.*", "test"],
    classifiers=['Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 3"
                 ]
)
