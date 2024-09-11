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
"""
Created on 3/15/23

@author: irenab
"""
import abc
from typing import Type, Sequence, Union, Tuple, Optional

from uni.common.core.multigraph.node_graph_api import GraphRequest
from uni.common.core.node_history import NodeHistory
from .base_factory import OnnxFactoryBase, validate_onnx
from uni.common.core.nnir_graph.nnir_nodes import NnirNode, ReduceMean, ReduceMax, ReduceSum, Identity
from uni.pytorch.onnx_parser import OnnxMetaNode


class OnnxReduceToNnirNodeBase(OnnxFactoryBase, abc.ABC):
    nnir_op: Type[NnirNode]

    @classmethod
    @validate_onnx(num_inputs=1, num_outputs=1, attrs=[], optional_attrs=['axes', 'keepdims'], opset_limits=(13, 17))
    def from_onnx(cls, onnx_node, graph_ctx=None) -> NnirNode:
        axes = onnx_node.get_attr_with_default('axes', None)
        if axes is None or len(axes) == 0:
            shape = graph_ctx.get_in_shapes()[0]
            axes = tuple(range(len(shape)))
        keepdims = bool(onnx_node.get_attr_with_default_from_schema('keepdims'))
        return cls.nnir_op(onnx_node.name, axes=axes, keepdims=keepdims)


#
# ReduceSum has a different interface, so not adding here (its opset 13 is the same as Mean/Max opset 18)
#


class OnnxReduceMeanToNnirNode(OnnxReduceToNnirNodeBase):
    """ https://github.com/onnx/onnx/blob/main/docs/Changelog.md#ReduceMean-13 """
    nnir_op = ReduceMean


class OnnxReduceMaxToNnirNode(OnnxReduceToNnirNodeBase):
    """ https://github.com/onnx/onnx/blob/main/docs/Changelog.md#ReduceMax-13 """
    nnir_op = ReduceMax


class OnnxReduceSumToNnirNode(OnnxFactoryBase):
    """
        https://github.com/onnx/onnx/blob/main/docs/Changelog.md#ReduceMax-13
        not inheritance from OnnxReduceToNnirNodeBase because can have 2 inputs and different attrs
    """
    nnir_op = ReduceSum

    @classmethod
    @validate_onnx(num_inputs=[1, 2], num_outputs=1, attrs=[], optional_attrs=['keepdims', "noop_with_empty_axes"])
    def from_onnx(cls, onnx_node, graph_ctx=None) -> Tuple[Union[Identity, ReduceSum], Optional[GraphRequest]]:
        from uni.pytorch.onnx_parser.onnx_parser import is_dummy_input

        in_nodes: Sequence[OnnxMetaNode] = graph_ctx.get_in_nodes()
        axes = tuple()    # type: ignore
        history = None
        req = None
        if len(in_nodes) > 1 and not is_dummy_input(in_nodes[1]):
            axes = tuple(in_nodes[1].get_const_data())
            history = NodeHistory(cls.onnx_op_info(onnx_node), desc='')
            req = GraphRequest(inputs_to_detach=list(range(len(in_nodes)))[1:])

        keepdims = bool(onnx_node.get_attr_with_default_from_schema('keepdims'))
        noop_with_empty_axes = bool(onnx_node.get_attr_with_default_from_schema('noop_with_empty_axes'))
        if len(axes) == 0:
            if noop_with_empty_axes:
                history = NodeHistory(cls.onnx_op_info(onnx_node),
                                      desc='axis is empty and noop_with_empty_axes is true')
                return Identity(onnx_node.name, history=history), req
            else:
                shape = graph_ctx.get_in_shapes()[0]
                axes = tuple(range(len(shape)))

        return ReduceSum(onnx_node.name, axes=axes, keepdims=keepdims, history=history), req
