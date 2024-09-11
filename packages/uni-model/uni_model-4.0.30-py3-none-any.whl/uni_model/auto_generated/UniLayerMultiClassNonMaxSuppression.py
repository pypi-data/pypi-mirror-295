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
import numpy as np
from typing import List, ClassVar
from uni_model.model.uni_layer import UniLayerBase, UniLayer
from uni_model.utils.immute import immute


@dataclass(frozen=True)
class _UniLayerBaseMultiClassNonMaxSuppression(UniLayerBase):
	scores_thresh: float
	max_size_per_class: int
	max_total_size: int
	clip_window: List[float]
	iou_thresh: float


@dataclass(frozen=True)
class UniLayerMultiClassNonMaxSuppression(UniLayer, _UniLayerBaseMultiClassNonMaxSuppression):
	op: ClassVar = "MultiClassNonMaxSuppression"
	valid_input_range: ClassVar = range(2, 3)
	valid_output_range: ClassVar = range(4, 5)
	input_names: ClassVar = ["boxes", "scores"]

	def __eq__(self, other):
		if self.name != other.name or not np.isclose(self.scores_thresh, other.scores_thresh) or self.max_size_per_class != other.max_size_per_class or self.max_total_size != other.max_total_size or not np.allclose(self.clip_window, other.clip_window) or not np.isclose(self.iou_thresh, other.iou_thresh) or self.out_shapes != other.out_shapes or self.out_dtypes != other.out_dtypes or self.breadcrumbs != other.breadcrumbs or self.history != other.history or any([v != other.extended_attr[k] if not isinstance(v, float) else not np.allclose(v, other.extended_attr[k]) for k, v in self.extended_attr.items()]):
			return False
		return True

	def __hash__(self):
		return hash((self.name, np.float32(self.scores_thresh), self.max_size_per_class, self.max_total_size, tuple(np.array(self.clip_window, dtype='float32')), np.float32(self.iou_thresh), tuple(self.out_shapes), tuple(self.out_dtypes), self.breadcrumbs, tuple(self.history), immute(self.extended_attr)))


