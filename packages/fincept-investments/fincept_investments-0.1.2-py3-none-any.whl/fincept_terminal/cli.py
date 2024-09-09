import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from .market import show_market_tracker_menu
from .data_fetcher import fetch_sectors_by_country, fetch_industries_by_sector, fetch_stocks_by_industry, display_fii_dii_data
from .assets import search_assets
from .data import get_countries_by_continent
from .themes import console
import yfinance as yf
from fuzzywuzzy import process 
import datetime
import time
from empyrical import (
    aggregate_returns, alpha, alpha_beta, alpha_beta_aligned, annual_return,
    annual_volatility, beta, beta_aligned, cum_returns, cum_returns_final,
    downside_risk, excess_sharpe, max_drawdown, omega_ratio, sharpe_ratio,
    sortino_ratio, tail_ratio, value_at_risk, calmar_ratio, conditional_value_at_risk
)
from empyrical.perf_attrib import perf_attrib
from empyrical.utils import get_fama_french
import requests
import matplotlib.pyplot as plt
import json
import vectorbt as vbt
import os
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

     
@click.group(invoke_without_command=True)
@click.version_option(version="0.1.2", prog_name="Fincept Investments")
@click.pass_context
def cli(ctx):
    """Fincept Investments CLI - Your professional financial terminal."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())  # Display help if no command is given

# Start Command
@cli.command()
def start():
    """Start the Fincept Investments terminal"""
    from .display import display_art
    display_art()
    show_main_menu()
    

def show_main_menu():
    """Main menu with navigation options."""
    console.print("\n")
    console.print("[bold cyan]MAIN MENU[/bold cyan]\n", style="info")
    
    main_menu_options = [
        "MARKET TRACKER", #1 
        "ECONOMICS & MACRO TRENDS", #2
        "NEWS & ANALYSIS", #3
        "STOCKS (Equities)", #4
        "FUNDS & ETFs", #5
        "BONDS & FIXED INCOME", #6
        "OPTIONS & DERIVATIVES", #7
        "CRYPTOCURRENCIES", #8
        "PORTFOLIO & INVESTMENT TOOLS", #9
        "CURRENCY MARKETS (Forex)", #10
        "COMMODITIES", #11
        "BACKTESTING STOCKS", #12
        "GenAI Query", #13
        "EDUCATION & RESOURCES", #14
        "SETTINGS & CUSTOMIZATION", #15
        "Terminal Documentation", #16
        "EXIT", #17
    ]

    # Display main menu in columns
    display_in_columns("Select an Option", main_menu_options)

    console.print("\n")
    choice = Prompt.ask("Enter your choice")
    console.print("\n")

    if choice == "1":
        show_market_tracker_menu()  # Market Tracker submenu
    elif choice == "2":
        console.print("[bold yellow]Economics section under development[/bold yellow]", style="warning")
    elif choice == "3":
        console.print("[bold yellow]News section under development[/bold yellow]", style="warning")
    elif choice == "4":
        show_equities_menu()  # Equities submenu for continent and country selection
    elif choice == "5":
        console.print("[bold yellow]Funds section under development[/bold yellow]", style="warning")
    elif choice == "6":
        console.print("[bold yellow]Bonds section under development[/bold yellow]", style="warning")
    elif choice == "7":
        console.print("[bold red]Exiting the Fincept terminal...[/bold red]", style="danger")
    elif choice == "9":
        show_portfolio_menu()
    elif choice == "12":
        show_backtesting_menu() 
    elif choice == "13":  # GenAI Query option
        show_genai_query()

        
PORTFOLIO_FILE = "portfolios.json"

def save_portfolios():
    """Save the portfolios to a JSON file."""
    serializable_portfolios = {name: [stock.info['symbol'] for stock in stocks] for name, stocks in portfolios.items()}
    
    with open(PORTFOLIO_FILE, "w") as file:
        json.dump(serializable_portfolios, file)
    
    console.print("[bold green]Portfolios saved successfully![/bold green]")

def load_portfolios():
    """Load portfolios from a JSON file if it exists and is valid."""
    if os.path.exists(PORTFOLIO_FILE):
        try:
            with open(PORTFOLIO_FILE, "r") as file:
                saved_portfolios = json.load(file)
                # Recreate portfolios with Ticker objects from the saved stock symbols
                return {name: [yf.Ticker(symbol) for symbol in stocks] for name, stocks in saved_portfolios.items()}
        except (json.JSONDecodeError, ValueError):
            console.print("[bold red]Error: The portfolio file is corrupted or empty. Starting with an empty portfolio.[/bold red]")
            return {}  # Return an empty dictionary if the JSON is invalid or corrupted
    return {}

# Load the portfolios at startup
portfolios = load_portfolios()

def show_portfolio_menu():
    """Portfolio menu with options to create, modify, delete, and manage portfolios."""
    while True:
        console.print("[bold cyan]PORTFOLIO MENU[/bold cyan]")
        menu_options = [
            "CREATE NEW PORTFOLIO",
            "SELECT AND MANAGE EXISTING PORTFOLIO",
            "VIEW ALL PORTFOLIOS",
            "MODIFY PORTFOLIO NAME",
            "DELETE PORTFOLIO",
            "BACK TO MAIN MENU"
        ]
        display_in_columns("Select an Option", menu_options)
        
        choice = Prompt.ask("Enter your choice")
        
        if choice == "1":
            create_new_portfolio()
        elif choice == "2":
            select_portfolio_to_manage()  # New function to select and manage portfolio
        elif choice == "3":
            console.print(list(portfolios.keys()))
        elif choice == "4":
            modify_portfolio_name()
        elif choice == "5":
            delete_portfolio()
        elif choice == "6":
            show_main_menu()
            return  # Exit to main menu
        else:
            console.print("[bold red]Invalid choice, please select a valid option.[/bold red]")

def select_portfolio_to_manage():
    """Display all portfolios and allow the user to select and manage one."""
    if not portfolios:
        console.print("[bold red]No portfolios available. Create a portfolio first.[/bold red]")
        return

    console.print("[bold cyan]Select an existing portfolio to manage:[/bold cyan]\n")
    portfolio_names = list(portfolios.keys())
    display_in_columns("Available Portfolios", portfolio_names)

    portfolio_choice = Prompt.ask("Enter the portfolio number to select")
    
    try:
        selected_portfolio_name = portfolio_names[int(portfolio_choice) - 1]
        country = Prompt.ask("Enter the country for this portfolio")
        manage_selected_portfolio(selected_portfolio_name, country)  # Pass the selected portfolio for management
    except (ValueError, IndexError):
        console.print("[bold red]Invalid choice, please select a valid portfolio number.[/bold red]")

def create_new_portfolio():
    """Create a new portfolio and manage it."""
    portfolio_name = Prompt.ask("Enter the new portfolio name")
    
    # Ask the user to input the country for the portfolio
    country = Prompt.ask("Enter the country for this portfolio (e.g., India, United States, etc.)")
    
    portfolios[portfolio_name] = []  # Initialize an empty portfolio
    console.print(f"Portfolio '{portfolio_name}' created successfully!")
    
    # Automatically go to manage the newly created portfolio
    manage_selected_portfolio(portfolio_name, country)


def select_portfolio():
    """Allow users to select an existing portfolio for adding stocks or analysis."""
    if not portfolios:
        console.print("[bold red]No portfolios available. Create a portfolio first.[/bold red]")
        return

    console.print("[bold cyan]Select an existing portfolio:[/bold cyan]\n")
    portfolio_names = list(portfolios.keys())
    display_in_columns("Available Portfolios", portfolio_names)

    portfolio_choice = Prompt.ask("Enter the portfolio number to select")
    selected_portfolio_name = portfolio_names[int(portfolio_choice) - 1]

    manage_selected_portfolio(selected_portfolio_name)


def manage_selected_portfolio(portfolio_name, country):
    """Manage the selected portfolio."""
    while True:
        console.print(f"\n[bold cyan]MANAGE PORTFOLIO: {portfolio_name}[/bold cyan]")
        manage_menu = [
            "ADD STOCK TO PORTFOLIO",
            "VIEW CURRENT PORTFOLIO",
            "ANALYZE PORTFOLIO PERFORMANCE",
            "BACKTEST PORTFOLIO",  # New option for backtesting
            "BACK TO PREVIOUS MENU"
        ]
        
        display_in_columns(f"Portfolio: {portfolio_name}", manage_menu)
        choice = Prompt.ask("Enter your choice")

        if choice == "1":
            add_stock_to_portfolio(portfolio_name)
        elif choice == "2":
            view_portfolio(portfolio_name)
        elif choice == "3":
            analyze_portfolio(portfolio_name, country)  # Pass both portfolio_name and country
        elif choice == "4":
            backtest_portfolio(portfolio_name)  # Call the backtest function here
        elif choice == "5":
            return  # Go back to the previous menu
        else:
            console.print("[bold red]Invalid choice, please select a valid option.[/bold red]")


def add_stock_to_portfolio(portfolio_name=None):
    """Allow users to add multiple stocks to the selected portfolio until they choose to return."""
    if portfolio_name is None:
        # Ask the user to select a portfolio if none provided
        if not portfolios:
            console.print("[bold red]No portfolios available. Please create a portfolio first.[/bold red]")
            return
        
        # Display available portfolios for selection
        portfolio_names = list(portfolios.keys())
        display_in_columns("Select a Portfolio", portfolio_names)
        portfolio_choice = Prompt.ask("Enter the portfolio number to select")
        portfolio_name = portfolio_names[int(portfolio_choice) - 1]
    
    while True:
        # Ask the user for a stock symbol
        ticker = Prompt.ask("Enter the stock symbol (or type 'back' to return to the portfolio menu)")
        if ticker.lower() == 'back':
            break  # Exit the loop and return to the portfolio menu
        
        try:
            # Create a yfinance.Ticker object from the symbol
            stock = yf.Ticker(ticker)
            stock_info = stock.history(period="1y")  # Fetch 1-year historical data
            
            if not stock_info.empty:
                # Add the Ticker object to the portfolio
                portfolios[portfolio_name].append(stock)
                console.print(f"[bold green]{ticker} added to portfolio '{portfolio_name}'![/bold green]")
            else:
                console.print(f"[bold red]No data found for {ticker}.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]")


def view_portfolio(portfolio_name):
    """Display the current portfolio."""
    portfolio = portfolios.get(portfolio_name, [])
    
    if not portfolio:
        console.print(f"[bold red]Portfolio '{portfolio_name}' is empty.[/bold red]")
        return

    table = Table(title=f"Portfolio: {portfolio_name}", header_style="bold", show_lines=True)
    table.add_column("Symbol", style="cyan", width=15)
    table.add_column("Name", style="green", width=50)
    
    for stock in portfolio:
        stock_info = stock.info
        table.add_row(stock_info.get('symbol', 'N/A'), stock_info.get('shortName', 'N/A'))

    console.print(table)


# Comprehensive list of stock exchanges by country
MARKET_INDEX_MAP = {
    "Afghanistan": None,  # No major stock exchange
    "Anguilla": None,  # No major stock exchange
    "Argentina": "^MERV",  # MERVAL Index
    "Australia": "^AXJO",  # ASX 200
    "Austria": "^ATX",  # Austrian Traded Index (ATX)
    "Azerbaijan": None,  # No major stock exchange
    "Bahamas": None,  # No major stock exchange
    "Bangladesh": "^DSEX",  # DSEX Index
    "Barbados": None,  # No major stock exchange
    "Belgium": "^BFX",  # BEL 20 Index
    "Belize": None,  # No major stock exchange
    "Bermuda": None,  # Bermuda Stock Exchange (BSX)
    "Botswana": None,  # Botswana Stock Exchange
    "Brazil": "^BVSP",  # Bovespa Index
    "British Virgin Islands": None,  # No major stock exchange
    "Cambodia": None,  # Cambodia Securities Exchange (CSX)
    "Canada": "^GSPTSE",  # S&P/TSX Composite Index
    "Cayman Islands": None,  # No major stock exchange
    "Chile": "^IPSA",  # Santiago Stock Exchange (IPSA)
    "China": "^SSEC",  # Shanghai Composite Index
    "Colombia": "^COLCAP",  # COLCAP Index
    "Costa Rica": None,  # No major stock exchange
    "Cyprus": None,  # Cyprus Stock Exchange (CSE)
    "Czech Republic": "^PX",  # PX Index (Prague)
    "Denmark": "^OMXC25",  # OMX Copenhagen 25
    "Dominican Republic": None,  # No major stock exchange
    "Egypt": "^EGX30",  # EGX 30 Index
    "Estonia": None,  # Tallinn Stock Exchange
    "Falkland Islands": None,  # No major stock exchange
    "Finland": "^OMXH25",  # OMX Helsinki 25
    "France": "^FCHI",  # CAC 40 Index
    "French Guiana": None,  # No major stock exchange
    "Gabon": None,  # No major stock exchange
    "Georgia": None,  # Georgian Stock Exchange (GSE)
    "Germany": "^GDAXI",  # DAX Index
    "Ghana": None,  # Ghana Stock Exchange
    "Gibraltar": None,  # No major stock exchange
    "Greece": "^ATG",  # Athens General Composite Index
    "Greenland": None,  # No major stock exchange
    "Guernsey": None,  # No major stock exchange
    "Hong Kong": "^HSI",  # Hang Seng Index
    "Hungary": "^BUX",  # BUX Index (Budapest)
    "Iceland": None,  # Iceland Stock Exchange (OMX Iceland)
    "India": "^NSEI",  # Nifty 50 (NSE)
    "Indonesia": "^JKSE",  # Jakarta Composite Index
    "Ireland": "^ISEQ",  # Irish Stock Exchange Overall Index
    "Isle of Man": None,  # No major stock exchange
    "Israel": "^TA125",  # TA-125 Index (Tel Aviv)
    "Italy": "^FTMIB",  # FTSE MIB Index
    "Ivory Coast": None,  # No major stock exchange
    "Japan": "^N225",  # Nikkei 225
    "Jersey": None,  # No major stock exchange
    "Jordan": None,  # Amman Stock Exchange (ASE)
    "Kazakhstan": None,  # Kazakhstan Stock Exchange (KASE)
    "Kenya": "^NSE20",  # Nairobi Securities Exchange 20 Share Index
    "Kyrgyzstan": None,  # Kyrgyz Stock Exchange
    "Latvia": None,  # Nasdaq Riga
    "Liechtenstein": None,  # No major stock exchange
    "Lithuania": None,  # Nasdaq Vilnius
    "Luxembourg": None,  # Luxembourg Stock Exchange
    "Macau": None,  # No major stock exchange
    "Macedonia": None,  # Macedonian Stock Exchange
    "Malaysia": "^KLSE",  # FTSE Bursa Malaysia KLCI
    "Malta": None,  # Malta Stock Exchange (MSE)
    "Mauritius": None,  # Stock Exchange of Mauritius
    "Mexico": "^MXX",  # IPC (Indice de Precios y Cotizaciones)
    "Monaco": None,  # No major stock exchange
    "Mongolia": None,  # Mongolian Stock Exchange (MSE)
    "Montenegro": None,  # Montenegro Stock Exchange
    "Morocco": "^MASI",  # Moroccan All Shares Index
    "Mozambique": None,  # No major stock exchange
    "Myanmar": None,  # Yangon Stock Exchange (YSX)
    "Namibia": None,  # Namibia Stock Exchange (NSX)
    "Netherlands": "^AEX",  # AEX Index
    "Netherlands Antilles": None,  # No major stock exchange
    "New Zealand": "^NZ50",  # S&P/NZX 50 Index
    "Nigeria": None,  # Nigerian Stock Exchange
    "Norway": "^OBX",  # OBX Total Return Index
    "Panama": None,  # Panama Stock Exchange
    "Papua New Guinea": None,  # Port Moresby Stock Exchange
    "Peru": "^SPBLPGPT",  # S&P Lima General Total Return Index
    "Philippines": "^PSEI",  # PSEi Composite Index
    "Poland": "^WIG20",  # WIG20 Index (Warsaw)
    "Portugal": "^PSI20",  # PSI-20 Index
    "Qatar": "^QSI",  # QE Index (Qatar Exchange)
    "Reunion": None,  # No major stock exchange
    "Romania": "^BETI",  # BET Index (Bucharest)
    "Russia": "^IMOEX",  # MOEX Russia Index
    "Saudi Arabia": "^TASI",  # Tadawul All Share Index (TASI)
    "Senegal": None,  # Regional Securities Exchange (BRVM)
    "Singapore": "^STI",  # Straits Times Index (STI)
    "Slovakia": None,  # Bratislava Stock Exchange
    "Slovenia": None,  # Ljubljana Stock Exchange (SBITOP)
    "South Africa": "^JTOPI",  # JSE Top 40 Index
    "South Korea": "^KS11",  # KOSPI Composite Index
    "Spain": "^IBEX",  # IBEX 35 Index
    "Suriname": None,  # No major stock exchange
    "Sweden": "^OMXS30",  # OMX Stockholm 30
    "Switzerland": "^SSMI",  # Swiss Market Index (SMI)
    "Taiwan": "^TWII",  # Taiwan Weighted Index
    "Tanzania": None,  # Dar es Salaam Stock Exchange
    "Thailand": "^SET50",  # SET50 Index
    "Turkey": "XU100.IS",  # BIST 100 Index
    "Ukraine": None,  # PFTS Stock Exchange
    "United Arab Emirates": "^ADX",  # Abu Dhabi Securities Exchange General Index
    "United Kingdom": "^FTSE",  # FTSE 100 Index
    "United States": "^GSPC",  # S&P 500 Index
    "Uruguay": None,  # No major stock exchange
    "Vietnam": "^VNINDEX",  # Vietnam Ho Chi Minh Stock Index
    "Zambia": None,  # Lusaka Stock Exchange (LuSE)
}

def detect_market_index(stock_symbol, country):
    """Detect the appropriate market index based on the stock's country or exchange."""
    market_index = MARKET_INDEX_MAP.get(country, None)
    
    if market_index:
        return market_index  # Return the market index if available for the country
    else:
        # If no market index is available, prompt the user for input
        console.print(f"[bold yellow]No default market index found for {country}. Please enter a valid market index:[/bold yellow]")
        index = Prompt.ask("Enter the index symbol (e.g., ^NSEI for Nifty 50)", default="^NSEI")
        return index  # If the user doesn't enter anything, use ^NSEI as the default

    
