from pubnub.callbacks import SubscribeCallback
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration

from backend.blockchain.block import Block

subscribe_key = 'sub-c-50a20862-16c3-11ea-9234-a6989f9d21fe'
publish_key = 'pub-c-8828949c-e025-4ecc-97d5-c2c29e37d781'

pnconfig = PNConfiguration()
pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key = publish_key

CHANNELS = {
    'TEST': "TEST",
    'BLOCK': 'BLOCK'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message):
        print(f'\nChannel: {message.channel} | Message: {message}')
        if message.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print(f"\n -- Successfully replaced chain")
            except Exception as e:
                print(f"\n -- Did not replace chain, {e}")


class PubSub:
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes of the blockchain network.
    """

    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

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
