import os
import gradio as gr
from groq import Groq


def inicializar_cliente():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("❌ GROQ_API_KEY não configurada! Configure nos Secrets do Space.")

    return Groq(api_key=api_key)


def gerar_plano(tarefa):

    if not tarefa or tarefa.strip() == "":
        return "⚠️ Por favor, digite uma tarefa válida."

    try:
        cliente = inicializar_cliente()

        prompt = f"""
        Você é um agente planejador especializado.
        Gere um plano simples, direto e passo a passo para a seguinte tarefa:
        "{tarefa}"

        Use etapas curtas, práticas e numeradas.
        Seja claro e objetivo.
        """

        resposta = cliente.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return resposta.choices[0].message.content

    except Exception as e:
        return f"❌ Erro ao gerar plano: {str(e)}\n\nVerifique se a chave da API está configurada corretamente nos Settings → Variables and secrets."



with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🤖 Mini Agente de Planejamento com IA

        Descreva sua tarefa e receba um plano de ação detalhado gerado por inteligência artificial!

        **Powered by:** Llama 3.3 70B (via Groq API)
        """
    )

    with gr.Row():
        with gr.Column():
            tarefa_input = gr.Textbox(
                label="📋 Digite sua tarefa",
                placeholder="Exemplo: criar um aplicativo web de tarefas, planejar viagem para o Japão, estudar Python...",
                lines=3
            )

            btn_gerar = gr.Button("✨ Gerar Plano", variant="primary", size="lg")

    with gr.Row():
        plano_output = gr.Textbox(
            label="📝 Plano Gerado",
            lines=15,
            show_copy_button=True
        )


    btn_gerar.click(
        fn=gerar_plano,
        inputs=tarefa_input,
        outputs=plano_output
    )


    gr.Examples(
        examples=[
            ["criar um aplicativo web de tarefas"],
            ["plano de estudos para aprender Python em 3 meses"],
            ["organizar viagem para o Japão por 15 dias"],
            ["iniciar canal no YouTube sobre tecnologia"],
            ["desenvolver um e-commerce do zero"]
        ],
        inputs=tarefa_input
    )

    gr.Markdown(
        """
        ---
        💡 **Dica:** Seja específico na sua descrição para obter planos mais detalhados!
        """
    )


if __name__ == "__main__":
    demo.launch()