from sqlalchemy import (
    Column,
    LargeBinary,
    SmallInteger,
    String,
    DateTime
    )

from sqlalchemy.orm import (
    synonym,
    )

from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

from angerona2 import (
    Base,
    DBSession,
)


class Secret(Base):
    __tablename__ = 'secret'
    uniqhash = Column(String(64), primary_key=True)
    nonce = Column(LargeBinary(32))
    salt = Column(LargeBinary(32))
    snippet_type = Column(String(8))
    expiry_time = Column(DateTime)
    lifetime_reads = Column(SmallInteger)
    stored_data = Column(LargeBinary)


    def __init__(self, uniqid):
        self.uniqhash = uniqid


    def _decrypt_data(self, uniqid):
        #generate the input for our key derivation formula
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, self.nonce))
        keyhash = hasher.digest()

        #derive our AES key (aes256 wants 32bytes)
        aeskey = PBKDF2(
            password=keyhash,
            salt=in_model.Salt,
            dkLen=32,
            count=10000,
            )

        #derive our Iv from the UniqID (16 bytes)
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, aeskey))
        aesiv = hasher.digest()[:16]

        #unpad from http://stackoverflow.com/a/12525165/274549
        BS = 16
        unpad = lambda s : s[0:-ord(s[-1])]

        #encrypt it w/ padding
        cipher = AES.new(aeskey, AES.MODE_CBC, aesiv)
        return unpad(cipher.decrypt(self.ciphertext))


    def _encrypt_data(self, plaintext):
        #get 32 long crypto-secure string using rng
        lookup = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWKYZ0123456789'
        uniqid = ''.join(lookup[ord(Random.get_random_bytes(1))%62] for _ in range(32))
        self.nonce = Random.get_random_bytes(32)
        self.salt = Random.get_random_bytes(32)

        #generate the hash of our UniqID (host-safing the data)
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, uniqid))
        self.uniqhash = hasher.hexdigest()

        #generate the input for our key derivation formula
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, self.nonce))
        keyhash = hasher.digest()

        #derive our AES key (aes256 wants 32bytes)
        aeskey = PBKDF2(
            password=keyhash,
            salt=self.salt,
            dkLen=32,
            count=10000,
            )

        #derive our Iv from the UniqID (16 bytes)
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, aeskey))
        aesiv = hasher.digest()[:16]

        #pad from http://stackoverflow.com/a/12525165/274549
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

        #encrypt it w/ padding
        cipher = AES.new(aeskey, AES.MODE_CBC, aesiv)
        self.stored_data = cipher.encrypt(pad(plaintext))

        # this is the only place the original uniqid is returned
        return uniqid

