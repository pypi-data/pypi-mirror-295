# We will use the OpenAI API to get the result of the image

import base64
import requests
import anthropic
import google.generativeai as genai
import PIL.Image

__all__ = ['get_gpt_result','encode_image','get_count','get_gpt_result2','multi_ref_prompt_openai','multi_ref_prompt_claude'
           ,'get_claude_result','get_claude_result2','get_claude_count']

prompt = "Count the number of {item} in the image and just return the number"
#gpt_prompt = f"Based on the reference image of weight {food_item_label} : {reference_image_gt}, what is the weight of the 2nd image? Please respond only in the format 'result : amount'."


# OpenAI API Key
api_key = None

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_gpt_result(image_path ,ref_image_path, api_key,prompt=prompt,detail="high"):
    # Getting the base64 string
    base64_image = encode_image(image_path)
    ref_base64_image = encode_image(ref_image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{ref_base64_image}",
                 "detail": detail
            }
            },
            {            
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                 "detail": detail
            }
            },
        ]
        }
    ],
    "max_tokens": 300}

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    return response


def get_gpt_result2(image_path , api_key,prompt=prompt,detail="high"):
    # Getting the base64 string
    base64_image = encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail" : detail
            }
            },
        ]
        }
    ],
    "max_tokens": 300}

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    return response

def get_count(response):
    try :
        result = float(response.json()['choices'][0]['message']['content'])
    except Exception as e:
        print(e)
        result = False
    return result

def multi_ref_prompt_openai(image_path, ref_image_list, api_key=None,prompt='test',detail="high"):
    """
    Multiple reference images in list format
    Args:
        image_path : str : Path to the image
        ref_image_list : list : List of reference images
        api_key : str : OpenAI API Key
        prompt : str : Prompt to be used
        detail : str : Detail of the image
    Returns:
        response : dict : Response from the API
    """

    base64_image = encode_image(image_path)
    if isinstance(ref_image_list, list):
        ref_base64_images = [encode_image(ref_image) for ref_image in ref_image_list]
    else:
        ref_base64_images = encode_image(ref_image_list)

    image_dict_data = [{"type": "text","text": prompt},
                       {"type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}",
                                      "detail": detail}
                        }]
    for i in range(len(ref_base64_images)):
        image_dict_data.append({"type":"image_url", 
                                "image_url":{"url":f"data:image/jpeg;base64,{ref_base64_images[i]}", 
                                             "detail": detail}})

    message_with_images = {"role": "user","content": image_dict_data }
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        message_with_images
        ]
    data = {
        "messages": messages,
        "model" : "gpt-4o",
        "temperature": 0.2
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
    
    response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    # print(response)
    # print(response.text)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return False
    
def multi_ref_prompt_claude(image_path, ref_image_list, api_key=None, prompt='test',max_tokens=700,temp=0.2):
    """
    Multiple reference images in list format
    Args:
        image_path : str : Path to the main image
        ref_image_list : list : List of paths to reference images
        api_key : str : Anthropic API Key
        prompt : str : Prompt to be used
    Returns:
        response : str : Response from the API
    """


    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    client = anthropic.Anthropic(api_key=api_key)

    base64_image = encode_image(image_path)
    image_data_type= "image/jpeg"

    image_dict_data = [
        {"type": "text", "text": prompt},
        { "type": "image","source":{"type": "base64", "media_type": image_data_type, "data": base64_image}}
    ]

    for ref_image in ref_image_list:
        ref_base64_image = encode_image(ref_image)
        image_val = 'Image' + str(ref_image_list.index(ref_image) + 1)
        image_dict_data.append({"type": "text", "text": image_val})
        image_dict_data.append({ "type": "image","source": {"type": "base64","media_type": image_data_type,"data": ref_base64_image}})

    try:
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=max_tokens,
            temperature=temp,
            system="You are a helpful assistant.",
            messages=[
                {
                    "role": "user",
                    "content": image_dict_data
                }
            ]
        )
        return message.content[0].text
    except anthropic.APIError as e:
        return f"Error: {e}"
    
def get_claude_result(image_path, ref_image_path, api_key, prompt,max_tokens=300,temp=0.7):
    client = anthropic.Anthropic(api_key=api_key)

    if type(image_path) == list:
        image_path = image_path[0]
    base64_image = encode_image(image_path)
    if type(ref_image_path) == list:
        ref_image_path = ref_image_path[0]
    ref_base64_image = encode_image(ref_image_path)
    image_data_type= "image/jpeg"

    content = [
        {"type": "text", "text": prompt},
        { "type": "image","source":{"type": "base64", "media_type": image_data_type, "data": ref_base64_image}},
        { "type": "image","source":{"type": "base64", "media_type": image_data_type, "data": base64_image}}
    ]

    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=max_tokens,
            temperature=temp,
            system="You are a helpful assistant. Analyze the images provided.",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return response
    except anthropic.APIError as e:
        print(f"Error: {e}")
        return None

def get_claude_result2(image_path, api_key, prompt,max_tokens=200,temp=0.7):
    client = anthropic.Anthropic(api_key=api_key)

    base64_image = encode_image(image_path)
    image_data_type = "image/jpeg"

    content = [
        {"type": "text", "text": prompt},
        { "type": "image","source":{"type": "base64", "media_type": image_data_type, "data": base64_image}}
    ]

    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=max_tokens,
            temperature=temp,
            system="You are a helpful assistant. Analyze the image provided.",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return response
    except anthropic.APIError as e:
        print(f"Error: {e}")
        return None
    

def get_claude_count(response):
    """
    Function to get float value from the response
    Args:
        response : str : Response from the API
    Returns:
        result : float : Float value
    """
    try :
        result = float(response.content[0].text)
    except Exception as e:
        print(e)
        result = False
    return result

## gemini api

def multi_ref_prompt_gemini(genai,image_path, ref_image_list,model_name="gemini-1.5-pro", prompt='test'):
    """
    Multiple reference images in list format
    Args:
        genai: gemini object
        image_path : str : Path to the main image
        ref_image_list : list : List of paths to reference images
        api_key : str : Anthropic API Key
        prompt : str : Prompt to be used
    Returns:
        response : str : Response from the API
    """
    model = genai.GenerativeModel(model_name=model_name)

    # base_image= PIL.Image.open(image_path)
    base_image = genai.upload_file(path=image_path,display_name="Base Image")
    prompt = [prompt]
    prompt.append(base_image)

    for ref_image in ref_image_list:
        display_name = "Reference Image" + str(ref_image_list.index(ref_image) + 1)
        ref_image = genai.upload_file(path=ref_image,display_name=display_name)
        prompt.append(ref_image)

    response = model.generate_content(prompt)
    return response.parts[0].text

def get_gemini_result(genai,image_path, ref_image_path,model_name="gemini-1.5-pro", prompt='test'):
    model = genai.GenerativeModel(model_name=model_name)

    base_image = genai.upload_file(path=image_path,display_name="Base Image")
    ref_image = genai.upload_file(path=ref_image_path,display_name="Reference Image")

    prompt = [prompt]
    prompt.append(base_image)
    prompt.append(ref_image)

    response = model.generate_content(prompt)
    try:
        return response.parts[0].text
    except:
        return False

def get_gemini_result2(genai,image_path,model_name="gemini-1.5-pro", prompt='test'):
    model = genai.GenerativeModel(model_name=model_name)

    base_image = genai.upload_file(path=image_path,display_name="Base Image")

    prompt = [prompt]
    prompt.append(base_image)

    response = model.generate_content(prompt)

    try:
        return response.parts[0].text
    except:
        return False
