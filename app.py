from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from huggingface_hub import InferenceClient

app = Flask(__name__)
CORS(app)

API_KEY = "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"
client = InferenceClient(provider="novita", api_key=API_KEY)

# HTML template for the chat UI
CHAT_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chat - Creative Edition</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --success-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --accent-color: #4facfe;
            --text-primary: #2d3748;
            --text-secondary: #718096;
            --bg-primary: #ffffff;
            --bg-secondary: #f7fafc;
            --bg-tertiary: #edf2f7;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.1), 0 1px 3px rgba(0,0,0,0.08);
            --shadow-lg: 0 10px 25px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
            --shadow-xl: 0 20px 40px rgba(0,0,0,0.1), 0 10px 20px rgba(0,0,0,0.05);
            --border-radius: 16px;
            --border-radius-sm: 8px;
            --border-radius-lg: 24px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: var(--primary-gradient);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            pointer-events: none;
        }

        .floating-shapes {
            position: absolute;
            width: 100%;
            height: 100%;
            overflow: hidden;
            pointer-events: none;
        }

        .shape {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            animation: float 6s ease-in-out infinite;
        }

        .shape:nth-child(1) {
            width: 80px;
            height: 80px;
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }

        .shape:nth-child(2) {
            width: 120px;
            height: 120px;
            top: 20%;
            right: 10%;
            animation-delay: 2s;
        }

        .shape:nth-child(3) {
            width: 60px;
            height: 60px;
            bottom: 20%;
            left: 20%;
            animation-delay: 4s;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }

        .main-container {
            position: relative;
            z-index: 10;
            max-width: 1200px;
            width: 100%;
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 30px;
            height: 90vh;
        }

        .sidebar {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: var(--border-radius-lg);
            padding: 30px;
            box-shadow: var(--shadow-xl);
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            flex-direction: column;
            gap: 25px;
        }

        .chat-area {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: var(--border-radius-lg);
            box-shadow: var(--shadow-xl);
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .brand-section {
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--bg-tertiary);
        }

        .brand-logo {
            width: 60px;
            height: 60px;
            background: var(--primary-gradient);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 15px;
            box-shadow: var(--shadow-md);
        }

        .brand-logo i {
            font-size: 24px;
            color: white;
        }

        .brand-title {
            font-size: 1.5rem;
            font-weight: 700;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }

        .brand-subtitle {
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 400;
        }

        .features-section {
            flex: 1;
        }

        .feature-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            border-radius: var(--border-radius-sm);
            margin-bottom: 8px;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .feature-item:hover {
            background: var(--bg-tertiary);
            transform: translateX(5px);
        }

        .feature-icon {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: white;
        }

        .feature-icon.ai { background: var(--primary-gradient); }
        .feature-icon.chat { background: var(--secondary-gradient); }
        .feature-icon.creative { background: var(--accent-gradient); }
        .feature-icon.smart { background: var(--success-gradient); }

        .feature-text {
            font-size: 0.9rem;
            font-weight: 500;
            color: var(--text-primary);
        }

        .stats-section {
            background: var(--bg-secondary);
            border-radius: var(--border-radius-sm);
            padding: 20px;
            text-align: center;
        }

        .stat-item {
            margin-bottom: 15px;
        }

        .stat-number {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-color);
        }

        .stat-label {
            font-size: 0.8rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .chat-header {
            background: var(--primary-gradient);
            color: white;
            padding: 25px 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .chat-header-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .ai-avatar {
            width: 45px;
            height: 45px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }

        .chat-info h3 {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 2px;
        }

        .chat-status {
            font-size: 0.85rem;
            opacity: 0.9;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #4ade80;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .chat-controls {
            display: flex;
            gap: 10px;
        }

        .control-btn {
            width: 35px;
            height: 35px;
            border: none;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .control-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.1);
        }

        .chat-messages {
            flex: 1;
            padding: 25px 30px;
            overflow-y: auto;
            background: var(--bg-secondary);
        }

        .message {
            margin-bottom: 20px;
            display: flex;
            align-items: flex-end;
            gap: 12px;
            animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message.user {
            flex-direction: row-reverse;
        }

        .message-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 14px;
            flex-shrink: 0;
        }

        .message.user .message-avatar {
            background: var(--secondary-gradient);
            color: white;
        }

        .message.ai .message-avatar {
            background: var(--primary-gradient);
            color: white;
        }

        .message-content {
            max-width: 70%;
            padding: 15px 20px;
            border-radius: var(--border-radius);
            position: relative;
            box-shadow: var(--shadow-sm);
        }

        .message.user .message-content {
            background: var(--secondary-gradient);
            color: white;
            border-bottom-right-radius: 5px;
        }

        .message.ai .message-content {
            background: white;
            color: var(--text-primary);
            border-bottom-left-radius: 5px;
            border: 1px solid var(--bg-tertiary);
        }

        .message-text {
            font-size: 0.95rem;
            line-height: 1.5;
            word-wrap: break-word;
        }

        .message-time {
            font-size: 0.75rem;
            opacity: 0.7;
            margin-top: 5px;
        }

        .message.user .message-time {
            text-align: right;
        }

        .chat-input-section {
            padding: 25px 30px;
            background: white;
            border-top: 1px solid var(--bg-tertiary);
        }

        .input-container {
            display: flex;
            gap: 15px;
            align-items: flex-end;
        }

        .input-wrapper {
            flex: 1;
            position: relative;
        }

        .chat-input {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid var(--bg-tertiary);
            border-radius: var(--border-radius);
            font-size: 0.95rem;
            font-family: inherit;
            outline: none;
            transition: all 0.3s ease;
            resize: none;
            min-height: 50px;
            max-height: 120px;
        }

        .chat-input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .send-btn {
            background: var(--primary-gradient);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            padding: 15px 25px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            min-width: 120px;
            justify-content: center;
        }

        .send-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }

        .send-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top: 2px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 15px 20px;
            background: white;
            border-radius: var(--border-radius);
            border: 1px solid var(--bg-tertiary);
            max-width: 70%;
            margin-bottom: 20px;
        }

        .typing-dots {
            display: flex;
            gap: 4px;
        }

        .typing-dot {
            width: 8px;
            height: 8px;
            background: var(--text-secondary);
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out;
        }

        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes typing {
            0%, 80%, 100% {
                transform: scale(0.8);
                opacity: 0.5;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }

        .welcome-message {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
        }

        .welcome-icon {
            font-size: 3rem;
            color: var(--primary-color);
            margin-bottom: 20px;
        }

        .welcome-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 10px;
        }

        .welcome-text {
            font-size: 1rem;
            line-height: 1.6;
            max-width: 400px;
            margin: 0 auto;
        }

        @media (max-width: 768px) {
            .main-container {
                grid-template-columns: 1fr;
                height: 100vh;
                gap: 0;
            }
            
            .sidebar {
                display: none;
            }
            
            .chat-area {
                border-radius: 0;
            }
            
            .chat-header {
                padding: 20px;
            }
            
            .chat-messages {
                padding: 20px;
            }
            
            .chat-input-section {
                padding: 20px;
            }
            
            .message-content {
                max-width: 85%;
            }
        }

        /* Scrollbar Styling */
        .chat-messages::-webkit-scrollbar {
            width: 6px;
        }

        .chat-messages::-webkit-scrollbar-track {
            background: var(--bg-tertiary);
            border-radius: 3px;
        }

        .chat-messages::-webkit-scrollbar-thumb {
            background: var(--primary-color);
            border-radius: 3px;
        }

        .chat-messages::-webkit-scrollbar-thumb:hover {
            background: var(--secondary-color);
        }
    </style>
