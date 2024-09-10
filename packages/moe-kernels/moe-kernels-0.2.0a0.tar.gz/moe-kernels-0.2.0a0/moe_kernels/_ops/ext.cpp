#include <torch/extension.h>

#include "ext.h"

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("moe_align_block_size", &moe_align_block_size,
        "Align tokens processed by experts such that they are divisible by the block size");
  m.def("silu_and_mul", &silu_and_mul, "Apply SwiGLU activaiton");
  m.def("topk_softmax", &topk_softmax, "Apply topk softmax to the gating outputs");

#ifndef USE_ROCM
  m.def("marlin_gemm_moe", &marlin_gemm_moe, "Marlin GEMM for MoE layers");
#endif
}
