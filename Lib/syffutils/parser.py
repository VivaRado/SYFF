#import lib.cssutils as cssutils
from .stylesheets import *
from .prodparser import *
from .css import *
from .tokenize2 import Tokenizer



def parseString(
        cssText, encoding=None, href=None, media=None, title=None, validate=None
    ):
        """Parse `cssText` as :class:`~cssutils.css.CSSStyleSheet`.
        Errors may be raised (e.g. UnicodeDecodeError).

        :param cssText:
            CSS string to parse
        :param encoding:
            If ``None`` the encoding will be read from BOM or an @charset
            rule or defaults to UTF-8.
            If given overrides any found encoding including the ones for
            imported sheets.
            It also will be used to decode `cssText` if given as a (byte)
            string.
        :param href:
            The ``href`` attribute to assign to the parsed style sheet.
            Used to resolve other urls in the parsed sheet like @import hrefs.
        :param media:
            The ``media`` attribute to assign to the parsed style sheet
            (may be a MediaList, list or a string).
        :param title:
            The ``title`` attribute to assign to the parsed style sheet.
        :param validate:
            If given defines if validation is used. Uses CSSParser settings as
            fallback
        :returns:
            :class:`~cssutils.css.CSSStyleSheet`.
        """
        
        # TODO: py3 needs bytes here!
        if isinstance(cssText, bytes):
            cssText = codecs.getdecoder('css')(cssText, encoding=encoding)[0]

        # if validate is None:
        #     validate = self._validate

        sheet = CSSStyleSheet(
            href=href,
            media=MediaList(media),
            title=title,
            validating=validate,
        )
        sheet._setFetcher()
        
        __tokenizer = Tokenizer(doComments=False)
        # tokenizing this ways closes open constructs and adds EOF
        sheet._setCssTextWithEncodingOverride(
            __tokenizer.tokenize(cssText, fullsheet=True),
            encodingOverride=encoding,
        )
        
        return sheet

