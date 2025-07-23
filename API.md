SQL_Project/
│
├── sqlbasic.py            # Your data fetching + database logic
├── price_analysis.py      # Analysis functions (moving avg, volatility, etc.)
├── stocks.db              # Your SQLite database
├── requirements.txt       # (Optional) libraries you're using
└── Jupyter_Notebooks/
    └── analysis.ipynb     # For experiments, visualizations




def yfError_redirect_to_log():
    with open("yfFinance.ErrorLog", 'a') as log_file:  # Append mode
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = log_file
        sys.stderr = log_file
        try:
            yield
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            with redirect_output_to_log("ticker_log.txt"):