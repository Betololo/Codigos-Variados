import tkinter as tk
from tkinter import ttk
import keyboard
import pyautogui
import math
from PIL import Image, ImageTk 

#TENTARIVA DE ARRUMAR O TEMPO


# Função para calcular a velocidade inicial com base na componente x e no ângulo
def calcular_velocidade_inicial(aceleracao_vento_x, alcance, diferenca, angulo_radianos, aceleracao_total_y):
    velocidade_inicial = math.sqrt((2 * (alcance + diferenca) * (aceleracao_total_y**2)) / (-4 * math.cos(angulo_radianos) * (math.sin(angulo_radianos)* aceleracao_total_y) - (4 * aceleracao_vento_x * (math.sin(angulo_radianos)*(math.sin(angulo_radianos))))))
    return velocidade_inicial


# Função para mapear a velocidade normalizada
def mapear_velocidade_normalizada(velocidade, velocidade_minima, velocidade_maxima):
    return (velocidade - velocidade_minima) / (velocidade_maxima - velocidade_minima) * 4.0


# Função para aumentar a gravidade
def aumentar_gravidade():
    gravidade_value = float(gravidade_entry.get())
    gravidade_entry.delete(0, tk.END)
    gravidade_entry.insert(0, gravidade_value + 10)

# Função para diminuir a gravidade
def diminuir_gravidade():
    gravidade_value = float(gravidade_entry.get())
    gravidade_entry.delete(0, tk.END)
    gravidade_entry.insert(0, gravidade_value - 10)

# Função para aumentar angulo
def aumentar_angulo():
    angulo_value = float(angulo_entry.get())
    angulo_entry.delete(0, tk.END)
    angulo_entry.insert(0, angulo_value + 1)

# Função para diminuir angulo
def diminuir_angulo():
    angulo_value = float(angulo_entry.get())
    angulo_entry.delete(0, tk.END)
    angulo_entry.insert(0, angulo_value - 1)

# Função para aumentar forca vento
def aumentar_vento():
    vento_value = float(forcavento_entry.get())
    forcavento_entry.delete(0, tk.END)
    forcavento_entry.insert(0, vento_value + 1)

# Função para diminuir forca vento
def diminuir_vento():
    vento_value = float(forcavento_entry.get())
    forcavento_entry.delete(0, tk.END)
    forcavento_entry.insert(0, vento_value - 1)

# Função para aumentar fator
def aumentar_fator():
    fator_value = float(fator_entry.get())
    fator_entry.delete(0, tk.END)
    fator_entry.insert(0, fator_value + 0.05)

# Função para diminuir fator
def diminuir_fator():
    fator_value = float(fator_entry.get())
    fator_entry.delete(0, tk.END)
    fator_entry.insert(0, fator_value - 0.05)

