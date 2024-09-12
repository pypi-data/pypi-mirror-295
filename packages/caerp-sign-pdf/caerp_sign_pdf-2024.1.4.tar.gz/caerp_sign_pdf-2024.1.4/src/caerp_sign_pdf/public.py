# -*- coding: utf-8 -*-
import logging
import hashlib

from io import BytesIO
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.pdf_utils.xref import ObjectHeaderReadError
from pyhanko.sign import fields, signers
from pyhanko.sign.general import SigningError
from pyhanko.stamp import TextStampStyle
from PyPDF4.pdf import PdfFileReader, PdfFileWriter
from pyramid.httpexceptions import HTTPUnsupportedMediaType

from caerp.views.files.controller import FileData

from .models import PDFSignatureHistory


logger = logging.getLogger(f"caerp.{__name__}")


ERROR_LOAD_CERTIFICATE_MSG = "Impossible de charger le certificat à utiliser \
pour signer numériquement le fichier. Veuillez contacter le support."

ERROR_PDF_FORMAT_MSG = "Le fichier PDF ne peut pas être signé numériquement \
car son format n'est pas correct. Vous pouvez essayer de l'imprimer dans un \
nouveau fichier PDF avant de le recharger."


class SignPDFService(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.dbsession = request.dbsession

    def _get_certificate_path(self) -> str:
        """
        Get the path to the certificate file defined in registry use to sign PDF
        """
        certificate_path = self.request.registry.settings.get(
            "caerp.sign_certificate_path"
        )
        if not certificate_path:
            raise Exception(
                "No certificate to use for signing PDF files (set \
'caerp.sign_certificate_path' in config)"
            )
        return certificate_path

    def _get_certificate_passphrase(self) -> str:
        """
        Get the passphrase defined in registry use to unlock the certificate file
        """
        return self.request.registry.settings.get("caerp.sign_certificate_passphrase")

    def _get_file_data_md5_hash(self, file_data: BytesIO) -> str:
        """
        Return the MD5 hash of the given file's data
        """
        return hashlib.md5(file_data.getvalue()).hexdigest()

    def _get_safe_pdf(self, file_data: BytesIO) -> str:
        """
        Create a new clean PDF buffer from the original
        to avoid some format errors
        """
        writer = PdfFileWriter()
        reader = PdfFileReader(file_data, strict=False)
        num_pages = reader.getNumPages()
        for page in range(num_pages):
            writer.addPage(reader.getPage(page))
        writer.write(file_data)
        return file_data

    def sign(
        self, pdf_data: FileData, node_id: int = None, with_stamp: bool = False
    ) -> bool:
        """
        Sign and stamp (if needed) a PDF file from FileData object coming
        from uploaded CAERP file

        :param FileData pdf_data: The FileData object describing the PDF file
        :param int node_id: The related node's id if relevant
        :param bool with_stamp: whether we want a stamp on result file or not
        :return bool: either the PDF has been signed or not
        """

        logger.info("Signing PDF file '{}'".format(pdf_data.name))

        # Check mimetype
        if not pdf_data.mimetype == "application/pdf":
            logger.warn("File is not a PDF, signing aborted")
            return False

        # Load sign certificate
        signer = signers.SimpleSigner.load_pkcs12(
            pfx_file=self._get_certificate_path(),
            passphrase=self._get_certificate_passphrase().encode(),
        )
        if not signer:
            logger.error(
                "Unable to load certificate for signing PDF files (check \
'caerp.sign_certificate_path' and 'caerp.sign_certificate_passphrase' in config)"
            )
            raise Exception(ERROR_LOAD_CERTIFICATE_MSG)

        # Prepare stamp (if needed)
        stamp = None
        if with_stamp:
            stamp = TextStampStyle(
                timestamp_format="%d/%m/%Y %H:%M:%S %Z",
                stamp_text="Signé par: %(signer)s\nLe: %(ts)s",
                border_width=2,
            )
        else:
            stamp = TextStampStyle(
                stamp_text="",
                border_width=0,
            )

        # Open original PDF
        try:
            pdf_data.data = self._get_safe_pdf(pdf_data.data)
            pdf_writer = IncrementalPdfFileWriter(pdf_data.data, strict=False)
        except Exception as error:
            logger.error(f"Error while opening original PDF file : {error}")
            raise HTTPUnsupportedMediaType(ERROR_PDF_FORMAT_MSG)

        # Add signature field on the PDF
        try:
            fields.append_signature_field(
                pdf_writer,
                sig_field_spec=fields.SigFieldSpec(
                    "SignatureCAERP", box=(445, 800, 580, 830)
                ),
            )
        except SigningError:
            logger.warn("File is already signed, nothing to do")
            return True
        except ObjectHeaderReadError as error:
            logger.error(f"Error while reading Xref header : {error}")
            raise HTTPUnsupportedMediaType(ERROR_PDF_FORMAT_MSG)

        # Sign PDF
        try:
            meta = signers.PdfSignatureMetadata(field_name="SignatureCAERP")
            pdf_signer = signers.PdfSigner(
                meta,
                signer=signer,
                stamp_style=stamp,
            )
            pdf_data.data = pdf_signer.sign_pdf(pdf_writer)
        except Exception as error:
            logger.error(f"Error while signing PDF file : {error}")
            raise HTTPUnsupportedMediaType(ERROR_PDF_FORMAT_MSG)
        logger.info(
            "File '{}' signed successfully by {} !".format(
                pdf_data.name, signer.subject_name
            )
        )

        # Log history
        history = PDFSignatureHistory()
        history.user_id = self.request.identity.id
        history.file_name = pdf_data.name
        history.file_hash = self._get_file_data_md5_hash(pdf_data.data)
        history.node_id = node_id
        self.dbsession.merge(history)
        self.dbsession.flush()

        return True
