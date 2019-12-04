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

    def to_json(self):
        """
        Serialize the blockchain to JSON
        :return:
        """
        return list(map(lambda block: block.to_json(), self.chain))

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
            print(str(chain[0]))
            raise Exception('Genesis block must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(last_block, block)

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized blocks into a Blockchain instance
        :param chain_json:
        :return:
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block: Block.from_json(block), chain_json))

        return blockchain
