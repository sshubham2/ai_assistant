# AI Assistant

## Overview

The AI Assistant is a Streamlit application designed to provide users with support in programming and natural language tasks. It utilizes multiple language models to offer functionalities such as code writing, debugging, multilingual translation, content summarization, and more.

## Features

- **Programming Language Expert**: 
  - Assist with writing, debugging, and optimizing code in various programming languages.
  - Provide explanations of programming concepts and deliver technical documentation.

- **Natural Language Expert**: 
  - Offer multilingual translation and content summarization.
  - Help with professional email composition and resume writing.

## Project Structure

The project is composed of the following files:

1. **main_page.py**: 
   - Initializes the Streamlit application and sets up navigation between different pages.

2. **home_page.py**: 
   - Contains the main content and user interface for the AI Assistant, including introductions and available functionalities.

3. **chatbot.py**: 
   - Implements the Programming Language Expert functionality using LangChain and various LLMs.

4. **chatbot_nne.py**: 
   - Implements the Natural Language Expert functionality using LangChain and various LLMs.

## Installation

To run the AI Assistant, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sshubham2/ai_assistant
   cd ai_assistant
2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
4. **Set up environment variables:**
   
   Create a `.env` file in the project root and add your API keys:
   ```bash
   OPENAI_API_KEY=<your_api_key_here>
   ANTHROPIC_API_KEY=<your_api_key_here>

## Usage
Run the application:
```bash
streamlit run main_page.py
```
Navigate through the application using the sidebar to access the Programming Language Expert or Natural Language Expert modules.

Input your queries in the chat interface and interact with the AI Assistant.

## Contribution
Contributions are welcome! If you have suggestions for improvements or new features, feel free to submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or inquiries, please contact [shubhendu Shubham](https://www.linkedin.com/in/shubhendu-shubham-5661b7aa/)

   
