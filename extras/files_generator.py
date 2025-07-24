from extras.mandate_image import makeJpg, makeTif
from extras.mandate_xml import makeXml
from mandate.models import Mandate
from mandate.custom_functions import presentation_object_factory
from datetime import datetime
from stat import S_IFREG
from stream_zip import ZIP_32

def bytes_to_generator(b):
    yield b


def filesGenerator(list, npci_user):
    for id in list:
        mandate = Mandate.objects.get(id=id)
        imageFile = mandate.mandate_image
        p = presentation_object_factory(npci_user)
        
        yield (
            p.filename_prefix + '_detailfront.jpg',
            datetime.now(),
            S_IFREG | 0o600,
            ZIP_32,
            bytes_to_generator(makeJpg(imageFile))
        )

        yield (
            p.filename_prefix + '_front.tif',
            datetime.now(),
            S_IFREG | 0o600,
            ZIP_32,
            bytes_to_generator(makeTif(imageFile))
        )

        yield (
            p.filename_prefix + '-INP.xml',
            datetime.now(),
            S_IFREG | 0o600,
            ZIP_32,
            bytes_to_generator(makeXml(mandate, p.npci_MsgId).read())
        )
