"""Top-level package for PreviseDx QuantStudio File Utils."""

__author__ = """Jaideep Sundaram"""
__email__ = 'sundaram.previse@gmail.com'
__version__ = '0.1.0'

from .xls.parser import Parser as QuantStudioXlsParser # noqa
from .record import Record as QuantStudioRecord # noqa
