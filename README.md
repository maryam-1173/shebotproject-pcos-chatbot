# shebotproject-pcos-chatbot
ai project
# SHE BOT – PCOS Chatbot

## Overview

SHE BOT is a desktop-based chatbot developed in Python to provide basic guidance and awareness about Polycystic Ovary Syndrome (PCOS). The chatbot answers user questions related to PCOS, including symptoms, causes, diagnosis, treatment, diet, lifestyle, and general health information.

Note: This chatbot is developed for educational and awareness purposes only. It should not be considered a substitute for professional medical advice, diagnosis, or treatment.

---

## Project Description

The chatbot uses Natural Language Processing (NLP) and Machine Learning techniques to understand user queries and provide relevant responses from a custom dataset. It is designed to work offline after the required files have been generated.

This project was developed as a **4th Semester Python Project** by Software Engineering students.

---

## Features

- Desktop-based chatbot application
- Text-based conversation interface
- Answers PCOS-related questions
- Provides information about symptoms, causes, treatment, diet, and lifestyle
- Uses a custom dataset for training
- Works offline after setup
- User-friendly interface

---

## Technologies Used

- Python 3.x
- Tkinter
- TensorFlow / Keras
- NLTK
- NumPy
- JSON
- Pickle

---

## Project Structure

```text
SHE-BOT/
│── chatbot.py
│── training.py
│── intents.json
│── chatbot_model.h5
│── words.pkl
│── classes.pkl
│── requirements.txt
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/SHE-BOT-PCOS-Chatbot.git
cd SHE-BOT-PCOS-Chatbot
```

### Install the required libraries

```bash
pip install -r requirements.txt
```

### Train the model (Optional)

If you modify the `intents.json` file, retrain the chatbot.

```bash
python training.py
```

### Run the chatbot

```bash
python chatbot.py
```

---

## Sample Questions

- What is PCOS?
- What are the symptoms of PCOS?
- What causes PCOS?
- Can PCOS be treated?
- What foods are recommended for PCOS?
- How can I manage PCOS naturally?
- Does PCOS affect fertility?
- What exercises are good for PCOS?

---

## Future Enhancements

- Voice input and output
- Multi-language support
- Improved NLP accuracy
- Web-based application
- Mobile application
- AI-powered conversational responses

---

## Authors

**Maryam Arif**  
Software Engineering Student  
National Textile University, Faisalabad

**Marium Fatima**  
Software Engineering Student  
National Textile University, Faisalabad

---

## License

This project was developed for educational purposes as part of a university semester project.
