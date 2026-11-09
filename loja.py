class Pessoa:
    # Guarda os dados pessoais e valida CPF e e-mail.
    def __init__(self, nome, cpf, email):
        self.nome = nome
        self.cpf = cpf
        self.email = email

    def validar_dados(self):
        if len(self.email) == 0:
            return "email vazio"
        if "@" not in self.email:
            return "email invalido"
        if len(self.cpf) != 11:
            return "cpf invalido"
        return "ok"

    def imprimir_identificacao(self, endereco, numero):
        cidade = endereco.cidade
        print("Pedido", numero, "-", self.nome, "-", cidade)


class Endereco:
    # Guarda o endereço e valida o CEP do cliente.
    def __init__(self, rua, cidade, cep):
        self.rua = rua
        self.cidade = cidade
        self.cep = cep

    def validar_cep(self):
        if len(self.cep) != 8:
            return "cep invalido"
        return "ok"


class Cliente:
    # Reúne os dados pessoais, endereço e tipo de um cliente.
    def __init__(self, pessoa, endereco, tipo):
        self.pessoa = pessoa
        self.endereco = endereco
        self.tipo = tipo

    def validar_dados(self):
        pessoa = self.pessoa
        resultado = pessoa.validar_dados()
        if resultado != "ok":
            return resultado

        endereco = self.endereco
        return endereco.validar_cep()

    def imprimir_identificacao(self, numero):
        pessoa = self.pessoa
        endereco = self.endereco
        pessoa.imprimir_identificacao(endereco, numero)

    def calcular_desconto(self, total):
        tipo = self.tipo
        return tipo.calcular_desconto(total)


class Produto:
    # Representa um produto e calcula seus valores.
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def calcular_subtotal(self, quantidade):
        return quantidade * self.preco

    def imprimir_item(self, quantidade):
        subtotal = self.calcular_subtotal(quantidade)
        print(
            "  ", quantidade, "x", self.nome,
            "= R$ %.2f" % subtotal
        )


class ItemDoPedido:
    # Representa um produto e sua quantidade em um pedido.
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def calcular_total(self):
        produto = self.produto
        quantidade = self.quantidade
        return produto.calcular_subtotal(quantidade)

    def imprimir(self):
        produto = self.produto
        quantidade = self.quantidade
        produto.imprimir_item(quantidade)


class ItensDoPedido:
    # Controla os itens de um pedido e suas operações.
    def __init__(self):
        self.__itens = []

    def adicionar(self, produto, quantidade):
        item = ItemDoPedido(produto, quantidade)
        itens = self.__itens
        itens.append(item)

    def esta_vazia(self):
        itens = self.__itens
        return len(itens) == 0

    def calcular_total(self):
        total = 0
        itens = self.__itens
        for item in itens:
            total = total + item.calcular_total()
        return total

    def imprimir(self):
        itens = self.__itens
        for item in itens:
            item.imprimir()


class StatusPedido:
    # Representa uma situação possível de um pedido.
    def __init__(self, descricao):
        self.descricao = descricao

    def imprimir(self):
        print("  status:", self.descricao)

    def esta_aberto(self):
        return self == StatusPedido.ABERTO

    def esta_pago(self):
        return self == StatusPedido.PAGO


StatusPedido.ABERTO = StatusPedido("aberto")
StatusPedido.PAGO = StatusPedido("pago")
StatusPedido.CANCELADO = StatusPedido("cancelado")


class TipoPedido:
    # Define e calcula o percentual de desconto de um pedido.
    def __init__(self, percentual_desconto):
        self.percentual_desconto = percentual_desconto

    def calcular_desconto(self, total):
        return total * self.percentual_desconto


TipoPedido.VAREJO = TipoPedido(0.10)
TipoPedido.FUNCIONARIO = TipoPedido(0.20)
TipoPedido.NORMAL = TipoPedido(0)


class Pedido:
    # Reúne o cliente, os itens e o status de um pedido.
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = ItensDoPedido()
        status_aberto = StatusPedido.ABERTO
        self.status = status_aberto

    def adicionar_item(self, produto, quantidade):
        itens = self.itens
        itens.adicionar(produto, quantidade)

    def calcular_total(self):
        itens = self.itens
        return itens.calcular_total()

    def calcular_desconto(self):
        total = self.calcular_total()
        cliente = self.cliente
        return cliente.calcular_desconto(total)

    def calcular_valor_a_pagar(self):
        total = self.calcular_total()
        desconto = self.calcular_desconto()
        return total - desconto

    def esta_vazio(self):
        itens = self.itens
        return itens.esta_vazia()

    def esta_pago(self):
        status = self.status
        return status.esta_pago()

    def esta_aberto(self):
        status = self.status
        return status.esta_aberto()

    def imprimir_identificacao(self, numero):
        cliente = self.cliente
        cliente.imprimir_identificacao(numero)

    def imprimir_status(self):
        status = self.status
        status.imprimir()

    def imprimir_itens(self):
        itens = self.itens
        itens.imprimir()

    def pagar(self):
        status = self.status
        if not status.esta_aberto():
            return False

        itens = self.itens
        if itens.esta_vazia():
            return False

        status_pago = StatusPedido.PAGO
        self.status = status_pago
        return True

    def cancelar(self):
        status = self.status
        if not status.esta_aberto():
            return False

        status_cancelado = StatusPedido.CANCELADO
        self.status = status_cancelado
        return True


