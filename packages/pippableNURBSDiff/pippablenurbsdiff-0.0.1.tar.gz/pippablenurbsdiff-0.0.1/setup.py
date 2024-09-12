from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CppExtension,CUDAExtension

try:
    setup(
        name='pippableNURBSDiff',
        url="https://github.com/orthly/NURBSDiff",
        ext_modules=[
            CppExtension(name='NURBSDiff.curve_eval_cpp',
                sources=['NURBSDiff/csrc/curve_eval.cpp','NURBSDiff/csrc/utils.cpp'],
                include_dirs=['NURBSDiff/csrc']),
            CppExtension(name='NURBSDiff.surf_eval_cpp',
                sources=['NURBSDiff/csrc/surf_eval.cpp','NURBSDiff/csrc/utils.cpp'],
                include_dirs=['NURBSDiff/csrc']),
            CUDAExtension(name='NURBSDiff.curve_eval_cuda',
                sources=['NURBSDiff/csrc/curve_eval_cuda.cpp',
                'NURBSDiff/csrc/curve_eval_cuda_kernel.cu']),
            CUDAExtension(name='NURBSDiff.surf_eval_cuda',
                sources=['NURBSDiff/csrc/surf_eval_cuda.cpp',
                'NURBSDiff/csrc/surf_eval_cuda_kernel.cu']),
        ],
        cmdclass={
            'build_ext': BuildExtension
        },
        packages=find_packages(),
        version='0.0.1')
except:
    print('installation of NURBSDiff with GPU wasnt successful, installing CPU version')
    setup(
        name='pippableNURBSDiff',
        url="https://github.com/orthly/NURBSDiff",
        ext_modules=[
            CppExtension(name='NURBSDiff.curve_eval_cpp',
                sources=['NURBSDiff/csrc/curve_eval.cpp','NURBSDiff/csrc/utils.cpp'],
                include_dirs=['NURBSDiff/csrc']),
            CppExtension(name='NURBSDiff.surf_eval_cpp',
                sources=['NURBSDiff/csrc/surf_eval.cpp','NURBSDiff/csrc/utils.cpp'],
                include_dirs=['NURBSDiff/csrc']),
        ],
        cmdclass={
            'build_ext': BuildExtension
        },
        packages=find_packages(),
        version='0.0.1')