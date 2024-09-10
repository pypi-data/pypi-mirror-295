import abc


class Basemodel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def model_input_output_attributes(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def inference(self, **kwargs):
        raise NotImplementedError()
