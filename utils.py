from xrpl.account import get_balance, get_next_valid_seq_number
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet, generate_faucet_wallet
from xrpl.core import keypairs
from xrpl.transaction import sign, submit_and_wait, XRPLReliableSubmissionException
from xrpl.models import Payment
from xrpl.models.transactions import NFTokenMint, NFTokenCreateOffer, NFTokenAcceptOffer
from xrpl.utils import str_to_hex, datetime_to_ripple_time
from xrpl.ledger import get_latest_validated_ledger_sequence
from datetime import datetime, timedelta

client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

def _generate_xrpl_wallet_seed() -> str:
    """
    Generate a random seed. Notice that if you create a wallet with this seed, it won't be a working wallet, because you need to fund it before. See https://xrpl.org/docs/concepts/accounts#creating-accounts.
    """
    return keypairs.generate_seed()

def get_wallet(seed: str | None = None) -> Wallet:
    """
    Generate a wallet.
    """
    if seed:
        wallet = Wallet.from_seed(seed)
    else:
        wallet = generate_faucet_wallet(client, debug=True)
    return wallet

def print_balances(wallets: list, client: JsonRpcClient) -> None:
    """
    Print the balances of wallets.
    """
    print("Balances:")
    for wallet in wallets:
        print(f"{wallet.address}: {get_balance(wallet.address, client)}")

def mint_nft_token(seed, uri, flags, transfer_fee, taxon):
    minter_wallet=Wallet.from_seed(seed)
    mint_tx=NFTokenMint(
        account=minter_wallet.address,
        uri=str_to_hex(uri),
        flags=int(flags),
        transfer_fee=int(transfer_fee),
        nftoken_taxon=int(taxon)
    )
    response=""
    try:
        response=submit_and_wait(mint_tx,client,minter_wallet)
        response=response.result
    except XRPLReliableSubmissionException as e:
        response=f"Submit failed: {e}"
    return response

def create_sell_offer(seed, amount, nftoken_id, expiration, destination):
    owner_wallet = Wallet.from_seed(seed)
    expiration_date = datetime.now()
    if expiration != '':
        expiration_date = datetime_to_ripple_time(expiration_date)
        expiration_date = expiration_date + int(expiration)
    sell_offer_tx=NFTokenCreateOffer(
        account=owner_wallet.address,
        nftoken_id=nftoken_id,
        amount=amount,
        destination=destination if destination != '' else None,
        expiration=expiration_date if expiration != '' else None,
        flags=1
    )
    response=""
    try:
        response=submit_and_wait(sell_offer_tx,client,owner_wallet)
        response=response.result
    except XRPLReliableSubmissionException as e:
        response=f"Submit failed: {e}"
    return response

def accept_sell_offer(seed, offer_index):
    buyer_wallet=Wallet.from_seed(seed)
    accept_offer_tx=NFTokenAcceptOffer(
       account=buyer_wallet.classic_address,
       nftoken_sell_offer=offer_index
    )
    try:
        response=submit_and_wait(accept_offer_tx,client,buyer_wallet)
        response=response.result
    except XRPLReliableSubmissionException as e:
        response=f"Submit failed: {e}"
    return response

MIN_AMOUNT = "2000"
MIN_FEE = "20"

def create_and_transfer_nft(seed_company, product_uri, taxon, seed_receiver = None, chain_url = "https://s.altnet.rippletest.net:51234"):
    try:
        client=JsonRpcClient(chain_url)

        wallet_company = get_wallet(seed_company)
        seed_company = wallet_company.seed
        
        flag = 8
        transfer_fee = 0
        response_mint_token = mint_nft_token(
                seed_company,
                product_uri,
                flag,
                transfer_fee,
                taxon
            )
        # print(f"{response_mint_token = }")
        NFT_token_id = response_mint_token['meta']['nftoken_id'] 

        wallet_receiver = get_wallet(seed_receiver)
        seed_receiver = wallet_receiver.seed
        # print(f"{seed_receiver = }")

        # Create account by sending funds
        current_validated_ledger = get_latest_validated_ledger_sequence(client)

        tx_payment = Payment(
            account=wallet_company.address,
            amount=MIN_AMOUNT,
            destination=wallet_receiver.address,
            last_ledger_sequence=current_validated_ledger + 20,
            sequence=get_next_valid_seq_number(wallet_company.address, client),
            fee=MIN_FEE,
        )
        my_tx_payment_signed = sign(tx_payment, wallet_company)
        tx_response = submit_and_wait(my_tx_payment_signed, client)

        # print_balances([wallet_company, wallet_receiver], client)

        # Create Sell Offer for the receiver account with amount 0 and accept it
        current_time = datetime.now()
        expiration_time = current_time + timedelta(minutes=60)
        expiration_time = datetime_to_ripple_time(expiration_time)

        response_sell_offer = create_sell_offer(seed_company, '0', NFT_token_id, expiration=expiration_time, destination=wallet_receiver.address)
        # print(f"{response_sell_offer = }")
        sell_offer_ledger_index = response_sell_offer['meta']['offer_id']

        # Accept sell offer of company by receiver
        response_accept_sell_offer = accept_sell_offer(seed_receiver, sell_offer_ledger_index)
        # print(f"{response_accept_sell_offer = }")

        if not response_accept_sell_offer['meta']['TransactionResult'] == 'tesSUCCESS':
            raise Exception(f'Didn\'t work: {e}')
    
        return wallet_receiver, NFT_token_id
    except Exception as e:
        raise Exception(f'Didn\'t work: {e}')