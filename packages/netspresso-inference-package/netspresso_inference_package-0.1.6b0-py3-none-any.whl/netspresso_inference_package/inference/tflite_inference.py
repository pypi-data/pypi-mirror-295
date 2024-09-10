import os
from typing import Dict, List, Tuple, Union

import numpy as np

from ..enums import EnumInputNodeShapeFormat, EnumNodeRawDataType
from ..exceptions import NotLoadableTFLITE
from .abs import Basemodel

try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    try:
        import tensorflow as tf

        tflite = tf.lite
    except ImportError:
        raise ImportError("Failed to load tensorflow")


class DataAttribute:
    def __init__(self):
        self.attributes = self.get_props()
        for i in self.attributes:
            setattr(self, f"_{i}", None)

    def __dir__(self):
        return self.attributes

    def __iter__(self):
        for i in dir(self):
            yield i, getattr(self, i)

    def __repr__(self):
        return f"DataAttribute class of '{'location' if self.location is not None else 'name'} {self.key}' layer"

    @property
    def key(self) -> Union[int, str]:
        return self.location if self.location is not None else self.name

    @property
    def shape(self) -> Union[None, Tuple]:
        return self._shape

    @shape.setter
    def shape(self, value: Tuple):
        if not isinstance(value, tuple):
            msg = f"{__class__}.shape should be tuple, but got {type(value)}."
            raise ValueError(msg)
        self._shape = value

    @property
    def dtype(self) -> Union[None, str]:
        return self._dtype

    @dtype.setter
    def dtype(self, value):
        self._dtype = EnumNodeRawDataType(value).value

    @property
    def quantization(self) -> Union[None, tuple]:
        return self._quantization

    @quantization.setter
    def quantization(self, value):
        self._quantization = value

    @property
    def format(self) -> Union[None, str]:
        return self._format

    @format.setter
    def format(self, value):
        self._format = EnumInputNodeShapeFormat(value).value

    @property
    def location(self) -> Union[None, int]:
        """Union[None, int]: location of the Node"""
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def name(self) -> Union[None, str]:
        """Union[None, str]: name of the Node"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def height(self) -> Union[None, int]:
        """Union[None, int]: returns height of the shape."""
        if self._height is None:
            if (self._shape and self._format) is None:
                return None
            if len(self._format) != len(self._shape):
                return None
            self._height = dict(zip(self._format, self._shape)).get("h")
        return self._height

    @property
    def width(self) -> Union[None, int]:
        """Union[None, int]: returns width of the shape."""
        if self._width is None:
            if (self._shape and self._format) is None:
                return None
            if len(self._format) != len(self._shape):
                return None
            self._width = dict(zip(self._format, self._shape)).get("w")
        return self._width

    @classmethod
    def get_props(cls) -> List:
        """returns all class properties as List."""
        return [x for x in dir(cls) if isinstance(getattr(cls, x), property)]


class TFLITE(Basemodel):
    def __init__(self, model_file_path:str, num_threads:int=1):
        try:
            with open(model_file_path, "rb") as f:
                self.interpreter_obj = tflite.Interpreter(model_content=f.read(), num_threads=num_threads)
        except:
            raise NotLoadableTFLITE()
        self.interpreter_obj.allocate_tensors()
        self.inputs, self.outputs = self.model_input_output_attributes()

    def model_input_output_attributes(self):
        inputs = {}
        outputs = {}

        for input_detail in self.interpreter_obj.get_input_details():
            input_data_attribute = DataAttribute()
            input_data_attribute.name = input_detail.get("name")
            input_data_attribute.location = input_detail.get("index")
            input_data_attribute.shape = tuple(input_detail.get("shape"))
            input_data_attribute.dtype = input_detail.get("dtype").__name__
            input_data_attribute.quantization = input_detail.get("quantization")
            inputs[input_data_attribute.key] = input_data_attribute

        for output_detail in self.interpreter_obj.get_output_details():
            output_data_attribute = DataAttribute()
            output_data_attribute.name = output_detail.get("name")
            output_data_attribute.location = output_detail.get("index")
            output_data_attribute.shape = tuple(output_detail.get("shape"))
            output_data_attribute.dtype = output_detail.get("dtype").__name__
            output_data_attribute.quantization = output_detail.get("quantization")
            outputs[output_data_attribute.key] = output_data_attribute

        return inputs, outputs

    def inference(self, preprocess_result: Dict[int, np.ndarray], **kwargs) -> Dict[int, np.ndarray]:
        for _k, v in self.inputs.items():
            if v.dtype in [np.uint8, np.int8, "int8", "unit8"]:
                pass

        for location, value in iter(preprocess_result.items()):
            self.interpreter_obj.set_tensor(location, value)
            # TODO: make function which return npy generator when len(preprocess_result[k]) > 1
        self.interpreter_obj.invoke()

        output_dict = {}
        for output_location in iter(self.outputs):
            output_dict[output_location] = self.interpreter_obj.get_tensor(output_location)
        return output_dict