</head>
<body>
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>

    <div class="main-container">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="brand-section">
                <div class="brand-logo">
                    <i class="fas fa-robot"></i>
                </div>
                <h1 class="brand-title">AI Chat</h1>
                <p class="brand-subtitle">Creative Edition</p>
            </div>

            <div class="features-section">
                <div class="feature-item">
                    <div class="feature-icon ai">
                        <i class="fas fa-brain"></i>
                    </div>
                    <span class="feature-text">Advanced AI</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon chat">
                        <i class="fas fa-comments"></i>
                    </div>
                    <span class="feature-text">Smart Conversations</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon creative">
                        <i class="fas fa-lightbulb"></i>
                    </div>
                    <span class="feature-text">Creative Solutions</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon smart">
                        <i class="fas fa-magic"></i>
                    </div>
                    <span class="feature-text">Instant Responses</span>
                </div>
            </div>

            <div class="stats-section">
                <div class="stat-item">
                    <div class="stat-number" id="message-count">0</div>
                    <div class="stat-label">Messages</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="session-time">0</div>
                    <div class="stat-label">Minutes</div>
                </div>
            </div>
        </div>

        <!-- Chat Area -->
        <div class="chat-area">
            <div class="chat-header">
                <div class="chat-header-left">
                    <div class="ai-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="chat-info">
                        <h3>AI Assistant</h3>
                        <div class="chat-status">
                            <div class="status-dot"></div>
                            <span>Online</span>
                        </div>
                    </div>
                </div>
                <div class="chat-controls">
                    <button class="control-btn" id="clear-chat" title="Clear Chat">
                        <i class="fas fa-trash"></i>
                    </button>
                    <button class="control-btn" id="export-chat" title="Export Chat">
                        <i class="fas fa-download"></i>
                    </button>
                </div>
            </div>

            <div class="chat-messages" id="chat-messages">
                <div class="welcome-message">
                    <div class="welcome-icon">
                        <i class="fas fa-hand-wave"></i>
                    </div>
                    <h2 class="welcome-title">مرحباً بك في AI Chat!</h2>
                    <p class="welcome-text">
                        أنا مساعدك الذكي الجاهز للإجابة على أسئلتك ومساعدتك في أي موضوع. 
                        ابدأ المحادثة الآن!
                    </p>
                </div>
            </div>

            <div class="chat-input-section">
                <form id="chat-form" autocomplete="off">
                    <div class="input-container">
                        <div class="input-wrapper">
                            <textarea 
                                class="chat-input" 
                                id="chat-input" 
                                placeholder="اكتب رسالتك هنا..." 
                                required 
                                autofocus
                                rows="1"
                            ></textarea>
                        </div>
                        <button class="send-btn" id="send-btn" type="submit">
                            <i class="fas fa-paper-plane"></i>
                            <span>إرسال</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chat-messages');
        const chatForm = document.getElementById('chat-form');
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        const clearChatBtn = document.getElementById('clear-chat');
        const exportChatBtn = document.getElementById('export-chat');
        const messageCountEl = document.getElementById('message-count');
        const sessionTimeEl = document.getElementById('session-time');

        let messages = [];
        let messageCount = 0;
        let sessionStartTime = Date.now();

        // Auto-resize textarea
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        // Update session time
        setInterval(() => {
            const minutes = Math.floor((Date.now() - sessionStartTime) / 60000);
            sessionTimeEl.textContent = minutes;
        }, 60000);

        function addMessage(role, content) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            
            const textDiv = document.createElement('div');
            textDiv.className = 'message-text';
            textDiv.textContent = content;
            
            const timeDiv = document.createElement('div');
            timeDiv.className = 'message-time';
            timeDiv.textContent = new Date().toLocaleTimeString('ar-SA', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
            
            contentDiv.appendChild(textDiv);
            contentDiv.appendChild(timeDiv);
            
            if (role === 'user') {
                messageDiv.appendChild(contentDiv);
                messageDiv.appendChild(avatar);
            } else {
                messageDiv.appendChild(avatar);
                messageDiv.appendChild(contentDiv);
            }
            
            // Remove welcome message if it exists
            const welcomeMessage = chatMessages.querySelector('.welcome-message');
            if (welcomeMessage) {
                welcomeMessage.remove();
            }
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            messageCount++;
            messageCountEl.textContent = messageCount;
        }

        function showTypingIndicator() {
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message ai typing-indicator';
            typingDiv.id = 'typing-indicator';
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.innerHTML = '<i class="fas fa-robot"></i>';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = `
                <div class="message-text">AI is typing</div>
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            `;
            
            typingDiv.appendChild(avatar);
            typingDiv.appendChild(contentDiv);
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function hideTypingIndicator() {
            const typingIndicator = document.getElementById('typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
        }

        function setLoading(loading) {
            if (loading) {
                sendBtn.disabled = true;
                sendBtn.innerHTML = '<div class="loading-spinner"></div><span>جاري الإرسال...</span>';
            } else {
                sendBtn.disabled = false;
                sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i><span>إرسال</span>';
            }
        }

        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const userMsg = chatInput.value.trim();
            if (!userMsg) return;
            
            addMessage('user', userMsg);
            messages.push({ role: 'user', content: userMsg });
            chatInput.value = '';
            chatInput.style.height = 'auto';
            
            setLoading(true);
            showTypingIndicator();
            
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ messages })
                });
                
                const data = await res.json();
                hideTypingIndicator();
                
                if (data.reply && data.reply.content) {
                    addMessage('ai', data.reply.content);
                    messages.push({ role: 'assistant', content: data.reply.content });
                } else {
                    addMessage('ai', 'عذراً، حدث خطأ في الرد. يرجى المحاولة مرة أخرى.');
                }
            } catch (err) {
                hideTypingIndicator();
                addMessage('ai', 'تعذر الاتصال بالخادم. يرجى التحقق من اتصالك بالإنترنت.');
            }
            
            setLoading(false);
        });

        // Clear chat functionality
        clearChatBtn.addEventListener('click', function() {
            if (confirm('هل أنت متأكد من حذف جميع الرسائل؟')) {
                messages = [];
                messageCount = 0;
                messageCountEl.textContent = '0';
                chatMessages.innerHTML = `
                    <div class="welcome-message">
                        <div class="welcome-icon">
                            <i class="fas fa-hand-wave"></i>
                        </div>
                        <h2 class="welcome-title">مرحباً بك في AI Chat!</h2>
                        <p class="welcome-text">
                            أنا مساعدك الذكي الجاهز للإجابة على أسئلتك ومساعدتك في أي موضوع. 
                            ابدأ المحادثة الآن!
                        </p>
                    </div>
                `;
            }
        });

        // Export chat functionality
        exportChatBtn.addEventListener('click', function() {
            if (messages.length === 0) {
                alert('لا توجد رسائل لتصديرها.');
                return;
            }
            
            const chatText = messages.map(msg => 
                `${msg.role === 'user' ? 'أنت' : 'AI'}: ${msg.content}`
            ).join('\\n\\n');
            
            const blob = new Blob([chatText], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `chat-export-${new Date().toISOString().slice(0, 10)}.txt`;
            a.click();
            URL.revokeObjectURL(url);
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (!sendBtn.disabled) {
                    chatForm.dispatchEvent(new Event('submit'));
                }
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(CHAT_HTML)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    messages = data.get('messages')
    if not messages or not isinstance(messages, list):
        return jsonify({"error": "Missing or invalid 'messages' list."}), 400
    
    # Simple but effective system prompt
    enhanced_messages = [
        {
            "role": "system",
            "content": (
"You are a highly advanced AI assistant designed to engage in natural, human-like conversations. "
"Your responses should be informative, friendly, and contextually relevant. "
"Always provide accurate information and clarify any ambiguities. "
"Use a tone that is respectful and engaging, and avoid overly technical jargon unless specifically requested. "
"You can also handle creative tasks and provide suggestions based on user input. "
"Remember to maintain user privacy and confidentiality in all interactions."
            )
        }
    ] + messages
    
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=enhanced_messages,
            temperature=0.7,
            max_tokens=800,
        )
        reply = completion.choices[0].message
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"error": f"عذراً، حدث خطأ في الاتصال: {str(e)}. يرجى المحاولة مرة أخرى."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)