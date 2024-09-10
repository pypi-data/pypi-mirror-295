import json
import os
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from openai import OpenAI
from datetime import datetime
from rich.live import Live
from rich.markdown import Markdown

try:
    os.getenv("SILICONFLOW_API_KEY")
except KeyError:
    raise ValueError("SILICONFLOW_API_KEY is not set")


# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"), base_url="https://api.siliconflow.cn/v1"
)


def get_system_prompt(default_system_message):
    return Prompt.ask("Enter system prompt", default=default_system_message)


def update_system_prompt(default_system_message, conversation_history):
    new_prompt = get_system_prompt(default_system_message)
    conversation_history[0] = {"role": "system", "content": new_prompt}


def save_conversation(model, conversation_history):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}_{model}.json"
    save_path = Path.home() / ".local/share/chat" / filename

    with open(save_path, "w") as f:
        json.dump(conversation_history, f, indent=2)
    return save_path


def chat():
    # Read the selected model from the JSON file
    model_file_path = Path.home() / ".local/share/chat/selected_model.json"
    with open(model_file_path, "r") as f:
        selected_model = json.load(f)
    model = (selected_model["id"],)

    # Create a Rich console
    console = Console()

    # Display the selected model
    console.print(f"Using model: {selected_model['id']}", style="bold blue")
    default_system_message = "You are a helpful AI assistant."
    conversation_history = [{"role": "system", "content": default_system_message}]

    console.print(
        "Chat started. Type 'exit' to end, 'system' to view/change the system prompt.",
        style="bold cyan",
    )

    while True:
        # Ask the user for a message
        user_message = Prompt.ask("You", default="exit")

        if user_message.lower() == "exit":
            save_path = save_conversation(model, conversation_history)
            console.print(f"Conversation saved to: {save_path}", style="bold green")
            console.print("Goodbye!", style="bold yellow")
            break
        elif user_message.lower() == "system":
            console.print(
                f"Current system prompt: {conversation_history[0]['content']}",
                style="bold magenta",
            )
            if (
                Prompt.ask(
                    "Do you want to update the system prompt?",
                    choices=["y", "n"],
                    default="n",
                )
                == "y"
            ):
                update_system_prompt(
                    default_system_message, conversation_history, console
                )
                console.print(
                    f"System prompt updated to: {conversation_history[0]['content']}",
                    style="bold yellow",
                )
            continue

        # Add user message to conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # Send the message to the OpenAI API with streaming
        try:
            stream = client.chat.completions.create(
                model=model, messages=conversation_history, stream=True
            )

            console.print("AI:", style="bold green", end="")

            full_response = ""
            with Live(Markdown(full_response), refresh_per_second=4) as live:
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        live.update(Markdown(full_response))

            # Add AI's response to conversation history
            conversation_history.append({"role": "assistant", "content": full_response})

        except Exception as e:
            console.print(f"An error occurred: {str(e)}", style="bold red")


if __name__ == "__main__":
    chat()