def analyze_portfolio(portfolio_name, country):
    """Analyze portfolio performance with dynamic market index selection."""
    portfolio = portfolios.get(portfolio_name, [])

    if not portfolio:
        console.print(f"[bold red]Portfolio '{portfolio_name}' is empty.[/bold red]")
        return

    portfolio_returns = pd.DataFrame()
    
    results = {}  # To store analysis results for export

    # Collect returns for each stock in the portfolio
    for stock in portfolio:
        ticker = stock.info['symbol']
        stock_history = stock.history(period="1y")['Close']  # Get the stock's closing prices
        stock_returns = stock_history.pct_change().dropna()  # Calculate daily returns
        portfolio_returns[ticker] = stock_returns

    try:
        mean_returns = portfolio_returns.mean(axis=1)
        
        # Compute key metrics
        cumulative_returns = cum_returns(mean_returns)
        cumulative_returns_final = cum_returns_final(mean_returns)
        annual_vol = annual_volatility(mean_returns)
        sharpe = sharpe_ratio(mean_returns)
        max_dd = max_drawdown(mean_returns)
        calmar = calmar_ratio(mean_returns)
        sortino = sortino_ratio(mean_returns)
        omega = omega_ratio(mean_returns)
        downside = downside_risk(mean_returns)
        tail = tail_ratio(mean_returns)
        var = value_at_risk(mean_returns)
        cvar = conditional_value_at_risk(mean_returns)
        ann_return = annual_return(mean_returns)
        monthly_returns = aggregate_returns(mean_returns, convert_to='monthly')

        # Get the market index dynamically based on the country
        market_index = detect_market_index(portfolio[0].info['symbol'], country)

        # Fetch market returns from the detected index
        market_ticker = yf.Ticker(market_index)
        market_history = market_ticker.history(period="1y")['Close'].pct_change().dropna()

        # Align the dates of market returns and portfolio returns
        aligned_returns = pd.concat([mean_returns, market_history], axis=1).dropna()
        aligned_portfolio_returns = aligned_returns.iloc[:, 0]
        aligned_market_returns = aligned_returns.iloc[:, 1]

        # Alpha and Beta
        alpha_value, beta_value = alpha_beta_aligned(aligned_portfolio_returns, aligned_market_returns)
        alpha_standalone = alpha(aligned_portfolio_returns, aligned_market_returns)
        beta_standalone = beta(aligned_portfolio_returns, aligned_market_returns)
        excess_sharpe_value = excess_sharpe(aligned_portfolio_returns, aligned_market_returns)

        # Store results in dictionary for export
        results.update({
            "Cumulative Returns": f"{cumulative_returns[-1]:.2%}",
            "Cumulative Returns Final": f"{cumulative_returns_final:.2%}",
            "Annual Return": f"{ann_return:.2%}",
            "Monthly Aggregated Returns": f"{monthly_returns.mean():.2%}",
            "Annual Volatility": f"{annual_vol:.2%}",
            "Sharpe Ratio": f"{sharpe:.2f}",
            "Max Drawdown": f"{max_dd:.2%}",
            "Calmar Ratio": f"{calmar:.2f}",
            "Sortino Ratio": f"{sortino:.2f}",
            "Omega Ratio": f"{omega:.2f}",
            "Downside Risk": f"{downside:.2%}",
            "Tail Ratio": f"{tail:.2f}",
            "Value at Risk (VaR)": f"{var:.2%}",
            "Conditional VaR (CVaR)": f"{cvar:.2%}",
            "Alpha (Standalone)": f"{alpha_standalone:.2f}",
            "Beta (Standalone)": f"{beta_standalone:.2f}",
            "Alpha (Aligned)": f"{alpha_value:.2f}",
            "Beta (Aligned)": f"{beta_value:.2f}",
            "Excess Sharpe": f"{excess_sharpe_value:.2f}"
        })

        # Display the analysis
        analysis_table = Table(title=f"Portfolio Performance Analysis: {portfolio_name}", header_style="bold", show_lines=True)
        analysis_table.add_column("Metric", style="cyan")
        analysis_table.add_column("Value", style="green")

        # Add the metrics to the table
        for metric, value in results.items():
            analysis_table.add_row(metric, value)

        console.print(analysis_table)

        # Export the analysis
        export_portfolio_results(results, portfolio_name)

    except Exception as e:
        console.print(f"[bold red]Error in analyzing portfolio: {e}[/bold red]")

        
