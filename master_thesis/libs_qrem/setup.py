from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from distutils.core import setup

ext_modules = [
    Extension(
        "hamming",
        sources=[
            "./libs_qrem/hamming.pyx",
            "./cpp/combinations.cpp",
            "./cpp/hamming.cpp"
        ],
        extra_compile_args=["-std=c++11"],
        language="c++"
    )
]

setup(
    name="libs_qrem",
    cmdclass={"build_ext": build_ext},
    ext_modules=cythonize(ext_modules, language_level=3),
    zip_safe=False,
    packages=["libs_qrem"],
    package_dir={
        "libs_qrem": "libs_qrem"
    },
)
