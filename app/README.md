# Legal Document Analysis System

A Streamlit application for analyzing legal documents, particularly focusing on foreclosure documents and risk assessment.

## 🚀 Features

- Document risk analysis
- Key issues identification
- Automated recommendations
- Analysis history tracking
- Multiple analysis types support

## 🛠️ Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## 💡 Usage

1. Select analysis type from the sidebar
2. Paste document text into the input area
3. Click "Analyze Document"
4. View results in the right panel
5. Check analysis history in the sidebar

## 📊 Analysis Types

- **Notice Requirements**: Analyzes compliance with foreclosure notice requirements
- **Authority Verification**: Checks authority documentation and delegation
- **Document Compliance**: Reviews general document compliance

## 🔒 Security

- API keys and sensitive data should be stored in `.env`
- Never commit `.env` file to version control
- Use environment variables for production deployment

## 📝 License

MIT License - see LICENSE file for details