def view_all_portfolios():
    """Display a list of all existing portfolios."""
    if not portfolios:
        console.print("[bold red]No portfolios available. Create a portfolio first.[/bold red]")
        return
    
    table = Table(title="All Portfolios", header_style="bold", show_lines=True)
    table.add_column("Portfolio Name", style="cyan", width=30)
    table.add_column("Number of Stocks", style="green", width=20)
    
    for portfolio_name, stocks in portfolios.items():
        table.add_row(portfolio_name, str(len(stocks)))

    console.print(table)
    
def modify_portfolio_name():
    """Modify the name of an existing portfolio."""
    portfolio_name = Prompt.ask("Enter the portfolio name you want to modify")
    
    if portfolio_name not in portfolios:
        console.print(f"[bold red]Portfolio '{portfolio_name}' does not exist.[/bold red]")
        return
    
    new_name = Prompt.ask("Enter the new portfolio name")
    portfolios[new_name] = portfolios.pop(portfolio_name)  # Rename the portfolio
    console.print(f"Portfolio '{portfolio_name}' renamed to '{new_name}' successfully!")
    save_portfolios()  # Save the changes


def delete_portfolio():
    """Delete an existing portfolio."""
    portfolio_name = Prompt.ask("Enter the portfolio name you want to delete")
    
    if portfolio_name not in portfolios:
        console.print(f"[bold red]Portfolio '{portfolio_name}' does not exist.[/bold red]")
        return
    
    confirm = Prompt.ask(f"Are you sure you want to delete the portfolio '{portfolio_name}'? (yes/no)", default="no")
    
    if confirm.lower() == "yes":
        portfolios.pop(portfolio_name)
        console.print(f"Portfolio '{portfolio_name}' deleted successfully!")
        save_portfolios()  # Save the changes


