from IPython.display import clear_output, display, Audio, HTML
from random import choice
import gradio as gr
import openai
import elevenlabs
import requests


crea_historial = open("/content/.historial.txt","a")
empieza = crea_historial.write("")
crea_historial.close()

if "Maria" in personaje:
  voz_eleven  = "EXAVITQu4vr4xnSDxMaL"
  descripcion_de_personaje = "María es la guía de un pueblo llamado atagarkura, ella conoce con mucho detalle la historia del pueblo, conoce múltiples puntos de interés, si tienes una duda solo acude a ella y conoceras todo por parte de la !mejor!"
  imagen_personaje = "/content/Gpt_Rol/personajes/Maria.png"
elif "Victor" in personaje:
  voz_eleven = "ErXwobaYiN019PkySvjV"
elif "Saimon" in personaje:
  voz_eleven = "pNInz6obpgDQGcFmaJgB"

def api(api_key):
  openai.api_key = api_key
  return "Enviado con exito"
  
def limpiar_texto():
  return gr.Textbox.update("")
  
def Gpt35(mensaje,api_eleven):
  ver_historial = open(".historial.txt","r")
  historial = "contexto anterior\n\n````\n"+ver_historial.read()+"````\n"

  fine_personalidad = open(f"/content/Gpt_Rol/personalidades/{personaje}.txt")
  razgo_personaje = fine_personalidad.read()

  respuesta = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages = [
        {"role":"system","content":razgo_personaje},
        {"role":"user","content":historial+mensaje}
    ]
  )

  gpt = respuesta["choices"][0]["message"]["content"]

  respuesta_historial = f"""user: {mensaje}

assistant: {gpt}"""

  with open(".historial.txt","a") as texto:
    texto.write(respuesta_historial+"\n\n")

  if api_eleven:
    CHUNK_SIZE = 1024
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voz_eleven}"

    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": f"{api_eleven}"
    }

    data = {
      "text": f"{gpt}",
      "model_id": "eleven_multilingual_v1",
      "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
      }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('.salida.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

  
  return gpt

with gr.Blocks(css="/content/Gpt_Rol/Css (CDG).css", theme=gr.themes.Soft(), title=f"GPT Rol {personaje}") as gptchat:
  gr.HTML("""<style>
  @import url('https://fonts.googleapis.com/css2?family=Pangolin&display=swap');
</style>
<h1 style="font-family: 'Pangolin', cursive;">GPT 3.5 con memoria `Rol`</h1><br>""", elem_id="titulo")

  with gr.Row(elem_id="seccion_de_lado",):
    with gr.Column(elem_id="seccion-personaje_imagen"):
      imagen = gr.Image(imagen_personaje, elem_id="imagen_personaje", show_label=False, show_share_button=False)
    with gr.Column():
      gr.HTML(f"""<style>
  @import url('https://fonts.googleapis.com/css2?family=Handlee&display=swap');
</style>
<h1 style="font-family: 'Handlee', cursive; font-size:20px">{descripcion_de_personaje}</h1>""", elem_id="descripcion_personaje")
      
  with gr.Row(elem_id="seccion_mensajes"):
    with gr.Column():
      PES_1_texto2 = gr.Textbox(label=f"{personaje}", placeholder=f"""Mensaje de {personaje}""", lines=2)
      with gr.Accordion(label="Ingresa tus Apis aqui\n", open=False, elem_id="seccion_apis"):
        PES_2_texto1 = gr.Textbox(label="API gpt", placeholder="Ingresa tu clave API de gpt",)
        PES_2_texto2 = gr.Textbox(label="API eleven (Opcional)", placeholder="Ingresa tu clave API de elevenlabs")
        PES_2_boton1 = gr.Button("Enviar")
        PES_2_texto3 = gr.Textbox(label="confirmacion")
    with gr.Column():
      PES_1_texto1 = gr.Textbox(label="Tu", placeholder="Ingresa tu mensaje", lines=2)
      PES_1_boton1 = gr.Button("Enviar")
      PES_1_boton2 = gr.Button("limpiar")


  PES_1_boton1.click(fn=Gpt35, inputs=[PES_1_texto1,PES_2_texto2], outputs=PES_1_texto2)
  PES_2_boton1.click(fn=api, inputs=PES_2_texto1, outputs=PES_2_texto3)
  PES_1_boton2.click(fn=limpiar_texto,inputs=None,outputs=PES_1_texto1)

gptchat.launch(share=True, inline=False, debug=True)
