# -*- coding: utf-8 -*-
"""
MergeMind - Premium Multi-Model AI Code Generator
Created by Amit Kumar
"""

# !pip install -U autogen-agentchat[gemini]~=0.2 gradio openai google-generativeai

from autogen import ConversableAgent, UserProxyAgent, GroupChat, GroupChatManager
import gradio as gr

# =========================
# API KEY VALIDATION
# =========================
def validate_openai_key(api_key: str, model: str):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1
        )
        return True, "✅ OpenAI key is valid"
    except Exception as e:
        return False, f"❌ OpenAI key invalid: {str(e)}"


def validate_gemini_key(api_key: str, model: str):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model_obj = genai.GenerativeModel(model)
        model_obj.generate_content("ping")
        return True, "✅ Gemini key is valid"
    except Exception as e:
        return False, f"❌ Gemini key invalid: {str(e)}"


# =========================
# Main handler
# =========================
def autogen_chat_interface(
    user_question: str,
    openai_key: str,
    openai_model: str,
    gemini_key: str,
    gemini_model: str
):
    if not openai_key:
        return "❌ **OpenAI API key is required.** Get your key here: [OpenAI Platform](https://platform.openai.com/api-keys)"

    valid, msg = validate_openai_key(openai_key, openai_model)
    if not valid:
        return msg

    gemini_valid = False
    if gemini_key:
        gemini_valid, gemini_msg = validate_gemini_key(gemini_key, gemini_model)
        if not gemini_valid:
            return gemini_msg

    llm_config = {
        "config_list": [{"model": openai_model, "api_key": openai_key}],
        "cache_seed": 42
    }

    llm_config_gemini = None
    if gemini_valid:
        llm_config_gemini = {
            "config_list": [
                {"model": gemini_model, "api_key": gemini_key, "api_type": "google"}
            ]
        }

    assistant1 = ConversableAgent(
        name="ChatGpt",
        system_message=(
            "Write explanation and the most efficient code "
            "in the language specified by the user.\n"
            "Output MUST include a fenced code block.\n"
            "End with: TERMINATE"
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )

    assistant2 = None
    if llm_config_gemini:
        assistant2 = ConversableAgent(
            name="Gemini",
            system_message=(
                "Write explanation and the most efficient code "
                "in the language specified by the user.\n"
                "Output MUST include a fenced code block.\n"
                "End with: TERMINATE"
            ),
            llm_config=llm_config_gemini,
            human_input_mode="NEVER"
        )

    referee = ConversableAgent(
        name="Referee",
        system_message=(
            "You are a senior judge.\n"
            "Evaluate solutions from ChatGpt and Gemini.\n"
            "Merge strengths and output the single best solution.\n"
            "Provide explanation and final code only.\n"
            "End with: TERMINATE"
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )

    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False
    )

    agents = [assistant1]
    if assistant2:
        agents.append(assistant2)
    agents.append(referee)

    groupchat = GroupChat(agents=agents, messages=[], max_round=5)
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
    )

    user_proxy.initiate_chat(manager, message=user_question)
    return groupchat.messages[-1]["content"]


