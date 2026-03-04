import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from config import system_prompt, MAX_ITERATIONS
from functions.call_function import available_functions, call_fucntion

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
  
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    user_prompt = args.user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    for _ in range(MAX_ITERATIONS):

        response = client.models.generate_content(model="gemini-2.5-flash", 
                                                contents= messages,
                                                config=types.GenerateContentConfig(system_instruction=system_prompt,
                                                                                    tools=[available_functions]))
        
        
        for candidate in response.candidates:
            messages.append(candidate.content)

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        
        if response.usage_metadata == None:
            raise RuntimeError("response.usage_metadata is None, check for API error")
        
        if response.function_calls == None:
            if args.verbose:
                print(f"User Prompt: {user_prompt}")
                print(f"Propt Tokens: {prompt_tokens}")
                print(f"Response Tokens: {response_tokens}")
                
            print(f"Response: {response.text}")
            return
        else:
            function_call_results = []
            for call in response.function_calls:
                call_result = call_fucntion(call, args.verbose)
                if not call_result.parts:
                    raise Exception("call_result.parts is empty")
                if call_result.parts[0].function_response == None:
                    raise Exception("FunctionResponse object missing ('None')")
                if call_result.parts[0].function_response.response == None:
                    raise Exception("FunctionResponse.response is missing ('None')")
                function_call_results.append(call_result.parts[0])

                messages.append(types.Content(role="user", parts=function_call_results))
    
    print("did not finish after max iterations")
    exit(1)

if __name__ == "__main__":
    main()
