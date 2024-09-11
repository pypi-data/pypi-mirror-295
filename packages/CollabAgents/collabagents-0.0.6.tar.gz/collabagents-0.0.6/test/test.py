import os
import asyncio
import nest_asyncio
from CollabAgents.helper import print_colored
from CollabAgents.agent import StructuredAgent
from CollabAgents.models import OpenaiChatModel
from CollabAgents.tools.FileOperationsTool import SaveFile, CreateFolder
from CollabAgents.memory import ConversationSummaryBufferMemory,ConversationSummaryMemory,ConversationBufferWindowMemory,ConversationBufferMemory

nest_asyncio.apply()

# Step 1: This concise description helps in understanding the agent's responsibilities and guides the system 
# in determining what types of tasks should be assigned to this agent. 
description = "Responsible for writing story."

# Step 2: Provide instructions for the agent (System Prompt)
instruction = "You are a creative storyteller who crafts imaginative narratives with vivid details, rich characters, and unexpected plot twists."

# Step 3: Load pre-defined tools that the agent will use
# These tools enable the agent to create folders and save files
tools = [CreateFolder, SaveFile]

# Step 4: Set your OpenAI API key
openai_api_key = "You API Key"

# openai_api_key = os.getenv('OPENAI_API_KEY')

# Step 5: Initialize the language model for the agent
model = OpenaiChatModel(model_name="gpt-4o-mini", api_key=openai_api_key, temperature=0)

# Step 6: Initialize memory - 4 different techniques are available.

# This option retains the entire conversation history. 
# Use this when you need to maintain a complete record of all interactions without any summarization or truncation.
memory = ConversationBufferMemory()        

# This option retains only the last K messages in the conversation.
# Ideal for scenarios where you want to limit memory usage and only keep the most recent interactions.
# memory = ConversationBufferWindowMemory(last_k=3)    

# This option automatically summarizes the conversation once it exceeds a specified number of messages.
# Use this to manage lengthy conversations by creating concise summaries while retaining overall context.
# memory = ConversationSummaryMemory(number_of_messages=5)   


# This option combines summarization with selective message retention. It summarizes the conversation after a certain point and retains only the most recent N messages.
# Perfect for balancing context preservation with memory constraints by keeping key recent interactions while summarizing earlier ones.
# memory = ConversationSummaryBufferMemory(buffer_size=5)    

# Step 7: Initialize the agent with the model, description, instructions, and tools. Set verbose to True to see the steps by step actions.
agent = StructuredAgent(model=model, agent_name="AI Assistant", agent_description=description, agent_instructions=instruction, tools=tools, assistant_agents=[],max_allowed_attempts=50, verbose=True,memory=memory)

if __name__ =="__main__":

    async def main():

        print_colored("Starting the application...........", "green")

        # Example user input
        user_input = "Create a story about AI agents and save it in a new folder. The story should have two chapters, and each chapter should be saved separately inside the folder"

        # Initialize the messages list to store conversation history
        messages = []

        # Step 8: Process user input and interact with the agent
        while user_input != "bye":

            # The agent processes the user input and generates a response
            output = agent.run(user_input, messages)

            # Update the messages list with the agent's response
            messages = agent.messages

            # If verbose=False is set during agent initialization, uncomment the following line to see the agent's responses
            # print_colored(f"Assistant : {output}", "purple")

            # Prompt the user for the next input
            user_input = input("User Input : ")

    asyncio.run(main())