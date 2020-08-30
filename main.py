from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

print('Imports done')

bdb_root_url = 'https://test.ipdb.io/'  # this is testnet url of BigchainDB

bdb = BigchainDB(bdb_root_url)
print(f'bdb configured {bdb}')

alice, bob = generate_keypair(), generate_keypair()
print('Keypairs successful')
print(f"Alice's public key: {alice.public_key}")
print(f"Bob's public key: {bob.public_key}")

bicycle = {
    'data': {
        'bicycle': {
            'serial_number': 'abcd1234',
            'manufacturer': 'bkfab',
        },
    },
}

prepared_creation_tx = bdb.transactions.prepare(operation='CREATE',
                                                signers=alice.public_key,
                                                asset=bicycle)
print('Transaction preperation successful')

fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx, private_keys=alice.private_key)
print('Transaction fulfilled')

sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

print(fulfilled_creation_tx == sent_creation_tx)

print(sent_creation_tx['id'])
