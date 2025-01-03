from utils_bridge import create_and_transfer_nft

seed_company = "sEd7uhRLEHf7sELoTUiKTcDwgn3zvdA"
seed_receiver = "sEd7vJWGo5cYxju2raWQ1yQSFPgVejN"
product_uri = "https://diadenn.vercel.app/product/mike-wind-1"
taxon = 0

if __name__ == '__main__':
    try:
        # Creazione NFT su XRPL e Ethereum
        contract_address, NFT_token_id = create_and_transfer_nft(seed_company, product_uri, taxon, seed_receiver=seed_receiver)
        print(f"Creazione completata:\nXRPL: {NFT_token_id}\nEthereum: NFT dinamico creato.")
    except Exception as e:
        print(f"Errore durante la creazione: {e}")
    