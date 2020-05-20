from setuptools import setup
about = {}
with open("py_dict_repr/__about__.py") as fp:
    exec(fp.read(), about)

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(name='py-dict-repr',
      version=about["__version__"],
      description=about["__summary__"],
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Zachary Cutlip",
      author_email="uid000@gmail.com",
      url="https://github.com/zcutlip/py-dict-repr",
      license="MIT",
      packages=['py_dict_repr'],
      python_requires='>=3.7',
      install_requires=[]
      )
