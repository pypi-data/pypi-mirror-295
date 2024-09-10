from enum import Enum


class Enums(Enum):
    FRAMEWORK = "framework"
    INPUTS = "inputs"
    OUTPUTS = "outputs"
    ONNX = "onnx"
    TFLITE = "tflite"
    NUMPY_FILE_SUFFIXES = [".npy", ".npz"]


class EnumInputNodeShapeFormat(Enum):
    NCHW = "nchw"
    NCWH = "ncwh"
    NHWC = "nhwc"
    NWHC = "nwhc"

    CHW = NCHW
    CWH = NCWH
    HWC = NHWC
    WHC = NWHC

    # tensorrt format
    LINEAR = NCHW
    CHW2 = NCHW
    HWC8 = NCHW
    CHW4 = NCHW
    CHW16 = NCHW
    CHW32 = NCHW

    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def _missing_(cls, value):
        value = str(value).upper()
        try:
            return cls[value]
        except KeyError:
            msg = f"{cls.__name__} expected {', '.join(list(cls.__members__.keys()))} but got `{value}`"
            raise KeyError(msg)


class EnumNodeRawDataType(Enum):
    # numpy data type
    FLOAT16 = "float16"
    FLOAT32 = "float32"
    FLOAT64 = "float64"
    INT8 = "int8"
    INT16 = "int16"
    INT32 = "int32"
    INT64 = "int64"
    UINT8 = "uint8"
    UINT16 = "uint16"
    UINT32 = "utin32"
    UINT64 = "uint64"
    # BOOL='bool_'

    # openvino data type
    FP16 = FLOAT16
    FP32 = FLOAT32
    FP64 = FLOAT64
    I8 = INT8
    I16 = INT16
    I32 = INT32
    I64 = INT64
    U8 = UINT8
    U16 = UINT16
    U32 = UINT32
    U64 = UINT64

    # tensorrt data type
    FLOAT = FLOAT32
    HALF = FLOAT16

    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def _missing_(cls, value):
        value = str(value).upper()
        try:
            return cls[value]
        except KeyError:
            msg = f"{cls.__name__} expected {', '.join(list(cls.__members__.keys()))} but got `{value}`"
            raise KeyError(msg)
