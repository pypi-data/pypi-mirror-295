import platform

try:
        from .onnxruntime_engine import PyOnnxRuntimeEngine
except ImportError:
    pass

try:
    from .openvino_engine import OpenVinoEngine
except ImportError:
    pass

try:
    from .pytorch_engine import PyTorchEngine
except ImportError:
    pass

if platform.system() == "Darwin" and platform.processor() == "arm":
    try:
        from .coreml_engine import CoreMLEngine
    except ImportError:
        pass
