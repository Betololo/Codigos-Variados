import tkinter as tk
from tkinter import ttk
import keyboard # type: ignore
import pyautogui # type: ignore
import math
from PIL import Image, ImageTk, ImageGrab # type: ignore
import pytesseract # type: ignore
import re
import cv2 # type: ignore
import numpy as np  # type: ignore
import os

# ========== CONFIGURAÇÃO TESSERACT ==========
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe" 

# ========== FUNÇÕES MATEMÁTICAS ==========
def calcular_forca(B40): return B40 * 0.004332712
def calcular_b40(B39, B37, B38, D42, D41): return math.sqrt(B39 / ((2 * B37 * B38) / D42 + (2 * D41 * B38**2) / D42**2))
def calcular_b39(B3, B4): return (800 / B3) * B4
def calcular_b37(B36): return math.cos(B36)
def calcular_b38(B36): return math.sin(B36)
def calcular_d42(B12, D40, B13): return B12 - D40 / B13
def calcular_d41(D39, B13): return D39 / B13
def calcular_b36(B5): return (B5 + 0.00001) * (math.pi / 180)
def calcular_d40(D38, B35): return D38 * B35
def calcular_d39(D37, B35): return D37 * B35
def calcular_d38(D36): return math.sin(D36)
def calcular_b35(B10, D35): return 0 if B10 == 0 else D35
def calcular_d37(D36): return math.cos(D36)
def calcular_d35(E35, B10): return B10 if E35 == 1 else B10 - 1
def calcular_d36(B9): return B9 * (math.pi / 180)
def calcular_e35(B9): return 1 if math.cos(math.radians(B9)) == -1 else math.cos(math.radians(B9))


# TIMEBOMB
def calcular_b69(B66,D68,K48,B64): return (B66 - 0.5 * D68 * K48**2) / (B64 * K48)
def calcular_b66(B3,B4): return (800/B3)*B4
def calcular_d68(D66,B13): return D66/B13
K48 = 2.134
def calcular_b64(B63): return math.cos(B63)
def calcular_d66(D64,B62): return D64*B62

def calcular_b63(B68): return (B68+0.00001)*(math.pi/180)
def calcular_d64(D63): return math.cos(D63)
def calcular_b62(B10,D62): return 0 if B10 == 0 else D62
def calcular_d63(B9): return B9*(math.pi/180)
def calcular_d62(E62,B10): return B10 if E62 == 1 else B10 - 1#PROBLEMA E62
def calcular_e62(B9): return 1 if math.cos(math.radians(B9)) == -1 else math.cos(math.radians(B9))
def calcular_b67(D69,K48,B66,D68): return (0+0,5*D69*(K48*K48))/(B66-0,5*D68*K48*K48)
def calcular_d69(B12,D67,B13): return B12-D67/B13
def calcular_d67(D65,B62): return D65*B62
def calcular_d65(D63): return math.sin(D63)


 

# ========== FUNÇÕES INTERFACE ==========
def aumentar_angulo():
    valor = float(angulo_entry.get())
    angulo_entry.delete(0, tk.END)
    angulo_entry.insert(0, valor + 1)

def diminuir_angulo():
    valor = float(angulo_entry.get())
    angulo_entry.delete(0, tk.END)
    angulo_entry.insert(0, valor - 1)

def aumentar_vento():
    valor = float(forcavento_entry.get())
    forcavento_entry.delete(0, tk.END)
    forcavento_entry.insert(0, valor + 1)

def diminuir_vento():
    valor = float(forcavento_entry.get())
    forcavento_entry.delete(0, tk.END)
    forcavento_entry.insert(0, valor - 1)

