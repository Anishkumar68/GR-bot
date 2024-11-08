# gift-chatbot

# GR-bot

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
   ```

3. **Install the packages listed in the new `requirements.txt`**:
   ```bash
   pip install -r requirements.txt
   ```

By following these steps, you should be able to resolve the `numpy` installation error and successfully install the required packages for your project.

---
