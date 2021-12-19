import sys

from algosdk.future import transaction
from algosdk import account
from algosdk.v2client import algod
import common

mnemonic = "candy eager deal flush pull elite job second art divorce task market cattle term write reform month sphere scissors fluid pumpkin feed issue abstract aunt"
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

local_ints = 0
local_bytes = 1
global_ints = 0
global_bytes = 1
global_schema = transaction.StateSchema(global_ints, global_bytes)
local_schema = transaction.StateSchema(local_ints, local_bytes)


def create_app(client, private_key, approval_program, clear_program, global_schema, local_schema):
    print("creating new app")

    # Define sender as creator
    sender = account.address_from_private_key(private_key)

    # Declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC.real

    # Get node suggested parameters
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 100

    # Create unsigned transaction
    txn = transaction.ApplicationCreateTxn(
        sender, params, on_complete,
        approval_program, clear_program,
        global_schema, local_schema
    )

    # Sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Send transaction
    client.send_transactions([signed_txn])

    # Await confirmation
    common

    def parse_config():
        err_msg = """Malformed configuration file: """
        author = 'Gim'
        APP_ID = 44
        return author, APP_ID

    def main():
        if len(sys.argv) < 2:
            print("Must supply at least command argument")
            return

        try:
            author, APP_ID = parse_config()
        except Exception as e:
            print(e)
            return

        # Initialize an `AlgodClient`
        algod_client = algod.AlgodClient(algod_token, algod_address)

        priv_key = common.get_private_key_from_mnemonic(mnemonic)
        pub_key = common.get_public_key_from_private_key(priv_key)

        if sys.argv[1] == 'deploy' or sys.argv[1] == 'update':
            if len(sys.argv) != 2:
                return

            # Read the smart contract source files
            smart_contract_file = open('./assets/blog_smart_contract.teal', "rb")
            smart_contract_source = smart_contract_file.read()
            smart_contract_program = common.compile_program(algod_client, smart_contract_source)

            clear_program_file = open('./assets/clear_program.teal', 'rb')
            clear_program_source = clear_program_file.read()
            clear_program = common.compile_program(algod_client, clear_program_source)

            # If this is a first time deploy
            if sys.argv[1] == 'deploy':
                # Create the blog application
                app_id = create_app(algod_client, private_key, smart_contract_program,
                           clear_program, global_schema, local_schema)
                print("Record the APP_ID {}}".format(app_id))