def calcular_velocidade_inicial_e_mostrar_resultado():
    try:
        B3 = 30
        B4 = float(alcance_entry.get()) * 30 / 800
        B5 = float(angulo_entry.get())
        B9 = float(angulovento_entry.get())
        if B9 > 180: B9 -= 360
        B10 = float(forcavento_entry.get())
        ajuste_desnivel = float(desnivel_entry.get()) * (360 / 1200) * (-1)
        B12 = float(gravidade_entry.get()) - ajuste_desnivel
        B13 = float(massa_entry.get())

        E35 = calcular_e35(B9)
        D36 = calcular_d36(B9)
        D35 = calcular_d35(E35, B10)
        D37 = calcular_d37(D36)
        B35 = calcular_b35(B10, D35)
        D38 = calcular_d38(D36)
        D39 = calcular_d39(D37, B35)
        D40 = calcular_d40(D38, B35)
        B36 = calcular_b36(B5)
        D41 = calcular_d41(D39, B13)
        D42 = calcular_d42(B12, D40, B13)
        B38 = calcular_b38(B36)
        B37 = calcular_b37(B36)
        B39 = calcular_b39(B3, B4)
        B40 = calcular_b40(B39, B37, B38, D42, D41)
        velocidade_inicial = calcular_forca(B40)

        atualizar_resultado_visual(velocidade_inicial)
        atualizar_janela_aro(velocidade_inicial)
        resultado_label.config(text=f"Força = {velocidade_inicial:.2f}", font=("Helvetica", 24))
    except ValueError as e:
        resultado_canvas.delete("all")
        resultado_label.config(text=f"Erro: {e}")

def calcular_timebomb():
    try:
        B3 = 30
        B4 = float(alcance_entry.get()) * 30 / 800
        B5 = float(angulo_entry.get())
        B9 = float(angulovento_entry.get())
        if B9 > 180: B9 -= 360
        B10 = float(forcavento_entry.get())
        ajuste_desnivel = float(desnivel_entry.get()) * (360 / 1200) * (-1)
        B12 = float(gravidade_entry.get()) - ajuste_desnivel
        B13 = float(massa_entry.get())
        K48 = 2.134

    except ValueError as e:
        resultado_canvas.delete("all")
        resultado_label.config(text=f"Erro: {e}")


def atualizar_resultado_visual(valor):
    largura = valor * 500 / 4.0
    resultado_canvas.delete("all")
    resultado_canvas.create_rectangle(0, 0, largura, 60, fill="red", outline="black")

def salvar_posicao_1():
    global posicao_1
    posicao_1 = pyautogui.position()
    print(f"Posição 1 salva: {posicao_1}")

def salvar_posicao_2():
    global posicao_2
    posicao_2 = pyautogui.position()
    print(f"Posição 2 salva: {posicao_2}")
    calcular_diferencas()
    calcular_diferencas2()

def calcular_diferencas():
    if posicao_1 and posicao_2:
        alcance = abs(posicao_1[0] - posicao_2[0])
        alcance_entry.delete(0, tk.END)
        alcance_entry.insert(0, alcance)

def calcular_diferencas2():
    if posicao_1 and posicao_2:
        desnivel = posicao_1[1] - posicao_2[1]
        desnivel_entry.delete(0, tk.END)
        desnivel_entry.insert(0, desnivel)

keyboard.add_hotkey('ctrl', salvar_posicao_1)
keyboard.add_hotkey('alt', salvar_posicao_2)

def get_angle(angle):
    global angulo_clicado
    angulo_clicado = angle
    angle_label.config(text=f"Ângulo: {angle}°")
    angulovento_entry.delete(0, tk.END)
    angulovento_entry.insert(0, angle)

def update_second_window():
    center_x, center_y = 325, 325
    radius = 300
    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, "rosa foto usavel.jpg")
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    background_label = tk.Label(second_window, image=photo)
    background_label.image = photo
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    for angle in range(0, 360, 5):
        x = center_x + int(radius * math.cos(math.radians(angle)))
        y = center_y - int(radius * math.sin(math.radians(angle)))
        label = tk.Label(second_window, text=str(angle) + "°", bg="blue", fg="white")
        label.place(x=x, y=y)
        label.bind("<Button-1>", lambda event, angle=angle: get_angle(angle))

    global angle_label
    angle_label = tk.Label(second_window, text="", bg="blue", fg="white")
    angle_label.place(x=center_x, y=center_y, anchor="center")

