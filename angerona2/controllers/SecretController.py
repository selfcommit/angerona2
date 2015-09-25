from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

from angerona2 import DBSession
from angerona2.models.secret import Secret

from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

import datetime

class SecretExpiredException(Exception):
    pass

class SecretController(object):
    '''
    Encrypts data and stores it into the provided Secret
    Decrypts data from a provided Secret and returns it
    '''

    def __init__(self):
        self._secret = None

    def create_secret(self, *args, **kwargs):
        '''create secret, encrypt, and return tuple'''
        self._secret = Secret()
        for key in ('expiry_time', 'snippet_type', 'lifetime_reads', 'early_delete'):
            if key == 'early_delete':
                self._secret.flag_delete_early = kwargs['early_delete']
                continue

            if key == 'lifetime_reads':
                if kwargs['lifetime_reads'] < 0:
                    self._secret.flag_unlimited_reads = True
                    continue

            setattr(self._secret, key, kwargs[key])

        session = DBSession()
        secret, uuid = self._encrypt(kwargs['plaintext'])
        DBSession.add(secret)
        DBSession.flush()
        return (secret, uuid)

    def decrypt_secret(self, uuid):
        '''retrieve secret from the database, decrypt and return tuple'''
        session = DBSession()
    
        hasher = SHA256.new()
        hasher.update(bytes('{}{}'.format(uuid, uuid), encoding='utf-8'))
        uniqhash = hasher.hexdigest()

        # see if we can find such a secret
        try:
            result = session.query(Secret).filter(
                        Secret.uniqhash == uniqhash,
                        Secret.expiry_time >= datetime.datetime.now(),
                        or_(
                            Secret.lifetime_reads > 0,
                            Secret.lifetime_reads == -1
                        )).one()
        except NoResultFound as e:
            raise SecretExpiredException()

        # excellent, decrement the views & immediately write to database
        if not result.flag_unlimited_reads:
            result.lifetime_reads -= 1
            session.update(result)
            session.flush()

        # decrypt the data in our secret, return them
        plaintext = _decrypt(result, uniqhash)
        return (result, plaintext)

    def _decrypt(self, secret, uuid):
        # generate the input for our key derivation formula
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, secret.nonce))
        keyhash = hasher.digest()

        # derive our AES key (aes256 wants 32bytes)
        aeskey = PBKDF2(
            password=keyhash,
            salt=secret.Salt,
            dkLen=32,
            count=25000,
            )

        # derive our Iv from the UniqID (16 bytes)
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, aeskey))
        aesiv = hasher.digest()[:16]

        # unpad from http://stackoverflow.com/a/12525165/274549
        BS = 16
        unpad = lambda s : s[0:-ord(s[-1])]

        # decrypt and unpad it
        cipher = AES.new(aeskey, AES.MODE_CBC, aesiv)
        return unpad(cipher.decrypt(secret.stored_data))

    def is_inrangeor(self, val, rmin, rmax, become):
        if int(val) < rmin and int(val) > rmax:
            return become
        else:
            return int(val)

    def is_supportedtype(self, val):
        '''makes sure our data is a supported syntax type, otherwise returns
        empty string indicating raw data'''
        choices = ('', 'as3','shell','cf','csharp','cpp','css','delphi','diff',
                   'erl','groovy','js','java','jfx','pl','php','plain','ps',
                   'py','ruby','scala','sql','vb','xml')

        if val in choices:
            return val
        else:
            return ''

    def _encrypt(self, plaintext):
        # get 32 long crypto-secure string using prng
        lookup = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWKYZ0123456789'
        uniqid = ''.join(lookup[ord(Random.get_random_bytes(1)) % 62] for _ in range(32))
        uniqid = bytes(uniqid, encoding='utf-8')
        self._secret.nonce = Random.get_random_bytes(32)
        self._secret.salt = Random.get_random_bytes(32)

        # generate the hash of our UniqID (host-safing the data)
        hasher = SHA256.new()
        hasher.update(bytes('{}{}'.format(uniqid, uniqid), encoding='utf-8'))
        self._secret.uniqhash = hasher.hexdigest()

        # generate the input for our key derivation formula
        hasher = SHA256.new()
        hasher.update(bytes('{}{}'.format(uniqid, self._secret.nonce), encoding='utf-8'))
        keyhash = hasher.digest()

        # derive our AES key (aes256 wants 32bytes)
        aeskey = PBKDF2(
            password=keyhash,
            salt=self._secret.salt,
            dkLen=32,
            count=25000,
            )

        # derive our Iv from the UniqID (16 bytes)
        hasher = SHA256.new()
        hasher.update(bytes('{}{}'.format(uniqid, aeskey), encoding='utf-8'))
        aesiv = hasher.digest()[:16]

        # pad from http://stackoverflow.com/a/12525165/274549
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')

        # encrypt it w/ padding
        cipher = AES.new(aeskey, AES.MODE_CBC, aesiv)
        self._secret.stored_data = cipher.encrypt(pad(plaintext))

        # this is the only place the original uniqid is returned
        return (self._secret, uniqid)
