from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
from Cython.Distutils import build_ext

ext_modules = [
    Extension(
        "mitigation", sources=[
            "./cython/hamming.pyx",
            "./libcpp/combinations.cpp",
        ],
        language="c++"
    )
]

setup(
    name="mitigation",
    cmdclass={"build_ext": build_ext},
    ext_modules=cythonize(ext_modules)
)