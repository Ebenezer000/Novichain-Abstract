from web3 import Web3
from hexbytes import HexBytes
from web3.middleware import construct_sign_and_send_raw_middleware
from contract_ABI import contract_abi

########################
## Instantiate Tron

#
"""
    An Api to interact with web3.py
"""
class WEBPY():
    def __init__(self) -> None:
        """
        Fetch Chain specific data using chain symbol

        Example:
            >>> from web3_hooks import ETHERS
            >>> ethers = ETHERS()
        """
        self.arbitrum = {
            "base": "ETH",
            "chain_name": "Arbitrum One Chain",
            "chain_id_main": 42161,
            "chain_id_test": 421613,
            "main_rpc": Web3(Web3.HTTPProvider('https://arb1.arbitrum.io/rpc')),
            "test_rpc": Web3(Web3.HTTPProvider('https://goerli-rollup.arbitrum.io/rpc')),
            "main_explorer": "https://arbiscan.io/",
            "test_explorer": "https://goerli.arbiscan.io/",
            "usdt_address_main": Web3.to_checksum_address('0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9'),
            "usdc_address_main": Web3.to_checksum_address('0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8'),
            "fee": 100000000000,
            "decimal": 18,
        }       

        self.arbitrum_sepolia = {
            "base": "ETH",
            "chain_name": "Arbitrum One Chain",
            "chain_id_main": 42161,
            "chain_id_test": 421613,
            "main_rpc": Web3(Web3.HTTPProvider('https://arb1.arbitrum.io/rpc')),
            "test_rpc": Web3(Web3.HTTPProvider('https://goerli-rollup.arbitrum.io/rpc')),
            "main_explorer": "https://arbiscan.io/",
            "test_explorer": "https://goerli.arbiscan.io/",
            "usdt_address_main": Web3.to_checksum_address('0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9'),
            "usdc_address_main": Web3.to_checksum_address('0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8'),
            "fee": 100000000000,
            "decimal": 18,
        }   

        self.chain = {
            "ARBI": self.arbitrum,
            "ARBI_TEST": self.arbitrum_sepolia,
        }

    def base(self, chain) -> dict:
        """
        Function to retieve chain data
        Args:
            chain[str]: Name of current chain
        Returns:
            dict: details of chain
                  mainnet and testnet rpc
        Example:
            >>> whatsapp.base(chain = "BSC")        
        """
        base_dict = self.chain[chain]
        return base_dict
    
    def base_bal(self, chain, state, address) -> int:
        """
        Function to retieve base balance of address
        Args:
            chain[str]: Name of current chain
            state[str]: Name of current chain type [testnet, mainnet, devnet]
            address[str]: Address of user
        Returns:
            int: balance of user     
        """
        w3 = ""
        balance = ""
        if state == "testnet":
            w3 = self.chain[chain]["test_rpc"]
        else:
            w3 = self.chain[chain]["main_rpc"]

        if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
            balance = w3.eth.get_balance(address)
        
        elif chain == "TRON":
            balance = w3.get_account_balance(address)

        return balance

    def create_wallet(self,chain) -> dict:
        """
        Function too create new user wallet on system
        Args:
            chain[str]: Name of current application layer or chain to create with [EVM ,TVM, BSC, ETH]
        Returns:
            account: Account object with EVM and TVM address and keys of user     
        """
        w3 = self.chain[chain]["test_rpc"]
        tron_w3 = self.chain['TRON']["test_rpc"]
        account = w3.eth.account.create('uwefwe2920r2jj303jr20rr09r4')
        tron_account = tron_w3.generate_address()
        account = {
                "evm_address": str(account.address),
                "evm_key": HexBytes.hex(account.key),
                "tvm_address": tron_account['base58check_address'],
                "tvm_key": tron_account['private_key']
            }

        return account
 
    def send_eth(self, chain, state, sender, receiver, amount, key) -> str:
        """
        Function to send raw ether in wrapped transaction
        Args:
            chain[str]: Name of current chain
            sender[str]: Address of transaction sender
            receiver[str]: Address of token receiver
            amount[str]: Amount of eth to send
            key[str]: Private Key of account
        Returns:
            translink[str] || error[str]: transaction hash if successful
                 error if unsuccessful      
        """
        w3 = ""
        explorer = ""
        strtx = ""
        chainId = ""
        if state == "testnet":
            if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                chainId = self.chain[chain]['chain_id_test']
            w3 = self.chain[chain]["test_rpc"]
            explorer = self.base(chain)["test_explorer"]

        else:
            if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                chainId = self.chain[chain]['chain_id_main']
            explorer = self.base(chain)["main_explorer"]
            w3 = self.chain[chain]["main_rpc"]

        if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
            nonce = w3.eth.get_transaction_count(sender)
            gas = w3.eth.estimate_gas(({"from":sender,"to":receiver}), "latest")
            base_fee = w3.eth.gas_price
            #build a transaction in a dictionary
            tx = {
                'chainId': chainId,
                'nonce': nonce,
                'to': receiver,
                'value': amount,
                'gas': gas,
                'gasPrice': base_fee
            }

            #sign the transaction
            signed_tx = w3.eth.account.sign_transaction(tx, key)

            #send transaction
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            strtx = Web3.to_hex(tx_hash)

        elif chain == "TRON":
            try:
                pkey = PrivateKey(bytes.fromhex(key))
                
                # create transaction and broadcast it
                txn = (
                    w3.trx.transfer(sender, receiver, int(amount))
                    .memo("Transaction Description")
                    .build()
                    .inspect()
                    .sign(pkey)
                    .broadcast()
                )
                # wait until the transaction is sent through and then return the details  
                strtx =  txn.wait()['id']

            # return the exception
            except Exception as e:
                print (e)
            
        trans_link = explorer+strtx
        return trans_link
    
    def send_token(self, chain, state, sender, receiver, amount, token_address, key) -> str:
        """
        Function to send erc20 tokens in wrapped transaction
        Args:
            chain[str]: Name of current chain
            sender[str]: Address of transaction sender
            receiver[str]: Address of token receiver
            amount[str]: Amount of token to send
            token_address[str]: Address of token to send
            key[str]: Private Key of account
        Returns:
            translink[str] || error[str]: transaction hash if successful
                 error if unsuccessful      
        """
        w3 = ""
        explorer = ""
        strtx = ""
        chainId = ""
        if state == "testnet":
            if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                chainId = self.chain[chain]['chain_id_test']
            w3 = self.chain[chain]["test_rpc"]
            explorer = self.base(chain)["test_explorer"]

        else:
            if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                chainId = self.chain[chain]['chain_id_main']
            explorer = self.base(chain)["main_explorer"]
            w3 = self.chain[chain]["main_rpc"]

        if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
            #main net
            token_contract = w3.eth.contract(Web3.to_checksum_address(token_address), abi= contract_abi.token_abi)
            nonce = w3.eth.get_transaction_count(sender)
            base_fee = w3.eth.gas_price
            gas_fee = token_contract.functions.transfer(receiver, amount).estimate_gas()

            print (f"Gas price is Base fee is: {base_fee}")

            tx = token_contract.functions.transfer(
            receiver, amount
            ).build_transaction({
            'chainId': chainId,
            'gas': gas_fee,
            'gasPrice': base_fee,
            'nonce': nonce,})

            signed_txn = w3.eth.account.sign_transaction(tx, key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            strtx = HexBytes.hex(tx_hash)



        elif  chain == "TRON":
            w3 = Tron(network='shasta')
            token_contract = w3.get_contract(token_address)
            txn = (
                 token_contract.functions.transfer(receiver, 1_000)
                 .with_owner(sender)  # address of the private key
                 .fee_limit(5_000_000)
                 .build()
                 .sign(key)
            )
            txn.broadcast()
            strtx =  txn.wait()['id']
            

        trans_link = explorer+strtx
        return trans_link

    def swap_token(self, chain, sender, amount, token1, token2, key) -> str:
        """
        Function to swap erc20 tokens in wrapped transaction
        Args:
            chain[str]: Name of current chain
            sender[str]: Address of transaction sender
            amount[str]: Amount of token to swap
            token1[str]: Address of token to swap
            token2[str]: Address of token to receive
            key[str]: Private Key of account
        Returns:
            str: transaction hash if successful
                 error if unsuccessful      
        """
        return "Token Swapped"


    def token_details(self, chain, state, token_address) -> dict:
        """
        Function to retieve details of erc20 token
        Args:
            chain[str]: Name of current chain
            token[str]: Address of current token
        Returns:
            dict: details of token       
        """
        w3 = ""
        token = ""
        if state == "testnet":
            w3 = self.chain[chain]["test_rpc"]
        else:
            w3 = self.chain[chain]["main_rpc"]

        if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
            token_contract = w3.eth.contract(Web3.to_checksum_address(token_address), abi= contract_abi.token_abi)
            token_name = token_contract.caller.name()
            token_symbol = token_contract.caller.symbol()
            token_decimal = token_contract.caller.decimals()
            token = {
                "name": token_name,
                "symbol": token_symbol,
                "decimal": token_decimal
            }
        
        elif chain == "TRON":
            token_contract = w3.get_contract(token_address)
            token_name = token_contract.functions.name()
            token_symbol = token_contract.functions.symbol()
            token_decimal = token_contract.functions.decimals()
            token = {
                "name": token_name,
                "symbol": token_symbol,
                "decimal": token_decimal
            }
        return token
       
    def token_bal(self, chain, state, user_address, token_address) -> int:
        """
        Function to retieve user balance of erc20 token
        Args:
            chain[str]: Name of current chain
            user_address[str]: Address of user
            token_address[str]: Address of current token
        Returns:
            int: user token balance     
        """
        w3 = ""
        balance = ""
        if state == "testnet":
            w3 = self.chain[chain]["test_rpc"]
        else:
            w3 = self.chain[chain]["main_rpc"]

        if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
            w3.eth.default_account = user_address
            token_contract = w3.eth.contract(Web3.to_checksum_address(token_address), abi= contract_abi.token_abi)
            balance = token_contract.caller.balanceOf(user_address)

        elif chain == "TRON":
            token_contract = w3.get_contract(token_address)
            balance = token_contract.functions.balanceOf(user_address)

        return balance

    def default_token_list(self, chain, state) -> list:
        """
        Function to return the default list of tokens for each chain
        Args:
            chain[str]: Name of current chain
            state[str]: Name of crrent chain state [testnet , mainnet, devnet]
        Returns:
            default_list[array]: Array of default token addresses of current chain using chain state   
        """
        _chain = self.chain[chain]
        default_list = []
        if chain == "ETH" or chain == "POLY":
            if state == "mainnet":
                default_list = [_chain['usdt_address_main'], 
                                _chain['usdc_address_main'],
                                _chain['busd_address_main']]
            else:
                default_list = []

        elif chain == "ARBI":
            if state == "mainnet":
                default_list = [_chain['usdt_address_main'], 
                                _chain['usdc_address_main']]
            else:
                default_list = []
            
        elif chain == "BUSD":
            if state == "mainnet":
                default_list = [_chain['usdt_address_main'], 
                                _chain['usdc_address_main'],
                                _chain['busd_address_main']]
            else:
                default_list = [_chain['usdt_address_test'], 
                                _chain['usdc_address_test'],
                                _chain['busd_address_test']]
        
        elif chain == "TRON":
            if state == "mainnet":
                default_list = [_chain['usdt_address_main'], 
                                _chain['usdc_address_main'],
                                _chain['busd_address_main']]
            else:
                default_list = []
        return default_list
    
    def is_address(self, chain, address) -> bool:
        """
        Function to confirm that string is address
        Args:
            address[str]: address in string
        Returns:
            is_add[bool]: returns True if address       
        """
        is_add = ""
        if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
            is_add = Web3.is_address(address)
        
        elif chain == "TRON":
            w3 = self.chain[chain]["test_rpc"]
            is_add = w3.is_address(str(address))
        return is_add
   
#



