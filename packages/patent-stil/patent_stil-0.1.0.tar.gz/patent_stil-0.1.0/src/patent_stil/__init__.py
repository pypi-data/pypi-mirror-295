from .fpo_patent import *
from .utils import createDirs,downloadFile
__all__ = [
    'downloadFile',
    'createDirs',
    'getPatentInfo',
    "getFpoPatentInfoByUrl",
    "getFpoSearchResult",
    "downloadPdf",
    "downloadPdfByUrl",
    "autoSpider"
]