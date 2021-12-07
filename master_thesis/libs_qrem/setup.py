from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
from Cython.Distutils import build_ext

ext_modules = [
    Extension(
        "hamming", 
        sources=[
            "./cython/hamming.pyx",
            "./cpp/combinations.cpp",
            "./cpp/hamming.cpp"
        ],
        extra_compile_args=["-std=c++11"],
        language="c++"
    )
]

setup(
    name="hamming",
    cmdclass={"build_ext": build_ext},
    ext_modules=cythonize(ext_modules)
)
