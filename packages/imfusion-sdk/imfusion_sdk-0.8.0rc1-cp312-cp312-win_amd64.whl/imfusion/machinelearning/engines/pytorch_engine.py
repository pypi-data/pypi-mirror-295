from __future__ import annotations
import imfusion._bindings as imf
import imfusion._bindings.machinelearning as ml
from typing import Optional, Union

# We cannot import torch when the TorchPlugin is loaded, due to conflicts
for plugin in imf.info().plugins:
    if plugin.name.lower() == "torchplugin":
        message = f"Could not register 'pytorch' engine: {plugin.name} is already loaded which prevents the import of 'torch'."
        imf.log_debug(message)
        raise ImportError(message)

# Check if pytorch is available
try:
    import torch
except ImportError as e:
    imf.log_debug(f"Could not register 'pytorch' engine: {str(e)}")
    raise


class PyTorchEngine(ml.Engine, factory_name="pytorch"):
    """
    Python inference engine based on PyTorch
    """

    def __init__(self, properties: imf.Properties):
        # Instantiates the base class, we can't use super() here because
        # pybind11 doesn't support this for bound types.
        ml.Engine.__init__(self, "pytorch")
        # Call base class `ìnit` method, this is required as it connects the signals
        # relative to changes of  `self.model_file` and `self.force_cpu`.
        ml.Engine.init(self, properties)
        # load the pytorch model, self.model_file is initialized in `ml.Engine.init`
        self.model = self._load_model(self.model_file)

    def on_model_file_changed(self) -> None:
        """
        Callback to handle changes of self.model_file. This can happen either
        in the sdk i.e. with ``engine.model_file = "another_model.pt"`` or
        in the ImFusionSuite when a new yaml model configuration is given to the
        MachineLearningModelController.
        """
        self.model = self._load_model(self.model_file)

    def predict(self, input_item: ml.DataItem) -> ml.DataItem:
        """
        Implements the ``Engine::predict`` pure virtual function.
        """
        # checks that the input item contains the field specified in
        # the ml.MachineLearningModel yaml config under ``EngineInputFields``.
        ml.Engine.check_input_fields(self, input_item)
        reference_input_img: imf.SharedImageSet = None

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
            input_ = self.__sis_to_torch_tensor(input_sis)

            # Move model and tensor to the GPU
            if self.should_run_on_cuda():
                input_ = input_.to("cuda")
                self.model = self.model.to("cuda")

            # Move input to same precision as the model
            model_dtype = next(self.model.parameters()).dtype
            input_ = input_.to(dtype=model_dtype)

            output = self.model(input_)
        else:
            # if we have multiple input, we check whether we have a reference
            # image component in the input data item.
            ref_image_comp = input_item.components.reference_image
            if input_item.components.reference_image is not None:
                reference_input_img = ref_image_comp.reference

            if self.should_run_on_cuda():
                self.model = self.model.to("cuda")

            model_dtype = next(self.model.parameters()).dtype

            input_list: list[torch.Tensor] = list()

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
                input_tensor = self.__sis_to_torch_tensor(
                    input_item[key].to_sis())

                # Move tensor to the GPU
                if self.should_run_on_cuda():
                    input_tensor = input_tensor.to("cuda")

                # Move input to same precision as the model
                input_tensor.to(dtype=model_dtype)

                input_list.append(input_tensor)

            output = self.model(*input_list)

        out_item = self.__torch_dict_to_data_item(
            output, reference_image=reference_input_img)
        # checks that the output contains the field specified in
        # the ml.MachineLearningModel yaml config under ``EngineOutputFields``.
        ml.Engine.check_output_fields(self, out_item)
        return out_item

    @staticmethod
    def _load_model(traced_model_file: str):
        """
        Loads an ML Model saved in traced format
        """
        if not traced_model_file.endswith('pt'):
            raise ValueError(
                f'TorchEngine expects a .pt model, got {traced_model_file}')

        model = torch.jit.load(traced_model_file)
        return model

    @staticmethod
    def __sis_to_torch_tensor(sis: imf.SharedImageSet) -> torch.Tensor:
        """
        Converts imf.SharedImageSet to an torch.Tensor
        """

        return sis.torch()

    def __torch_dict_to_data_item(
            self,
            torch_dict: Union[torch.Tensor, dict, tuple],
            reference_image: imf.SharedImageSet = None) -> ml.DataItem:
        """
        Converts the torch model output dictionary to a ml.DataItem
        """
        output = ml.DataItem()

        if isinstance(torch_dict, torch.Tensor):
            torch_dict = {"Prediction": torch_dict}

        if isinstance(torch_dict, tuple):
            torch_dict = {
                f"Prediction_{i}": v
                for i, v in enumerate(torch_dict)
            }

        assert isinstance(torch_dict, dict)

        for out_field, out_array in zip(self.output_fields,
                                        torch_dict.values()):

            out_sis = imf.SharedImageSet.from_torch(out_array)

            if reference_image is not None:
                for n in range(len(out_sis)):
                    out_sis[n].spacing = reference_image[n].spacing
                    out_sis[n].matrix = reference_image[n].matrix

            output[out_field] = ml.ImageElement(out_sis.clone())
        return output

    def should_run_on_cuda(self) -> bool:
        return not self.force_cpu and torch.cuda.is_available()

    def available_providers(self) -> list[ml.ExecutionProvider]:
        providers = [ml.ExecutionProvider.CPU]
        if torch.cuda.is_available():
            providers += [ml.ExecutionProvider.CUDA]
        return providers

    def provider(self) -> Optional[ml.ExecutionProvider]:
        return ml.ExecutionProvider.CUDA if self.should_run_on_cuda(
        ) else ml.ExecutionProvider.CPU
