import json
from uuid import uuid4
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
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

    def sign(self, data):
        """
        Generate signature based on the daat
        :param data:
        :return:
        """
        return self.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))

    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify signature with the public key
        :param public_key:
        :param data:
        :param signature:
        :return:
        """
        try:
            public_key.verify(signature, json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))
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
