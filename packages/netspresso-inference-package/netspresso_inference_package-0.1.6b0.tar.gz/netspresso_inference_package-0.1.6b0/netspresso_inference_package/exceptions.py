class BaseException(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return f"{self.message}"


class UnsupportedArchiveFormat(BaseException):
    def __init__(self, message="Unsupported Archive Format."):
        super().__init__(message)


class WrongFileInfo(BaseException):
    def __init__(self, message="Either a URL or a file must be provided."):
        super().__init__(message)


class NumpyLoadError(BaseException):
    def __init__(self, message="Failed to load the .npy file."):
        super().__init__(message)


class NotSupportedFramework(BaseException):
    def __init__(self, message="Only .onnx and .tflite files are supported."):
        super().__init__(message)


class NotLoadableONNX(BaseException):
    def __init__(self, message="Can not load this onnx file."):
        super().__init__(message)


class NotLoadableTFLITE(BaseException):
    def __init__(self, message="Can not load this tflite file."):
        super().__init__(message)


class WrongDatsetFile(BaseException):
    def __init__(self, message="Dataset file is a not archive file neither '.npy' file.",):
        super().__init__(message)
