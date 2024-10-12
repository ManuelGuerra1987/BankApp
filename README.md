# Banking Web Application

## About

This project was submitted as the final project for CS50w from HarvardX.

## Project Description

This project is a web application developed using Django framework on the back-end and Vainilla JavaScript on the front-end that simulates banking functionalities, allowing users to manage their accounts, make deposits and withdrawals, transfer money, and trade stocks. The application features a user-friendly interface for managing accounts in both USD and EUR, with real-time exchange rates and transaction history.

![GIF](https://github.com/ManuelGuerra1987/BankApp/blob/main/Bank.gif)

## Features

- **User Authentication:** Users can register, log in, and log out. Each user has a unique account number.
- **Account Management:** Users can view their account balance in both USD and EUR.
- **Deposit & Withdraw:** Users can deposit money into their account and withdraw funds, with validation for sufficient funds.
- **Money Transfer:** Users can transfer money to other users by entering the recipient's account number.
- **Currency Exchange:** Users can convert between USD and EUR with real-time exchange rates via exchangeratesapi
- **Stock Trading:** Users can buy and sell stocks with their account balance. The application simulates stock prices for various popular companies.
- **Transaction History:** Users can view their recent transactions, including deposits, withdrawals, transfers, and stock trades.



## How to Run the Application

To run the application, follow these steps:

1. **Clone the Repository:**:
```git clone https://github.com/ManuelGuerra1987/BankApp```
2. **Install requirements:**:
```pip install -r requirements.txt```
3. **Set up the database:**:
```python manage.py migrate```
4. **Run the server:**:
```python manage.py runserver```
5. **Register in exchangeratesapi for the APIKEY:**:
```https://manage.exchangeratesapi.io```
6. **Save the APIKEY in a .env file:**
```API_KEY=yourApiKey```






