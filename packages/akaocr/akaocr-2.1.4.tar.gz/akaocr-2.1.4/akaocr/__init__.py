# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

from .detect import BoxEngine
from .recog import TextEngine
from .rotate import ClsEngine

__version__ = 'akaocr-v2.1.4'
__all__ = ['BoxEngine', 'TextEngine', 'ClsEngine']
