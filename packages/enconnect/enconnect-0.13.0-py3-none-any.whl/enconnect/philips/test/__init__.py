"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from .helpers import ByteStreamAsync
from .helpers import ByteStreamBlock



SAMPLES = (
    Path(__file__).parent
    / 'samples')



__all__ = [
    'ByteStreamBlock',
    'ByteStreamAsync']
