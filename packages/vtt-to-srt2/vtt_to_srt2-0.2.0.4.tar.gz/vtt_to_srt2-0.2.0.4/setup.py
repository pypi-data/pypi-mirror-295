import setuptools

with open(file="README.md", mode="r", encoding="utf-8") as fh:

    long_description = fh.read()

setuptools.setup(name='vtt_to_srt2',
                 version='0.2.0.4',
                 author="Jeison Cardoso",
                 author_email="j@jsonzilla.com",
                 maintainer="Jeison Cardoso",
                 description="vtt to srt subtitles converter package",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/jsonzilla/vtt_to_srt2",
                 packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
                 classifiers=["Programming Language :: Python :: 2.7",
                              "Operating System :: OS Independent"],
                 entry_points={
                     "console_scripts":
                     ["vtt_to_srt=vtt_to_srt.vtt_to_srt:main"]
                 },
                 )
