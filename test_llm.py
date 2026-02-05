from groq import Groq

client = Groq()

resp = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Say OK"}]
)

print(resp.choices[0].message.content)
