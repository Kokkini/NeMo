# =============================================================================
# Copyright 2020 NVIDIA. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import numpy as np

from nemo import logging

__all__ = ['eval_iter_callback', 'eval_epochs_done_callback']


def eval_iter_callback(tensors, global_vars):

    for kv, v in tensors.items():
        if 'loss' in kv:
            if "loss" not in global_vars.keys():
                global_vars["loss"] = []
            for loss in v:
                global_vars["loss"].append(loss.item())


def eval_epochs_done_callback(global_vars):
    res = {}
    if 'loss' in global_vars:
        loss = np.mean(global_vars["loss"])
        logging.info("Dev loss: {0}".format(np.round(loss, 3)))
        perplexity = np.exp(loss)
        logging.info("Dev perplexity: {0}".format(np.round(perplexity, 3)))
        global_vars["loss"] = []
        res["Dev loss"] = loss
        res["Dev perplexity"] = perplexity
    return res