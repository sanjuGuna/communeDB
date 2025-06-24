# Communicate with Database

A powerful full-stack application that allows users to interact with databases using natural language prompts. The application converts natural language queries into SQL statements and executes them against your database, displaying results in a user-friendly interface.

## Features

- **Natural Language to SQL**: Convert plain English queries into SQL statements using AI
- **Database Connectivity**: Connect to MySQL databases with custom connection parameters
- **Real-time Results**: Execute queries and view results instantly
- **User-friendly Interface**: Clean, responsive React frontend
- **Copy to Clipboard**: Easy copying of generated SQL queries
- **Error Handling**: Comprehensive error messages and validation

## Tech Stack

### Frontend
- **React** - Modern JavaScript framework
- **Hooks** (useState, useEffect, useRef) - State management and side effects
- **Responsive Design** - Clean, modern UI

### Backend
- **FastAPI** - High-performance Python web framework
- **LangChain** - AI/LLM integration framework
- **Groq** - AI model provider for natural language processing
- **SQLAlchemy** - SQL toolkit and ORM
- **PyMySQL** - MySQL database connector
- **Uvicorn** - ASGI server

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL database
- Groq API key

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/sanjuGuna/communeDB.git
cd communeDB
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

5. Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Usage

1. **Database Connection**: Fill in your database connection details:
   - Host (e.g., localhost)
   - Port (e.g., 3306)
   - Username
   - Password
   - Database name

2. **Natural Language Query**: Enter your query in plain English, such as:
   - "Show me all users who registered last month"
   - "Find the top 10 products by sales"
   - "Get the average salary by department"

3. **Execute**: Click "Run Query" to generate SQL and execute it

4. **View Results**: See the generated SQL query and results in a formatted table

5. **Copy SQL**: Use the copy button to copy the generated SQL to your clipboard

## API Endpoints

### POST /query
Processes natural language prompts and executes database queries.

**Request Body:**
```json
{
  "prompt": "Show me all users",
  "connection": {
    "host": "localhost",
    "port": "3306",
    "user": "username",
    "password": "password",
    "database": "dbname"
  }
}
```

**Response:**
```json
{
  "sql": "SELECT * FROM users;",
  "data": [
    {"id": 1, "name": "John", "email": "john@example.com"},
    {"id": 2, "name": "Jane", "email": "jane@example.com"}
  ]
}
```

## Dependencies

### Core Backend Dependencies
- `fastapi==0.115.13` - Web framework
- `langchain==0.3.26` - LLM integration
- `langchain-groq==0.3.2` - Groq provider
- `sqlalchemy==2.0.41` - Database ORM
- `pymysql==1.1.1` - MySQL connector
- `uvicorn==0.34.3` - ASGI server
- `python-dotenv==1.1.1` - Environment variables

### AI/ML Dependencies
- `groq==0.28.0` - Groq API client
- `langchain-core==0.3.66` - LangChain core functionality
- `pydantic==2.11.7` - Data validation

### HTTP/Network Dependencies
- `httpx==0.28.1` - HTTP client
- `requests==2.32.4` - HTTP library
- `certifi==2025.6.15` - SSL certificates

## Project Structure

```
communeDB/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database connection logic
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   └── index.js        # React entry point
│   ├── public/
│   └── package.json        # Node.js dependencies
├── .env                    # Environment variables
└── README.md              # This file
```

## Environment Variables

Create a `.env` file with the following variables:

```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=mysql://user:password@localhost:3306/dbname  # Optional default
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid database connections
- Malformed SQL queries
- Network connectivity issues
- API rate limits
- Empty or invalid prompts

## Security Considerations

- Database credentials are not stored permanently
- API keys are stored in environment variables
- Input validation on both frontend and backend
- SQL injection prevention through parameterized queries

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please create an issue in the GitHub repository or contact the maintainer.

## Acknowledgments

- Built with LangChain for AI integration
- Powered by Groq for fast inference
- Uses FastAPI for high-performance backend
- React for modern frontend experience
