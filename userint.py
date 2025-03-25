import gradio as gr
import json
import asyncio
from GameManager import GameManager

# Load story data
with open("story_data.json", "r") as f:
    story_data = json.load(f)

game_manager = GameManager(api_key="key")

current_story_index = 0
current_story = []
game_over = False

async def start_game():
    global current_story, game_over

    game_manager.select_game(current_story_index)
    current_story = [story_data[current_story_index]["introduction"]]
    game_over = False
    return "\n".join(current_story)

async def next_action(action):
    global game_over
    
    if game_over:
        return "Game over. Please reset to play again."
    
    interpreted_action, output, is_conclusion = await game_manager.next_action(action)
    
    if interpreted_action:
        current_story.append(interpreted_action)
    
    current_story.append(output)
    
    if is_conclusion:

        game_over = True
        conclusion = await game_manager.generate_conclusion()
        current_story.append(conclusion)
        
    return "\n".join(current_story)

async def reset_game():
    game_manager.reset_game()
    return await start_game()

with gr.Blocks() as ui:

    gr.Markdown("# Wait, That Was an Option?")
    
    story_display = gr.Textbox(label="Story", lines=10, interactive=False)
    user_input = gr.Textbox(label="Your Action")
    
    submit_btn = gr.Button("Next")
    reset_btn = gr.Button("Reset Game")
    
    submit_btn.click(fn=next_action, inputs=user_input, outputs=story_display)
    reset_btn.click(fn=reset_game, outputs=story_display)
    
    start_game_task = asyncio.run(start_game())
    story_display.value = start_game_task

ui.launch()