# Função principal para calcular a velocidade inicial e mostrar o resultado
def calcular_velocidade_inicial_e_mostrar_resultado():
    try:
        angulo = float(angulo_entry.get())
        angulo_radianos = float(math.radians(angulo))
        gravidade = float(gravidade_entry.get())       
        alcance = float(alcance_entry.get())
        diferenca = float(diferenca_entry.get())
        fator = float(fator_entry.get())
        forca_x = float(forca_x_entry.get())
        forca_y = float(forca_y_entry.get())
       

       
        angulovento = float(angulovento_entry.get())
        angulovento_rad = math.radians(angulovento)
        forcavento_visual = float(forcavento_entry.get())
        forcavento_real_y = (forcavento_visual / 50 * forca_y) * fator #222 -talvez aumentar um pouco - (RAON 300)
        forcavento_real_x= (forcavento_visual / 50 * forca_x) * fator  #600 -talvez diminuir um pouco - (RAON 300)  
        tolerancia = 1e-10 
        aceleracao_vento_y = forcavento_real_y * math.sin(angulovento_rad)      #ESSE TALVEZ TENHA QUE MULTIPLICAR POR -1 (multipliquei - ) - ERA ISSO!!!!
        if abs(aceleracao_vento_y) < tolerancia:
            aceleracao_vento_y = 0
        aceleracao_vento_x = forcavento_real_x * math.cos(angulovento_rad) * (-1) #TALVEZ TENHA QUE REMOVER O -1 (removi - parece que só inverteu a ordem de favor e contra)
        if abs(aceleracao_vento_x) < tolerancia:
            aceleracao_vento_x = 0
        aceleracao_total_y = (gravidade * (-1))  + aceleracao_vento_y #TALVEZ TENHA QUE MULTIPLICAR POR (-1)
             

           
        print("Alcance:", alcance)
        print("Angulo:", angulo)
        print("Angulo do vento:", angulovento)
        print("Angulo do vento Rad:", angulovento_rad)
        print("Forca Vento Real Y:", forcavento_real_y)
        print("Forca Vento Real X:", forcavento_real_x)
        print("Aceleracao Vento Y:", aceleracao_vento_y)
        print("Aceleracao Vento X:", aceleracao_vento_x)
        print("Aceleracao Total Y:", aceleracao_total_y)            
       
       
        

        velocidade_inicial = calcular_velocidade_inicial(aceleracao_vento_x, alcance, diferenca, angulo_radianos, aceleracao_total_y)
        velocidade_normalizada = mapear_velocidade_normalizada(velocidade_inicial, 0, 1149.76)
        print("Velocidade Inicial (resultado)", velocidade_inicial)
        print("Velocidade Inicial Normalizada:", velocidade_normalizada)

        atualizar_resultado_visual(velocidade_normalizada)

        resultado_label.config(text=f"Força = {velocidade_normalizada:.2f}", font=("Helvetica", 24))
    except ValueError as e:
        resultado_canvas.delete("all")
        resultado_label.config(text=f"Erro: {e}")

# Função para atualizar o resultado visual
def atualizar_resultado_visual(velocidade_normalizada):
    largura = velocidade_normalizada * 500 / 4.0
    resultado_canvas.delete("all")
    resultado_canvas.create_rectangle(0, 0, largura, 60, fill="red", outline="black")

# Função para salvar a posição 1
def salvar_posicao_1():
    global posicao_1
    posicao_1 = pyautogui.position()
    print(f"Posição 1 salva: {posicao_1}")

# Função para salvar a posição 2 e calcular as diferenças
def salvar_posicao_2():
    global posicao_2
    posicao_2 = pyautogui.position()
    print(f"Posição 2 salva: {posicao_2}")
    calcular_diferencas()

# Função para calcular as diferenças entre as posições salvas
def calcular_diferencas():
    global posicao_1, posicao_2

    if posicao_1 is not None and posicao_2 is not None:
        alcance = abs(posicao_1[0] - posicao_2[0])
        alcance_entry.delete(0, tk.END)
        alcance_entry.insert(0, alcance)

# Configuração dos atalhos de teclado para salvar posições
keyboard.add_hotkey('ctrl', salvar_posicao_1)
keyboard.add_hotkey('alt', salvar_posicao_2)


#########################################################################################

# Função para salvar a posição do peão 
def salvar_posicao_1d():
    global posicao_1d
    posicao_1d = pyautogui.position()
    print(f"Posição 1d salva: {posicao_1d}")

# Função para salvar a posição de onde a bala caiu
def salvar_posicao_2d():
    global posicao_2d
    posicao_2d = pyautogui.position()
    print(f"Posição 2d salva: {posicao_2d}")
    calcular_diferencasd()

# Função para calcular as diferenças entre as posições salvas
def calcular_diferencasd():
    global posicao_1d, posicao_2d

    if posicao_1d is not None and posicao_2d is not None:
        diferenca = posicao_1d[0] - posicao_2d[0]
        diferenca_entry.delete(0, tk.END)
        diferenca_entry.insert(0, diferenca)

# Configuração dos atalhos de teclado para salvar posições das diferenças
keyboard.add_hotkey('z', salvar_posicao_1d)
keyboard.add_hotkey('x', salvar_posicao_2d)

