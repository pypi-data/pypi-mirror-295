# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import os.path


class TRTLLMHelper:
    @classmethod
    def _validate_checkpoint_directory(cls, checkpoint_directory) -> None:
        if not os.path.exists(checkpoint_directory) or not os.path.isdir(checkpoint_directory):
            raise FileNotFoundError(f"{checkpoint_directory} does not exist, or is not a directory.")

    @classmethod
    def prune(cls, checkpoint_directory: str, output_directory: str):
        cls._validate_checkpoint_directory(checkpoint_directory)
        try:
            from tensorrt_llm.commands.prune import prune_and_save
            prune_and_save(
                ckpt_dir=os.path.abspath(checkpoint_directory),
                out_dir=os.path.abspath(output_directory))
        except ImportError:
            raise RuntimeError("Failed to import tensorrt_llm, please make sure that TensorRT LLM is installed")
        except Exception:
            raise RuntimeError(f"Failed to prune LLM checkpoint in {checkpoint_directory}")