def export_portfolio_results(results, portfolio_name):
    """Export portfolio results to CSV or Excel."""
    choice = Prompt.ask("Do you want to export the results? (yes/no)", default="no")
    
    if choice.lower() == "yes":
        export_format = Prompt.ask("Choose export format: CSV or Excel", choices=["csv", "excel"], default="csv")
        file_name = f"{portfolio_name}_analysis.{export_format}"
        
        df = pd.DataFrame.from_dict(results, orient='index', columns=["Value"])
        
        try:
            if export_format == "csv":
                df.to_csv(file_name, index_label="Metric")
            elif export_format == "excel":
                df.to_excel(file_name, index_label="Metric")
            console.print(f"[bold green]Portfolio analysis exported to {file_name} successfully![/bold green]")
        except Exception as e:
            console.print(f"[bold red]Failed to export data: {e}[/bold red]")

def export_backtest_results(pf, portfolio_name):
    """Export backtest results to CSV or Excel."""
    choice = Prompt.ask("Do you want to export the backtest results? (yes/no)", default="no")
    
    if choice.lower() == "yes":
        export_format = Prompt.ask("Choose export format: CSV or Excel", choices=["csv", "excel"], default="csv")
        file_name = f"{portfolio_name}_backtest_results.{export_format}"
        
        df = pf.to_dataframe()
        
        try:
            if export_format == "csv":
                df.to_csv(file_name, index=True)
            elif export_format == "excel":
                df.to_excel(file_name, index=True)
            console.print(f"[bold green]Backtest results exported to {file_name} successfully![/bold green]")
        except Exception as e:
            console.print(f"[bold red]Failed to export data: {e}[/bold red]")


