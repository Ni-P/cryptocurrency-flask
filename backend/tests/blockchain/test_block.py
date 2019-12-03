import pytest

from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary
from time import sleep, time_ns


def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty


def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    # assert genesis.timestamp == GENESIS_DATA['timestamp']
    # assert genesis.last_hash == GENESIS_DATA['last_hash']
    # assert genesis.hash == GENESIS_DATA['hash']
    # assert genesis.data == GENESIS_DATA['data']

    for key, value in GENESIS_DATA.items():
        assert value == getattr(genesis, key)


def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty + 1


def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')

    sleep(MINE_RATE / SECONDS)

    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty - 1


def test_mine_block_difficulty_limits_at_one():
    last_block = Block(
        time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,
        0
    )

    sleep(MINE_RATE / SECONDS)

    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == 1


@pytest.fixture
def last_block():
    return Block.genesis()


@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'test_data')


def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)


def test_is_valid_block_is_bad_hash(last_block, block):
    block.last_hash = 'bad_hash'
    with pytest.raises(Exception, match='The block last_hash must be correct'):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_proof_of_work(last_block, block):
    block.hash = 'fff'

    with pytest.raises(Exception, match="The PoW was not met"):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_jumped_difficulty(last_block, block):
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty
    block.hash = f"{'0' * jumped_difficulty}111"

    with pytest.raises(Exception, match='Difficulty must adjust by one'):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_block_hash(last_block, block):
    block.hash = '00000000000000bbbaa'

    with pytest.raises(Exception, match='The block hash must be correct'):
        Block.is_valid_block(last_block, block)
