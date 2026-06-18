import tkinter as tk
from tkinter import messagebox

class JogoDeXadrez:
    def __init__(self, root):
        self.root = root
        self.root.title("Xadrez Completo")
        
        # Estado do jogo
        self.jogo_ativo = True
        self.turno = "BRANCAS" # Brancas começam
        self.casa_selecionada = None
        
        # Representação do tabuleiro (Maiúsculas = Brancas, Minúsculas = Pretas)
        self.tabuleiro = [
            ["t", "c", "b", "q", "k", "b", "c", "t"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["T", "C", "B", "Q", "K", "B", "C", "T"]
        ]
        
        self.pecas_unicode = {
            "T": "♖", "C": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙",
            "t": "♜", "c": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
            ".": ""
        }
        
        # Painel de Status (Indica a vez do jogador)
        self.label_status = tk.Label(
            self.root, 
            text="VEZ DAS BRANCAS", 
            font=("Helvetica", 14, "bold"), 
            bg="#333333", 
            fg="#FFFFFF", 
            pady=5
        )
        self.label_status.pack(fill=tk.X)
        
        # Container do tabuleiro
        self.container_tabuleiro = tk.Frame(self.root)
        self.container_tabuleiro.pack()
        
        self.botoes = [[None for _ in range(8)] for _ in range(8)]
        self.criar_tabuleiro()

    def criar_tabuleiro(self):
        for linha in range(8):
            for coluna in range(8):
                cor_fundo = "#DDBB88" if (linha + coluna) % 2 == 0 else "#AA7744"
                botao = tk.Button(
                    self.container_tabuleiro, 
                    text=self.pecas_unicode[self.tabuleiro[linha][coluna]],
                    font=("Helvetica", 24),
                    width=4, 
                    height=2,
                    bg=cor_fundo,
                    command=lambda l=linha, c=coluna: self.clique_casa(l, c)
                )
                botao.grid(row=linha, column=coluna)
                self.botoes[linha][coluna] = botao

    def clique_casa(self, linha, coluna):
        if not self.jogo_ativo:
            return
            
        peca = self.tabuleiro[linha][coluna]
        
        if self.casa_selecionada is None:
            if peca != "." and self.eh_peca_do_turno(peca):
                self.casa_selecionada = (linha, coluna)
                self.botoes[linha][coluna].config(bg="#77FF77")
        else:
            lin_origem, col_origem = self.casa_selecionada
            
            if lin_origem == linha and col_origem == coluna:
                self.atualizar_cores_tabuleiro()
                self.casa_selecionada = None
                return

            if self.movimento_valido(lin_origem, col_origem, linha, coluna):
                peca_capturada = self.tabuleiro[linha][coluna]
                
                # Executa o movimento
                self.tabuleiro[linha][coluna] = self.tabuleiro[lin_origem][col_origem]
                self.tabuleiro[lin_origem][col_origem] = "."
                
                self.casa_selecionada = None
                self.atualizar_interface()
                
                # Verifica se o Rei foi capturado (Vitória/Derrota)
                if peca_capturada.upper() == "K":
                    self.jogo_ativo = False
                    vencedor = "BRANCAS" if self.turno == "BRANCAS" else "PRETAS"
                    self.label_status.config(text=f"FIM DE JOGO! VITÓRIA DAS {vencedor}!", bg="#228B22")
                    messagebox.showinfo("Fim de Jogo", f"O Rei foi capturado! Vitória das {vencedor}!")
                    return
                
                # Verifica se houve empate por falta de peças
                if self.verificar_empate():
                    self.jogo_ativo = False
                    self.label_status.config(text="FIM DE JOGO! EMPATE!", bg="#8B0000")
                    messagebox.showinfo("Fim de Jogo", "Empate por material insuficiente! Não há peças para dar mate.")
                    return

                # Alterna o turno se o jogo continuar
                self.turno = "PRETAS" if self.turno == "BRANCAS" else "BRANCAS"
                self.label_status.config(text=f"VEZ DAS {self.turno}")
            else:
                messagebox.showwarning("Movimento Inválido", "Movimento ilegal para esta peça!")
                self.atualizar_cores_tabuleiro()
                self.casa_selecionada = None

    def eh_peca_do_turno(self, peca):
        if self.turno == "BRANCAS" and peca.isupper(): return True
        if self.turno == "PRETAS" and peca.islower(): return True
        return False

    def movimento_valido(self, o_l, o_c, d_l, d_c):
        peca = self.tabuleiro[o_l][o_c]
        destino = self.tabuleiro[d_l][d_c]
        
        if destino != "." and self.eh_peca_do_turno(destino):
            return False
            
        diff_l = d_l - o_l
        diff_c = d_c - o_c
        abs_l = abs(diff_l)
        abs_c = abs(diff_c)

        if peca.upper() == "C":
            return (abs_l == 2 and abs_c == 1) or (abs_l == 1 and abs_c == 2)

        if peca.upper() == "K":
            return abs_l <= 1 and abs_c <= 1

        if peca.upper() == "T":
            if o_l != d_l and o_c != d_c: return False
            return self.caminho_livre(o_l, o_c, d_l, d_c)

        if peca.upper() == "B":
            if abs_l != abs_c: return False
            return self.caminho_livre(o_l, o_c, d_l, d_c)

        if peca.upper() == "Q":
            if (o_l == d_l or o_c == d_c) or (abs_l == abs_c):
                return self.caminho_livre(o_l, o_c, d_l, d_c)
            return False

        if peca.upper() == "P":
            direcao = -1 if peca.isupper() else 1
            linha_inicial = 6 if peca.isupper() else 1
            
            if diff_c == 0 and destino == ".":
                if diff_l == direcao: return True
                if o_l == linha_inicial and diff_l == 2 * direcao:
                    if self.tabuleiro[o_l + direcao][o_c] == ".": return True
            
            if abs_c == 1 and diff_l == direcao and destino != ".":
                return True
                
            return False

        return False

    def caminho_livre(self, o_l, o_c, d_l, d_c):
        passo_l = 0 if o_l == d_l else (1 if d_l > o_l else -1)
        passo_c = 0 if o_c == d_c else (1 if d_c > o_c else -1)
        
        atual_l = o_l + passo_l
        atual_c = o_c + passo_c
        
        while atual_l != d_l or atual_c != d_c:
            if self.tabuleiro[atual_l][atual_c] != ".":
                return False
            atual_l += passo_l
            atual_c += passo_c
        return True

    def verificar_empate(self):
        """ Retorna True se sobrarem poucas peças no tabuleiro inviabilizando o mate """
        pecas_restantes = []
        for linha in range(8):
            for coluna in range(8):
                peca = self.tabuleiro[linha][coluna]
                if peca != ".":
                    pecas_restantes.append(peca.upper())
        
        # 1. Apenas Rei contra Rei
        if len(pecas_restantes) == 2 and pecas_restantes.count("K") == 2:
            return True
            
        # 2. Rei e Bispo vs Rei OU Rei e Cavalo vs Rei
        if len(pecas_restantes) == 3:
            if "K" in pecas_restantes and ("B" in pecas_restantes or "C" in pecas_restantes):
                return True
                
        return False

    def atualizar_interface(self):
        for linha in range(8):
            for coluna in range(8):
                self.botoes[linha][coluna].config(text=self.pecas_unicode[self.tabuleiro[linha][coluna]])
        self.atualizar_cores_tabuleiro()

    def atualizar_cores_tabuleiro(self):
        for linha in range(8):
            for column in range(8):
                cor_fundo = "#DDBB88" if (linha + column) % 2 == 0 else "#AA7744"
                self.botoes[linha][column].config(bg=cor_fundo)

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoDeXadrez(root)
    root.mainloop()