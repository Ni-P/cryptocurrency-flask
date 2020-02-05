from backend.blockchain.block import Block
from backend.config import MINING_REWARD_INPUT
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


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
            blocks must be formatted properly
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

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce the rules of the blockchain
            - Each transaction must only appear once int ge blockchain
            - There can only be one mining reward per block
            - Each transaction must be valid
        :param chain:
        :return:
        """
        transaction_ids = set()

        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(f"There can only be one mining reward in a block. Check block {block.hash}")
                    has_mining_reward = True
                else:
                    if transaction.id in transaction_ids:
                        raise Exception(f"Transaction {transaction.id} is not unique")

                    transaction_ids.add(transaction.id)

                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]

                    historic_balance = Wallet.calculate_balance(historic_blockchain,
                                                                transaction.input['address'])

                    if historic_balance != transaction.input['amount']:
                        raise Exception(
                            f"Transaction {transaction.id} has an invalid input amount"
                        )

                    Transaction.is_valid_transaction(transaction)

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
