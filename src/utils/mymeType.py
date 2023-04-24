import mimetypes


def getMymetype(url):
    return mimetypes.MimeTypes().guess_type(url, strict=True)
