# Chatbot with LangChain, RAG, and Django API

This project implements an AI chatbot leveraging LangChain, Retrieval-Augmented Generation (RAG), and Django to expose the chatbot's functionalities through API endpoints. The chatbot is designed to provide detailed and accurate responses based on structured data stored in a ChromaDB vector database.

## Table of Contents
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Documentation](#api-documentation)
6. [Directory Structure](#directory-structure)
7. [Contributing](#contributing)
8. [License](#license)

---

## Features
- **Conversational AI**: Provides intelligent and context-aware responses based on Manu's resume and personality data.
- **RAG-Based Search**: Retrieves relevant information using similarity search from vectorized documents stored in ChromaDB.
- **Agent Execution**: Uses LangChain's reactive agent architecture for dynamic and task-specific responses.
- **Django API**: Exposes chatbot interactions through a RESTful API.

---

## Tech Stack
- **Backend**: Python, Django
- **AI Framework**: LangChain, LangGraph
- **Vector Database**: ChromaDB
- **Embedding Models**: OpenAI GPT models
- **Document Processing**: LangChain Text Splitter, Docx2txt, PyPDFLoader

---

## Installation

### Prerequisites
1. Python 3.8+
2. Virtual environment tools like `venv` or `conda`
3. OpenAI API Key (store in a `.env` file)
4. Django and required libraries (`requirements.txt` file provided)

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/chatbot-django-rag.git
    cd chatbot-django-rag
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the data directory:
   - Inside the project root directory, create a `data` folder with the following structure:
     ```
     data/
     ├── Resume_Data/        # Store resume-related .docx files here
     └── Personality_Data/   # Store personality-related .docx files here
     ```
   - Add `.docx` files for:
     - **Resume Data**: Include one or more `.docx` files with professional experience, projects, and achievements.
     - **Personality Data**: Include `.docx` files with personal traits, hobbies, or character-related information.

   - **Example**:
     ```
     data/
     ├── Resume_Data/
     │   ├── resume1.docx
     │   ├── resume2.docx
     └── Personality_Data/
         ├── personality_traits.docx
         ├── hobbies.docx
     ```

   - You can add multiple `.docx` files to each folder as needed.

5. Set up the environment variables:
    - Create a `.env` file in the root directory with the following content:
      ```
      OPENAI_API_KEY=your_openai_api_key
      ```

6. Initialize the vector database and process documents:
    ```bash
    python vectorstore.py
    ```

7. Run the Django development server:
    ```bash
    python manage.py runserver
    ```

---

---

## Usage

### Interacting with the API
1. Start the server (`python manage.py runserver`).
2. Use tools like Postman or `curl` to send a POST request to the `/send_message/` endpoint.
    - **Endpoint**: `http://127.0.0.1:8000/send_message/`
    - **Request Body**:
      ```json
      {
          "question": "What are Manu's skills?"
      }
      ```
    - **Response**:
      ```json
      {
          "response": "Manu is skilled in Python, Django, LangChain, and more..."
      }
      ```

---

## API Documentation

### POST `/send_message/`
- **Description**: Handles user queries and returns responses based on structured data.
- **Request Body**:
  ```json
  {
      "question": "Your question here"
  }
  ```
- **Response**:
  - `200 OK`: Returns the chatbot's response.
  - Example:
    ```json
    {
        "response": "Manu has experience working with AI, Python, and more..."
    }
    ```

---

## Directory Structure
```
chatbot-django-rag/
│
├── llm_utils/
│   ├── chatbot.py        # Main chatbot logic
│   └── vectorstore.py    # Vector database setup
│
├── views.py              # API endpoint logic
│
├── data/
│   ├── Resume_Data/      # Directory for resume documents
│   └── Personality_Data/ # Directory for personality documents
│
├── requirements.txt      # Python dependencies
├── manage.py             # Django management script
├── .env                  # Environment variables
└── README.md             # Project documentation
```

---

## Contributing
1. Fork the repository.
2. Create a new branch (`feature/new-feature`).
3. Commit your changes.
4. Push to the branch.
5. Create a pull request.

---

## License
This project is licensed under the [MIT License](LICENSE).
