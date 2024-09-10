"""
XML utilities
"""


class XML:
    """
    A thin wrapper around [xmltodict]_.

    References:
        .. [xmltodict] https://pypi.org/project/xmltodict/

    Example:
        >>> # xdoctest: +REQUIRES(module:xmltodict)
        >>> from kwutil.util_xml import *  # NOQA
        >>> text = ub.codeblock(
            '''
            <mydocument has="an attribute">
              <and>
                <many>elements</many>
                <many>more elements</many>
              </and>
              <plus a="complex">
                element as well
              </plus>
            </mydocument>
            ''')
        >>> data = XML.loads(text)
        >>> print(f'data = {ub.urepr(data, nl=-1)}')
        >>> recon = XML.dumps(data, pretty=True)
        >>> print(recon)
    """
    @staticmethod
    def loads(text, process_namespaces=False, backend='xmltodict'):
        import xmltodict
        data = xmltodict.parse(text, process_namespaces=process_namespaces)
        return data

    @staticmethod
    def load(file, process_namespaces=False, backend='xmltodict'):
        import xmltodict
        data = xmltodict.parse(file, process_namespaces=process_namespaces)
        return data

    @staticmethod
    def dump(data, fp, pretty=False, backend='xmltodict'):
        import xmltodict
        text = xmltodict.unparse(data, output=fp, pretty=pretty)
        return text

    @staticmethod
    def dumps(data, pretty=False, backend='xmltodict'):
        import xmltodict
        text = xmltodict.unparse(data, pretty=pretty)
        return text