##########################################################################################


# Variável global para armazenar o ângulo clicado
angulo_clicado = None

# Função chamada quando o ângulo é clicado na janela secundária
def get_angle(angle):
    global angulo_clicado
    print(f"Ângulo clicado: {angle}°")
    angle_label.config(text=f"Ângulo: {angle}°")
    angulo_clicado = angle  # Armazenar o ângulo na variável global
    
    # Atualizar o Entry na janela principal com o ângulo clicado
    angulovento_entry.delete(0, tk.END)
    angulovento_entry.insert(0, angle)

# Função para obter o ângulo clicado a partir da janela principal
def obter_angulo_clicado():
    global angulo_clicado
    return angulo_clicado

# Função de atualização da segunda janela com 24 marcações
def update_second_window():
    center_x, center_y = 325, 325
    radius = 300
    image = Image.open("rosa foto usavel.jpg")
    photo = ImageTk.PhotoImage(image)
    background_label = tk.Label(second_window, image=photo)
    background_label.image = photo
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Ocupa toda a janela


    for angle in range(0, 360, 5):  # Alterado para 15 graus
        x = center_x + int(radius * math.cos(math.radians(angle)))
        y = center_y - int(radius * math.sin(math.radians(angle)))

        label = tk.Label(second_window, text=str(angle) + "°", bg="blue", fg="white", bd=0, highlightthickness=0)
        label.place(x=x, y=y)
        label.bind("<Button-1>", lambda event, angle=angle: get_angle(angle))

    global angle_label
    angle_label = tk.Label(second_window, text="", bg="blue", fg="white", bd=0, highlightthickness=0)
    angle_label.place(x=center_x, y=center_y, anchor="center")

# Janela principal
janela = tk.Tk()
janela.title("Chart do Betão")
janela.geometry("575x400")

# Carregar a imagem
#background_image = Image.open("dogfeio croppado.png")
#background_photo = ImageTk.PhotoImage(background_image)
#background_label = tk.Label(janela, image=background_photo)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Widgets e layout...

angulo_label = ttk.Label(janela, text="Ângulo (graus):")
angulo_label.grid(row=0, column=0, padx=10, pady=10)

angulo_entry = ttk.Entry(janela)
angulo_entry.grid(row=0, column=1, padx=10, pady=10)

gravidade_label = ttk.Label(janela, text="Gravidade (pixel/s²):")
gravidade_label.grid(row=1, column=0, padx=10, pady=10)

gravidade_default = tk.StringVar(value="530.78") #Raon = 530.78; Lightning = 420.78

gravidade_entry = ttk.Entry(janela, textvariable=gravidade_default)
gravidade_entry.grid(row=1, column=1, pady=10, padx=(0, 5))

btn_diminuir_gravidade = ttk.Button(janela, text="-", command=diminuir_gravidade, width=8)
btn_diminuir_gravidade.grid(row=1, column=0, pady=10, padx=(260, 0))

btn_aumentar_gravidade = ttk.Button(janela, text="+", command=aumentar_gravidade, width=8)
btn_aumentar_gravidade.grid(row=1, column=3, pady=10, padx=(5, 0))

btn_diminuir_angulo = ttk.Button(janela, text="-", command=diminuir_angulo, width=8)
btn_diminuir_angulo.grid(row=0, column=0, pady=10, padx=(260, 0))

btn_aumentar_angulo = ttk.Button(janela, text="+", command=aumentar_angulo, width=8)
btn_aumentar_angulo.grid(row=0, column=3, pady=10, padx=(5, 0))

btn_diminuir_vento = ttk.Button(janela, text="-", command=diminuir_vento, width=8)
btn_diminuir_vento.grid(row=4, column=0, pady=10, padx=(260, 0))

btn_aumentar_vento = ttk.Button(janela, text="+", command=aumentar_vento, width=8)
btn_aumentar_vento.grid(row=4, column=3, pady=10, padx=(5, 0))

