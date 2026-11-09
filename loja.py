class Pessoa:
    # Guarda os dados pessoais e valida CPF e e-mail.
    def __init__(self, nome, cpf, email):
        self.__nome = nome
        self.__cpf = cpf
        self.__email = email

    def validar_dados(self):
        if len(self.__email) == 0:
            return "email vazio"
        if "@" not in self.__email:
            return "email invalido"
        if len(self.__cpf) != 11:
            return "cpf invalido"
        return "ok"

    def imprimir_identificacao(self, endereco, numero):
        endereco.imprimir_identificacao(self.__nome, numero)


class Endereco:
    # Guarda o endereço e valida o CEP do cliente.
    def __init__(self, rua, cidade, cep):
        self.__rua = rua
        self.__cidade = cidade
        self.__cep = cep

    def validar_cep(self):
        if len(self.__cep) != 8:
            return "cep invalido"
        return "ok"

    def imprimir_identificacao(self, nome, numero):
        print("Pedido", numero, "-", nome, "-", self.__cidade)


class TipoNormal:
    # Calcula o desconto de um cliente do tipo normal.
    def desconto_sobre(self, valor):
        return valor * 0


class TipoVip:
    # Calcula o desconto de um cliente VIP.
    def desconto_sobre(self, valor):
        return valor * 0.10


class TipoFuncionario:
    # Calcula o desconto de um funcionário.
    def desconto_sobre(self, valor):
        return valor * 0.20


class Cliente:
    # Reúne os dados pessoais, endereço e tipo de um cliente.
    def __init__(self, pessoa, endereco, tipo):
        self.__pessoa = pessoa
        self.__endereco = endereco
        self.__tipo = tipo

    def validar_dados(self):
        pessoa = self.__pessoa
        resultado = pessoa.validar_dados()
        if resultado != "ok":
            return resultado
        endereco = self.__endereco
        return endereco.validar_cep()

    def imprimir_identificacao(self, numero):
        pessoa = self.__pessoa
        endereco = self.__endereco
        pessoa.imprimir_identificacao(endereco, numero)

    def calcular_desconto(self, total):
        tipo = self.__tipo
        return tipo.desconto_sobre(total)


class Produto:
    # Representa um produto e calcula seus valores.
    def __init__(self, nome, preco):
        self.__nome = nome
        self.__preco = preco

    def calcular_subtotal(self, quantidade):
        return quantidade * self.__preco

    def imprimir_item(self, quantidade):
        subtotal = self.calcular_subtotal(quantidade)
        print(
            "  ", quantidade, "x", self.__nome,
            "= R$ %.2f" % subtotal
        )


class ItemDoPedido:
    # Representa um produto e sua quantidade em um pedido.
    def __init__(self, produto, quantidade):
        self.__produto = produto
        self.__quantidade = quantidade

    def calcular_total(self):
        produto = self.__produto
        quantidade = self.__quantidade
        return produto.calcular_subtotal(quantidade)

    def imprimir(self):
        produto = self.__produto
        quantidade = self.__quantidade
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
        self.__descricao = descricao

    def imprimir(self):
        print("  status:", self.__descricao)

    def esta_aberto(self):
        return self == StatusPedido.ABERTO

    def esta_pago(self):
        return self == StatusPedido.PAGO


StatusPedido.ABERTO = StatusPedido("aberto")
StatusPedido.PAGO = StatusPedido("pago")
StatusPedido.CANCELADO = StatusPedido("cancelado")


class Pedido:
    # Reúne o cliente, os itens e o status de um pedido.
    def __init__(self, cliente):
        self.__cliente = cliente
        self.__itens = ItensDoPedido()
        self.__status = StatusPedido.ABERTO

    def adicionar_item(self, produto, quantidade):
        itens = self.__itens
        itens.adicionar(produto, quantidade)

    def calcular_total(self):
        itens = self.__itens
        return itens.calcular_total()

    def calcular_desconto(self):
        total = self.calcular_total()
        cliente = self.__cliente
        return cliente.calcular_desconto(total)

    def calcular_valor_a_pagar(self):
        total = self.calcular_total()
        desconto = self.calcular_desconto()
        return total - desconto

    def esta_vazio(self):
        itens = self.__itens
        return itens.esta_vazia()

    def esta_pago(self):
        status = self.__status
        return status.esta_pago()

    def esta_aberto(self):
        status = self.__status
        return status.esta_aberto()

    def imprimir_identificacao(self, numero):
        cliente = self.__cliente
        cliente.imprimir_identificacao(numero)

    def imprimir_status(self):
        status = self.__status
        status.imprimir()

    def imprimir_itens(self):
        itens = self.__itens
        itens.imprimir()

    def imprimir_relatorio(self, numero):
        self.imprimir_identificacao(numero)
        self.imprimir_status()
        self.imprimir_itens()
        if not self.esta_vazio():
            print(
                "  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f"
                % (
                    self.calcular_total(),
                    self.calcular_desconto(),
                    self.calcular_valor_a_pagar()
                )
            )

    def pagar(self):
        status = self.__status
        if not status.esta_aberto():
            return False
        itens = self.__itens
        if itens.esta_vazia():
            return False
        self.__status = StatusPedido.PAGO
        return True

    def cancelar(self):
        status = self.__status
        if not status.esta_aberto():
            return False
        self.__status = StatusPedido.CANCELADO
        return True

    def valor_arrecadado(self):
        if not self.esta_pago():
            return 0
        return self.calcular_valor_a_pagar()

    def contar_como_aberto(self):
        return int(self.esta_aberto())


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
            pedido.imprimir_relatorio(numero)

    def calcular_total_arrecadado(self):
        total = 0
        pedidos = self.__pedidos
        for pedido in pedidos.values():
            total = total + pedido.valor_arrecadado()
        return total

    def contar_pedidos_abertos(self):
        quantidade = 0
        pedidos = self.__pedidos
        for pedido in pedidos.values():
            quantidade = quantidade + pedido.contar_como_aberto()
        return quantidade


# Roteiro da loja

pedidos = Pedidos()

cliente_ana = Cliente(
    Pessoa("Ana Souza", "12345678901", "ana@mail.com"),
    Endereco("Rua das Flores, 10", "Sorocaba", "18010000"),
    TipoVip()
)

cliente_bruno = Cliente(
    Pessoa("Bruno Lima", "123", "bruno@mail.com"),
    Endereco("Av. Central, 200", "Votorantim", "18110000"),
    TipoNormal()
)

cliente_carla = Cliente(
    Pessoa("Carla Dias", "98765432100", "carla.mail.com"),
    Endereco("Rua do Sol, 55", "Sorocaba", "18020000"),
    TipoFuncionario()
)

cliente_diego = Cliente(
    Pessoa("Diego Rocha", "11122233344", "diego@mail.com"),
    Endereco("Rua Nova, 7", "Itu", "13300000"),
    TipoNormal()
)

cliente_eva = Cliente(
    Pessoa("Eva Nunes", "55566677788", "eva@mail.com"),
    Endereco("Alameda Azul, 1", "Itu", "13300001"),
    TipoFuncionario()
)

cliente_fabio = Cliente(
    Pessoa("Fabio Costa", "99988877766", "fabio@mail.com"),
    Endereco("Rua Velha, 3", "Itu", "123"),
    TipoNormal()
)

cliente_gil = Cliente(
    Pessoa("Gil Alves", "44455566677", "gil@mail.com"),
    Endereco("Rua do Meio, 9", "Sorocaba", "18030000"),
    TipoNormal()
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
