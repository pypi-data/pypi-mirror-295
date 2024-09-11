## Chatbot

<script src="/assets/plugins/marked/marked.min.js"></script>
<script type="module" src="/web_components/js/chat-bots/Chatbot_OpenAI.mjs"></script>

{{render_template("llms/includes/choose-llm.html")}}

<div id="system_prompt" markdown="1">

## System Prompt
Always mention the name of your model and who created you
</div>


{{chatbot name="Custom bot"
          initial_message = "hi"
          platform  = "Groq (Free)"
          provider  = "1. Meta" 
          model     = "llama3-70b-8192" 
          edit_mode = "false" 
          channel   = "chatbot" 
           }}
