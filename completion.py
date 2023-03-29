import os
import openai
openai.organization = "org-Spv6866zY4nPaWVWmzmOnauG"
openai.api_key = os.getenv("OPENAI_API_KEY")
models = openai.Model.list()
print(models)
