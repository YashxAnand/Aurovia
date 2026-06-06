document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn      = document.getElementById("chatbot-toggle");
    const closeBtn       = document.getElementById("chatbot-close");
    const chatbotWindow  = document.getElementById("chatbot-window");
    const chatbotForm    = document.getElementById("chatbot-form");
    const chatbotInput   = document.getElementById("chatbot-input");
    const chatbotMessages = document.getElementById("chatbot-messages");

    let isOpen = false;

    // ─── Helper: open / close with animation ───────────────────────────────
    function openChat() {
        isOpen = true;
        chatbotWindow.classList.remove("closing");
        chatbotWindow.classList.add("open");
    }

    function closeChat() {
        isOpen = false;
        chatbotWindow.classList.remove("open");
        chatbotWindow.classList.add("closing");
        chatbotWindow.addEventListener("animationend", () => {
            chatbotWindow.classList.remove("closing");
        }, { once: true });
    }

    // ─── Auto-open after intro animation completes ────────────────────────────
    function handleIntroComplete() {
        setTimeout(openChat, 800);
    }

    if (sessionStorage.getItem('introSeen')) {
        setTimeout(openChat, 1500);
    } else {
        window.addEventListener('introComplete', handleIntroComplete, { once: true });
    }

    // ─── Toggle on button click ──────────────────────────────────────────────
    toggleBtn.addEventListener("click", () => {
        isOpen ? closeChat() : openChat();
    });

    closeBtn.addEventListener("click", closeChat);

    // ══════════════════════════════════════════════════════════════════════════
    // INTENT CLASSIFIER — keyword-scoring (replaces unreliable Brain.js LSTM)
    //
    // Each intent has a list of keyword tokens. The classifier counts how many
    // tokens appear in the user message and picks the intent with the highest
    // score. Handles multi-intent messages (e.g. "pricing and contact") by
    // returning ALL matched intents above a threshold.
    // ══════════════════════════════════════════════════════════════════════════

    const INTENTS = [
        {
            name: 'greeting',
            keywords: ['hi', 'hello', 'hey', 'howdy', 'good morning', 'good afternoon',
                       'good evening', 'greetings', 'sup', 'hiya', 'namaste'],
            weight: 1.5   // boost so short greetings always win
        },
        {
            name: 'contact',
            keywords: ['phone', 'number', 'call', 'email', 'mail', 'reach', 'contact',
                       'address', 'location', 'located', 'whatsapp', 'instagram',
                       'social', 'message', 'dm', 'touch', 'get in touch', 'office',
                       'visit', 'find you', 'connect'],
            weight: 1.0
        },
        {
            name: 'pricing',
            keywords: ['price', 'pricing', 'cost', 'charge', 'charges', 'fee', 'fees',
                       'package', 'packages', 'budget', 'rate', 'rates', 'quote',
                       'expensive', 'affordable', 'cheap', 'how much', 'payment',
                       'pay', 'rupees', 'inr', 'money', 'worth'],
            weight: 1.0
        },
        {
            name: 'services',
            keywords: ['service', 'services', 'offer', 'shoot', 'shoots', 'photography',
                       'videography', 'video', 'wedding', 'pre-wedding', 'prewedding',
                       'engagement', 'party', 'birthday', 'corporate', 'event',
                       'candid', 'portrait', 'reel', 'cinematic', 'album', 'drone',
                       'what do you do', 'what you do', 'do you cover', 'do you shoot'],
            weight: 1.0
        },
        {
            name: 'about',
            keywords: ['about', 'aurovia', 'who are you', 'tell me', 'yourself',
                       'experience', 'years', 'team', 'story', 'history', 'founded',
                       'background', 'portfolio', 'work', 'style', 'approach',
                       'philosophy', 'unique', 'different', 'why choose'],
            weight: 1.0
        },
        {
            name: 'booking',
            keywords: ['book', 'booking', 'reserve', 'available', 'availability',
                       'schedule', 'date', 'slot', 'confirm', 'hire', 'appointment',
                       'enquire', 'enquiry', 'inquiry'],
            weight: 1.0
        }
    ];

    /**
     * Classify user message → returns array of matched intent names (sorted by score).
     * Falls back to ['unknown'] if nothing matches.
     */
    function classifyIntent(rawText) {
        const text = rawText.toLowerCase()
                            .replace(/[^a-z0-9\s\-]/g, ' ')  // strip punctuation
                            .replace(/\s+/g, ' ')
                            .trim();

        const scores = {};

        for (const intent of INTENTS) {
            let score = 0;
            for (const kw of intent.keywords) {
                // Check whole-word / phrase presence
                const pattern = new RegExp(`\\b${kw.replace(/[-]/g, '[-]?')}\\b`, 'i');
                if (pattern.test(text)) {
                    score += intent.weight;
                }
            }
            if (score > 0) scores[intent.name] = score;
        }

        if (Object.keys(scores).length === 0) return ['unknown'];

        // Sort by score descending; return top intents (those within 50% of top score)
        const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
        const topScore = sorted[0][1];
        const matched = sorted
            .filter(([, s]) => s >= topScore * 0.5)
            .map(([name]) => name);

        return matched;
    }

    // ─── Responses ────────────────────────────────────────────────────────────

    const RESPONSES = {
        greeting: "👋 Hello! How can I help make your big day unforgettable? Ask me about our services, pricing, or how to reach us!",
        contact:  "📞 You can reach us at **+91 9838358799**, email us at **info@auroviaproductions.com**, or DM us on Instagram [@auroviaweddings](https://instagram.com/auroviaweddings). We'd love to hear from you!",
        pricing:  "💰 Our packages are fully customised to your needs. Prices vary by event type, duration, and deliverables. Please [get in touch](get-in-touch.html) or call us for a personalised quote!",
        services: "🎬 We specialise in **Weddings**, **Pre-Weddings**, **Engagements**, **Parties & Birthdays**, and **Corporate Events** — covering both photography and cinematic videography. [See all services →](services.html)",
        about:    "📸 Aurovia is a passionate wedding photography studio with **9+ years** of experience and **1000+ smiles** captured. Our style is Clean, Consistent & Creative — blending candid moments with artful direction.",
        booking:  "📅 To check availability or book a date, please [fill out our contact form](get-in-touch.html) or call **+91 9838358799**. We recommend enquiring early as dates fill up fast!",
        unknown:  "🤔 I didn't quite catch that! I can help with:\n• **Services** we offer\n• **Pricing** & packages\n• **Booking** a session\n• **Contact** details\n• **About** Aurovia\n\nTry asking one of those!"
    };

    /**
     * Build a reply for one or more matched intents.
     * If multiple intents matched (e.g. "pricing and contact"), combine their replies.
     */
    function buildReply(intents) {
        if (intents.length === 1) return RESPONSES[intents[0]] ?? RESPONSES.unknown;

        // Deduplicate & join
        const parts = [...new Set(intents)]
            .map(i => RESPONSES[i])
            .filter(Boolean);
        return parts.join('\n\n');
    }

    // ─── Message handling ─────────────────────────────────────────────────────

    chatbotForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const msg = chatbotInput.value.trim();
        if (!msg) return;

        addMessage(msg, 'user');
        chatbotInput.value = "";

        // Show typing indicator then reply
        const typingId = showTyping();
        setTimeout(() => {
            removeTyping(typingId);
            const intents = classifyIntent(msg);
            addMessage(buildReply(intents), 'bot');
        }, 600);
    });

    // ─── UI helpers ───────────────────────────────────────────────────────────

    function addMessage(text, sender) {
        const div = document.createElement("div");
        div.style.padding       = "10px 14px";
        div.style.borderRadius  = sender === 'user' ? "12px 12px 0 12px" : "12px 12px 12px 0";
        div.style.maxWidth      = "85%";
        div.style.fontSize      = "0.88rem";
        div.style.lineHeight    = "1.5";
        div.style.opacity       = "0";
        div.style.transform     = "translateY(10px)";
        div.style.transition    = "opacity 0.3s, transform 0.3s";
        div.style.whiteSpace    = "pre-wrap";

        if (sender === 'user') {
            div.style.background = "linear-gradient(135deg, #c9a050, #a07830)";
            div.style.color      = "white";
            div.style.alignSelf  = "flex-end";
            div.textContent      = text;
        } else {
            div.style.background = "#f0ebe0";
            div.style.color      = "#333";
            div.style.alignSelf  = "flex-start";
            // Render simple markdown: **bold** and [link](url)
            div.innerHTML = renderMarkdown(text);
        }

        chatbotMessages.appendChild(div);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

        requestAnimationFrame(() => {
            div.style.opacity   = "1";
            div.style.transform = "translateY(0)";
        });
    }

    /** Render **bold** and [text](url) markdown in bot messages */
    function renderMarkdown(text) {
        return text
            // Escape HTML first
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            // Bold
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            // Links
            .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" style="color:#a07830;text-decoration:underline;" target="_self">$1</a>');
    }

    /** Show animated typing dots; returns the element so it can be removed */
    function showTyping() {
        const wrap = document.createElement("div");
        wrap.style.cssText = "display:flex;gap:4px;align-items:center;padding:10px 14px;background:#f0ebe0;border-radius:12px 12px 12px 0;align-self:flex-start;";
        wrap.dataset.typing = "1";

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement("span");
            dot.style.cssText = `width:7px;height:7px;border-radius:50%;background:#a07830;opacity:0.3;animation:typingDot 1.2s ${i * 0.2}s infinite ease-in-out;`;
            wrap.appendChild(dot);
        }

        // Inject keyframes once
        if (!document.getElementById('typing-style')) {
            const st = document.createElement('style');
            st.id = 'typing-style';
            st.textContent = '@keyframes typingDot{0%,80%,100%{opacity:0.3;transform:scale(0.8)}40%{opacity:1;transform:scale(1)}}';
            document.head.appendChild(st);
        }

        chatbotMessages.appendChild(wrap);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        return wrap;
    }

    function removeTyping(el) {
        el?.remove();
    }
});
