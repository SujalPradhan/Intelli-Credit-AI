FINANCIAL_KEYWORDS = [
    "balance sheet",
    "profit and loss",
    "statement of income",
    "financial highlights",
    "cash flow",
    "revenue",
    "total assets",
    "total liabilities"
]

HIGH_VALUE_SECTIONS = [
    # Financial statements
    "balance sheet",
    "statement of financial position", 
    "profit and loss",
    "income statement",
    "statement of profit",
    "cash flow statement",
    "statement of cash flows",
    
    # Key metrics
    "financial highlights",
    "key financial indicators",
    "five year summary",
    "ten year summary",
    
    # For anomaly detection
    "segment revenue",
    "quarterly results",
    "management discussion",   # MD&A has forward-looking risk info
    "significant accounting",
]

NOISE_SECTIONS = [
    "notice of annual",
    "director's report",       # mostly narrative
    "corporate governance",
    "csr activities",
    "auditor's report",        # boilerplate
    "chairman's message",
    "our journey",
    "about us",
]