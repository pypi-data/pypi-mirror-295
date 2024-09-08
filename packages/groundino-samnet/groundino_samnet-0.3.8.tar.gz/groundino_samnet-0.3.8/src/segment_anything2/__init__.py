# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from hydra import initialize_config_module

initialize_config_module("segment_anything2.sam2_config", version_base="1.2")