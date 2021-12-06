from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
from Cython.Distutils import build_ext

ext_modules = [
    Extension(
        "libs_qrem", sources=[
            "./cython/hamming.pyx",
            "./libcpp/combinations.cpp",
            "./libcpp/hamming.cpp"
        ],
        language="c++"
    )
]

setup(
    name="libs_qrem",
    cmdclass={"build_ext": build_ext},
    ext_modules=cythonize(ext_modules)
)