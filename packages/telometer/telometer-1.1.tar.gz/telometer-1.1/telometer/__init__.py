__version__ = '1.01'
__author__ = 'Santiago E Sanchez'
__email__ = 'santy.esanchez@gmail.com'
__license__ = 'MIT'

import logging
from .telometer import (
    process_bam_file,
    measure_telomere_length,
    identify_telomere_regions,
    get_telomere_repeats,
    reverse_complement,
    process_read_wrapper,
    process_read,
    detect_discontinuities,
    check_gap,
    run_telometer
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

__all__ = [
    'process_bam_file',
    'measure_telomere_length',
    'identify_telomere_regions',
    'get_telomere_repeats',
    'reverse_complement',
    'process_read_wrapper',
    'process_read',
    'detect_discontinuities',
    'check_gap',
    'run_telometer'
]

