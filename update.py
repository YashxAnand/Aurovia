import os
import re

html_files = [
    'index.html',
    'about-us.html',
    'portfolio.html',
    'services.html',
    'blogs.html',
    'get-in-touch.html'
]

footer_html = """
    <!-- Footer -->
    <footer style="background-color: #fff; padding: 4rem 0; color: #333; border-top: 1px solid #eaeaea;">
        <div class="container">
            <div class="footer-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; align-items: center; text-align: center;">
                <div class="footer-col" style="text-align: left;">
                    <h2 style="font-family: var(--font-heading); margin-bottom: 1.5rem; color: #000;">Menu</h2>
                    <div style="display: flex; gap: 15px; margin-bottom: 1.5rem;">
                        <a href="tel:+917986288550" style="color: #000;"><i class="fa-solid fa-phone" style="font-size: 1.2rem;"></i></a>
                        <a href="https://www.instagram.com/auroviaweddings" target="_blank" style="color: #000;"><i class="fa-brands fa-instagram" style="font-size: 1.2rem;"></i></a>
                        <a href="mailto:info@auroviaproductions.com" style="color: #000;"><i class="fa-regular fa-envelope" style="font-size: 1.2rem;"></i></a>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 10px; font-weight: 500;">
                        <a href="index.html" style="color: #333; text-decoration: none;">Home</a>
                        <a href="about-us.html" style="color: #333; text-decoration: none;">About Us</a>
                        <a href="portfolio.html" style="color: #333; text-decoration: none;">Portfolio</a>
                        <a href="services.html" style="color: #333; text-decoration: none;">Services</a>
                        <a href="blogs.html" style="color: #333; text-decoration: none;">Blog</a>
                        <a href="get-in-touch.html" style="color: #333; text-decoration: none;">Get In Touch</a>
                    </div>
                </div>
                
                <div class="footer-col" style="display: flex; justify-content: center; gap: 10px;">
                    <img src="assets/front/assets/images/f-g-1.jpg" onerror="this.src='https://auroviaproductions.com/front/assets/images/f-g-1.jpg'" alt="Logo 1" style="max-height: 150px;">
                    <img src="assets/front/assets/images/f-g-2.jpg" onerror="this.src='https://auroviaproductions.com/front/assets/images/f-g-2.jpg'" alt="Logo 2" style="max-height: 150px;">
                </div>
                
                <div class="footer-col" style="text-align: left;">
                    <h2 style="font-family: var(--font-heading); margin-bottom: 1rem; color: #000;">WED GUIDE</h2>
                    <p style="margin-bottom: 1.5rem;">Subscribe to our newsletter for updates and news</p>
                    <form style="display: flex; flex-direction: column; gap: 10px;" onsubmit="event.preventDefault(); alert('Subscribed!');">
                        <input type="text" placeholder="Name" required style="padding: 10px; border: 1px solid #ddd; background: transparent; width: 100%;">
                        <input type="email" placeholder="Email Address" required style="padding: 10px; border: 1px solid #ddd; background: transparent; width: 100%;">
                        <button type="submit" style="padding: 10px; background: transparent; border: none; text-align: left; font-weight: bold; cursor: pointer; color: #000;">Subscribe</button>
                    </form>
                </div>
            </div>
            
            <div class="footer-bottom" style="text-align: center; padding-top: 3rem; margin-top: 3rem; border-top: 1px solid #eee; font-size: 0.9rem;">
                <p>&copy; Aurovia 2026 - All rights reserved.</p>
            </div>
        </div>
    </footer>
"""

whatsapp_html = """
    <!-- WhatsApp & Chatbot Widgets -->
    <a href="https://api.whatsapp.com/send?phone=917986288550" id="whatsapp" target="_blank" style="position: fixed; bottom: 20px; left: 20px; z-index: 1000; background: #25d366; color: white; width: 55px; height: 55px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: transform 0.3s ease;">
        <i class="fa-brands fa-whatsapp"></i>
    </a>

    <!-- Chatbot Toggle Button -->
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
            <div style="background: #eee; padding: 10px; border-radius: 10px; max-width: 80%; align-self: flex-start; font-size: 0.9rem;">Hi! I'm Aurovia's AI Assistant. Ask me about our wedding services, pricing, or contact details.</div>
        </div>
        <form id="chatbot-form" style="display: flex; border-top: 1px solid #eee; padding: 10px; background: white;">
            <input type="text" id="chatbot-input" placeholder="Type a message..." style="flex: 1; border: none; outline: none; padding: 5px; font-size: 0.9rem;">
            <button type="submit" style="background: none; border: none; color: var(--primary); cursor: pointer; font-size: 1.2rem;"><i class="fa-solid fa-paper-plane"></i></button>
        </form>
    </div>
    
    <script src="js/chatbot.js"></script>
"""

for file_name in html_files:
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Update Instagram link
        content = content.replace('https://www.instagram.com/aurovia51', 'https://www.instagram.com/auroviaweddings')
        
        # Replace Footer
        content = re.sub(r'<!-- Footer -->\s*<footer.*?>.*?</footer>', footer_html, content, flags=re.DOTALL)
        
        # Remove old WhatsApp & Chatbot if already exists (for idempotency)
        content = re.sub(r'<!-- WhatsApp & Chatbot Widgets -->.*?</script>\s*$', '', content, flags=re.DOTALL)
        
        # Inject WhatsApp & Chatbot before </body>
        content = content.replace('</body>', whatsapp_html + '\n</body>')
        
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
            
print("Files updated successfully.")