def backtest_portfolio(portfolio_name):
    """Perform a backtest on the entire portfolio by combining all stock prices."""
    portfolio = portfolios.get(portfolio_name, [])
    
    if not portfolio:
        console.print(f"[bold red]Portfolio '{portfolio_name}' is empty.[/bold red]")
        return

    portfolio_returns = pd.DataFrame()

    # Collect historical data for each stock and combine returns into a single DataFrame
    for stock in portfolio:
        ticker = stock.info['symbol']
        stock_history = stock.history(period="1y")['Close']  # Get stock prices for 1 year
        
        if stock_history.empty:
            console.print(f"[bold red]No data available for {ticker}.[/bold red]")
            continue
        
        stock_history = stock_history.asfreq('D').fillna(method='ffill')  # Forward fill missing data
        portfolio_returns[ticker] = stock_history.pct_change().dropna()  # Calculate daily returns
    
    # Check if there are enough stocks in the portfolio
    if portfolio_returns.empty:
        console.print(f"[bold red]No valid stock data found in the portfolio '{portfolio_name}'[/bold red]")
        return

    # Create a portfolio-wide return series by averaging individual returns (or weighting them if needed)
    portfolio_returns['Portfolio'] = portfolio_returns.mean(axis=1)

    console.print(f"\nGenerating backtest charts for {portfolio_name} (combined portfolio)...")

    try:
        # Use vectorbt to run the backtest on the combined portfolio
        pf = vbt.Portfolio.from_holding(portfolio_returns['Portfolio'], freq='D')  # Set frequency to daily (D)

        # Plot the backtest charts for the entire portfolio
        pf.plot().show()

        # Display portfolio-wide performance metrics in table format
        display_backtest_metrics(pf, portfolio_name)
        
    except Exception as e:
        console.print(f"[bold red]Error in backtesting portfolio: {e}[/bold red]")


