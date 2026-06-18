import os
from dotenv import load_dotenv
from google import genai
from prediction_engine import predict_capacity  # Import your prediction tool

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    print("Error: Could not find API_KEY in .env file.")
    exit()

# Initialize the client
client = genai.Client(api_key=api_key)

def start_smartech1():
    print("Smartech1 is ready! (Type 'quit' to exit)")
    model_name = "gemini-1.5-flash"
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        
        # Smartech1 Prediction Logic
        # Smartech1 Prediction Logic
        if "predict" in user_input.lower():
            print("Please enter the values separated by commas (Amine, Area, Humidity, Temp):")
            raw_input = input("Values: ") 
            
            try:
                # This turns your typed numbers into the format the model needs
                params = [float(p.strip()) for p in raw_input.split(",")]
                
                if len(params) == 4:
                    result = predict_capacity(params[0], params[1], params[2], params[3])
                    print(f"Smartech1: The predicted CO2 capacity is {result} mmol/g.")
                else:
                    print("Error: Please provide exactly 4 values (Amine, Area, Humidity, Temp).")
            except ValueError:
                print("Error: Please make sure you only enter numbers separated by commas.")
        else:
            # Standard chat logic
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_input
                )
                print(f"Smartech1: {response.text}")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_smartech1()