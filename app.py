from flask import Flask, render_template, request, jsonify, send_file
import os
import logging
from datetime import datetime
import io
import base64
from PIL import Image
import requests
import google.generativeai as genai
from huggingface_hub import InferenceClient
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Initialize APIs
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

# Initialize Hugging Face client - use standard API for free models
try:
    # Primary client - standard HF inference API (best for free models)
    hf_client = InferenceClient(token=os.environ.get('HUGGINGFACE_API_KEY'))
    logger.info("Hugging Face standard client initialized")
except Exception as e:
    hf_client = None
    logger.error(f"Failed to initialize HF client: {e}")

# Initialize secondary client (can try Nebius for premium models if needed)
try:
    hf_client_nebius = InferenceClient(
        provider="nebius",
        api_key=os.environ.get('HUGGINGFACE_API_KEY')
    )
    logger.info("Nebius provider client available for premium models")
except (TypeError, Exception) as e:
    hf_client_nebius = None
    logger.info("Nebius provider not available - using standard HF only")

# LocalStableDiffusion class removed as requested

class GraphicStoryCreator:
    def __init__(self):
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Use only FLUX.1-dev model as requested (no local generation)
        self.flux_model = "black-forest-labs/FLUX.1-dev"
        self.current_model_index = 0
    
    def optimize_prompt_with_gemini(self, user_prompt, context="infographic"):
        """
        Use Gemini to optimize and enhance the user's prompt for better image generation
        """
        try:
            optimization_prompt = f"""
            You are an expert prompt engineer for AI image generation. 
            The user wants to create a {context} with the following description: "{user_prompt}"
            
            Please optimize this prompt for FLUX.1-dev image generation model to create high-quality infographics/visual narratives.
            
            CRITICAL REQUIREMENTS:
            - ENSURE ALL TEXT IN THE IMAGE USES PERFECT ENGLISH GRAMMAR AND SPELLING
            - Specify "correct English spelling and grammar for all text elements"
            - Include "professional typography with accurate spelling"
            - Add "error-free text content" as a requirement
            
            Additional Guidelines:
            - Make the prompt more specific and detailed
            - Include visual style instructions (modern, clean, professional)
            - Add composition guidelines (layout, typography, color scheme)
            - Specify infographic elements (charts, icons, timelines if relevant)
            - Keep it under 250 words
            - Focus on visual storytelling elements
            - Emphasize readable, well-formatted text
            
            IMPORTANT: The generated image must have all text content in correct, professional English with proper spelling and grammar.
            
            Return only the optimized prompt, nothing else.
            """
            
            response = self.gemini_model.generate_content(optimization_prompt)
            optimized_prompt = response.text.strip()
            logger.info(f"Original prompt: {user_prompt}")
            logger.info(f"Optimized prompt: {optimized_prompt}")
            return optimized_prompt
            
        except Exception as e:
            logger.error(f"Error optimizing prompt with Gemini: {str(e)}")
            return user_prompt  # Return original if optimization fails
    
    def generate_image_with_flux(self, optimized_prompt):
        """
        Generate image using FLUX.1-dev only (no local generation)
        """
        
        # Generate using FLUX.1-dev only
        logger.info("🌐 Generating with FLUX.1-dev API...")
        model = self.flux_model
        
        # Try both Nebius and standard HF clients
        clients_to_try = []
        if hf_client_nebius:
            clients_to_try.append(('nebius', hf_client_nebius))
        if hf_client:
            clients_to_try.append(('standard', hf_client))
        
        for provider_name, client in clients_to_try:
            if client is None:
                continue
                
            try:
                logger.info(f"Attempting FLUX.1-dev generation with {provider_name} provider...")
                
                # FLUX optimized parameters
                image = client.text_to_image(
                    prompt=optimized_prompt,
                    model=model,
                    width=1024,
                    height=1024
                )
                
                # Convert to base64 for web display
                buffer = io.BytesIO()
                image.save(buffer, format='PNG')
                buffer.seek(0)
                
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                
                logger.info(f"✅ Successfully generated image with FLUX.1-dev ({provider_name})")
                return {
                    'success': True,
                    'image_base64': img_base64,
                    'image': image,
                    'model_used': model,
                    'model_type': 'api_premium',
                    'provider': provider_name
                }
                
            except Exception as e:
                error_message = str(e).lower()
                logger.warning(f"Failed with FLUX.1-dev on {provider_name}: {str(e)}")
                
                # If rate limited or payment required, try next provider
                if any(x in error_message for x in ["402", "payment required", "rate limit", "quota"]):
                    logger.info(f"💳 Rate limit/payment issue with FLUX.1-dev on {provider_name}, trying next provider...")
                    continue
                # For other errors, try next provider
                else:
                    continue
        
        # If all attempts failed, return detailed error
        return {
            'success': False,
            'error': 'FLUX.1-dev generation failed. This could be due to:\n• Rate limits on API providers\n• Payment required for FLUX.1-dev model\n• Network connectivity issues\n\nSuggestions:\n• Check your Hugging Face API credits\n• Try again in a few minutes (API has usage limits)\n• Check your internet connection',
            'error_type': 'flux_failed'
        }

# Initialize the creator
story_creator = GraphicStoryCreator()

@app.route('/')
def index():
    """Main page for the graphic story creator"""
    return render_template('index.html')

@app.route('/create-story', methods=['POST'])
def create_story():
    """
    Main endpoint to create a graphic story from user input
    """
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '')
        story_type = data.get('type', 'infographic')  # infographic, timeline, poster, etc.
        
        if not user_prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Step 1: Optimize prompt with Gemini
        optimized_prompt = story_creator.optimize_prompt_with_gemini(user_prompt, story_type)
        
        # Step 2: Generate image with Stable Diffusion XL (free) or fallback models
        result = story_creator.generate_image_with_flux(optimized_prompt)
        
        if result['success']:
            return jsonify({
                'success': True,
                'original_prompt': user_prompt,
                'optimized_prompt': optimized_prompt,
                'image_base64': result['image_base64'],
                'model_used': result.get('model_used', 'unknown'),
                'model_type': result.get('model_type', 'unknown'),  # free or premium
                'provider': result.get('provider', 'unknown'),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"Error in create_story: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/optimize-prompt', methods=['POST'])
def optimize_prompt():
    """
    Endpoint to just optimize a prompt without generating image
    """
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '')
        context = data.get('context', 'infographic')
        
        if not user_prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        optimized_prompt = story_creator.optimize_prompt_with_gemini(user_prompt, context)
        
        return jsonify({
            'success': True,
            'original_prompt': user_prompt,
            'optimized_prompt': optimized_prompt
        })
        
    except Exception as e:
        logger.error(f"Error in optimize_prompt: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/models')
def get_models():
    """Show current model configuration for debugging"""
    return jsonify({
        'local_sd_available': False,
        'local_sd_model': None,
        'api_model': story_creator.flux_model,
        'libraries_available': False,
        'primary_method': 'api',
        'fallback_method': 'FLUX.1-dev API'
    })

@app.route('/status')
def get_status():
    """Check system status and capabilities"""
    return jsonify({
        'local_sd_available': False,
        'local_sd_loaded': False,
        'cuda_available': False,
        'device': "cpu",
        'api_fallback_available': hf_client is not None,
        'gemini_configured': os.environ.get('GEMINI_API_KEY') is not None
    })

if __name__ == '__main__':
    # Check for required environment variables
    required_vars = ['GEMINI_API_KEY', 'HUGGINGFACE_API_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.warning("Please set these variables before running the app")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
