import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer

# Ensure that necessary NLTK resources are downloaded
try:
    nltk.download('punkt')
    nltk.download('wordnet')
except Exception as e:
    print(f"Error downloading NLTK resources: {e}")
    exit()

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents file (PATH UPDATED)
try:
    with open('C:/Users/TOSHIBA/Desktop/chatbot/chatbot/intents.json', 'r') as file:
        intents = json.load(file)
except Exception as e:
    print(f"Error opening or reading intents file: {e}")
    exit()

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',', 'a', 'the']

# Process each intent in the JSON file
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word in the sentence
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list) 
        documents.append((word_list, intent['tag'])) 
    if intent['tag'] not in classes:
        classes.append(intent['tag'])

# Lemmatize and lower each word and remove duplicates
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

# Save words and classes to pickle files
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Create training data
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1 if word in word_patterns else 0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append(bag + output_row)

# Shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)

# Create train and test lists. X - patterns, Y - intents
train_x = training[:, :len(words)]
train_y = training[:, len(words):]

# Create model - 3 layers
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, input_shape=(len(train_x[0]),), activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(train_y[0]), activation='softmax')
])

# Compile model
sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Fitting and saving the model
hist = model.fit(train_x, train_y, epochs=300, batch_size=10, verbose=1)
model.save('chatbot_model.h5')

print('Model training completed and saved.')
