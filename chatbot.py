import nltk
import random
import json
import pickle
import numpy as np
import tkinter as tk
from tkinter import scrolledtext, messagebox
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

# Download NLTK data (only once)
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')

# Load intents
with open(r'C:/Users/TOSHIBA/Desktop/chatbot/chatbot/intents.json', 'r') as file:
    intents = json.load(file)

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

# === NLP Functions ===
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    return [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence, words, classes):
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]

def get_response(intents_list, intents_json):
    if not intents_list:
        return "I'm not sure how to help with that. Can you rephrase?"
    tag = intents_list[0]['intent']
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "Sorry, I do not understand."

# === MAIN CHAT WINDOW ===
def open_chat_window():
    welcome_window.destroy()  # Close welcome screen
    chat_window = tk.Tk()
    chat_window.title("SheBot")
    chat_window.geometry("650x550")
    chat_window.configure(bg='white')  # Whole background white

    def send_message(event=None):
        user_input = message_entry.get().strip()
        if not user_input:
            return
        message_entry.delete(0, tk.END)

        chat_area.config(state='normal')
        chat_area.insert(tk.END, f"\nYou: {user_input}\n", 'user_tag')

        ints = predict_class(user_input, words, classes)
        response = get_response(ints, intents)

        # === Emergency Flag Logic ===
        if ints and ints[0]['intent'] == 'emergency':
            response += "\n\n⚠ This may be serious. Please visit a doctor immediately."
            messagebox.showwarning("Emergency Alert", "Your symptoms may be serious. Please consult a doctor right away.")

        chat_area.insert(tk.END, f"SheBot: {response}\n", 'bot_tag')
        chat_area.config(state='disabled')
        chat_area.see(tk.END)

    # Title: Chat with SheBot (Pink Box)
    title_label = tk.Label(chat_window, text="Chat with SheBot", font=("Helvetica", 20, "bold"), bg='#ff4081', fg="white", pady=10)
    title_label.pack(fill=tk.X)

    # Chat Area
    chat_area = scrolledtext.ScrolledText(chat_window, wrap=tk.WORD, font=("Arial", 12), bg="#fdfbff", fg="black", state='disabled', padx=10, pady=10, relief='flat')
    chat_area.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

    # Styling
    chat_area.tag_configure('user_tag', foreground='white', background='#ff4081', font=('Arial', 12, 'bold'), lmargin1=10, lmargin2=10, spacing3=5)
    chat_area.tag_configure('bot_tag', foreground='black', background='white', font=('Arial', 12), lmargin1=10, lmargin2=10, spacing3=10)

    # Input Area
    input_frame = tk.Frame(chat_window, bg="white")
    input_frame.pack(padx=10, pady=10, fill=tk.X)

    message_entry = tk.Entry(input_frame, font=('Arial', 14), bd=2, relief='solid')
    message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=6)
    message_entry.bind("<Return>", send_message)

    send_button = tk.Button(input_frame, text="Send", font=('Arial', 12, 'bold'), bg='#6ab04c', fg='white', padx=15, pady=5, relief='flat', command=send_message)
    send_button.pack(side=tk.RIGHT)

    chat_window.mainloop()

# === WELCOME SCREEN ===
welcome_window = tk.Tk()
welcome_window.title("SheBot")
welcome_window.geometry("600x400")
welcome_window.configure(bg="white")  # Whole background white

# Top Title Pink Box
title_frame = tk.Frame(welcome_window, bg="#ff4081")
title_frame.pack(fill=tk.X)

title = tk.Label(title_frame, text="SHEBOT", font=("Helvetica", 24, "bold"), bg="#ff4081", fg="white", pady=15)
title.pack(fill=tk.X)

# Rest white area
welcome_msg = tk.Label(welcome_window, text="Welcome to SheBot", font=("Arial", 16), bg="white", fg="#333")
welcome_msg.pack(pady=(40, 10))

sub_msg = tk.Label(welcome_window, text="Start here to ask your questions", font=("Arial", 12), bg="white", fg="#333")
sub_msg.pack(pady=(0, 30))

start_btn = tk.Button(welcome_window, text="Start", font=("Arial", 14, "bold"), bg="#6c5ce7", fg="white", padx=20, pady=10, relief='flat', command=open_chat_window)
start_btn.pack()

welcome_window.mainloop()