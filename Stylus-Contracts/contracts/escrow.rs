#[arbitrum_contract]
mod escrow {
    use stylus_sdk::contract::{Address};

    #[contract]
    pub struct Escrow {
        buyer: Address,
        seller: Address,
        amount: u64,
        is_complete: bool,
    }

    impl Escrow {
        pub fn deposit(&mut self, from: Address, amount: u64) {
            assert_eq!(self.buyer, from, "Only buyer can deposit funds.");
            self.amount = amount;
        }

        pub fn release(&mut self) {
            assert!(!self.is_complete, "Transaction already complete.");
            self.is_complete = true;
            // Logic for transferring funds to seller
        }
    }
}
