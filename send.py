from bitcoinlib.keys import Key
from bitcoinlib.transactions import Transaction
import requests

def load_private_keys(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def load_destination_address(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def get_balance_from_private_key(private_key):
    key = Key(import_key=private_key, network='testnet')
    return key.balance()  # Lấy số dư trực tiếp từ key

def create_transaction(private_key, to_address, amount):
    key = Key(import_key=private_key, network='testnet')
    
    # Khởi tạo giao dịch mới
    tx = Transaction()
    tx.add_input(key.address, amount)
    tx.add_output(to_address, amount)
    
    # Ký giao dịch
    tx.sign(key)

    # Gửi giao dịch
    response = tx.send()
    
    green = "\033[92m"
    yellow = "\033[93m"
    reset = "\033[0m"
    print(f"{green}Đã chuyển {yellow}{amount} sBTC từ địa chỉ {yellow}{key.address}{green} đến ví yêu cầu. Hash giao dịch: {yellow}{response['txid']}{reset}")

def main():
    private_keys = load_private_keys('prkey.txt')  # Tải private keys từ file
    destination_address = load_destination_address('walletmain.txt')  # Tải địa chỉ ví chính từ file

    for private_key in private_keys:
        key = Key(import_key=private_key)  # Tạo đối tượng key từ private key
        balance = get_balance_from_private_key(private_key)  # Kiểm tra số dư bằng private key

        red = "\033[91m"
        yellow = "\033[93m"
        reset = "\033[0m"

        if balance > 0:
            print(f"{yellow}Ví với private key ({yellow}{private_key[-5:]}{yellow}) có {balance} sBTC.{reset}")
            create_transaction(private_key, destination_address, balance)  # Chuyển tất cả token về ví chính
        else:
            print(f"{red}Ví với private key ({yellow}{private_key[-5:]}{red}) không có sBTC.{reset}")

if __name__ == "__main__":
    main()