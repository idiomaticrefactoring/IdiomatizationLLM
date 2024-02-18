import openai, tiktoken,traceback
from retry import retry
# openai.api_key = "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"#"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"  # os.getenv("OPENAI_API_KEY")
# openai.api_key = "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"#"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"  # os.getenv("OPENAI_API_KEY")
# openai.api_key = "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"#"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"  # os.getenv("OPENAI_API_KEY")
openai.api_key ="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"
MAX_TOKENS=4097
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            # print("encode value: ",value,encoding.encode(value))
            decoder_value = [encoding.decode_single_token_bytes(token) for token in encoding.encode(value)]
            # print("decoder_value: ",decoder_value)

            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def format_message(prompt,examples=None,sys_msg=None):
    messages=[]
    if sys_msg:
        messages.append({"role": "system",
             "content": sys_msg})
    if examples:
        '''
        https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
          {"role": "user", "content": "Help me translate the following corporate jargon into plain English."},
        {"role": "assistant", "content": "Sure, I'd be happy to!"},
        '''
        for user_prompt,response in examples:
            messages.extend([
            {"role": "system", "name": "example_user",
             "content": user_prompt},
            {"role": "system", "name": "example_assistant",
             "content": str(response)}])
    messages.append( {"role": "user", "content": prompt})
    return messages

def format_message_2(prompt,examples=None,sys_msg=None):
    messages=[]
    if sys_msg:
        messages.append({"role": "system",
             "content": sys_msg})
    if examples:
        '''
        https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
          {"role": "user", "content": "Help me translate the following corporate jargon into plain English."},
        {"role": "assistant", "content": "Sure, I'd be happy to!"},
        '''
        for user_prompt,response in examples:
            messages.extend([
            {"role": "user",
             "content": user_prompt},
            {"role": "assistant",
             "content": str(response)}])
    messages.append( {"role": "user", "content": prompt})
    return messages


@retry(delay=0, tries=6,backoff=1, max_delay=120)
def chatGPT_result(messages,model="gpt-3.5-turbo-0301"):
    '''
    https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb

To help clarify that the example messages are not part of a real conversation, and shouldn't be referred back to by the model,
you can try setting the name field of system messages to example_user and example_assistant.

Transforming the few-shot example above, we could write:

In [9]:
# The business jargon translation example, but with example names for the example messages
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."},
        {"role": "system", "name":"example_user", "content": "New synergies will help drive top-line growth."},
        {"role": "system", "name": "example_assistant", "content": "Things working well together will increase revenue."},
        {"role": "system", "name":"example_user", "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
        {"role": "system", "name": "example_assistant", "content": "Let's talk later when we're less busy about how to do better."},
        {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
    ],
    temperature=0,
)

print(response["choices"][0]["message"]["content"])
    '''
    # example token count from the OpenAI API
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
        request_timeout=120
    )
    # print("response: ",response)
    # print(f'{response["usage"]["prompt_tokens"]} prompt tokens used.')
    return response

def get_response_content(response):
    try:
        resp_content = response["choices"][0]["message"]["content"]

    except:
        resp_content = traceback.format_exc()

    return resp_content

def get_sys_examp_user(msg):
    example_list=[]
    print("msg: ",msg)
    sys_msg=""
    for each_dict in msg[:-1]:
        print("each_dict: ",each_dict)
        role=each_dict["role"]
        if 'system'==role:
            sys_msg=each_dict["content"]
        elif role=='user':
            example_list.append(each_dict["content"])
        elif role=='assistant':
            example_list[-1]+="\n******ASSISTANT******\n"+each_dict["content"]
    example_str="\n>>>>>>>>>Example\n".join(example_list)
    user_str=msg[-1]["content"]
    print("sys_msg,example_str,user_str: ",sys_msg,example_str,user_str)
    return sys_msg,example_str,user_str