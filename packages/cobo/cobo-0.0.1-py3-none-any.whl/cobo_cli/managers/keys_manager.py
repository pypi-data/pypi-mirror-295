import secrets

import ed25519


class KeysManager(object):
    @classmethod
    def generate(cls, alg, secret=None):
        if not secret:
            secret = secrets.token_hex(32)

        if alg == "ed25519":
            sk = ed25519.SigningKey(sk_s=bytes.fromhex(secret))
            return secret, sk.get_verifying_key().to_bytes().hex()

        raise NotImplementedError("Algorithm {} is not supported".format(alg))
