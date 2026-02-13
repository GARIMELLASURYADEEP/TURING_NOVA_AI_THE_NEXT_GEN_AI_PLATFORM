# AI Code Generator

A Streamlit web application that generates code using the OpenRouter API (StepFun Step-3.5-Flash model).

## Features
- **Multi-language Support**: Generate code in Python, Java, C++, JavaScript, etc.
- **OpenRouter Integration**: Uses the free `stepfun/step-3.5-flash` model.
- **Clean UI**: Simple interface with syntax highlighting and copy functionality.

## Setup Instructions

### Prerequisites
- Python 3.8+
- An OpenRouter API Key

### Local Installation

1. **Clone the repository** (if applicable) or navigate to your project folder.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Key**:
   Create a `.env` file in the root directory and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Deployment to Streamlit Cloud

1. Push your code to a GitHub repository.
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud).
3. Connect your repository and deploy the app.
4. **Configure Secrets**:
   - Go to your app's dashboard.
   - Click on "Settings" -> "Secrets".
   - Add your API key in the TOML format:
     ```toml
     OPENROUTER_API_KEY = "your_key_here"
     ```

## Project Structure
- `app.py`: Main application code.
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables (API Key) - **Do not commit this file**.
