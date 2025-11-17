from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-nano",
#input = "Tell me the definition of domestic abuse."

)

print(response.output_text)
