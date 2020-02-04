import json
from uuid import uuid4
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

from backend.config import STARTING_BALANCE


class Wallet:
    """
    An individual wallet for a miner
    Keeps track of balance and allows miner to auth transacions
    """

    def __init__(self):
        self.address = str(uuid4())[0:8]
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1, default_backend())
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()

    def sign(self, data):
        """
        Generate signature based on the data
        :param data:
        :return:
        """
        return decode_dss_signature(self.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256())))

    def serialize_public_key(self):
        """
        Reset the public key to its serialized version
        :return:
        """
        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify signature with the public key
        :param public_key:
        :param data:
        :param signature:
        :return:
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        (r, s) = signature

        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s),
                json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature as e:
            print(e)
            return False


def main():
    wallet = Wallet()
    print(f'wallet: {wallet.__dict__}')
    data = {'foo': 'bar'}
    sign = wallet.sign(data)
    print(f'sign: {sign}')

    should_be_valid = Wallet.verify(wallet.public_key, data, sign)
    print(f'Should be valid: {should_be_valid}')

    should_be_invalid = Wallet.verify(Wallet().public_key, data, sign)
    print(f'Should be invalid: {should_be_invalid}')


if __name__ == '__main__':
    main()