class Pedidos:
    # Gerencia os pedidos cadastrados e os relatórios da loja.
    def __init__(self):
        self.__pedidos = {}

    def novo_pedido(self, numero, cliente):
        resultado = cliente.validar_dados()
        if resultado != "ok":
            print("pedido", numero, "recusado:", resultado)
            return None

        pedido = Pedido(cliente)
        pedidos = self.__pedidos
        pedidos[numero] = pedido
        return pedido

    def imprimir_relatorio(self):
        pedidos = self.__pedidos
        for numero, pedido in pedidos.items():
            pedido.imprimir_identificacao(numero)
            pedido.imprimir_status()
            pedido.imprimir_itens()
            if not pedido.esta_vazio():
                print(
                    "  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f"
                    % (
                        pedido.calcular_total(),
                        pedido.calcular_desconto(),
                        pedido.calcular_valor_a_pagar()
                    )
                )

    def calcular_total_arrecadado(self):
        total = 0
        pedidos = self.__pedidos
        for pedido in pedidos.values():
            if pedido.esta_pago():
                total = total + pedido.calcular_valor_a_pagar()
        return total

    def contar_pedidos_abertos(self):
        quantidade = 0
        pedidos = self.__pedidos
        for pedido in pedidos.values():
            if pedido.esta_aberto():
                quantidade = quantidade + 1
        return quantidade


# Roteiro da loja

pedidos = Pedidos()

cliente_ana = Cliente(
    Pessoa("Ana Souza", "12345678901", "ana@mail.com"),
    Endereco("Rua das Flores, 10", "Sorocaba", "18010000"),
    TipoPedido.VAREJO
)

cliente_bruno = Cliente(
    Pessoa("Bruno Lima", "123", "bruno@mail.com"),
    Endereco("Av. Central, 200", "Votorantim", "18110000"),
    TipoPedido.NORMAL
)

cliente_carla = Cliente(
    Pessoa("Carla Dias", "98765432100", "carla.mail.com"),
    Endereco("Rua do Sol, 55", "Sorocaba", "18020000"),
    TipoPedido.FUNCIONARIO
)

cliente_diego = Cliente(
    Pessoa("Diego Rocha", "11122233344", "diego@mail.com"),
    Endereco("Rua Nova, 7", "Itu", "13300000"),
    TipoPedido.NORMAL
)

cliente_eva = Cliente(
    Pessoa("Eva Nunes", "55566677788", "eva@mail.com"),
    Endereco("Alameda Azul, 1", "Itu", "13300001"),
    TipoPedido.FUNCIONARIO
)

cliente_fabio = Cliente(
    Pessoa("Fabio Costa", "99988877766", "fabio@mail.com"),
    Endereco("Rua Velha, 3", "Itu", "123"),
    TipoPedido.NORMAL
)

cliente_gil = Cliente(
    Pessoa("Gil Alves", "44455566677", "gil@mail.com"),
    Endereco("Rua do Meio, 9", "Sorocaba", "18030000"),
    TipoPedido.NORMAL
)


produto_caderno = Produto("Caderno", 15.5)
produto_caneta = Produto("Caneta", 2.5)
produto_livro = Produto("Livro", 89.5)
produto_fone = Produto("Fone", 60.0)


pedido_da_ana = pedidos.novo_pedido(1, cliente_ana)
pedido_da_ana.adicionar_item(produto_caderno, 2)
pedido_da_ana.adicionar_item(produto_caneta, 5)

pedidos.novo_pedido(2, cliente_bruno)

segundo_pedido_da_ana = pedidos.novo_pedido(3, cliente_ana)
segundo_pedido_da_ana.adicionar_item(produto_livro, 1)

pedidos.novo_pedido(4, cliente_carla)

pedido_do_diego = pedidos.novo_pedido(5, cliente_diego)

pedido_da_eva = pedidos.novo_pedido(6, cliente_eva)
pedido_da_eva.adicionar_item(produto_fone, 1)

pedidos.novo_pedido(7, cliente_fabio)

pedido_do_gil = pedidos.novo_pedido(8, cliente_gil)
pedido_do_gil.adicionar_item(produto_fone, 2)


print("pagar 1:", pedido_da_ana.pagar())
print("pagar 3:", segundo_pedido_da_ana.pagar())
print("pagar 5:", pedido_do_diego.pagar())
print("pagar 6:", pedido_da_eva.pagar())
print("cancelar 5:", pedido_do_diego.cancelar())
print("cancelar 1:", pedido_da_ana.cancelar())

pedidos.imprimir_relatorio()
print("arrecadado: R$ %.2f" % pedidos.calcular_total_arrecadado())
print("abertos:", pedidos.contar_pedidos_abertos())

