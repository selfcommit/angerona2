from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

from angerona2.models.secret import Secret


class SecretController(object):
    '''
    Encrypts data and stores it into the provided Secret
    Decrypts data from a provided Secret and returns it
    '''

    def __init__(self):
        self._secret = None

    def create_secret(self, *args, **kwargs):
        '''create secret & encrypt plaintext'''
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

        return self._encrypt(kwargs['plaintext'])

    def decrypt_secret(self, uuid):
        '''retrieve secret from the database, decrypt and return data'''
        pass

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
            count=10000,
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


class DecoderRing(object):
    def __init__(self, secret, uuid=False):
        if not isinstance(Secret, secret):
            raise ValueError('Secret must be a <Secret>')

        self.secret = secret
        self._uuid = uuid
        self._data = None
        self._isready = False

    @property
    def data(self):
        if not self.uuid:
            raise ValueError('Must set uuid before attempting to read data.')

        if not self._isready:
            self._decrypt_data(self.uuid)

        return self._data

    @data.setter
    def data(self, value):
        self._isready = False
        self._data = value

    def _decrypt_data(self, uniqid):
        # generate the input for our key derivation formula
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, self.secret.nonce))
        keyhash = hasher.digest()

        # derive our AES key (aes256 wants 32bytes)
        aeskey = PBKDF2(
            password=keyhash,
            salt=in_model.Salt,
            dkLen=32,
            count=10000,
            )

        # derive our Iv from the UniqID (16 bytes)
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, aeskey))
        aesiv = hasher.digest()[:16]

        # unpad from http://stackoverflow.com/a/12525165/274549
        BS = 16
        unpad = lambda s : s[0:-ord(s[-1])]

        # encrypt it w/ padding
        cipher = AES.new(aeskey, AES.MODE_CBC, aesiv)
        self._data = unpad(cipher.decrypt(self.secret.stored_data))
        self._isready = True

    
