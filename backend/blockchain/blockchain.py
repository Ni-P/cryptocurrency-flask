from backend.blockchain.block import Block


class Blockchain:
    """
    Blockchain: a public ledger of transactions
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        """
        Replace the local chain with with the incoming if the following rules apply:
        The incoming chain must be longer
        incoming chain is formatted properly
        :param chain:
        :return:
        """
        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace, incoming chain must be longer")

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f"Cannot replace, the incoming chain is invalid: {e}")

        self.chain = chain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the given blockchain
        Enforce the following rules:
            the chain must start with genesis block
            blocks must bu formatted properly
        :param chain:
        :return:
        """
        if chain[0] != Block.genesis():
            raise Exception('Genesis block must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(last_block, block)
