import hashlib

import ed25519


class Signer(object):
    def __init__(self, private_key=None, public_key=None, algorithm="ed25519"):
        self.private_key = private_key
        self.public_key = public_key
        self.algorithm = algorithm

    def sign(self, content: str):
        assert self.private_key
        if self.algorithm == "ed25519":
            sk = ed25519.SigningKey(sk_s=bytes.fromhex(self.private_key))
            return sk.sign(self.content_hash(content))
        else:
            raise NotImplementedError("Only ed25519 is supported")

    @classmethod
    def content_hash(cls, content):
        return hashlib.sha256(hashlib.sha256(content.encode()).digest()).digest()
