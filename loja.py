class Cliente:
    # Guarda os dados de identificação e endereço de um cliente.
    def __init__(self, nome, cpf, email, rua, cidade, cep):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep


class Produto:
    # Representa um produto que pode ser vendido pela loja.
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


class ItemDoPedido:
    # Representa um produto e sua quantidade em um pedido.
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade


class ItensDoPedido:
    # Controla os itens de um pedido e suas operações.
    def __init__(self):
        self.__itens = []

    def adicionar(self, produto, quantidade):
        item = ItemDoPedido(produto, quantidade)
        self.__itens.append(item)

    def esta_vazia(self):
        return len(self.__itens) == 0

    def calcular_total(self):
        total = 0
        for item in self.__itens:
            total = total + item.quantidade * item.produto.preco
        return total

    def imprimir(self):
        for item in self.__itens:
            print("  ", item.quantidade, "x", item.produto.nome, "= R$ %.2f" % (
                item.quantidade * item.produto.preco
            ))


class StatusPedido:
    # Representa uma situação possível de um pedido.
    def __init__(self, descricao):
        self.descricao = descricao


StatusPedido.ABERTO = StatusPedido("aberto")
StatusPedido.PAGO = StatusPedido("pago")
StatusPedido.CANCELADO = StatusPedido("cancelado")


class TipoPedido:
    # Define o percentual de desconto aplicado ao pedido.
    def __init__(self, percentual_desconto):
        self.percentual_desconto = percentual_desconto


TipoPedido.VAREJO = TipoPedido(0.10)
TipoPedido.FUNCIONARIO = TipoPedido(0.20)
TipoPedido.NORMAL = TipoPedido(0)


class Pedido:
    # Reúne o cliente, o tipo, os itens e o status de um pedido.
    def __init__(self, cliente, tipo):
        self.cliente = cliente
        self.tipo = tipo
        self.itens = ItensDoPedido()
        self.status = StatusPedido.ABERTO

    def get_status(self):
        return self.status

    def set_status(self, valor):
        self.status = valor

    def adicionar_item(self, produto, quantidade):
        self.itens.adicionar(produto, quantidade)

    def calcular_total(self):
        return self.itens.calcular_total()


def validar_dados(cliente):
    if len(cliente.email) > 0:
        if "@" in cliente.email:
            if len(cliente.cpf) == 11:
                if len(cliente.cep) == 8:
                    return "ok"
                else:
                    return "cep invalido"
            else:
                return "cpf invalido"
        else:
            return "email invalido"
    else:
        return "email vazio"


def calcular_desconto(tipo, total):
    return total * tipo.percentual_desconto


def calcular_valor_a_pagar(pedido):
    return pedido.calcular_total() - calcular_desconto(
        pedido.tipo, pedido.calcular_total()
    )


class Pedidos:
    # Gerencia os pedidos cadastrados e os relatórios da loja.
    def __init__(self):
        self.__pedidos = {}

    def novo_pedido(self, numero, cliente, tipo):
        resultado = validar_dados(cliente)
        if resultado != "ok":
            print("pedido", numero, "recusado:", resultado)
            return None
        else:
            pedido = Pedido(cliente, tipo)
            self.__pedidos[numero] = pedido
            return pedido

    def imprimir_relatorio(self):
        for numero, pedido in self.__pedidos.items():
            print("Pedido", numero, "-", pedido.cliente.nome, "-", pedido.cliente.cidade)
            print("  status:", pedido.get_status().descricao)
            pedido.itens.imprimir()
            if not pedido.itens.esta_vazia():
                print("  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f" % (
                    pedido.calcular_total(),
                    calcular_desconto(pedido.tipo, pedido.calcular_total()),
                    calcular_valor_a_pagar(pedido)
                ))

    def calcular_total_arrecadado(self):
        total = 0
        for pedido in self.__pedidos.values():
            if pedido.get_status() == StatusPedido.PAGO:
                total = total + calcular_valor_a_pagar(pedido)
        return total

    def contar_pedidos_abertos(self):
        quantidade = 0
        for pedido in self.__pedidos.values():
            if pedido.get_status() == StatusPedido.ABERTO:
                quantidade = quantidade + 1
        return quantidade


