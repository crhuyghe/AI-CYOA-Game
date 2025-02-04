from openai import OpenAI

key = "<key>"
client = OpenAI(api_key=key)

prompt = "Looking at the user's reaction to a scenario, return whether the user's character will survive. Format the output as JSON. For example, {\"survive\": <boolean value>}"

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": "I choose to self-destruct"
        },
        {
            "role": "assistant",
            "content": '{"survive": false}'
        },
        {
            "role": "user",
            "content": input()
        },

    ]
)

print(completion.choices[0].message.content)
