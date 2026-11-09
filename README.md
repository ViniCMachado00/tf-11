# TF-11 — Refatoração de código

### 1. Normalização
A normalização ajuda a organizar os dados e evitar informações duplicadas. No exemplo da Ana, separamos os dados pessoais e o endereço em classes próprias, deixando cada responsabilidade mais clara.

### 2. Primitive Obsession
Primitive Obsession acontece quando usamos tipos primitivos para representar conceitos que deveriam ter suas próprias classes. Criamos objetos como `Cpf` e `Dinheiro` para concentrar validações e comportamentos específicos.

### 3. Tell Don't Ask
Tell Don't Ask significa pedir que um objeto execute uma ação, em vez de consultar seus dados e decidir por ele. Por isso, o próprio pedido possui os métodos `pagar()` e `cancelar()`, responsáveis por controlar essas operações.

### 4. Fail First
Fail First consiste em verificar primeiro as condições de erro e interromper a execução quando necessário. Isso evita estruturas complexas com `else` e permite utilizar polimorfismo para tratar os diferentes tipos de cliente.

### 5. Classes e responsabilidades
Cada classe deve ter uma responsabilidade bem definida. Por exemplo, `Cliente` reúne pessoa, endereço e tipo de cliente, enquanto `ItensDoPedido` administra os itens e `Pedidos` administra a coleção de pedidos.

### 6. Dívida técnica
Dívida técnica é o custo futuro causado por decisões de implementação que dificultam a manutenção do código. A refatoração reduz essa dívida ao melhorar a organização, legibilidade e separação de responsabilidades.
