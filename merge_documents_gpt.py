from openai import OpenAI
import os
import json

#dao function
def get_gpt_response(input, resp):
    
    #convert everything to string as needed by gpt
    input = str(input)
    resp = str(resp)
    
    try:
        
        os.environ['OPENAI_API_KEY'] = "get from developer"
        client = OpenAI()
        command='read '+input+' and update the new information in '+resp+'. If the json key already has data, and if nothing new is mentioned in this text then leave as is. for any key with no data just put NO_DATA_FOUND'
        command = (
            "Read the following input text: " + input + ".\n\n"
            "Then update the JSON object: " + resp + "\n\n"
            "Instructions:\n"
            "- Only update fields where new information is clearly present in the input.\n"
            "- If a key already has data and the input does not mention anything new, leave it unchanged.\n"
            "- If a key is empty and the input has no relevant information, set its value to 'NO_DATA_FOUND'.\n"
            "- Preserve the data types strictly (e.g., arrays remain arrays, strings remain strings).\n"
            "- Do not mix unrelated content across fields.\n"
            "- Return only valid, plain JSON with no markdown or explanation."
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in documentation. You will structure updates accurately into a provided JSON format."
                },
                {
                    "role": "user",
                    "content": command
                }
            ]
        )
        
        #parse response
        response_str = completion.choices[0].message.content
        
        #clean up response
        if response_str.startswith("```"):
            response_str = response_str.strip("`")
            response_str = response_str.lstrip("json\n")
        
    except Exception as e:
        return f"Error in get_gpt_response: {str(e)}"
    
    return response_str