def display_backtest_metrics(pf, portfolio_name):
    """Display backtest performance metrics in a table for the entire portfolio."""
    console.print(f"\nBacktesting results for {portfolio_name}")
    
    # Create a rich table to display the backtest metrics
    table = Table(title=f"Backtest Performance for {portfolio_name}", header_style="bold", show_lines=True)
    table.add_column("Metric", style="cyan", justify="left")
    table.add_column("Value", style="green", justify="right")

    # Add the metrics to the table, handling both Series and scalar values
    try:
        total_return = pf.total_return() if not isinstance(pf.total_return(), pd.Series) else pf.total_return().iloc[-1]
        annualized_return = pf.annualized_return() if not isinstance(pf.annualized_return(), pd.Series) else pf.annualized_return().iloc[-1]
        max_drawdown = pf.max_drawdown() if not isinstance(pf.max_drawdown(), pd.Series) else pf.max_drawdown().iloc[-1]
        sharpe_ratio = pf.sharpe_ratio() if not isinstance(pf.sharpe_ratio(), pd.Series) else pf.sharpe_ratio().iloc[-1]
        sortino_ratio = pf.sortino_ratio() if not isinstance(pf.sortino_ratio(), pd.Series) else pf.sortino_ratio().iloc[-1]

        # Add the metrics to the table
        table.add_row("Total Return", f"{total_return:.2%}")
        table.add_row("Annualized Return", f"{annualized_return:.2%}" if not pd.isna(annualized_return) else "nan")
        table.add_row("Max Drawdown", f"{max_drawdown:.2%}" if not pd.isna(max_drawdown) else "nan")
        table.add_row("Sharpe Ratio", f"{sharpe_ratio:.2f}" if not pd.isna(sharpe_ratio) else "nan")
        table.add_row("Sortino Ratio", f"{sortino_ratio:.2f}" if not pd.isna(sortino_ratio) else "nan")
    
    except Exception as e:
        console.print(f"[bold red]Error in calculating metrics: {e}[/bold red]")
    
    console.print(table)

def show_backtesting_menu():
    """Backtesting menu where users can run backtests on their portfolios."""
    console.print("[bold cyan]BACKTESTING MENU[/bold cyan]\n", style="info")
    console.print("1. Backtest Portfolio\n2. Back to Main Menu")
    
    choice = Prompt.ask("Enter your choice")

    if choice == "1":
        portfolio_name = Prompt.ask("Enter the portfolio name to backtest")
        if portfolio_name not in portfolios:
            console.print(f"[bold red]Portfolio '{portfolio_name}' not found![/bold red]")
            return
        
        # Perform backtest
        backtest_portfolio(portfolio_name)
    elif choice == "2":
        return  # Go back to the main menu        



# Equities submenu
def show_equities_menu():
    """Equities submenu that allows selection of stocks based on continent and country."""
    continents = ["Asia", "Europe", "Africa", "North America", "South America", "Oceania", "Middle East", "Main Menu"]

    while True:
        console.print("[bold cyan]EQUITIES MENU[/bold cyan]\n", style="info")
        display_in_columns("Select a Continent", continents)
        
        console.print("\n")
        choice = Prompt.ask("Enter your choice")
        console.print("\n")
        
        if choice == "8":
            show_main_menu()
            return  # Exit equities menu and return to main menu

        selected_continent = continents[int(choice) - 1]

        # If country/sector fetching fails, return to the continent selection
        if not show_country_menu(selected_continent):
            continue  # Loop back to continent selection if no valid data is found
        
def genai_query(user_input):
    """
    Send the user's query to the GenAI API and return the response.
    
    Parameters:
    user_input (str): The query/question entered by the user.
    
    Returns:
    str: The formatted response from the GenAI API.
    """
    api_url = "https://fincept.share.zrok.io/process-gemini/"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "user_input": user_input
    }

    try:
        # Send POST request
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Check for HTTP errors
        
        # Parse the JSON response and extract the 'gemini_response'
        api_response = response.json()
        raw_text = api_response.get("gemini_response", "No response received from the server.")
        
        # Handle any Markdown-like syntax and format the text dynamically
        formatted_response = format_genai_response(raw_text)
        return formatted_response
    
    except requests.exceptions.RequestException as e:
        return f"Error processing query: {str(e)}"


def format_genai_response(response):
    """
    Dynamically format the response text: remove unnecessary symbols, handle Markdown-like syntax, and apply styling.
    
    Parameters:
    response (str): The raw response text from the API.
    
    Returns:
    Text: A Rich Text object with formatted response.
    """
    # Remove Markdown-like symbols (e.g., **, ##) and apply rich formatting
    response = response.replace("**", "").replace("##", "").strip()

    # Create a Rich Text object with cyan color and bold style
    formatted_text = Text(response, style="bold cyan")

    return formatted_text


def show_genai_query():
    """Prompt the user for a finance-related query and send it to the GenAI API."""
    console.print("[bold cyan]GENAI QUERY[/bold cyan]\n", style="info")

    while True:
        query = Prompt.ask("Enter your finance-related query (or type 'back' to return to main menu)")

        if query.lower() == 'back':
            return  # Exit back to the main menu if user types 'back'

        # Send the query to the GenAI API
        console.print("\n[bold yellow]Processing your query...[/bold yellow]\n", style="info")
        response = genai_query(query)

        # Display the formatted response in a panel
        console.print(Panel(response, title="GenAI Query Response", style="cyan on #282828"))

        # Ask if the user wants to make another query
        another_query = Prompt.ask("\nWould you like to make another query? (yes/no)")

        if another_query.lower() == 'no':
            console.print("\n[bold yellow]Redirecting to the main menu...[/bold yellow]", style="info")
            show_main_menu()
            return  # Redirect back to the main menu if user types 'no'

