# Simulation of Human Behavior Through LLM-Based Autonomous Agents
This project comes in the form of a simulated town where each person will act in a human way through prompting LLMs.

For the LLM, we are using Llama 3.1 with the Ollama Python package. The game visuals use PyGame, a Python game development library.

To run the code, you must first install Ollama from https://ollama.com/ and run `pip install pygame` to install PyGame. Then you can simply run `python main.py` to execute our code and run the simulation. The `main.py` handles basically all of how the agents can interact with each other. The Agents folder contains classes for different possible parts of the environment, the Dialogue folder contains behaviour for how dialogue boxes should be rendered, and the Prompts folder contain the text files for agent bios.
