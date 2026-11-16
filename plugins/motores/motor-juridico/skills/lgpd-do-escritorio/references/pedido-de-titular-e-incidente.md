# Pedido de titular e incidente de segurança

Leia nos modos pedido de titular e incidente. Citações marcadas pelas regras de `docs/citacoes.md`. Nos dois roteiros, quem decide e quem envia é a pessoa: o encarregado (`encarregado_lgpd`) e o advogado responsável.

## 1. Pedido de titular

### Quem pede e o que fazer

| Quem pede | O que fazer |
|---|---|
| O próprio cliente, ou ex-cliente | Seguir os passos abaixo |
| Representante (procurador, responsável por criança ou por pessoa curatelada) | Pedir a comprovação da representação, só o necessário, e seguir |
| Contato que nunca virou cliente | Seguir; normalmente há pouco dado e pode ser apagado |
| Parte contrária, testemunha ou terceiro pedindo dados de um caso | **Parar.** Vai ao advogado: sigilo profissional e exercício regular de direitos `[CONFERIR]`. Nenhum rascunho até ele decidir |
| Autoridade (ANPD, juízo, polícia) | Vai ao advogado e ao encarregado no mesmo dia. Nenhum rascunho |

### Os passos

1. **Registrar** em `07-operacao/juridico/lgpd/pedidos/AAAA-MM-DD-NN.md`: data e hora de chegada, canal, iniciais de quem pede, o que pede nas palavras dele, o prazo de resposta `[CONFERIR: art. 19 da Lei 13.709/2018 e a regulamentação vigente]`.
2. **Confirmar quem é**, pelo canal que o escritório já usa com a pessoa. Não peça documento além do necessário.
3. **Achar os dados** pelo mapa: comercial, caso, financeiro, WhatsApp, IA, base de partes.
4. **Separar o que pode e o que não pode:**
   - o que a lei manda guardar ou o que serve à defesa em processo pode ficar `[CONFERIR: art. 16 da Lei 13.709/2018]`;
   - dado de outra pessoa misturado (a conversa que fala do ex-cônjuge) não vai na cópia;
   - o que está sob sigilo profissional segue as regras da advocacia `[CONFERIR]`.
5. **Rascunhar a resposta** pela base abaixo e mostrar. As conferências ficam no cabeçalho "Antes de enviar". Quem envia é a pessoa, pelo canal oficial.
6. **Cumprir** o que foi decidido (apagar, corrigir, mandar cópia) e **fechar o registro** com a data e o que foi feito, sem copiar os dados para o registro.

### Direitos que o titular pode pedir (para conferir)

`art. 18 da Lei 13.709/2018 [CONFERIR: incisos e redação vigente]`: confirmação de que o escritório trata dados dele; acesso; correção; anonimização, bloqueio ou eliminação do que é desnecessário ou excessivo; portabilidade; eliminação do que foi tratado com consentimento; informação sobre com quem o escritório compartilha; informação sobre a possibilidade de não consentir; revogação do consentimento.

### Resposta-base: eliminação pedida por ex-cliente

```
---
antes_de_enviar:
  - conferir o prazo de resposta (art. 19 da Lei 13.709/2018) [CONFERIR]
  - conferir com o advogado o que fica por obrigação ou defesa (art. 16) [CONFERIR]
  - conferir o canal: responder pelo mesmo canal em que a pessoa pediu
---

[NOME], recebemos o seu pedido em [DATA].

Apagamos os dados que não precisamos mais: [O QUE FOI APAGADO, EM LINGUAGEM SIMPLES].

Alguns documentos do seu caso precisam ficar guardados por mais um tempo, porque a lei exige ou porque podem ser necessários para proteger os seus direitos e os do escritório: [O QUE FICA E ATÉ QUANDO]. Eles ficam com acesso restrito e serão apagados no fim desse prazo.

Se quiser saber mais, fale com [ENCARREGADO] por [CONTATO].
[ASSINATURA DA FICHA]
```

### Resposta-base: acesso (cópia dos dados)

```
[NOME], recebemos o seu pedido em [DATA]. Estes são os dados que o escritório guarda sobre você:
- [CATEGORIA]: [O QUE É], para [FINALIDADE], guardado até [PRAZO].
Os documentos do seu caso seguem em anexo [OU: estão à disposição para retirada], pelo canal oficial.
[ASSINATURA DA FICHA]
```

## 2. Incidente de segurança

Incidente é qualquer situação em que dado pessoal pode ter sido visto, copiado, perdido ou alterado por quem não devia: mensagem para a pessoa errada, celular perdido, e-mail invadido, link de pasta aberto, documento esquecido na impressora, conta de IA usada por outra pessoa.

### A ordem (não muda)

1. **Conter agora** (a pessoa que viu): apagar o envio onde der e pedir a quem recebeu que apague; trocar senha; revogar o link; bloquear o aparelho; tirar o acesso.
2. **Avisar hoje** o encarregado e o advogado responsável, pelo caminho de `urgencia_vai_para`. Antes de qualquer documento.
3. **Registrar** em `07-operacao/juridico/lgpd/incidentes/AAAA-MM-DD.md` (`assets/registro-de-incidente.md`), sem copiar os dados vazados.
4. **Avaliar o risco** com as perguntas abaixo. A conclusão é do encarregado.
5. **Decidir a comunicação** à ANPD e aos titulares, no prazo da regulamentação `[CONFERIR: art. 48 da Lei 13.709/2018 e a resolução da ANPD sobre comunicação de incidente; prazo, forma e conteúdo vigentes, e de quando o prazo conta]`. A habilidade prepara o rascunho; o encarregado envia pelo canal oficial da ANPD `[CONFERIR]`.
6. **Corrigir a causa** (grupo de WhatsApp separado, revisão de quem acessa a pasta, a regra de uso de IA) e registrar o aprendizado.

### Perguntas de risco

| Pergunta | Resposta |
|---|---|
| Que dados? Tem dado sensível, de criança, financeiro, de processo em segredo? | |
| De quantos titulares? | |
| Quem recebeu ou acessou? Conhecido, desconhecido, público? | |
| O dado foi apagado por quem recebeu? Há confirmação? | |
| O dado estava protegido (senha, criptografia)? | |
| Que dano pode causar à pessoa (constrangimento, discriminação, fraude, risco físico)? | |
| Desde quando o escritório sabe? | |
| Conclusão do encarregado: risco relevante ou não, e por quê | |

### Comunicação ao titular (rascunho para o encarregado)

```
---
antes_de_enviar:
  - decisão do encarregado de comunicar, com data [A CONFIRMAR]
  - conferir prazo e conteúdo exigidos (art. 48 e resolução da ANPD) [CONFERIR]
  - notícia sensível: de preferência por ligação do advogado antes da mensagem
---

[NOME], queremos te contar uma coisa que aconteceu no escritório e que envolve dados seus.

Em [DATA], [O QUE ACONTECEU, EM UMA FRASE SIMPLES]. Os dados envolvidos foram [QUAIS].

Assim que soubemos, [O QUE O ESCRITÓRIO FEZ]. Para evitar que se repita, [O QUE MUDOU].

[O QUE A PESSOA PODE FAZER, SE HOUVER].

Se quiser conversar, fale com [ENCARREGADO] por [CONTATO].
[ASSINATURA DA FICHA]
```

### O que nunca fazer

- Esperar o fim da semana para avisar o encarregado.
- Apagar o registro do que aconteceu.
- Mandar a comunicação ao titular sem o encarregado decidir, ou por mensagem automática.
- Contar o caso do cliente a quem não precisa saber, para explicar o incidente.
