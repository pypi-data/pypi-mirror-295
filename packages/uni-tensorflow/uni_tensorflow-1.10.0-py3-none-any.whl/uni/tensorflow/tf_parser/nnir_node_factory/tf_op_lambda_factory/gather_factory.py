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
from typing import List

import tensorflow as tf
from uni.common.core.error import ParamErrorInfo, OpInputErrorInfo, raise_op_error, ErrorInfo
from uni.common.core.nnir_graph.nnir_nodes import TopKGather
from uni.tensorflow.tf_parser.nnir_node_factory.tf_op_lambda_factory.tf_op_lambda_factory_base import \
    TFOpLambdaToNnirFactory, validate_tf_op_lambda, OpLambdaAttrs
from uni.tensorflow.tf_parser.tf_meta_node import TFMetaNode
from uni.tensorflow.tf_parser.tf_reader_helper import get_rank, get_input


class TFGatherToNnir(TFOpLambdaToNnirFactory):
    """ https://www.tensorflow.org/api_docs/python/tf/gather """

    indices_dtype_err_msg = "The dtype of indices must be tf.int32"
    axis_batch_dims_err_msg = "The axis must be equal to batch_dims and must be set to the last axis of the tensor."

    @classmethod
    @validate_tf_op_lambda(attrs=['indices'], optional_attrs=["validate_indices", "axis", "batch_dims"])
    def convert(cls, node: TFMetaNode, attrs: OpLambdaAttrs) -> TopKGather:
        indices = attrs['indices']
        errors: List[ErrorInfo] = []
        history = cls.tf_op_history(node)
        assert node.inbound_node_index is not None

        node_input = get_input(node.keras_layer)
        params_rank = get_rank(node_input)
        axis = attrs.get("axis")
        batch_dims = attrs.get("batch_dims")
        last_axis = params_rank - 1
        supported_axes = [-1, last_axis]

        if indices.dtype != tf.int32:
            errors.append(OpInputErrorInfo(input_index=1, input_name='indices', reason=cls.indices_dtype_err_msg))
        if axis not in supported_axes:
            errors.append(ParamErrorInfo(name="axis", value=axis, reason=cls.axis_batch_dims_err_msg))
        if batch_dims not in supported_axes:
            errors.append(ParamErrorInfo(name="batch_dims", value=batch_dims, reason=cls.axis_batch_dims_err_msg))
        if errors:
            raise_op_error(cls.tf_op_info(node), errors=errors, history=history)

        return TopKGather(node.name, axis, history=history)
