from backend.wallet.wallet import Wallet


def test_verify_valid_signature():
    data = {'foo': '_data'}
    wallet = Wallet()
    signa = wallet.sign(data)

    assert Wallet.verify(wallet.public_key, data, signa) is True


def test_verify_invalid_signature():
    data = {'foo': '_data'}
    wallet = Wallet()
    signa = wallet.sign(data)

    assert Wallet.verify(Wallet().public_key, data, signa) is False