def show_country_menu(continent):
    """Display available countries for a given continent and allow the user to select one."""
    countries = get_countries_by_continent(continent)

    if not countries:
        console.print(f"[bold red]No countries available for {continent}[/bold red]", style="danger")
        return

    console.print(f"[bold cyan]Countries in {continent}[/bold cyan]\n", style="info")
    display_in_columns(f"Select a Country in {continent}", countries)
    
    console.print("\n")
    choice = Prompt.ask("Enter your choice")
    selected_country = countries[int(choice) - 1]
    console.print("\n")
    
    show_sectors_in_country(selected_country)
    
def show_country_menu(continent):
    """Display available countries for a given continent and allow the user to select one."""
    countries = get_countries_by_continent(continent)

    if not countries:
        console.print(f"[bold red]No countries available for {continent}[/bold red]", style="danger")
        return False  # Indicate that there are no countries and return to the main menu

    console.print(f"[bold cyan]Countries in {continent}[/bold cyan]\n", style="info")
    display_in_columns(f"Select a Country in {continent}", countries)
    
    console.print("\n")
    choice = Prompt.ask("Enter your choice")
    selected_country = countries[int(choice) - 1]
    console.print("\n")
    
    # Check if sectors are available, otherwise return to country menu
    return show_sectors_in_country(selected_country)

def fetch_sectors_with_retry(country, max_retries=3, retry_delay=2):
    """Fetch sectors with retry logic."""
    sectors_url = f"https://fincept.share.zrok.io/FinanceDB/equities/sectors_and_industries_and_stocks?filter_column=country&filter_value={country}"
    
    retries = 0
    while retries < max_retries:
        try:
            # Simulate fetching sectors (replace this with actual request logic)
            response = requests.get(sectors_url)
            response.raise_for_status()
            sectors = response.json().get('sectors', [])
            return sectors
        except requests.exceptions.RequestException:
            retries += 1
            time.sleep(retry_delay)  # Wait before retrying
            if retries >= max_retries:
                return None  # Return None after max retries


def show_sectors_in_country(country):
    """Fetch sectors for the selected country and allow the user to select one."""
    console.print(f"[bold cyan]Fetching sectors for {country}...[/bold cyan]\n", style="info")
    
    # Fetch sectors with retries
    sectors = fetch_sectors_with_retry(country)
    
    if not sectors:
        # Display user-friendly error after retries
        console.print(f"[bold red]Data temporarily unavailable for {country}. Redirecting to the main menu...[/bold red]", style="danger")
        return False  # Indicate failure to fetch sectors, return to main menu

    console.print(f"[bold cyan]Sectors in {country}[/bold cyan]\n", style="info")
    display_in_columns(f"Select a Sector in {country}", sectors)

    console.print("\n")
    choice = Prompt.ask("Enter your choice")
    selected_sector = sectors[int(choice) - 1]

    show_industries_in_sector(country, selected_sector)
    return True  # Continue normally if sectors were fetched successfully

def show_industries_in_sector(country, sector):
    """Fetch industries for the selected sector and allow the user to select one."""
    industries = fetch_industries_by_sector(country, sector)

    if not industries:
        console.print(f"[bold red]No industries available for {sector} in {country}.[/bold red]", style="danger")
        return

    console.print(f"[bold cyan]Industries in {sector}, {country}[/bold cyan]\n", style="info")
    display_in_columns(f"Select an Industry in {sector}", industries)
    
    choice = Prompt.ask("Enter your choice")
    selected_industry = industries[int(choice) - 1]

    show_stocks_in_industry(country, sector, selected_industry)
    
# After displaying the stocks, ask the user if they want to search more information
def show_stocks_in_industry(country, sector, industry):
    """Display stocks available in the selected industry."""
    stock_data = fetch_stocks_by_industry(country, sector, industry)

    if stock_data.empty:
        console.print(f"[bold red]No stocks available for {industry} in {sector}, {country}.[/bold red]", style="danger")
    else:
        display_equities(stock_data)

        while True:
            console.print("\n")
            choice = Prompt.ask("Would you like to search for more information on a specific stock? (yes/no)")
            if choice.lower() == 'yes':
                ticker_name = Prompt.ask("Please enter the stock symbol or company name (partial or full)")
                closest_ticker = find_closest_ticker(ticker_name, stock_data)
                if closest_ticker:
                    display_stock_info(closest_ticker)
                else:
                    console.print(f"[bold red]No matching ticker found for '{ticker_name}'.[/bold red]", style="danger")
            else:
                return  # Return to the previous menu instead of directly to the main menu

def find_closest_ticker(user_input, stock_data):
    """Find the closest matching ticker or company name from the displayed stocks."""
    stock_symbols = stock_data['symbol'].tolist()
    stock_names = stock_data['name'].tolist()

    # Combine symbols and names into a list for fuzzy matching
    stock_list = stock_symbols + stock_names

    # Use fuzzy matching to find the closest match
    closest_match, score = process.extractOne(user_input, stock_list)
    
    if score > 70:
        if closest_match in stock_names:
            return stock_data.loc[stock_data['name'] == closest_match, 'symbol'].values[0]
        return closest_match
    return None


