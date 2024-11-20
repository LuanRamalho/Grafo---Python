import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx


class Node:
    """Classe que representa um nó na árvore binária AVL."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # A altura de um nó é inicialmente 1


class AVLTree:
    """Classe que representa a Árvore Binária AVL."""
    def __init__(self):
        self.root = None

    def insert(self, value):
        """Insere um valor na árvore e balanceia a árvore."""
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        """Recursivamente insere um valor na árvore e balanceia após a inserção."""
        if not node:
            return Node(value)

        # Passo 1: Inserção padrão (como em uma árvore binária de busca)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            # Se o valor já existir, não faz nada
            return node

        # Passo 2: Atualiza a altura do nó atual
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Passo 3: Calcula o fator de balanceamento
        balance = self._get_balance(node)

        # Passo 4: Verifica o balanceamento e faz rotações se necessário

        # Caso 1: Rotação simples à direita (esquerda pesada)
        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)

        # Caso 2: Rotação simples à esquerda (direita pesada)
        if balance < -1 and value > node.right.value:
            return self._rotate_left(node)

        # Caso 3: Rotação dupla à direita (direita-esquerda)
        if balance > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Caso 4: Rotação dupla à esquerda (esquerda-direita)
        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _get_height(self, node):
        """Retorna a altura de um nó."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """Calcula o fator de balanceamento de um nó."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_left(self, z):
        """Rotação à esquerda."""
        y = z.right
        T2 = y.left

        # Realiza a rotação
        y.left = z
        z.right = T2

        # Atualiza as alturas
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        # Retorna o novo nó raiz
        return y

    def _rotate_right(self, z):
        """Rotação à direita."""
        y = z.left
        T3 = y.right

        # Realiza a rotação
        y.right = z
        z.left = T3

        # Atualiza as alturas
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        # Retorna o novo nó raiz
        return y

    def generate_edges(self):
        """Gera as arestas para a visualização da árvore."""
        edges = []
        self._generate_edges(self.root, edges)
        return edges

    def _generate_edges(self, node, edges):
        """Gera recursivamente as arestas."""
        if node:
            if node.left:
                edges.append((node.value, node.left.value))
                self._generate_edges(node.left, edges)
            if node.right:
                edges.append((node.value, node.right.value))
                self._generate_edges(node.right, edges)


class BinaryTreeApp:
    """Classe que representa a aplicação gráfica."""
    def __init__(self, root):
        self.tree = AVLTree()

        # Configuração da janela principal
        self.root = root
        self.root.title("Árvore Binária AVL")
        self.root.geometry("400x300")
        self.root.configure(bg="#e0f7fa")

        # Título
        self.title_label = tk.Label(root, text="Árvore Binária AVL", font=("Arial", 16), bg="#e0f7fa", fg="#00796b")
        self.title_label.pack(pady=10)

        # Caixa de entrada para o número
        self.input_label = tk.Label(root, text="Digite um número:", font=("Arial", 12), bg="#e0f7fa", fg="#00796b")
        self.input_label.pack()

        self.number_entry = tk.Entry(root, font=("Arial", 12))
        self.number_entry.pack(pady=5)

        # Botões
        self.insert_button = tk.Button(root, text="Inserir na Árvore", font=("Arial", 12), bg="#004d40", fg="white", command=self.insert_number)
        self.insert_button.pack(pady=10)

        self.display_button = tk.Button(root, text="Exibir Árvore", font=("Arial", 12), bg="#004d40", fg="white", command=self.display_tree)
        self.display_button.pack(pady=5)

    def insert_number(self):
        """Insere o número digitado na árvore binária AVL."""
        try:
            value = int(self.number_entry.get())
            self.tree.insert(value)
            messagebox.showinfo("Sucesso", f"O número {value} foi inserido na árvore!")
            self.number_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido.")

    def display_tree(self):
        """Exibe a árvore binária AVL graficamente."""
        if not self.tree.root:
            messagebox.showwarning("Aviso", "A árvore está vazia. Insira números antes de exibi-la.")
            return

        edges = self.tree.generate_edges()
        graph = nx.DiGraph()
        graph.add_edges_from(edges)

        # Definindo layout para a árvore sem dependência de pygraphviz
        pos = nx.spring_layout(graph, seed=42)  # Usando o layout de força (spring layout)

        # Desenhando a árvore
        plt.figure(figsize=(8, 6))
        nx.draw(
            graph, pos, with_labels=True, arrows=True,
            node_size=1500, node_color="#81d4fa", font_size=12, font_color="black"
        )
        plt.title("Árvore Binária AVL", fontsize=16)
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryTreeApp(root)
    root.mainloop()
