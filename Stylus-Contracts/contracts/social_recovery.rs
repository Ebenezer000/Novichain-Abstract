#[arbitrum_contract]
mod social_recovery {
    use stylus_sdk::contract::{Address};

    #[contract]
    pub struct SocialRecovery {
        owner: Address,
        guardians: Vec<Address>,
        recovery_request: Option<RecoveryRequest>,
    }

    impl SocialRecovery {
        pub fn new(owner: Address, guardians: Vec<Address>) -> Self {
            SocialRecovery {
                owner,
                guardians,
                recovery_request: None,
            }
        }

        pub fn request_recovery(&mut self, new_owner: Address) {
            let request = RecoveryRequest {
                new_owner,
                approvals: 0,
                is_active: true,
            };
            self.recovery_request = Some(request);
        }

        pub fn approve_recovery(&mut self, guardian: Address) -> bool {
            if let Some(ref mut request) = self.recovery_request {
                if self.guardians.contains(&guardian) && request.is_active {
                    request.approvals += 1;
                    if request.approvals >= self.guardians.len() / 2 + 1 {
                        self.owner = request.new_owner;
                        request.is_active = false;
                    }
                    return true;
                }
            }
            false
        }

        pub fn cancel_recovery(&mut self) {
            if let Some(ref mut request) = self.recovery_request {
                request.is_active = false;
            }
        }
    }

    // Define a struct for tracking the recovery request
    pub struct RecoveryRequest {
        pub new_owner: Address,
        pub approvals: u64,
        pub is_active: bool,
    }
}