alcance_label = ttk.Label(janela, text="Alcance (pixels):")
alcance_label.grid(row=2, column=0, padx=10, pady=10)

alcance_entry = ttk.Entry(janela)
alcance_entry.grid(row=2, column=1, padx=10, pady=10)

angulovento_label = ttk.Label(janela, text="Ângulo do vento:")
angulovento_label.grid(row=3, column=0, padx=10, pady=10)

angulovento_default = tk.StringVar(value="0")

angulovento_entry = ttk.Entry(janela, textvariable=angulovento_default)
angulovento_entry.grid(row=3, column=1, padx=10, pady=10)

forcavento_label = ttk.Label(janela, text="Força do vento")
forcavento_label.grid(row=4, column=0, padx=10, pady=10)

forcavento_default = tk.StringVar(value="0")

forcavento_entry = ttk.Entry(janela, textvariable=forcavento_default)
forcavento_entry.grid(row=4, column=1, padx=10, pady=10)

calcular_button = ttk.Button(janela, text="Calcular força", command=calcular_velocidade_inicial_e_mostrar_resultado)
calcular_button.grid(row=5, column=0, columnspan=2, pady=10)

resultado_canvas = tk.Canvas(janela, width=500, height=60, bg="white", borderwidth=0, highlightthickness=0)
resultado_canvas.grid(row=6, column=0, columnspan=2, pady=10)

resultado_label = ttk.Label(janela, text="", font=("Helvetica", 24))
resultado_label.grid(row=7, column=0, columnspan=2, pady=10)


#botão do fator

fator_label = ttk.Label(janela, text="Fator de correção:")
fator_label.grid(row=8, column=0, padx=10, pady=10)

fator_default = tk.StringVar(value="1")

fator_entry = ttk.Entry(janela, textvariable=fator_default)
fator_entry.grid(row=8, column=1, pady=10, padx=(0, 5))

btn_diminuir_fator = ttk.Button(janela, text="-", command=diminuir_fator, width=8)
btn_diminuir_fator.grid(row=8, column=0, pady=10, padx=(260, 0))

btn_aumentar_fator = ttk.Button(janela, text="+", command=aumentar_fator, width=8)
btn_aumentar_fator.grid(row=8, column=3, pady=10, padx=(5, 0))

#entrada para força Y

forca_y_label = ttk.Label(janela, text="Força Y:")
forca_y_label.grid(row=9, column=0, padx=10, pady=10)

forca_y_default = tk.StringVar(value="300") #222 -talvez aumentar um pouco - (RAON 300)


forca_y_entry = ttk.Entry(janela, textvariable=forca_y_default)
forca_y_entry.grid(row=9, column=1, pady=10, padx=(0, 5))

#entrada para força X

forca_x_label = ttk.Label(janela, text="Força X:")
forca_x_label.grid(row=10, column=0, padx=10, pady=10)

forca_x_default = tk.StringVar(value="300")#600 -talvez diminuir um pouco - (RAON 300)  


forca_x_entry = ttk.Entry(janela, textvariable=forca_x_default)
forca_x_entry.grid(row=10, column=1, pady=10, padx=(0, 5))



####################################################################################
#entrada para diferença

diferenca_label = ttk.Label(janela, text="Diferença: ")
diferenca_label.grid(row=11, column=0, padx=10, pady=10)

diferenca_default = tk.StringVar(value="0")

diferenca_entry = ttk.Entry(janela, textvariable=diferenca_default)
diferenca_entry.grid(row=11, column=1, pady=10, padx=(0, 5))
####################################################################################



# Vincular a tecla 'Enter' à função de cálculo
janela.bind('<Return>', lambda event: calcular_velocidade_inicial_e_mostrar_resultado())

# Janela secundária
second_window = tk.Toplevel(janela)
second_window.title("Rosa dos Ventos")
second_window.geometry("650x650")

update_second_window()  # Inicia a atualização da segunda janela

janela.mainloop()
