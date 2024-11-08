# gift-chatbot

# GR-bot

Gifty: Your Personal Gift Recommendation Chatbot 🎁

Finding the perfect gift just got easier with Gifty. Simple, direct, and to the point, Gifty provides personalized gift suggestions for any occasion and recipient. Whether it's a birthday, anniversary, holiday, or just because, let Gifty help you discover the ideal present with ease. Start chatting and find the perfect gift today!


Fig : interface of the chatbot

![image](https://github.com/user-attachments/assets/a968df4b-c1e6-4753-a8fb-3b7c8c0ad8c9)

### Handling Installation Errors with `requirements.txt`

When installing packages using `requirements.txt`, you may encounter an error with the installation of `numpy`. To address this issue, follow these steps:

1. **Install `numpy` manually**:

   ```bash
   pip install numpy
   ```

2. **Create a new `requirements.txt` file** and add the following packages:

   ```
   django
   python-dotenv
   langchain
   openai
   pinecone-client
   spacy
   requests
   beautifulsoup4
   en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl#sha256=1932429db727d4bff3deed6b34cfc05df17794f4a52eeb26cf8928f7c1a0fb85
   ```

3. **Install the packages listed in the new `requirements.txt`**:
   ```bash
   pip install -r requirements.txt
   ```

By following these steps, you should be able to resolve the `numpy` installation error and successfully install the required packages for your project.

---
