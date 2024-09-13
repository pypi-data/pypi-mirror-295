import os
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension


def append_nvcc_threads(nvcc_extra_args):
    nvcc_threads = os.getenv("NVCC_THREADS") or "4"
    return nvcc_extra_args + ["--threads", nvcc_threads]


SKIP_CUDA_BUILD = os.getenv("MOE_SKIP_CUDA_BUILD", "FALSE") == "TRUE"

ext_modules = []
cc_flag = []

if not SKIP_CUDA_BUILD:
    cc_flag.append("-gencode")
    cc_flag.append("arch=compute_80,code=sm_80")
    cc_flag.append("-gencode")
    cc_flag.append("arch=compute_86,code=sm_86")
    cc_flag.append("-gencode")
    cc_flag.append("arch=compute_90,code=sm_90")

    extra_compile_args = {
        "nvcc": append_nvcc_threads(
            [
                "-O3",
                "-std=c++17",
                "-U__CUDA_NO_HALF_OPERATORS__",
                "-U__CUDA_NO_HALF_CONVERSIONS__",
                "-U__CUDA_NO_HALF2_OPERATORS__",
                "-U__CUDA_NO_BFLOAT16_CONVERSIONS__",
                "--expt-relaxed-constexpr",
                "--expt-extended-lambda",
                "--use_fast_math",
            ]
            + cc_flag
        )
    }

    (
        ext_modules.append(
            CUDAExtension(
                name="moe_kernels._ops",
                sources=[
                    "moe_kernels/_ops/ext.cpp",
                    "moe_kernels/_ops/activation_kernels.cu",
                    "moe_kernels/_ops/marlin_moe_ops.cu",
                    "moe_kernels/_ops/moe_align_block_size_kernels.cu",
                    "moe_kernels/_ops/topk_softmax_kernels.cu",
                ],
                extra_compile_args=extra_compile_args,
            )
        ),
    )

setup(
    name="moe_kernels",
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExtension} if ext_modules else {},
)
