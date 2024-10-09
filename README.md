# Novichain-Abstract

**Novichain-Abstract** is a chatbot-powered crypto wallet designed for abstract account wallets. This project aims to simplify the use of crypto wallets, making it easy for users to manage their digital assets without the complexities of traditional wallets. It also addresses challenges in GameFi through session keys and offers social recovery features for enhanced security.

## Vision

The vision of this project is to revolutionize crypto wallet interaction by simplifying onboarding for both newcomers and experienced users. Through a chatbot-powered system, it offers a seamless, user-friendly experience, promoting wider adoption of decentralized technologies.

## Features

- **Abstract Account Wallets**: Manage crypto assets without the need for complicated wallet setups.
- **Session Keys**: Addresses GameFi challenges by allowing session-based transactions for gaming interactions.
- **Social Recovery**: Enables users to recover their wallets through trusted social recovery mechanisms, enhancing security.
- **Gasless Transactions**: Facilitates transactions without requiring users to manage gas fees.
  
## Key Components

### 1. **Stylus-Bot**
   - A chatbot hosted on the number +2348030401593.
   - Provides a seamless interaction for users to manage their abstract wallets, send tokens, execute payments, and more.

### 2. **Stylus-Contracts**
   - Smart contracts that handle abstract account creation, session keys for gaming, social recovery, and more on the Arbitrum network using Rust and EIP-4337.

## Installation & Setup

To set up this project on your local machine, follow these steps:

### Prerequisites

- Python 3.x
- Web3.py
- Tron API
- Arbitrum SDK

### Clone the Repository

```bash
git clone https://github.com/ebenezer000/Novichain-Abstract.git
```

### Navigate to the project directory
```bash
cd Novichain-Abstract
```

### Deploy Contracts
In the Stylus-Contracts folder, you can deploy the contracts using the Arbitrum Stylus SDK for rust. Ensure you have the necessary network configurations.

### Install dependencies

In the Stylus-Bot folder, install necessary dependencies:

```bash
pip install -r requirements.txt
```

Run the Bot
To run the chatbot, execute:

```bash
python app.py
```