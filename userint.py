import gradio as gr
import json
import asyncio
from GameManager import GameManager

# Load story data
with open("story_data.json", "r") as f:
    story_data = json.load(f)

gm = GameManager(api_key="key")

current_story_index = 0
game_over = False

async def start_game():
    global game_over

    gm.select_game(current_story_index)
    game_over = False
    return "\n\n".join(gm.current_story), gm.get_story_status(conclusion=False)

async def next_action(action):
    global game_over

    if game_over:
        await gm.generate_conclusion()
        return "\n\n".join(gm.current_story), gr.update(value=""), gr.update()
    else:
        _, is_conclusion = await gm.next_action(action)

        if is_conclusion:
            update = (gr.update(value="", interactive=False), gr.update(value="Finish", interactive=True))
            game_over = True

        else:
            update = (gr.update(value=""), gr.update(interactive=True))

        return "\n\n".join(gm.current_story), gm.get_story_status(conclusion=False), *update

async def reset_game():
    gm.reset_game()
    return await start_game()

with gr.Blocks(theme="citrus") as ui:

    gr.Markdown("# Wait, That Was an Option?")

    story_display = gr.Textbox(label="Story", lines=10, interactive=False)
    user_input = gr.Textbox(label="Your Action")

    submit_btn = gr.Button("Next")
    reset_btn = gr.Button("Reset Game")

    status_display = gr.Textbox(label="Status", lines=10, interactive=False)

    user_input.submit(fn=next_action, inputs=user_input, outputs=[story_display, user_input])
    submit_btn.click(fn=lambda: (gr.update(interactive=False), gr.update(interactive=False)), outputs=[submit_btn, reset_btn]).then(fn=next_action, inputs=user_input, outputs=[story_display, status_display, user_input, submit_btn]).then(fn=lambda: gr.update(interactive=True), outputs=[reset_btn])
    reset_btn.click(fn=lambda: (gr.update(interactive=False), gr.update(interactive=False)), outputs=[submit_btn, reset_btn]).then(fn=reset_game, outputs=[story_display, status_display]).then(fn=lambda: (gr.update(value="Next", interactive=True), gr.update(interactive=True), gr.update(interactive=True)), outputs=[submit_btn, reset_btn, user_input])

    start_game_task = asyncio.run(start_game())
    story_display.value = start_game_task[0]
    status_display.value = start_game_task[1]


ui.launch()
