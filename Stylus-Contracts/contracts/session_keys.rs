#[arbitrum_contract]
mod session_keys {
    use stylus_sdk::contract::{Address};

    #[contract]
    pub struct SessionKeys {
        owner: Address,
        session_keys: Vec<SessionKey>,
    }

    impl SessionKeys {
        pub fn new(owner: Address) -> Self {
            SessionKeys {
                owner,
                session_keys: Vec::new(),
            }
        }

        pub fn add_session_key(&mut self, key: Address, expiration: u64) {
            let session_key = SessionKey {
                key,
                expiration,
            };
            self.session_keys.push(session_key);
        }

        pub fn is_key_valid(&self, key: Address) -> bool {
            for session_key in self.session_keys.iter() {
                if session_key.key == key && session_key.is_active() {
                    return true;
                }
            }
            false
        }

        pub fn remove_session_key(&mut self, key: Address) {
            self.session_keys.retain(|session_key| session_key.key != key);
        }
    }

    // Define a struct for representing a session key with an expiration time
    pub struct SessionKey {
        pub key: Address,
        pub expiration: u64,
    }

    impl SessionKey {
        pub fn is_active(&self) -> bool {
            // Assuming we have access to the current block timestamp
            let current_time = stylus_sdk::block::timestamp();
            current_time < self.expiration
        }
    }
}
