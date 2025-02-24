# CLAUDE.md - Insurance Chatbot Guidelines

## Commands
- Run the Streamlit app: `streamlit run src/streamlit_app.py`
- Run the CLI version: `python src/main.py`
- Test database: `python src/database/populate_db.py`
- Install dependencies: `pip install -r requirements.txt`
- Development install: `pip install -e .`

## Code Style Guidelines
- **Imports**: Standard library first, then third-party, then local modules
- **Error Handling**: Use try/except with specific exceptions and logging
- **Logging**: Use the logger from `src.utils.logging`
- **Type Hints**: Add type hints for function parameters and return values
- **Doc Strings**: Use docstrings for all functions ("""description""")
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Path Handling**: Use os.path for path manipulation
- **Environment Variables**: Load with dotenv, access via os.getenv()
- **Database Interactions**: Use ChromaDB client from src.database.chroma_db
- **Exception Pattern**: Catch exceptions, log errors, provide fallbacks

## Project Structure
- `/src`: Main source code
- `/data`: Knowledge base and documents
- `streamlit_app.py`: Web interface
- `main.py`: CLI interface