""" vendors: a collection of proprietary vendor codes.

"""

class Vendor():
    url = None
    root_uid = None
    PREFIX = None

class TopsOrtho(Vendor):
    url = "http://topsortho.com/topsdb"
    PREFIX = "TOPS"

class OpenOrtho(Vendor):
    url = "http://open-ortho.org/terminology"
    root_uid = "1.3.6.1.4.1.61741.11.3"
    PREFIX = "OPOR"
    
class DentalEyePad(Vendor):
    url = "https://dentaleyepad.de/dentaleyepad-image-types"
    PREFIX = 'DEYE'
