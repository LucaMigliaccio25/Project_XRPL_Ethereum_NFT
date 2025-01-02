from utils import create_and_transfer_nft

seed_company = "sEd7uhRLEHf7sELoTUiKTcDwgn3zvdA"
seed_receiver = "sEd7vJWGo5cYxju2raWQ1yQSFPgVejN"
product_uri = "https://diadenn.vercel.app/product/mike-wind-1"
taxon = 0

if __name__ == '__main__':
    wallet_receiver, NFT_token_id = create_and_transfer_nft(seed_company, product_uri, taxon, seed_receiver=seed_receiver)
    print("Everything ok")
    print(f"{wallet_receiver, NFT_token_id = }")
    