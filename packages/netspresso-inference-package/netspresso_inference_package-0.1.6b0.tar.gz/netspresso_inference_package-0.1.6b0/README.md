# How to use

## Use directly
* model_file_path: Model file path(ONNX, TFLite)
* dataset_file_path: The path to the compressed file or the individual npy files where the delimiter of the input layer is used as the file name.

```bash
python3 inference.py --model_file_path tests/your_model_file.tflite --dataset_file_path tests/your_dataset_file.npy 
```

## Import and use

```python
from netspresso_inference_package.inference.inference_service import InferenceService
inf_service = InferenceService(
        model_file_path="/app/tests/people_detection.onnx"
        )
inf_service.run(dataset_file_path="/app/tests/dataset_for_onnx.npy")
print(inf_service.result_file_path)
```