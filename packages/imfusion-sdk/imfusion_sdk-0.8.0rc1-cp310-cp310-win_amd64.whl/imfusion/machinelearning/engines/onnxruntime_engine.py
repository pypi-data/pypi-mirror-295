import imfusion._bindings as imf
import imfusion._bindings.machinelearning as ml
import numpy as np
from typing import Optional, Union, Dict, List


# We cannot import onnxruntime when the ONNXPlugin is loaded, due to conflicts
for plugin in imf.info().plugins:
    if plugin.name.lower() == "onnxruntimeplugin":
        message = f"Could not register 'pyonnxruntime' engine: {plugin.name} is already loaded which prevents the import of the 'onnxruntime' python module."
        imf.log_debug(message)
        raise ImportError(message)


# Check if onnxruntime is available
try:
    import onnxruntime as ort
except ImportError as e:
    imf.log_debug(f"Could not register 'pyonnxruntime' engine: {str(e)}")
    raise


class PyOnnxRuntimeEngine(ml.Engine, factory_name="pyonnxruntime"):
    """
    Python inference engine based on OnnxRuntime
    """

    def __init__(self, properties: imf.Properties):
        # Instantiates the base class, we can't use super() here because
        # pybind11 doesn't support this for bound types.
        ml.Engine.__init__(self, "pyonnxruntime")
        # Call base class `ìnit` method, this is required as it connects the signals
        # relative to changes of  `self.model_file` and `self.force_cpu`.
        ml.Engine.init(self, properties)
        # create the main session
        self.session = self._create_session(self.model_file)

    def on_model_file_changed(self) -> None:
        """
        Callback to handle changes of self.model_file. This can happen either
        in the sdk i.e. with ``engine.model_file = "another_model.pt"`` or
        in the ImFusionSuite when a new yaml model configuration is given to the
        MachineLearningModelController.
        """
        self.session = self._create_session(self.model_file)

    def predict(self, input_item: ml.DataItem) -> ml.DataItem:
        """
        Implements the ``Engine::predict`` pure virtual function.
        """
        # checks that the input item contains the field specified in
        # the ml.MachineLearningModel yaml config under ``EngineInputFields``.
        ml.Engine.check_input_fields(self, input_item)
        reference_input_img: imf.SharedImageSet = None

        if not self.session:
            raise RuntimeError("Session was not properly created")

        # In case we have a single image as input, we use the image
        # as reference for setting the metadata in the output
        if len(input_item.fields) == 1:
            input_element = input_item[self.input_fields[0]]

            if input_element.type != ml.ElementType.IMAGE:
                raise ValueError(
                    f'Single input element only support images, got type {input_element.type}'
                )

            input_sis = input_element.to_sis()
            reference_input_img = input_sis
            input_ = self.__sis_to_tensor(input_sis)

            # Get name of the input for the model itself
            ort_input_info = self.session.get_inputs()
            assert len(ort_input_info) == 1
            ort_input_name = ort_input_info[0].name

            output = self.session.run(None, {ort_input_name: input_})
        else:
            # if we have multiple input, we check whether we have a reference
            # image component in the input data item.
            ref_image_comp = input_item.components.reference_image
            if input_item.components.reference_image is not None:
                reference_input_img = ref_image_comp.reference

            input_dict: Dict[str, np.ndarray] = {}

            for key in self.input_fields:
                if key not in input_item:
                    raise ValueError(
                        f'Key "{key}" not input_item, got {list(input_item.keys())}'
                    )
                if input_item[key].type not in {
                        ml.ElementType.IMAGE or ml.ElementType.VECTOR
                }:
                    raise ValueError(
                        f'Got element type {input_item[key].type}, for now the supported ones are [IMAGE, VECTOR]'
                    )

                input_tensor = self.__sis_to_tensor(input_item[key].to_sis())
                input_dict[key] = input_tensor

            output = self.session.run(None, input_dict)

        out_item = self.__tensor_dict_to_data_item(
            output, reference_image=reference_input_img)
        # checks that the output contains the field specified in
        # the ml.MachineLearningModel yaml config under ``EngineOutputFields``.
        ml.Engine.check_output_fields(self, out_item)
        return out_item

    def _create_session(self, model_file: str):
        """
        Creates a session from a model saved in onnx format
        """
        if not model_file.endswith('onnx'):
            raise ValueError(
                f'OnnxRuntime expects a .onnx model, got {model_file}')

        session = ort.InferenceSession(
            model_file,
            providers=[self.IMF_PROVIDER_TO_ORT_PROVIDER[self.provider()]])
        return session

    @staticmethod
    def __sis_to_tensor(sis: imf.SharedImageSet) -> np.array:
        """
        Converts imf.SharedImageSet to an input tensor for onnxruntime
        """

        input_np = sis.numpy()
        if len(input_np.shape) == 5:
            input_np = np.transpose(input_np, (0, 4, 1, 2, 3))
        elif len(input_np.shape) == 4:
            input_np = np.transpose(input_np, (0, 3, 1, 2))
        else:
            raise RuntimeError(
                "Only 4D (batch of 2d images) or 5D (batch of 3d volumes) are supported"
            )
        return input_np

    def __tensor_dict_to_data_item(
            self,
            input_dict: Union[np.ndarray, dict, tuple],
            reference_image: imf.SharedImageSet = None) -> ml.DataItem:
        """
        Converts the model output dictionary to a ml.DataItem
        """
        output = ml.DataItem()

        if isinstance(input_dict, np.ndarray):
            input_dict = {"Prediction": input_dict}

        if isinstance(input_dict, tuple) or isinstance(input_dict, list):
            input_dict = {
                f"Prediction_{i}": v
                for i, v in enumerate(input_dict)
            }

        assert isinstance(input_dict, dict)

        for out_field, out_array in zip(self.output_fields,
                                        input_dict.values()):

            if len(out_array.shape) == 5:
                out_array = np.transpose(out_array, (0, 2, 3, 4, 1))
            elif len(out_array.shape) == 4:
                out_array = np.transpose(out_array, (0, 2, 3, 1))
            else:
                raise RuntimeError(
                    "Only 4D (batch of 2d images) or 5D (batch of 3d volumes) are supported"
                )
            out_sis = imf.SharedImageSet(out_array)

            if reference_image is not None:
                for n in range(len(out_sis)):
                    out_sis[n].spacing = reference_image[n].spacing
                    out_sis[n].matrix = reference_image[n].matrix

            output[out_field] = ml.ImageElement(out_sis.clone())
        return output

    ORT_PROVIDER_TO_IMF_PROVIDER: Dict[str, ml.ExecutionProvider] = {
        "CPUExecutionProvider": ml.ExecutionProvider.CPU,
        "CUDAExecutionProvider": ml.ExecutionProvider.CUDA,
        "DmlExecutionProvider": ml.ExecutionProvider.DIRECTML,
        "OpenVINOExecutionProvider": ml.ExecutionProvider.OPENVINO,
    }

    IMF_PROVIDER_TO_ORT_PROVIDER = {
        v: k
        for (k, v) in ORT_PROVIDER_TO_IMF_PROVIDER.items()
    }

    def should_run_on_cuda(self) -> bool:
        return not self.force_cpu and self.provider(
        ) == ml.ExecutionProvider.CUDA

    def available_providers(self) -> List[ml.ExecutionProvider]:
        ort_providers = ort.get_available_providers()
        providers = [
            self.ORT_PROVIDER_TO_IMF_PROVIDER[p] for p in ort_providers
            if p in self.ORT_PROVIDER_TO_IMF_PROVIDER.keys()
        ]
        return providers

    def provider(self) -> Optional[ml.ExecutionProvider]:

        if not self.force_cpu:
            for gpu_provider in [
                    ml.ExecutionProvider.CUDA, ml.ExecutionProvider.DIRECTML
            ]:
                if gpu_provider in self.available_providers():
                    return gpu_provider

        return ml.ExecutionProvider.CPU