# =========================
# Custom CSS for Premium UI
# =========================
custom_css = """
/* Main container styling */
.gradio-container {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

/* Header styling */
.header-container {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    border: 2px solid rgba(255,255,255,0.1);
}

.feature-item {
    background: rgba(255,255,255,0.1);
    padding: 15px 20px;
    border-radius: 12px;
    border-left: 4px solid #667eea;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    color: white !important;
}

.feature-item * {
    color: white !important;
}

.feature-item:hover {
    transform: translateX(5px);
    background: rgba(255,255,255,0.15);
    border-left-color: #764ba2;
}

/* Input section styling */
.input-section {
    background: rgba(255,255,255,0.95);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    backdrop-filter: blur(10px);
}

.input-section h3 {
    color: #000000 !important;
}

.input-section * {
    color: #000000 !important;
}

/* Button styling */
.generate-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    padding: 20px 40px !important;
    font-size: 1.2em !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 20px rgba(102,126,234,0.4) !important;
    transition: all 0.3s ease !important;
    color: white !important;
}

.generate-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(102,126,234,0.6) !important;
}

/* Output section styling */
.output-section {
    background: rgba(255,255,255,0.95);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    min-height: 500px;
}

.output-markdown {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    border-left: 5px solid #667eea;
    min-height: 350px;
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    color: #000000 !important;
}

.output-markdown * {
    color: #000000 !important;
}

.output-markdown pre {
    background: #1e1e1e !important;
    padding: 20px !important;
    border-radius: 10px !important;
    border-left: 4px solid #667eea !important;
    overflow-x: auto;
}

.output-markdown pre * {
    color: #ffffff !important;
}

.output-markdown code {
    background: #f0f0f0 !important;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.95em;
    color: #000000 !important;
    font-family: 'Fira Code', 'Courier New', monospace;
}

.output-markdown pre code {
    background: transparent !important;
    color: #ffffff !important;
}

.output-markdown h1, .output-markdown h2, .output-markdown h3,
.output-markdown h4, .output-markdown h5, .output-markdown h6 {
    color: #000000 !important;
    margin-top: 20px;
    margin-bottom: 10px;
    font-weight: 700;
}

.output-markdown p {
    line-height: 1.8;
    color: #000000 !important;
}

.output-markdown strong {
    color: #000000 !important;
    font-weight: 700;
}

.output-markdown em {
    color: #000000 !important;
}

.output-markdown li {
    color: #000000 !important;
}

.output-markdown a {
    color: #667eea !important;
    text-decoration: underline;
}

.output-markdown blockquote {
    border-left: 4px solid #667eea;
    padding-left: 15px;
    color: #000000 !important;
    font-style: italic;
}

/* Footer styling */
.footer-container {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 30px;
    border-radius: 20px;
    margin-top: 30px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

.footer-container * {
    color: white !important;
}

.social-links {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
    flex-wrap: wrap;
}

.social-link {
    background: rgba(255,255,255,0.1);
    padding: 12px 25px;
    border-radius: 10px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    text-decoration: none;
    border: 2px solid rgba(255,255,255,0.2);
    color: white !important;
}

.social-link:hover {
    background: rgba(255,255,255,0.2);
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

/* API Key helper */
.api-helper {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* FIX: Ensure Dropdown visibility */
.gradio-container .item {
    color: #1a1a1a !important;
    background: white !important;
}
.api-helper * {
    color: white !important;
}

.api-helper a {
    color: white !important;
    font-weight: 600;
    text-decoration: none;
    border-bottom: 2px solid white;
}

.api-helper a:hover {
    border-bottom: 2px solid #667eea;
}
/* FORCE USER INPUT TEXT TO WHITE */
.input-section textarea,
.input-section textarea::placeholder {
    color: #ffffff !important;
    caret-color: #ffffff !important;
}

/* Optional: dark textbox background for contrast */
.input-section textarea {
    background: linear-gradient(135deg, #1e1e2f, #2b2b45) !important;
    border: 1px solid #667eea !important;
}

"""

