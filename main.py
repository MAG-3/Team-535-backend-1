from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

alice, bob = generate_keypair(), generate_keypair()

bdb_root_url = 'https://test.ipdb.io'  # Use YOUR BigchainDB Root URL here

bdb = BigchainDB(bdb_root_url)

hello_1 = {'data': {'msg': 'Hello BigchainDB 1!'}, }

# bicycle_asset_metadata = {
#     'planet': 'earth'
# }

prepared_creation_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset=hello_1
    # metadata=bicycle_asset_metadata
)

fulfilled_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx,
    private_keys=alice.private_key
)

sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

txid = fulfilled_creation_tx['id']

asset_id = txid

print(f'Asset id: {asset_id}')

transfer_asset = {
    'id': asset_id
}

output_index = 0
output = fulfilled_creation_tx['outputs'][output_index]

transfer_input = {
    'fulfillment': output['condition']['details'],
    'fulfills': {
        'output_index': output_index,
        'transaction_id': fulfilled_creation_tx['id']
    },
    'owners_before': output['public_keys']
}

prepared_transfer_tx = bdb.transactions.prepare(
    operation='TRANSFER',
    asset=transfer_asset,
    inputs=transfer_input,
    recipients=bob.public_key,
)

fulfilled_transfer_tx = bdb.transactions.fulfill(
    prepared_transfer_tx,
    private_keys=alice.private_key,
)

sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)

print("Is Bob the owner?",
      sent_transfer_tx['outputs'][0]['public_keys'][0] == bob.public_key)

print("Was Alice the previous owner?",
      fulfilled_transfer_tx['inputs'][0]['owners_before'][0] == alice.public_key)

print(bdb.assets.get(search='hello')[0]['data'])

print(bdb.metadata.get(search='earth')[0]['id'])
print(bdb.blocks.get(txid=txid))
