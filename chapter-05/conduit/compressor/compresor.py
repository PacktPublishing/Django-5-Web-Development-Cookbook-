import logging
logger = logging.getLogger(__name__)
logger.info('Compressor settings loaded')

# conduit/compressor/compressor.py
from compressor.filters import CompilerFilter


COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]
