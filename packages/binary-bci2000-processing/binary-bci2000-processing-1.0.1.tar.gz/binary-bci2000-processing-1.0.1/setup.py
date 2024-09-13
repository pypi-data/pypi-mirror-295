from setuptools import setup
import binary_bci2000_processing

with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
setup(
    name="binary-bci2000-processing",
    author="sn-10",
    url="https://github.com/s-n-1-0/binary-bci2000-processing",
    download_url="https://github.com/s-n-1-0/binary-bci2000-processing",
    version=binary_bci2000_processing.__version__,
    description="Binary Processing",
    install_requires=[], # BCPy2000の初期パッケージとkerasさえあれば良い。
    packages=["binary_bci2000_processing"],
    license="MIT",
    keywords= [],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown"
)