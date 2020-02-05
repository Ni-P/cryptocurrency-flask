from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.enums import PNReconnectionPolicy
from pubnub.pubnub import PubNub

from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

subscribe_key = 'sub-c-50a20862-16c3-11ea-9234-a6989f9d21fe'
publish_key = 'pub-c-8828949c-e025-4ecc-97d5-c2c29e37d781'

pnconfig = PNConfiguration()
pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key = publish_key
pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR

CHANNELS = {
    'TEST': "TEST",
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool: TransactionPool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(f'\nChannel: {message_object.channel} | Message: {message_object}')
        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print(f"\n -- Successfully replaced chain")
            except Exception as e:
                print(f"\n -- Did not replace chain, {e}")
        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print(f'\n -- Set the new transaction in the transaction pool')


class PubSub:
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes of the blockchain network.
    """

    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Public message object to the channel
        :param channel:
        :param message:
        :return:
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a Block object to al nodes
        :param block:
        :return:
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Bradcast a trasaction to all nodes
        :param transaction:
        :return:
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())
