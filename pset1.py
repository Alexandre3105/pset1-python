# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo:
#    Matrícula:
#    Turma:
#    Email:
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Importações necessárias para manipulação de imagens, criação de interfaces gráficas, e operações matemáticas
import math
from PIL import Image as PILImage
from io import BytesIO
import tkinter
import base64
import sys


class Imagem:
    """
    Classe para manipulação de imagens em tons de cinza.
    """

    def __init__(self, largura, altura, pixels):
        """
        Inicializa uma nova imagem com largura, altura e uma lista de pixels.
        """
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def usar_kernel(self, kernel):
        """
        Aplica um kernel a uma imagem (convolução).
        """
        Il = self.largura  # Largura da imagem original
        Ih = self.altura  # Altura da imagem original
        Kl = kernel.largura  # Largura do kernel
        Kh = kernel.altura  # Altura do kernel
        Dl = int((Kl - 1) / 2)  # Deslocamento para o centro do kernel
        com_kernel = Imagem.nova(Il, Ih)  # Cria uma nova imagem do mesmo tamanho da original

        # Percorre cada pixel da imagem original
        for ix in range(Il):
            for iy in range(Ih):
                pixel = 0  # Valor inicial do pixel resultante
                # Aplica o kernel sobre a região correspondente da imagem original
                for kx in range(Kl):
                    for ky in range(Kh):
                        # Obtém o valor do pixel da imagem original considerando o deslocamento do kernel
                        Ip = self.pixels[self.get_pixel(ix + kx - Dl, iy + ky - Dl)]
                        # Obtém o valor do kernel na posição atual
                        Kp = kernel.pixels[kernel.get_pixel(kx, ky)]
                        # Soma o resultado da multiplicação do pixel pelo valor do kernel
                        pixel += Ip * Kp
                # Define o valor do pixel na nova imagem
                com_kernel.set_pixel(ix, iy, pixel)

        return com_kernel  # Retorna a nova imagem com o kernel aplicado

    def kernel_sem_arrendondar(self, kernel):
        """
        Aplica um kernel a uma imagem sem arredondar os valores dos pixels resultantes.
        """
        Il = self.largura  # Largura da imagem original
        Ih = self.altura  # Altura da imagem original
        Kl = kernel.largura  # Largura do kernel
        Kh = kernel.altura  # Altura do kernel
        Dl = int((Kl - 1) / 2)  # Deslocamento para centralizar o kernel
        com_kernel = Imagem.nova(Il, Ih)  # Cria uma nova imagem para receber os valores modificados

        # Aplica o kernel sobre cada pixel da imagem original
        for ix in range(Il):
            for iy in range(Ih):
                pixel = 0  # Valor inicial para o pixel resultante
                for kx in range(Kl):
                    for ky in range(Kh):
                        # Obter o pixel da imagem original considerando o deslocamento do kernel
                        Ip = self.pixels[self.get_pixel(ix + kx - Dl, iy + ky - Dl)]
                        # Obter o valor do kernel para a posição correspondente
                        Kp = kernel.pixels[kernel.get_pixel(kx, ky)]
                        # Soma o resultado da multiplicação do pixel pelo kernel
                        pixel += Ip * Kp
                # Define o valor do pixel resultante na nova imagem
                com_kernel.set_pixel(ix, iy, pixel)

        return com_kernel  # Retorna a imagem com o kernel aplicado sem arredondar

    def bordas(self):
        """
        Detecção de bordas usando os kernels Sobel nas direções X e Y.
        """
        l = self.largura  # Largura da imagem original
        h = self.altura  # Altura da imagem original

        # Criação de kernels Sobel para detectar bordas horizontais e verticais
        kernelX = Imagem(3, 3, [-1, 0, 1,
                                -2, 0, 2,
                                -1, 0, 1])
        kernelY = Imagem(3, 3, [-1, -2, -1,
                                0, 0, 0,
                                1, 2, 1])

        # Aplicação dos kernels sem arredondamento para detectar bordas nas direções X e Y
        auxiliarX = self.kernel_sem_arrendondar(kernelX)
        auxiliarY = self.kernel_sem_arrendondar(kernelY)

        # Lista para armazenar a intensidade das bordas
        listaBorda = []
        # Calcula a magnitude das bordas usando a distância Euclidiana
        for j in range(l * h):
            pixel = math.sqrt(auxiliarX.pixels[j] ** 2 + auxiliarY.pixels[j] ** 2)
            # Limita o valor do pixel entre 0 e 255 para evitar extrapolações
            if pixel > 255:
                pixel = 255
            if pixel < 0:
                pixel = 0
            # Armazena o valor arredondado do pixel
            listaBorda.append(round(pixel))

        # Cria uma nova imagem com as bordas detectadas
        borda = Imagem(l, h, listaBorda)

        return borda  # Retorna a imagem com as bordas detectadas

    def __eq__(self, other):
        """
        Compara duas instâncias de Imagem para verificar se são iguais.
        """
        return all(getattr(self, attr) == getattr(other, attr)
                   for attr in ('altura', 'largura', 'pixels'))  # Verifica se os atributos são iguais

    def __repr__(self):
        """
        Retorna uma representação textual da classe Imagem.
        """
        return f"Imagem({self.largura}, {self.altura}, {self.pixels})"  # Retorna uma descrição simples da imagem

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem de um arquivo e retorna uma instância da classe Imagem.
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)  # Abre a imagem usando PIL
            img_data = img.getdata()  # Obtém os dados dos pixels da imagem
            # Converte para tons de cinza conforme o modo da imagem original
            if img.mode.startswith('RGB'):
                pixels = [round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError("Modo de imagem não suportado")
            largura, altura = img.size  # Obtém a largura e altura da imagem
            return cls(largura, altura, pixels)  # Retorna uma nova instância de Imagem

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria uma nova imagem em branco (toda preenchida com 0).
        """
        return cls(largura, altura,
                   [0 for _ in range(largura * altura)])  # Retorna uma nova instância de Imagem em branco

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem no disco ou em um objeto semelhante a um arquivo.
        """
        # Cria uma nova imagem PIL e coloca os dados de pixels
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)  # Define os pixels da imagem PIL
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)  # Salva a imagem no arquivo
        else:
            saida.save(nome_arquivo, modo)  # Salva a imagem com um modo específico
        saida.close()  # Fecha a imagem para liberar recursos

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem como uma imagem GIF.
        """
        buffer = BytesIO()  # Cria um buffer em memória
        self.salvar(buffer, modo='GIF')  # Salva a imagem como GIF no buffer
        return base64.b64encode(buffer.getvalue())  # Retorna a versão codificada em base64 do GIF

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tkinter.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            return  # Se o Tkinter não estiver disponível, não faz nada
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()  # Cria uma nova janela
        # Cria um canvas para mostrar a imagem
        tela = tkinter.Canvas(toplevel, height=self.altura, width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())  # Mostra a imagem no canvas
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)  # Define a posição da imagem no canvas

        def ao_redimensionar(event):
            """
            Lida com o redimensionamento da janela.
            """
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))  # Cria uma nova imagem PIL
            nova_imagem.putdata(self.pixels)  # Coloca os pixels na imagem
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)  # Redimensiona a imagem
            buffer = BytesIO()  # Cria um novo buffer
            nova_imagem.save(buffer, 'GIF')  # Salva a imagem no buffer como GIF
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))  # Atualiza a imagem no canvas
            tela.configure(height=event.height, width=event.width)  # Ajusta o tamanho do canvas
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)  # Mostra a imagem no canvas

        tela.bind('<Configure>', ao_redimensionar)  # Liga a função ao evento de redimensionamento
        toplevel.bind('<Configure>',
                      lambda e: tela.configure(height=e.height, width=e.width))  # Ajusta o canvas ao redimensionamento

        # Define a ação ao fechar a janela para destruir a raiz do Tkinter
        toplevel.protocol("WM_DELETE_WINDOW", tk_root.destroy)


# Configuração para o Tkinter (se estiver disponível)
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()  # Esconde a janela principal
    tcl = tkinter.Tcl()  # Inicia o Tcl


    def refaz_apos():
        tcl.after(500, refaz_apos)  # Reforça uma função após um tempo


    tcl.after(500, refaz_apos)  # Chama a função periodicamente
except:
    tk_root = None  # Se o Tkinter não estiver disponível, define como None

WINDOWS_OPENED = False  # Variável global para verificar se janelas foram abertas

# Bloco para executar testes ou demonstrar a funcionalidade quando o arquivo é executado diretamente
if __name__ == "__main__":
    
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    pass

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
