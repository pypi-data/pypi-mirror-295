from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="o1-preview",
    messages=[
        {
            "role": "user", 
            "content": "Write a bash script that takes a matrix represented as a string with format '[1,2],[3,4],[5,6]' and prints the transpose in the same format."
        }
    ]
)
#output = self.sync_client.chat.completions.create(
print(response.choices[0].message.content)