# ========== INTERFACE PRINCIPAL ==========
janela = tk.Tk()
janela.title("Chart do Betão")
janela.geometry("575x400")

# Entradas e botões
def adicionar_entry_rotulo(linha, texto, var=None, valor_default=None):
    rotulo = ttk.Label(janela, text=texto)
    rotulo.grid(row=linha, column=0, padx=10, pady=10)
    entrada = ttk.Entry(janela, textvariable=var)
    entrada.grid(row=linha, column=1, padx=10, pady=10)
    if valor_default:
        entrada.insert(0, valor_default)
    return entrada

angulo_entry = adicionar_entry_rotulo(0, "Ângulo (graus):")
gravidade_entry = adicionar_entry_rotulo(1, "Gravidade (pixel/s²):", tk.StringVar(value="390"))
alcance_entry = adicionar_entry_rotulo(2, "Alcance (pixels):")
angulovento_entry = adicionar_entry_rotulo(3, "Ângulo do vento:")
forcavento_entry = adicionar_entry_rotulo(4, "Força do vento")
massa_entry = adicionar_entry_rotulo(9, "Massa", tk.StringVar(value="0.254"))
desnivel_entry = adicionar_entry_rotulo(10, "Desnível", tk.StringVar(value="0"))

ttk.Button(janela, text="-", command=diminuir_angulo, width=8).grid(row=0, column=0, padx=(260, 0))
ttk.Button(janela, text="+", command=aumentar_angulo, width=8).grid(row=0, column=3, padx=(5, 0))
ttk.Button(janela, text="-", command=diminuir_vento, width=8).grid(row=4, column=0, padx=(260, 0))
ttk.Button(janela, text="+", command=aumentar_vento, width=8).grid(row=4, column=3, padx=(5, 0))
ttk.Button(janela, text="Calcular força", command=calcular_velocidade_inicial_e_mostrar_resultado).grid(row=5, column=0, columnspan=2)
ttk.Button(janela, text="Ler OCR", command=lambda: resultado_label.config(text="OCR: " + janela_ocr.capturar_texto_ocr())).grid(row=5, column=2)

resultado_canvas = tk.Canvas(janela, width=500, height=60, bg="white", borderwidth=0, highlightthickness=0)
resultado_canvas.grid(row=6, column=0, columnspan=2, pady=10)

resultado_label = ttk.Label(janela, text="", font=("Helvetica", 24))
resultado_label.grid(row=7, column=0, columnspan=2, pady=10)

janela.bind('<Return>', lambda event: calcular_velocidade_inicial_e_mostrar_resultado())

# ========== ROSA DOS VENTOS ==========
second_window = tk.Toplevel(janela)
second_window.title("Rosa dos Ventos")
second_window.geometry("650x650")
update_second_window()

