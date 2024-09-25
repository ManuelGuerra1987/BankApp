# Banking Web Application

## Project Description

This project is a web application developed using Django on the back-end and JavaScript on the front-end that simulates banking functionalities, allowing users to manage their accounts, make deposits and withdrawals, transfer money, and trade stocks. The application features a user-friendly interface for managing accounts in both USD and EUR, with real-time exchange rates and transaction history.

![GIF](https://github.com/ManuelGuerra1987/BankApp/blob/main/Bank.gif)

## Features

- **User Authentication:** Users can register, log in, and log out. Each user has a unique account number.
- **Account Management:** Users can view their account balance in both USD and EUR.
- **Deposit & Withdraw:** Users can deposit money into their account and withdraw funds, with validation for sufficient funds.
- **Money Transfer:** Users can transfer money to other users by entering the recipient's account number.
- **Currency Exchange:** Users can convert between USD and EUR with real-time exchange rates via exchangeratesapi
- **Stock Trading:** Users can buy and sell stocks with their account balance. The application simulates stock prices for various popular companies.
- **Transaction History:** Users can view their recent transactions, including deposits, withdrawals, transfers, and stock trades.

## Distinctiveness and Complexity

This project satisfies the distinctiveness and complexity requirements due to the following reasons:
- **Distinctiveness**: This project is very distinct in nature than the projects from the lessons. The application simulates a banking experience, providing functionalities such as deposits, withdrawals, transfers, and stock trading.
- **Complexity**: It incorporates the use of an external API for currency conversion. Also to secure sensitive information, such as the API key, the project utilizes environment variables managed through a `.env` file. This approach ensures that the API key is not hard-coded into the application, promoting better security practices.

## Code and organization

The main files and their contents in the project are as follows:

- **models.py:** Defines the `User`, `StockPortfolio`, and `Transactions` models for managing users, stock portfolios, and transaction records.
- **views.py:** Contains the view functions that handle user registration, login, logout, deposit, withdrawal, transfer, and stock trading operations.
- **urls.py:** Defines the URL patterns for the application, mapping URLs to their respective view functions.
- **templates/:** Contains HTML templates for rendering the frontend of the application, including pages for login, registration, depositing, withdrawing, transferring, and viewing stock portfolios and transaction history.
- **Static Files:** The project includes a `static` directory that contains essential JavaScript for enhancing user interactions. The JavaScript file is designed to perform the following functionalities:

1. Receiver Name Check: 
   When the user inputs a receiver's account number, the application fetches the corresponding account name from the server and displays it in real-time. 

2. EUR/USD Exchange Rate: 
   Users can retrieve the current EUR/USD exchange rate by clicking a button. The rate is displayed dynamically.

3. Stock Price Retrieval: 
   Users can input a stock symbol to fetch its current price. The application also calculates the total amount based on the number of shares the user intends to buy.


## How to Run the Application
To run the application, follow these steps:

1. **Clone the Repository**: git clone https://github.com/ManuelGuerra1987/BankApp
2. **Install requirements**: pip install -r requirements.txt
3. **Set up the database**: python manage.py migrate
4. **Run the server**: python manage.py runserver



## About

This project was submitted as the capstone project for CS50w from HarvardX.


