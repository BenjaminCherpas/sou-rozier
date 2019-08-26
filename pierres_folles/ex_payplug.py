# -*- coding: utf-8 -*-

import base64
from decimal import Decimal
import OpenSSL.crypto as crypto
import urllib

def encoded_dict(in_dict):
    """encode dictionary"""
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict


def payplug_example():
    """try to adapt php example in Python"""
    payment_data = {
        'amount': int(Decimal('10.50') * 100),  # in cents
        'currency': 'EUR',
        'ipn_url': 'http://www.example.org/ipn.php',
        'email': 'ljean@apidev.fr',
        'first_name': 'Luc',
        'last_name': 'Jean',
        #'return_url': '',
        #'cancel_url': '',
        'customer': 1
    }

    payment_data = encoded_dict(payment_data)

    url_params = urllib.urlencode(payment_data)
    encoded_payment_data = urllib.quote_plus(url_params.encode('base64'))

    rsa_key = open('payplug.pem', 'r').read()
    private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, rsa_key)
    signed_data = crypto.sign(private_key, url_params, "sha1")

    out_str = base64.encodestring(signed_data)
    encoded_signed_data = urllib.quote_plus(out_str)

    payment_url = '{0}?data={1}&sign={2}'.format(
        'https://www.payplug.com/p/test/z5K7',
        encoded_payment_data,
        encoded_signed_data
    )
    print(payment_url)


if __name__ == '__main__':
    payplug_example()