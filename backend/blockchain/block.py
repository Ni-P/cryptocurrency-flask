from time import time_ns

from backend.util.crypto_hash import crypto_hash
from backend.config import MINE_RATE
from backend.util.hex_to_binary import hex_to_binary

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
    """
    Block: a unit of storage
    Store transactions in a blockchain
    """

    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp},'
            f'last_hash: {self.last_hash},'
            f'hash: {self.hash},'
            f'Block - data: {self.data}, '
            f'Difficulty:  {self.difficulty}, '
            f'Nonce: {self.nonce},'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on a given last_block and data until a block hash that meets the leading zeroes PoW requirement
        :param last_block:
        :param data:
        :return:
        """
        timestamp = time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, time_ns())
        nonce = 1
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time_ns()
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        """
        Generate the genesis block
        :return:
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate adjusted difficulty according to the MINE_RATE
        :param last_block:
        :param new_timestamp:
        :return:
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if last_block.difficulty > 1:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate a block by enforcing the rules:
        the block must have the proper hash reference
        the block must meet the PoW requirement
        the difficulty must be adjusted by 1
        the block must have a valid combination of the block fields
        :param last_block:
        :param block:
        :return:
        """
        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct')

        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception("The PoW was not met")

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception("Difficulty must adjust by one")

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        )

        print(block)
        print(reconstructed_hash)
        print(last_block)
        if block.hash != reconstructed_hash:
            raise Exception("The block hash must be correct")


def main():
    genesis_block = Block.genesis()
    # last_block = Block(genesis_block, '', '', '', 3, 1)
    block = Block.mine_block(genesis_block, 'test_data')
    print(genesis_block)
    print(block)
    Block.is_valid_block(genesis_block, block)


if __name__ == '__main__':
    main()
