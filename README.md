# Finance Tracker

A desktop application for tracking personal finances built with Python and Tkinter. This app helps you monitor your expenses, categorize spending, and visualize your financial data.

## Features

- 📊 **Dashboard Overview**: Personal profile with month progress and expense trends
- 🏷️ **Category-wise Expenses**: Visual cards showing spending by category (Food, Rent, Transport, etc.)
- 📝 **Transaction History**: Complete transaction log with search functionality
- ➕ **Add Transactions**: Easy form to add new expenses with details
- 🔮 **Upcoming Transactions**: Track planned future expenses
- 📈 **Charts**: Visual graphs showing spending patterns over time
- 💾 **Local Database**: All data stored locally in SQLite database

## Prerequisites

Before running the application, make sure you have:

- **Python 3.6 or higher** installed on your system
- **pip** (Python package installer) available

### Check Python Installation

Open your terminal/command prompt and run:
```bash
python --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

## Installation

1. **Clone or download** this project to your local machine

2. **Navigate to the project directory**:
   ```bash
   cd finance-tracker
   ```

3. **Install required dependencies**:
   ```bash
   pip install matplotlib
   ```

   Note: `tkinter` and `sqlite3` are included with Python by default, so they don't need separate installation.

## How to Run

### Windows
```bash
python main.py
```

### macOS/Linux
```bash
python3 main.py
```

The application will open in a new window with the finance tracker interface.

## Usage Guide

### Adding Transactions
1. Click the **"➕ Add Transaction"** button
2. Fill in the form:
   - **Date**: Enter in YYYY-MM-DD format (e.g., 2024-01-15)
   - **Category**: Select from dropdown (Food, Rent, Transport, etc.)
   - **Amount**: Enter the expense amount
   - **Notes**: Add any additional details
   - **Payment Type**: Choose Cash or Card
   - **Upcoming**: Check if this is a future transaction
3. Click **Submit**

### Searching Transactions
- Use the search box to find specific transactions
- Search works across all fields (date, category, amount, notes)

### Viewing Data
- **Category Cards**: See total spending by category with color-coded cards
- **Transaction History**: View all transactions in a sortable table
- **Charts**: Visual representation of spending over time
- **Upcoming Transactions**: Track planned future expenses

## File Structure

```
finance-tracker/
├── main.py              # Main application file
├── database.py          # Database initialization and setup
├── finance_tracker.db   # SQLite database (created automatically)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Database

The application uses SQLite to store transaction data locally. The database file (`finance_tracker.db`) is created automatically when you first run the application.

### Database Schema
- **transactions table**: Stores all transaction data
  - id (Primary Key)
  - date
  - category
  - amount
  - notes
  - upcoming
  - payment_type

## Troubleshooting

### Common Issues

1. **"Python not found" error**
   - Make sure Python is installed and added to your system PATH
   - Try using `python3` instead of `python` on macOS/Linux

2. **"Module not found" error**
   - Install missing dependencies: `pip install matplotlib`
   - Make sure you're in the correct directory

3. **Tkinter not available**
   - On Ubuntu/Debian: `sudo apt-get install python3-tk`
   - On CentOS/RHEL: `sudo yum install tkinter`
   - On Windows/macOS: Tkinter is included with Python

4. **Permission errors**
   - Make sure you have write permissions in the project directory
   - Run as administrator if needed (Windows)

### Getting Help

If you encounter any issues not covered here:
1. Check that all dependencies are installed correctly
2. Ensure you're running the latest version of Python
3. Try running the application from a different directory

## Features in Detail

### Categories
The app includes predefined categories with emojis and colors:
- 🍔 Food
- 🏠 Rent
- 🚗 Transport
- 💡 Bills
- 💊 Healthcare
- 📚 Education
- 💰 Investment
- 🧾 Other

### Charts
- Line chart showing daily spending trends
- Automatically updates when new transactions are added
- Displays spending patterns over time

### Search Functionality
- Real-time search across all transaction fields
- Case-insensitive matching
- Instant results as you type

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests

---

**Happy Finance Tracking! 💰**
