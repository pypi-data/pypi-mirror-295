from typing import Any, Dict, Union

import numpy as np
import onnx
import onnxruntime

from ..exceptions import NotLoadableONNX
from .abs import Basemodel


def create_outputs(outputs:Dict[Union[str, int], Any], results:Dict[Union[str, int], Any]):
    if len(outputs) != len(results):
        raise ValueError("The length of 'outputs' and 'results' must be the same.")

    for (key, _value), result in zip(outputs.items(), results):
        outputs[key] = result

    return outputs


class ONNX(Basemodel):
    def __init__(self, model_file_path:str, num_threads=1):
        try:
            self.model_obj = onnxruntime.InferenceSession(model_file_path)
        except:
            raise NotLoadableONNX()
        self.inputs, self.outputs = self.model_input_output_attributes(model_file_path)

    def model_input_output_attributes(self, model_file_path:str):
        inputs = {}
        outputs = {}
        try:
            model = onnx.load(model_file_path)
        except:
            raise NotLoadableONNX()

        for inp in model.graph.input:
            shape = str(inp.type.tensor_type.shape.dim)
            inputs[inp.name] = [int(s) for s in shape.split() if s.isdigit()]

        for oup in model.graph.output:
            shape = str(oup.type.tensor_type.shape.dim)
            outputs[oup.name] = [int(s) for s in shape.split() if s.isdigit()]

        return inputs, outputs

    def inference(self, preprocess_result: Dict[int, np.ndarray]) -> Dict[int, np.ndarray]:
        inputs = {}
        for k, _v in preprocess_result.items():
            ortvalue = onnxruntime.OrtValue.ortvalue_from_numpy(preprocess_result[k])
            inputs[k] = ortvalue
            # TODO: make function which return npy generator when len(preprocess_result[k]) > 1

        outputs_list = []
        for k in self.outputs:
            outputs_list.append(k)

        results = self.model_obj.run(outputs_list, inputs)
        output_dict = create_outputs(self.outputs, results)
        return output_dict
