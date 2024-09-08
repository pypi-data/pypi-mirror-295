# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from collections import UserDict
from functools import partial
from typing import Any

from monai.transforms.utils_pytorch_numpy_unification import max, mean, median, min, percentile, std

__all__ = ["Operations", "SampleOperations", "SummaryOperations"]


class Operations(UserDict):
    """
    Base class of operation interface
    """

    def evaluate(self, data: Any, **kwargs: Any) -> dict:
        """
        For key-value pairs in the self.data, if the value is a callable,
        then this function will apply the callable to the input data.
        The result will be written under the same key under the output dict.

        Args:
            data: input data.

        Returns:
            a dictionary which has same keys as the self.data if the value
                is callable.
        """
        return {k: v(data, **kwargs) for k, v in self.data.items() if callable(v)}


class SampleOperations(Operations):
    """
    Apply statistical operation to a sample (image/ndarray/tensor).

    Notes:
        Percentile operation uses a partial function that embeds different kwargs (q).
        In order to print the result nicely, data_addon is added to map the numbers
        generated by percentile to different keys ("percentile_00_5" for example).
        Annotation of the postfix means the percentage for percentile computation.
        For example, _00_5 means 0.5% and _99_5 means 99.5%.

    Example:

        .. code-block:: python

            # use the existing operations
            import numpy as np
            op = SampleOperations()
            data_np = np.random.rand(10, 10).astype(np.float64)
            print(op.evaluate(data_np))

            # add a new operation
            op.update({"sum": np.sum})
            print(op.evaluate(data_np))
    """

    def __init__(self) -> None:
        self.data = {
            "max": max,
            "mean": mean,
            "median": median,
            "min": min,
            "stdev": std,
            "percentile": partial(percentile, q=[0.5, 10, 90, 99.5]),
        }
        self.data_addon = {
            "percentile_00_5": ("percentile", 0),
            "percentile_10_0": ("percentile", 1),
            "percentile_90_0": ("percentile", 2),
            "percentile_99_5": ("percentile", 3),
        }

    def evaluate(self, data: Any, **kwargs: Any) -> dict:
        """
        Applies the callables to the data, and convert the
        numerics to list or Python numeric types (int/float).

        Args:
            data: input data
        """
        ret = super().evaluate(data, **kwargs)
        for k, v in self.data_addon.items():
            cache = v[0]
            idx = v[1]
            if isinstance(v, tuple) and cache in ret:
                ret.update({k: ret[cache][idx]})

        for k, v in ret.items():
            ret[k] = v.tolist()  # type: ignore
        return ret


class SummaryOperations(Operations):
    """
    Apply statistical operation to summarize a dict. The key-value looks like: {"max", "min"
    ,"mean", ....}. The value may contain multiple values in a list format. Then this operation
    will apply the operation to the list. Typically, the dict is generated by multiple
    `SampleOperation` and `concat_multikeys_to_dict` functions.

    Examples:

        .. code-block:: python

            import numpy as np
            data = {
                "min": np.random.rand(4),
                "max": np.random.rand(4),
                "mean": np.random.rand(4),
                "sum": np.random.rand(4),
            }
            op = SummaryOperations()
            print(op.evaluate(data)) # "sum" is not registered yet, so it won't contain "sum"

            op.update({"sum", np.sum})
            print(op.evaluate(data)) # output has "sum"
    """

    def __init__(self) -> None:
        self.data = {
            "max": max,
            "mean": mean,
            "median": mean,
            "min": min,
            "stdev": mean,
            "percentile_00_5": mean,
            "percentile_10_0": mean,
            "percentile_90_0": mean,
            "percentile_99_5": mean,
        }

    def evaluate(self, data: Any, **kwargs: Any) -> dict:
        """
        Applies the callables to the data, and convert the numerics to list or Python
        numeric types (int/float).

        Args:
            data: input data
        """
        return {k: v(data[k], **kwargs).tolist() for k, v in self.data.items() if (callable(v) and k in data)}