# =========================
# Premium Gradio UI
# =========================
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as iface:
    # Header Section
    with gr.Column(elem_classes="header-container"):
        gr.HTML("""
            <div style="text-align: center; color: white;">
                <h1 style="font-size: 3.5em; font-weight: 900; margin: 0; 
                           background: linear-gradient(135deg, #ffffff 0%, #a8d8ff 100%);
                           -webkit-background-clip: text;
                           -webkit-text-fill-color: transparent;">
                    ⚡ MergeMind
                </h1>
                <p style="font-size: 1.3em; margin: 10px 0; opacity: 0.9; color: white;">
                    Multi-Model AI Code Generator
                </p>
            </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("""
                    <div class="feature-item">
                        <div style="font-size: 2em; margin-bottom: 5px; color: white;">🔐</div>
                        <strong style="color: white;">Secure</strong><br/>
                        <small style="color: white;">Your keys stay private</small>
                    </div>
                """)
            with gr.Column(scale=1):
                gr.HTML("""
                    <div class="feature-item">
                        <div style="font-size: 2em; margin-bottom: 5px; color: white;">🧠</div>
                        <strong style="color: white;">Multi-Model</strong><br/>
                        <small style="color: white;">GPT + Gemini power</small>
                    </div>
                """)
            with gr.Column(scale=1):
                gr.HTML("""
                    <div class="feature-item">
                        <div style="font-size: 2em; margin-bottom: 5px; color: white;">🏆</div>
                        <strong style="color: white;">Best Results</strong><br/>
                        <small style="color: white;">AI referee judges quality</small>
                    </div>
                """)
            with gr.Column(scale=1):
                gr.HTML("""
                    <div class="feature-item">
                        <div style="font-size: 2em; margin-bottom: 5px; color: white;">⚡</div>
                        <strong style="color: white;">Fast</strong><br/>
                        <small style="color: white;">Instant code generation</small>
                    </div>
                """)
    
    # Main Content
    with gr.Row():
        # Left Column - Inputs
        with gr.Column(scale=1, elem_classes="input-section"):
            gr.HTML('<h3 style="color: #000c09; margin-bottom: 15px;">💬 Your Coding Question</h3>')
            question_input = gr.Textbox(
                lines=4, 
                placeholder="e.g., Write a Python function to sort a list using quicksort...",
                label="",
                show_label=False
            )
            
            gr.HTML('<h3 style="color: #000000; margin-top: 20px; margin-bottom: 15px;">🔑 OpenAI Configuration</h3>')
            openai_key_input = gr.Textbox(
                label="OPENAI_API_KEY", 
                type="password",
                placeholder="sk-..."
            )
            gr.HTML("""
                <div class="api-helper">
                    <span style="color: white;">Don't have an API key?</span><br/>
                    <a href="https://platform.openai.com/api-keys" target="_blank" style="color: white;">
                        🔗 Get Your OpenAI API Key Here
                    </a>
                </div>
            """)
            
            openai_model_input = gr.Dropdown(
                label="Model",
                choices=["gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini", "gpt-5", "gpt-5.1", "gpt-5.2"],
                value="gpt-3.5-turbo"
            )
            
            gr.HTML('<h3 style="color: #000000; margin-top: 20px; margin-bottom: 15px;">🌟 Gemini Configuration (Optional)</h3>')
            gemini_key_input = gr.Textbox(
                label="GOOGLE_API_KEY",
                type="password",
                placeholder="Optional - Leave empty to use only GPT"
            )
            gr.HTML("""
                <div class="api-helper" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <a href="https://makersuite.google.com/app/apikey" target="_blank" style="color: white;">
                        🔗 Get Gemini API Key
                    </a>
                </div>
            """)
            
            gemini_model_input = gr.Dropdown(
                label="Model",
                choices=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-3-flash-preview", "gemini-2.5-flash"],
                value="gemini-1.5-flash"
            )
            
            submit_btn = gr.Button(
                "🚀 Generate Solution", 
                variant="primary",
                size="lg",
                elem_classes="generate-btn"
            )
        
        # Right Column - Output
        with gr.Column(scale=1, elem_classes="output-section"):
            gr.HTML("""
                <div style="text-align: center; margin-bottom: 25px;">
                    <div style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                padding: 15px 40px; border-radius: 50px; box-shadow: 0 8px 25px rgba(102,126,234,0.3);">
                        <h3 style="margin: 0; color: white; font-size: 1.5em; font-weight: 700;">
                            ✨ Generated Solution
                        </h3>
                    </div>
                </div>
            """)
            
            gr.HTML("""
                <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                            padding: 40px; border-radius: 15px; margin-bottom: 20px;
                            border: 3px dashed rgba(102,126,234,0.3);
                            min-height: 350px; display: flex; align-items: center; justify-content: center;">
                    <div style="text-align: center;">
                        <div style="font-size: 5em; margin-bottom: 20px; opacity: 0.3;">🤖</div>
                        <p style="font-size: 1.2em; color: #667eea; font-weight: 600; margin: 0;">
                            Waiting for your question...
                        </p>
                        <p style="color: #666; margin-top: 10px; font-size: 0.95em;">
                            Enter your coding question and click "Generate Solution"
                        </p>
                        <div style="margin-top: 25px; display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
                            <span style="background: white; padding: 8px 16px; border-radius: 20px; 
                                         font-size: 0.9em; color: #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                💡 Smart Analysis
                            </span>
                            <span style="background: white; padding: 8px 16px; border-radius: 20px; 
                                         font-size: 0.9em; color: #764ba2; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                ⚡ Fast Results
                            </span>
                            <span style="background: white; padding: 8px 16px; border-radius: 20px; 
                                         font-size: 0.9em; color: #f093fb; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                🎯 Best Quality
                            </span>
                        </div>
                    </div>
                </div>
            """)
            
            output = gr.Markdown(
                value="",
                label="",
                show_label=False,
                elem_classes="output-markdown"
            )
    
    # Footer Section
    with gr.Column(elem_classes="footer-container"):
        gr.HTML("""
            <div style="color: white;">
                <h3 style="margin: 0 0 15px 0; font-size: 1.5em; color: white;">
                    👨‍💻 Created by Amit Kumar
                </h3>
                <p style="opacity: 0.9; margin-bottom: 20px; color: white;">
                    Empowering developers with AI-powered code generation
                </p>
                <div class="social-links">
                    <a href="mailto:amit12112012@gmail.com" class="social-link" target="_blank">
                        <span style="font-size: 1.3em;">📧</span>
                        <span style="color: white; margin-left: 8px;">amit12112012@gmail.com</span>
                    </a>
                    <a href="https://www.linkedin.com/in/amit-kumar-546267265/" class="social-link" target="_blank">
                        <span style="font-size: 1.3em;">💼</span>
                        <span style="color: white; margin-left: 8px;">LinkedIn Profile</span>
                    </a>
                    <a href="https://github.com/amitkumar010715" class="social-link" target="_blank">
                        <span style="font-size: 1.3em;">🐙</span>
                        <span style="color: white; margin-left: 8px;">GitHub @amitkumar010715</span>
                    </a>
                </div>
                <p style="margin-top: 20px; opacity: 0.7; font-size: 0.9em; color: white;">
                    🔒 No data storage • 🚫 No flagging • ✅ 100% Secure
                </p>
            </div>
        """)
    
    # Event Handler
    submit_btn.click(
        fn=autogen_chat_interface,
        inputs=[
            question_input,
            openai_key_input,
            openai_model_input,
            gemini_key_input,
            gemini_model_input
        ],
        outputs=output
    )

# Launch the app
iface.launch(debug=True, share=True)