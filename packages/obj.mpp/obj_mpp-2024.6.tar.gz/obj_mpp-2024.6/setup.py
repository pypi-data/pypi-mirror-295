# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2018)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from pathlib import Path

from setuptools import find_namespace_packages, setup


AUTHOR = "Eric Debreuve"
E_MAIL = "eric.debreuve@univ-cotedazur.fr"

PYPI_NAME = "obj.mpp"
DESCRIPTION = "Object/pattern detection using a Marked Point Process"
VERSION = (2024, 6)  # /!\ str(2021.10) -> "2021.1"
PY_VERSION = "3.8"

REPOSITORY_NAME = "Obj.MPP"
REPOSITORY_USER = "edebreuv"
REPOSITORY_SITE = "gitlab.inria.fr"
DOCUMENTATION_SITE = f"{REPOSITORY_USER}.gitlabpages.inria.fr"

IMPORT_NAME = "NOT_SET"

HERE = Path(__file__).parent.resolve()


long_description = (HERE / "README.rst").read_text(encoding="utf-8")
repository_url = f"https://{REPOSITORY_SITE}/{REPOSITORY_USER}/{REPOSITORY_NAME}"
documentation_url = f"https://{DOCUMENTATION_SITE}/{REPOSITORY_NAME}"
version = f"{VERSION[0]}.{VERSION[1]}"

setup(
    # Remove: obj.mpp.egg-info/ build/ dist/
    # python setup.py bdist_wheel
    # twine upload dist/*
    # https://pypi.org/project/{PYPI_NAME}
    author=AUTHOR,
    author_email=E_MAIL,
    #
    name=PYPI_NAME,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    version=version,
    license="CeCILL-2.1",
    #
    classifiers=[
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
        f"Programming Language :: Python :: {PY_VERSION}",
        "Programming Language :: C",
        "Development Status :: 4 - Beta",
    ],
    keywords="signal, image, image analysis, object detection, pattern detection, marked point process",
    #
    url=repository_url,
    project_urls={
        "Documentation": documentation_url,
        "Source": repository_url,
    },
    #
    packages=find_namespace_packages(
        include=["brick", "brick.*", "helper", "helper.*"]
    ),
    package_data={
        "brick.marked_point.threeD": [
            "c_extension/ellipsoid-linux.so",
            "c_extension/ellipsoid-win32.so",
        ],
        "brick.marked_point.twoD": [
            "c_extension/circle-linux.so",
            "c_extension/circle-win32.so",
            "c_extension/ellipse-linux.so",
            "c_extension/ellipse-win32.so",
            "c_extension/rectangle-linux.so",
            "c_extension/rectangle-win32.so",
            "c_extension/superquadric-linux.so",
            "c_extension/superquadric-win32.so",
        ],
    },
    py_modules=[
        "mpp_detector_cli",
        "mpp_detector_gi",
        "mpp_quality_chooser",
        "mpp_doc_searcher",
    ],
    entry_points={
        "console_scripts": [
            "mpp_detector_cli=mpp_detector_cli:Main",
            "mpp_detector_gi=mpp_detector_gi:Main",
            "mpp_quality_chooser=mpp_quality_chooser:Main",
            "mpp_doc_searcher=mpp_doc_searcher:Main",
        ],
    },
    #
    python_requires=f">={PY_VERSION}",
    install_requires=[
        "Pillow",
        "PyQt5",
        "colorama",
        "imageio",
        "matplotlib",
        "networkx",
        "numpy",
        "scikit-image",
        "scipy",
        "tifffile",
    ],
)
