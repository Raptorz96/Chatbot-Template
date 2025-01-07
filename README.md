# Insurance Chatbot Template

An intelligent customer service chatbot for the insurance industry, built with modern AI and NLP technologies. This template provides a ready-to-use solution for insurance companies looking to improve their customer service through AI-powered automation.

## 🌟 Key Features

- **Intelligent Chat**: Answers user questions using a customizable knowledge base
- **Categorized FAQs**: Organized FAQ system covering different insurance types (auto, home, life, etc.)
- **Premium Calculator**: Built-in tool for insurance premium calculations
- **Escalation System**: Automated handling of cases requiring human assistance
- **Vector Knowledge Base**: ChromaDB implementation for efficient semantic search
- **Comprehensive Logging**: Detailed tracking of all interactions
- **Streamlit Interface**: Clean, responsive web interface

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/NLP**: LangChain + OpenAI
- **Vector Database**: ChromaDB
- **Language**: Python 3.8+
- **Logging**: Python logging module
- **Environment Management**: python-dotenv

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Raptorz96/Chatbot-Template.git
cd Chatbot-Template
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
```env
OPENAI_API_KEY=your-api-key-here
```

5. Launch the application:
```bash
streamlit run streamlit_app.py
```

## 💼 Template Usage

This template can be easily customized for various insurance industry use cases:

### Knowledge Base Customization
- Add your FAQs and information in the `data` directory
- Organize information using the category system
- Update the vector database with your company's documentation

### UI Customization
- Modify `streamlit_app.py` to match your brand
- Customize the chat interface
- Add new features specific to your needs

### Business Logic
- Customize premium calculation logic
- Modify escalation rules
- Add your own business-specific workflows

## 🔍 Features in Detail

### Smart Chat System
- Context-aware responses using LangChain
- Semantic search in the knowledge base
- Automatic FAQ suggestions

### Premium Calculator
- Configurable calculation rules
- Support for multiple insurance types
- Real-time premium estimates

### Escalation Management
- Automatic case prioritization
- Email notification system
- Ticket creation for complex cases

## 🔒 Security Features

- Secure API key management
- Interaction logging for audit
- Configurable access control
- Data encryption support

## 📈 Future Roadmap

- Dashboard for analytics
- Multi-language support
- Integration with CRM systems
- Advanced reporting features
- Token streaming responses
- Response caching system

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## 📞 Support

For support and queries, please open an issue in the GitHub repository: [Chatbot-Template Issues](https://github.com/Raptorz96/Chatbot-Template/issues)