#[arbitrum_contract]
mod token {
    use stylus_sdk::erc20::{ERC20, ERC20Interface};

    #[contract]
    pub struct Token {
        total_supply: u64,
    }

    impl ERC20Interface for Token {
        fn transfer(&self, recipient: &Address, amount: u64) -> bool {
            // Logic for token transfer
            true
        }
        
        fn balance_of(&self, account: &Address) -> u64 {
            // Return balance of account
            1000
        }
        
        fn total_supply(&self) -> u64 {
            self.total_supply
        }
    }

    impl Token {
        pub fn new(total_supply: u64) -> Self {
            Token { total_supply }
        }
    }
}
