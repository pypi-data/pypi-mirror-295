# Supabase Overleaf Template Crawler

This project crawls LaTeX templates from Overleaf and stores them in a local Supabase instance.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure your local Supabase instance is running.
3. Run the crawler:

```bash
python src/main.py
```

## Project Structure

- `src/`: Contains the source code
- `main.py`: Main entry point
- `crawler_general.py`: Crawls general template information
- `crawler_detail.py`: Crawls detailed template information
- `db_handler.py`: Handles database operations
- `config/`: Contains configuration files
- `data/`: (Optional) For storing any local data