def display_stock_info(ticker):
    """Fetch and display detailed stock information using yfinance."""
    stock = yf.Ticker(ticker)
    stock_info = stock.info

    if not stock_info:
        console.print(f"[bold red]No information found for {ticker}.[/bold red]", style="danger")
        return

    # Filter out null values and unwanted keys
    filtered_info = {k: v for k, v in stock_info.items() if v is not None and k not in [
        'uuid', 'gmtOffSetMilliseconds', 'messageBoardId', 'compensationAsOfEpochDate', 'maxAge'
    ]}

    # Display `longBusinessSummary` in one row (full width)
    console.print(f"\n[highlight]Business Summary[/highlight]: {filtered_info.get('longBusinessSummary', 'N/A')}", style="info")

    # Display `companyOfficers` in a structured way
    if 'companyOfficers' in filtered_info:
        console.print("\n[highlight]Company Officers:[/highlight]", style="highlight")
        officers_table = Table(show_lines=True, style="info", header_style="bold white on #282828")

        officers_table.add_column("Name", style="cyan on #282828")
        officers_table.add_column("Title", style="green on #282828")
        officers_table.add_column("Total Pay", style="magenta on #282828")
        officers_table.add_column("Age", style="yellow on #282828")
        
        for officer in filtered_info['companyOfficers']:
            name = officer.get('name', 'N/A')
            title = officer.get('title', 'N/A')
            total_pay = officer.get('totalPay', 'N/A')
            age = officer.get('age', 'N/A')
            officers_table.add_row(name, title, str(total_pay), str(age))
        console.print(officers_table)
        console.print("\n")

    # Remove `longBusinessSummary` and `companyOfficers` from the filtered info as we already displayed them
    filtered_info.pop('longBusinessSummary', None)
    filtered_info.pop('companyOfficers', None)

    # Display the remaining data in three columns
    display_info_in_three_columns(filtered_info)

    # Ask if the user wants to export the data
    choice = Prompt.ask("\nWould you like to export the data to CSV or Excel? (yes/no)", default="no")
    
    if choice.lower() == "yes":
        export_choice = Prompt.ask("Choose export format: CSV or Excel?", choices=["csv", "excel"], default="csv")
        export_stock_info(filtered_info, ticker, export_choice)

def display_info_in_three_columns(info):
    """Display key-value pairs in three columns, skipping long values."""
    table = Table(show_lines=True, style="info", header_style="bold white on #282828")

    # Add columns for three attributes and values
    table.add_column("Attribute 1", style="cyan on #282828", width=25)
    table.add_column("Value 1", style="green on #282828", width=35)
    table.add_column("Attribute 2", style="cyan on #282828", width=25)
    table.add_column("Value 2", style="green on #282828", width=35)
    table.add_column("Attribute 3", style="cyan on #282828", width=25)
    table.add_column("Value 3", style="green on #282828", width=35)

    max_value_length = 40  # Set a maximum length for displayed values
    keys = list(info.keys())
    values = list(info.values())

    for i in range(0, len(keys), 3):
        row_data = []
        for j in range(3):
            if i + j < len(keys):
                key = keys[i + j]
                value = values[i + j]
                # Skip long values and add a placeholder
                if isinstance(value, str) and len(value) > max_value_length:
                    row_data.append(str(key))
                    row_data.append("[value too long]")
                else:
                    row_data.append(str(key))
                    row_data.append(str(value))
            else:
                row_data.append("")
                row_data.append("")
        table.add_row(*row_data)

    console.print(table)

def export_stock_info(info, ticker, export_format):
    """Export stock information to CSV or Excel."""
    # Convert the info dictionary to a pandas DataFrame
    df = pd.DataFrame(list(info.items()), columns=["Attribute", "Value"])

    # Define the file name
    file_name = f"{ticker}_stock_info.{export_format}"

    try:
        if export_format == "csv":
            df.to_csv(file_name, index=False)
        elif export_format == "excel":
            df.to_excel(file_name, index=False)
        console.print(f"[bold green]Stock information successfully exported to {file_name}![/bold green]", style="success")
    except Exception as e:
        console.print(f"[bold red]Failed to export data: {e}[/bold red]", style="danger")

def display_equities(stock_data):
    """Display stock data in a tabular format."""
    table = Table(title="Available Stocks", title_justify="left", header_style="bold", show_lines=True)
    table.add_column("Symbol", style="cyan", justify="left", width=15)
    table.add_column("Name", style="green", justify="left", width=50)
    table.add_column("Market Cap", style="yellow", justify="left", width=20)

    for _, row in stock_data.iterrows():
        table.add_row(str(row['symbol']), str(row['name']), str(row['market_cap']))

    console.print("\n")
    console.print(table)

# Function to display lists in columns with max 7 rows per column (no "Column 1" heading)
def display_in_columns(title, items):
    """Display the items in a table with multiple columns if they exceed 7 rows."""
    table = Table(title=title, header_style="bold green on #282828", show_lines=True)  # show_lines=True adds spacing between rows
    max_rows = 7  # Maximum number of rows per column
    num_columns = (len(items) + max_rows - 1) // max_rows  # Calculate the required number of columns

    # Add the columns (empty headers to remove column titles)
    for _ in range(num_columns):
        table.add_column("", style="highlight", justify="left")

    # Add rows in columns
    rows = [[] for _ in range(max_rows)]  # Empty rows to hold the items
    for index, item in enumerate(items):
        row_index = index % max_rows
        rows[row_index].append(f"{index+1}. {item}")

    # Fill the table
    for row in rows:
        # If the row has fewer elements than the number of columns, fill the rest with empty strings
        row += [""] * (num_columns - len(row))
        table.add_row(*row)

    console.print(table)


# Submenu handling for Market Tracker in `market.py`
def show_market_tracker_menu():
    """Market Tracker submenu."""
    while True:
        console.print("[highlight]MARKET TRACKER[/highlight]\n", style="info")

        tracker_text = """
1. FII/DII DATA INDIA
2. NIFTY 50 LIST
3. SEARCH ASSETS
4. BACK TO MAIN MENU
        """

        tracker_panel = Panel(tracker_text, title="MARKET TRACKER MENU", title_align="center", style="bold green on #282828", padding=(1, 2))
        console.print(tracker_panel)

        choice = Prompt.ask("Enter your choice")

        if choice == "1":
            display_fii_dii_data()  
        elif choice == "2":
            console.print("[bold yellow]Nifty 50 list under development[/bold yellow]", style="warning")
        elif choice == "3":
            search_assets() 
        elif choice == "4":
            break

if __name__ == '__main__':
    cli()
