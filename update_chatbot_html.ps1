$files = @('index.html', 'about-us.html', 'portfolio.html', 'services.html', 'blogs.html', 'get-in-touch.html')

$oldToggle = '    <!-- Chatbot Toggle Button -->
    <div id="chatbot-toggle" style="position: fixed; bottom: 20px; right: 20px; z-index: 1000; background: var(--primary); color: white; width: 55px; height: 55px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: pointer; transition: transform 0.3s ease;">
        <i class="fa-solid fa-message"></i>
    </div>

    <!-- Chatbot Window -->
    <div id="chatbot-window" style="display: none; position: fixed; bottom: 85px; right: 20px; z-index: 1000; width: 300px; height: 400px; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); overflow: hidden; flex-direction: column; font-family: var(--font-body);">
        <div style="background: var(--primary); color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: bold;">Aurovia Assistant</span>
            <i class="fa-solid fa-xmark" id="chatbot-close" style="cursor: pointer;"></i>
        </div>
        <div id="chatbot-messages" style="flex: 1; padding: 15px; overflow-y: auto; background: #f9f9f9; display: flex; flex-direction: column; gap: 10px;">
            <div style="background: #eee; padding: 10px; border-radius: 10px; max-width: 80%; align-self: flex-start; font-size: 0.9rem;">Hi! I''m Aurovia''s AI Assistant. Ask me about our wedding services, pricing, or contact details.</div>
        </div>
        <form id="chatbot-form" style="display: flex; border-top: 1px solid #eee; padding: 10px; background: white;">
            <input type="text" id="chatbot-input" placeholder="Type a message..." style="flex: 1; border: none; outline: none; padding: 5px; font-size: 0.9rem;">
            <button type="submit" style="background: none; border: none; color: var(--primary); cursor: pointer; font-size: 1.2rem;"><i class="fa-solid fa-paper-plane"></i></button>
        </form>
    </div>'

$newWidget = '    <!-- Chatbot Button + Window -->
    <div class="chatbot-btn-wrap">
        <span class="chatbot-label">Chat with us 📸</span>
        <button id="chatbot-toggle" aria-label="Open chat">
            <span class="chatbot-icon">📷</span>
        </button>
    </div>

    <!-- Chatbot Window -->
    <div id="chatbot-window">
        <div class="chatbot-header">
            <div class="chatbot-header-info">
                <div class="chatbot-avatar">📷</div>
                <div class="chatbot-header-text">
                    <h4>Aurovia Assistant</h4>
                    <p>📸 Your wedding photography guide</p>
                </div>
            </div>
            <button class="chatbot-close-btn" id="chatbot-close" aria-label="Close chat">&#10005;</button>
        </div>
        <div id="chatbot-messages" style="flex: 1; padding: 15px; overflow-y: auto; background: #fafaf8; display: flex; flex-direction: column; gap: 10px;">
            <div style="background: #f0ebe0; padding: 10px 14px; border-radius: 12px 12px 12px 0; max-width: 85%; align-self: flex-start; font-size: 0.88rem; line-height: 1.5;">👋 Hi! I''m Aurovia''s AI photographer assistant. Ask me about services, pricing, or contact details!</div>
        </div>
        <form id="chatbot-form" style="display: flex; border-top: 1px solid #eee; padding: 10px 12px; background: white; gap: 8px; align-items: center;">
            <input type="text" id="chatbot-input" placeholder="Ask something..." style="flex: 1; border: 1px solid #eee; border-radius: 20px; outline: none; padding: 8px 14px; font-size: 0.88rem; font-family: inherit; background: #fafafa;">
            <button type="submit" style="background: linear-gradient(135deg, #c9a050, #a07830); border: none; color: white; cursor: pointer; font-size: 1rem; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><i class="fa-solid fa-paper-plane"></i></button>
        </form>
    </div>'

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        if ($content -match [regex]::Escape('id="chatbot-toggle"')) {
            $content = $content -replace [regex]::Escape($oldToggle), $newWidget
            Set-Content -Path $file -Value $content -Encoding UTF8
        }
    }
}
Write-Host "Done"
