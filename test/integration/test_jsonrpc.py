import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from alterdotd import AlterdotDaemon
from alterdot_config import AlterdotConfig


def test_alterdotd():
    config_text = AlterdotConfig.slurp_config_file(config.alterdot_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000dea5d2c92cf3f1dce5031cc2b368b2a5e3ebea73ea1278fef673d10b1345'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = AlterdotConfig.get_rpc_creds(config_text, network)
    alterdotd = AlterdotDaemon(**creds)
    assert alterdotd.rpc_command is not None

    assert hasattr(alterdotd, 'rpc_connection')

    # Alterdot testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = alterdotd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert alterdotd.rpc_command('getblockhash', 0) == genesis_hash
