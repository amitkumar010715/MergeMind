# MergeMind

MergeMind is a premium multi-model AI code generator that leverages the power of OpenAI's GPT models and Gemini models to provide efficient and accurate coding solutions. This project is designed to help developers generate, evaluate, and refine code snippets for various use cases.

## Features
- **Multi-Model Support**: Integrates OpenAI GPT models and Gemini models.
- **Referee System**: Combines the strengths of multiple models to provide the best solution.
- **Secure API Key Handling**: Ensures sensitive information like API keys is not stored.
- **Customizable UI**: Built with Gradio for an interactive and user-friendly interface.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/MergeMind.git
   cd MergeMind
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory.
   - Add your API keys:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     GEMINI_API_KEY=your_gemini_api_key
     ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open the Gradio interface in your browser.

3. Enter your coding question, select the models, and get the best solution.

## Deployment

### Deploy to Hugging Face Spaces
1. Push the project to Hugging Face Spaces.
2. Ensure `app.py` is the main entry point.
3. Verify the deployment at your Hugging Face Space URL.

### Deploy to GitHub
1. Push the project to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```
2. Share the repository URL with others.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [OpenAI](https://openai.com/)
- [Hugging Face](https://huggingface.co/)
