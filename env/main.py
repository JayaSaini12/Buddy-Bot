import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
import wikipedia
import streamlit as st

nltk.download('punkt', quiet=True)

def get_wikipedia_content(topic):
    try:
        page = wikipedia.page(topic)
        return page.content
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options
        return f"Please specify your query further. Did you mean any of these: {', '.join(options)}"
    except wikipedia.exceptions.PageError:
        return "I couldn't find any information on that topic. Can you please ask something else?"
    except wikipedia.exceptions.WikipediaException:
        return "Sorry, an error occurred while fetching the Wikipedia page. Please try again later."

def greeting(text):
    text = text.lower()
    response = ['hello', 'hi', 'hey', 'hola', 'greetings']
    user = ['hi', 'hello', 'hey', 'greetings', 'hola', 'wassup']

    for word in text.split():
        if word in user:
            return random.choice(response)

def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index

def bot_response(user_input,sentence_list):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            flag = 1
            j = j + 1
        if j > 2:
            break

    if flag == 0:
        bot_response = bot_response + ' ' + "I apologize, I dont understand."
        sentence_list.remove(user_input)
    return bot_response

def main():
    st.set_page_config(page_title="Chat Bot", page_icon=":robot:")
    st.sidebar.title("Chat Bot")
    st.sidebar.markdown("I am your buddy bot. I will try to answer your queries.")

    exit_list = ["exit", "bye", "see you later", "quit"]

    topic = st.sidebar.text_input("Wikipedia Topic")
    content = get_wikipedia_content(topic)
    sentence_list = nltk.sent_tokenize(content)

    num_questions = st.sidebar.number_input("Number of questions", min_value=1, max_value=10, value=1, step=1)

    for i in range(num_questions):
        user_input = st.text_input(f"Question {i+1}", key=f"user_input_{i}", value='')

        if user_input.lower() in exit_list:
            st.write("Buddy Bot: Okay, see you later!")
            break
        else:
            if user_input != "":
                if greeting(user_input) is not None:
                    st.write("Buddy Bot: " + greeting(user_input))
                else:
                    st.write("Buddy Bot: " + bot_response(user_input,sentence_list))
    
        st.write("---")

if __name__ == '__main__':
    main()








