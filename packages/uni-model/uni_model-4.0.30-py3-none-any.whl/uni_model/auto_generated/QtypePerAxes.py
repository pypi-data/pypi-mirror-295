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

# This class is auto-generated in PythonGenerator of UniModel. Please don't change
from dataclasses import dataclass
from uni_model.auto_generated import Shape
import numpy as np
from uni_model.auto_generated.Qtype import Qtype
from uni_model.auto_generated.Dtype import Dtype
from uni_model.auto_generated.MultipleMinMax import MultipleMinMax
from typing import List
from uni_model.model.accuracy.min_max import MinMax, MinMaxCloseEnded


@dataclass(frozen=True)
class QtypePerAxes(Qtype, Dtype, MultipleMinMax):
	value_n_bits: int 
	axes: List[bool] 
	min_maxes: List[MinMax] 

	def validate_shapes(self, shape: Shape):
		real_indices_for_axes = [i for i, axis in enumerate(self.axes) if axis]
		if np.prod([elem for i, elem in enumerate(shape.elements) if i in real_indices_for_axes]) == len(self.min_maxes):
			return None
		else:
			return f"shape {shape} in axes {real_indices_for_axes} product doesn't match given min max list with size {len(self.min_maxes)}"

	def __post_init__(self):
		if len(self.min_maxes) == 0:
			raise Exception("min_maxes mustn't be empty")

	def __hash__(self):
		return hash((self.value_n_bits, tuple(self.axes), tuple(self.min_maxes)))

	def get_min_max(self) -> List[MinMaxCloseEnded]:
		return [mm.to_min_max_close_ended(self.value_n_bits) for mm in self.min_maxes]


