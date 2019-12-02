from time import time

from backend.util.crypto_hash import crypto_hash

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': []
}


class Block:
    """
    Block: a unit of storage
    Store transactions in a blockchain
    """

    def __init__(self, timestamp, last_hash, hash, data):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}'
            f'last_hash: {self.last_hash}'
            f'hash: {self.hash}'
            f'Block - data: {self.data})'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on a given last_block and data
        :param last_block:
        :param data:
        :return:
        """
        timestamp = time()
        last_hash = last_block.hash
        hash = crypto_hash(timestamp, last_hash, data)

        return Block(timestamp, last_hash, hash, data)

    @staticmethod
    def genesis():
        """
        Generate the genesis block
        :return:
        """
        # return Block(
        #              timestamp=GENESIS_DATA["timestamp"],
        #              last_hash=GENESIS_DATA["genesis_last_hash"],
        #              hash=GENESIS_DATA["genesis_hash"],
        #              data=GENESIS_DATA["data"])
        return Block(**GENESIS_DATA)


def main():
    genesis_block = Block.genesis()
    block = Block(genesis_block, '', '', '')
    print(block)


if __name__ == '__main__':
    main()