# ========== JANELA ARO ==========
class BBoxAro(tk.Toplevel):
    def __init__(self, master, title, default_pos=(100, 500), cor_borda="magenta"):
        super().__init__(master)
        self.title(title)
        self.geometry(f"500x60+{default_pos[0]}+{default_pos[1]}")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", "white")
        self.config(bg="white")

        self.canvas = tk.Canvas(self, width=500, height=60, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.borda_largura = 2
        self.cor_borda = cor_borda
        self.redesenhar_borda()

        self._move_data = None
        self.canvas.bind("<ButtonPress-1>", self.iniciar_move)
        self.canvas.bind("<B1-Motion>", self.movendo)
        self.canvas.bind("<ButtonRelease-1>", self.parar_move)

        self.grip_size = 10
        self.grip = tk.Frame(self.canvas, bg='black', cursor='bottom_right_corner')
        self.grip.place(relx=1.0, rely=1.0, x=-self.grip_size, y=-self.grip_size,
                        width=self.grip_size, height=self.grip_size)
        self.grip.bind("<ButtonPress-1>", self.iniciar_redim)
        self.grip.bind("<B1-Motion>", self.redimensionando)
        self.grip.bind("<ButtonRelease-1>", self.parar_redim)

        self._resize_data = None

    def redesenhar_borda(self):
        self.canvas.delete("borda")
        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 0 or h <= 0: w, h = 500, 60
        self.canvas.create_rectangle(self.borda_largura/2, self.borda_largura/2,
                                     w - self.borda_largura/2, h - self.borda_largura/2,
                                     outline=self.cor_borda, width=self.borda_largura, tags="borda")

    def iniciar_move(self, event):
        if event.widget == self.grip: return
        self._move_data = (event.x_root, event.y_root, self.winfo_x(), self.winfo_y())

    def movendo(self, event):
        if self._move_data:
            x_root, y_root, x_win, y_win = self._move_data
            self.geometry(f"+{x_win + event.x_root - x_root}+{y_win + event.y_root - y_root}")

    def parar_move(self, event): self._move_data = None

    def iniciar_redim(self, event):
        self._resize_data = (event.x_root, event.y_root, self.winfo_width(), self.winfo_height())

    def redimensionando(self, event):
        if self._resize_data:
            x_root, y_root, w, h = self._resize_data
            dx = event.x_root - x_root
            dy = event.y_root - y_root
            new_w = w + dx
            new_h = h + dy
            self.geometry(f"{new_w}x{new_h}+{self.winfo_x()}+{self.winfo_y()}")
            self.canvas.config(width=new_w, height=new_h)
            self.redesenhar_borda()

    def parar_redim(self, event): self._resize_data = None

    def desenhar_marcacao(self, valor_normalizado):
        self.canvas.delete("marcacao")
        largura_total = self.winfo_width()
        x = min(max(int(valor_normalizado * largura_total / 4.0), 0), largura_total)
        self.canvas.create_line(x, 0, x, self.winfo_height(), fill="red", width=2, tags="marcacao")

# ========== INSTÂNCIAS DAS JANELAS ==========
janela_aro = BBoxAro(janela, "Aro da Força")
def atualizar_janela_aro(valor): janela_aro.desenhar_marcacao(valor)



def corrigir_erro_ocr(texto):
    substituicoes = {
        'O': '0',
        'o': '0',
        'I': '1',
        'l': '1',
        'S': '5',
        'B': '8'
    }
    corrigido = ''.join(substituicoes.get(c, c) for c in texto)
    return corrigido

class BBoxOCR(BBoxAro):
    def __init__(self, master, title="OCR", default_pos=(200, 200), cor_borda="yellow"):
        super().__init__(master, title, default_pos, cor_borda)

    def capturar_texto_ocr(self):
        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()
        imagem = ImageGrab.grab(bbox=(x, y, x + w, y + h))

        # Pré-processamento mais leve
        imagem = imagem.convert('L')  # Escala de cinza

        # Redimensiona com filtro bom para preservar qualidade
        imagem = imagem.resize((w * 3, h * 3), Image.LANCZOS)

        # (opcional) descomente se quiser tentar binarização
        # imagem = imagem.point(lambda p: 255 if p > 160 else 0)

        # imagem.show(title="DEBUG OCR")

        # OCR: tenta psm 8 + whitelist
        # OCR com whitelist
        config = r'--psm 8 -c tessedit_char_whitelist=0123456789'
        texto_bruto = pytesseract.image_to_string(imagem, config=config)

        # Corrigir erros comuns como O → 0
        texto_bruto = corrigir_erro_ocr(texto_bruto)
        print("Texto bruto OCR corrigido:", texto_bruto.strip())

        # Debug de todos os números encontrados
        print("Todos encontrados:", re.findall(r'\d+', texto_bruto))

        # Pegue o primeiro número de 2 dígitos
        encontrado = re.findall(r'\d+', texto_bruto)
        resultado = next((x for x in encontrado if len(x) == 2), "??")
        print("Resultado final OCR:", resultado)
        angulo_entry.delete(0, tk.END)
        angulo_entry.insert(0, resultado)        
        return resultado
        

janela_ocr = BBoxOCR(janela, "OCR")

janela.mainloop()
