# -------------------------------------------------------------------------------
# (c) Copyright 2023 Sony Semiconductor Israel, Ltd. All rights reserved.
#
#      This software, in source or object form (the "Software"), is the
#      property of Sony Semiconductor Israel Ltd. (the "Company") and/or its
#      licensors, which have all right, title and interest therein, You
#      may use the Software only in accordance with the terms of written
#      license agreement between you and the Company (the "License").
#      Except as expressly stated in the License, the Company grants no
#      licenses by implication, estoppel, or otherwise. If you are not
#      aware of or do not agree to the License terms, you may not use,
#      copy or modify the Software. You may use the source code of the
#      Software only for your internal purposes and may not distribute the
#      source code of the Software, any part thereof, or any derivative work
#      thereof, to any third party, except pursuant to the Company's prior
#      written consent.
#      The Software is the confidential information of the Company.
# -------------------------------------------------------------------------------
'''
Created on 7/16/23

@author: zvikaa
'''

from uni_model.validation.error_codes import ErrorCodes
import abc
from dataclasses import dataclass


class MinMax(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def to_min_max_close_ended(self, value_n_bits: int):
        raise NotImplementedError



@dataclass
class MinMaxCloseEnded(MinMax):
    def __init__(self, min: float, max: float):
        self.min = min
        self.max = max

    def to_min_max_close_ended(self, value_n_bits: int):
        return self

    def __hash__(self):
        return hash((self.min, self.max))


@dataclass
class MinMaxOpenEnded(MinMax):
    def __init__(self, min: float, max: float):
        self.min = min
        self.max = max

    def to_min_max_close_ended(self, value_n_bits: int) -> MinMaxCloseEnded:
        return MinMaxCloseEnded(self.min, self.max - ((self.max - self.min) / 2 ** value_n_bits))

    def __hash__(self):
        return hash((self.min, self.max))

@dataclass
class SymmetricThreshold(MinMax):
    def __init__(self, threshold: float):
        if threshold <= 0:
            raise Exception(
                f"[{ErrorCodes.TMBP}]: {ErrorCodes.TMBP.value}")
        self.threshold = threshold

    def to_min_max_close_ended(self, value_n_bits: int) -> MinMaxCloseEnded:
        return MinMaxOpenEnded(-self.threshold, self.threshold).to_min_max_close_ended(value_n_bits)

    def __hash__(self):
        return hash(self.threshold)

@dataclass
class PositiveThreshold(MinMax):
    def __init__(self, threshold: float):
        if threshold <= 0:
            raise Exception(
                f"[{ErrorCodes.TMBP}]: {ErrorCodes.TMBP.value}")
        self.threshold = threshold

    def to_min_max_close_ended(self, value_n_bits: int) -> MinMaxCloseEnded:
        return MinMaxOpenEnded(0, self.threshold).to_min_max_close_ended(value_n_bits)

    def __hash__(self):
        return hash(self.threshold)

# if __name__ == "__main__":
#     v = MinMaxCloseEnded(1, 3)
#     print(v)
#     print(hash(v))