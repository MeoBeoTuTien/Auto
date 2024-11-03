import requests
import time
from datetime import datetime

def load_wallet_addresses():
    with open("wallet.txt", "r") as file:
        addresses = [line.strip() for line in file if line.strip()]
    return addresses

def claim_faucet(address):
    url = f"https://signetfaucet.bublina.eu.org/claim/?address={address}"
    
    green = "\033[92m"
    red = "\033[91m"
    yellow = "\033[93m"
    light_blue = "\033[96m"
    reset = "\033[0m"

    short_address = address[-5:] 

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{green}Yêu cầu faucet cho ({yellow}{short_address}{green}) thành công!{reset}")
            return True  
        elif response.status_code == 429:
            print(f"{red}Địa chỉ ví ({yellow}{short_address}{red}). Mã lỗi: ({yellow}{response.status_code}{red}), thử lại sau.{reset}")
        else:
            print(f"{light_blue}Địa chỉ ví ({yellow}{short_address}{light_blue}). Mã lỗi: ({yellow}{response.status_code}{light_blue}), thử lại sau.{reset}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi kết nối với địa chỉ {address}: {e}")
    
    return False 

def save_successful_claims(successful_addresses):
    with open("done.txt", "a") as file:
        file.write("Danh sách faucet thành công:\n")
        file.write(f"Thời gian: {datetime.now().strftime('%H:%M:%S, %d/%m/%Y')}\n")
        for address in successful_addresses:
            file.write(f"Địa chỉ ví: {address}\n")
        file.write("\n") 

def main():
    addresses = load_wallet_addresses()
    total_addresses = len(addresses)

    while True:
        success_count = 0 
        successful_addresses = [] 

        for address in addresses:
            if claim_faucet(address):
                successful_addresses.append(address)
                success_count += 1 
            time.sleep(0)

        yellow = "\033[93m"
        green = "\033[92m"
        reset = "\033[0m"
        
        print(f"{green}Code by Telegram @MeIi0das{reset}")
        print(f"{green}Đã Faucet thành công {success_count}/{total_addresses} địa chỉ ví{reset}")
        
        print(f"{yellow}Hoàn thành yêu cầu cho tất cả các địa chỉ. Chờ 1 tiếng trước khi lặp lại...{reset}")
        
        if success_count > 0: 
            save_successful_claims(successful_addresses)

        time.sleep(3600) 

if __name__ == "__main__":
    main()