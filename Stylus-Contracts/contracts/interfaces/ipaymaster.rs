#[arbitrum_contract]
mod ipaymaster {
    use stylus_sdk::contract::{Address};

    #[contract]
    pub trait IPaymaster {
        fn validate_paymaster_user_op(&self, user_op: UserOperation) -> bool;

        fn deposit_funds(&mut self, amount: u64) -> bool;

        fn withdraw_funds(&mut self, amount: u64, recipient: Address) -> bool;
    }

    impl IPaymaster for Paymaster {
        fn validate_paymaster_user_op(&self, user_op: UserOperation) -> bool {
            // Logic to validate user operation for gasless transaction
            true
        }

        fn deposit_funds(&mut self, amount: u64) -> bool {
            // Logic to deposit funds into the paymaster for covering gas fees
            self.funds += amount;
            true
        }

        fn withdraw_funds(&mut self, amount: u64, recipient: Address) -> bool {
            // Logic to withdraw funds from paymaster
            assert!(self.funds >= amount, "Insufficient funds");
            self.funds -= amount;
            // Transfer amount to recipient
            true
        }
    }

    #[contract]
    pub struct Paymaster {
        funds: u64,
    }

    impl Paymaster {
        pub fn new() -> Self {
            Paymaster {
                funds: 0,
            }
        }
    }

    // Define UserOperation struct (same as in IERC4337Wallet)
    pub struct UserOperation {
        pub sender: Address,
        pub nonce: u64,
        pub init_code: Vec<u8>,
        pub call_data: Vec<u8>,
        pub call_gas_limit: u64,
        pub verification_gas_limit: u64,
        pub pre_verification_gas: u64,
        pub max_fee_per_gas: u64,
        pub max_priority_fee_per_gas: u64,
        pub paymaster_and_data: Vec<u8>,
        pub signature: Vec<u8>,
    }
}
