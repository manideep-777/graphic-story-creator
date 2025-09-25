# Graphic Story Creator

A Gen AI-powered web application that transforms text descriptions into stunning visual narratives, infographics, and posters using advanced AI models.

## 🚀 Features

- **AI-Powered Prompt Optimization**: Uses Google's Gemini to enhance and optimize user prompts
- **High-Quality Image Generation**: Leverages FLUX.1-dev for professional-grade visual creation
- **Multiple Story Types**: Support for infographics, timelines, posters, and dashboards
- **Web Interface**: Clean, responsive web interface built with Flask and Bootstrap
- **Real-time Generation**: Fast image generation with progress indicators

## 🛠 Technology Stack

- **Backend**: Python Flask
- **AI Models**: 
  - Google Gemini (Prompt optimization)
  - FLUX.1-dev via Hugging Face (Image generation)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **APIs**: Hugging Face Hub, Google Generative AI

## 📋 Prerequisites

Before running the application, you'll need:

1. **Python 3.8+** installed on your system
2. **API Keys**:
   - Google Gemini API key from [Google AI Studio](https://makersuite.google.com/)
   - Hugging Face API token from [Hugging Face](https://huggingface.co/settings/tokens)

## 🔧 Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd "d:\final-year-projects\graphic story creator"
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Fill in your API keys:
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` file:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key
   HUGGINGFACE_API_KEY=your_actual_huggingface_token
   SECRET_KEY=your_random_secret_key
   ```

## 🚀 Running the Application

1. **Activate the virtual environment** (if not already activated):
   ```bash
   venv\Scripts\activate
   ```

2. **Run the Flask application**:
   ```bash
   python app.py
   ```

3. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📖 Usage

1. **Choose Story Type**: Select from infographic, timeline, poster, or dashboard
2. **Enter Description**: Describe what you want to create in detail
3. **Generate**: Click "Generate Visual Story" and wait for AI processing
4. **Download**: Save your generated visual story

### Example Prompts

- "Create an infographic about climate change showing temperature rise over the last century with charts and statistics"
- "Design a timeline poster showing the major events of World War II with dates and key information"
- "Generate a dashboard visualization showing social media engagement metrics with charts and KPIs"

## 🏗 Project Structure

```
graphic story creator/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── templates/
│   └── index.html       # Main web interface
├── static/              # Static files (CSS, JS, images)
└── README.md           # This file
```

## 🔑 API Integration

### Gemini Integration
- Optimizes user prompts for better image generation
- Adds technical details and styling instructions
- Improves prompt structure for FLUX.1-dev

### FLUX.1-dev Integration
- Generates high-quality images from optimized prompts
- Supports various visual styles and formats
- Returns base64-encoded images for web display

## 🛡 Error Handling

The application includes comprehensive error handling for:
- Missing API keys
- API rate limits
- Network connectivity issues
- Invalid prompts
- Image generation failures

## 🔧 Configuration

Key configuration options in `config.py`:
- `FLUX_MODEL`: Image generation model
- `DEFAULT_IMAGE_SIZE`: Output image dimensions
- `MAX_PROMPT_LENGTH`: Maximum prompt length
- `GEMINI_MODEL`: Text optimization model

## 📝 Development Notes

- The app uses environment variables for secure API key management
- Image generation typically takes 30-60 seconds
- Generated images are returned as base64 for immediate display
- The interface is responsive and mobile-friendly

## 🤝 Contributing

This is a final year project. For improvements or bug reports, please:
1. Document the issue or enhancement
2. Test thoroughly before implementing changes
3. Follow the existing code structure and style

## 📄 License

This project is created for educational purposes as part of a final year project.

## 🆘 Troubleshooting

### Common Issues:

1. **Missing API Keys**: Ensure all required environment variables are set in `.env`
2. **Slow Generation**: FLUX.1-dev generation can take time; this is normal
3. **Connection Errors**: Check internet connectivity and API key validity
4. **Module Not Found**: Ensure virtual environment is activated and dependencies installed

### Getting Help:

- Check the console logs for detailed error messages
- Verify API keys are correctly configured
- Ensure all dependencies are installed with correct versions