def pagar_pedido(pedido):
    if pedido.get_status() == StatusPedido.ABERTO:
        if not pedido.itens.esta_vazia():
            pedido.set_status(StatusPedido.PAGO)
            return True
        else:
            return False
    else:
        return False


def cancelar_pedido(pedido):
    if pedido.get_status() == StatusPedido.ABERTO:
        pedido.set_status(StatusPedido.CANCELADO)
        return True
    else:
        return False


# Roteiro da loja

pedidos = Pedidos()

cliente_ana = Cliente(
    "Ana Souza", "12345678901", "ana@mail.com",
    "Rua das Flores, 10", "Sorocaba", "18010000"
)

cliente_bruno = Cliente(
    "Bruno Lima", "123", "bruno@mail.com",
    "Av. Central, 200", "Votorantim", "18110000"
)

cliente_carla = Cliente(
    "Carla Dias", "98765432100", "carla.mail.com",
    "Rua do Sol, 55", "Sorocaba", "18020000"
)

cliente_diego = Cliente(
    "Diego Rocha", "11122233344", "diego@mail.com",
    "Rua Nova, 7", "Itu", "13300000"
)

cliente_eva = Cliente(
    "Eva Nunes", "55566677788", "eva@mail.com",
    "Alameda Azul, 1", "Itu", "13300001"
)

cliente_fabio = Cliente(
    "Fabio Costa", "99988877766", "fabio@mail.com",
    "Rua Velha, 3", "Itu", "123"
)

cliente_gil = Cliente(
    "Gil Alves", "44455566677", "gil@mail.com",
    "Rua do Meio, 9", "Sorocaba", "18030000"
)


produto_caderno = Produto("Caderno", 15.5)
produto_caneta = Produto("Caneta", 2.5)
produto_livro = Produto("Livro", 89.5)
produto_fone = Produto("Fone", 60.0)


pedido_da_ana = pedidos.novo_pedido(1, cliente_ana, TipoPedido.VAREJO)
pedido_da_ana.adicionar_item(produto_caderno, 2)
pedido_da_ana.adicionar_item(produto_caneta, 5)

pedidos.novo_pedido(2, cliente_bruno, TipoPedido.NORMAL)

segundo_pedido_da_ana = pedidos.novo_pedido(3, cliente_ana, TipoPedido.VAREJO)
segundo_pedido_da_ana.adicionar_item(produto_livro, 1)

pedidos.novo_pedido(4, cliente_carla, TipoPedido.FUNCIONARIO)

pedido_do_diego = pedidos.novo_pedido(5, cliente_diego, TipoPedido.NORMAL)

pedido_da_eva = pedidos.novo_pedido(6, cliente_eva, TipoPedido.FUNCIONARIO)
pedido_da_eva.adicionar_item(produto_fone, 1)

pedidos.novo_pedido(7, cliente_fabio, TipoPedido.NORMAL)

pedido_do_gil = pedidos.novo_pedido(8, cliente_gil, TipoPedido.NORMAL)
pedido_do_gil.adicionar_item(produto_fone, 2)


print("pagar 1:", pagar_pedido(pedido_da_ana))
print("pagar 3:", pagar_pedido(segundo_pedido_da_ana))
print("pagar 5:", pagar_pedido(pedido_do_diego))
print("pagar 6:", pagar_pedido(pedido_da_eva))
print("cancelar 5:", cancelar_pedido(pedido_do_diego))
print("cancelar 1:", cancelar_pedido(pedido_da_ana))

pedidos.imprimir_relatorio()
print("arrecadado: R$ %.2f" % pedidos.calcular_total_arrecadado())
print("abertos:", pedidos.contar_pedidos_abertos())
