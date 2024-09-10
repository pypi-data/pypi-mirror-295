from setuptools import setup
from scratchattachplus import __version__

with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()

setup(
    name="scratchattachplus",
    version=__version__,
    description="scratchattachの追加機能版",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="kakeruzoku",
    author_email="kakeruzoku@gmail.com",
    maintainer="kakeruzoku",
    maintainer_email="kakeruzoku@gmail.com",
    url="https://github.com/kakeruzoku/scratchattachplus",
    download_url="https://github.com/kakeruzoku/scratchattachplus",
    packages=["scratchattachplus"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    license="MIT",
    keywords=['scratch api', 'scratchattach', 'scratch api python', 'scratch python', 'scratch for python', 'scratch', 'scratch cloud', 'scratch cloud variables', 'scratch bot'],
    install_requires=["scratchattach","requests"]
)
