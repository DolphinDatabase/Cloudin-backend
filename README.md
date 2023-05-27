### How to use a Python env

If you have not the package intalled previuously, start with that in you machine
```python
pip install virtualenv
```

Create your env
```python
python -m venv myenv
```

Activate your env
  - In windows
    ```bash
    myenv/Scripts/activate.bat
    ```

  - In macOS/Linux
    ```bash
    source myenv/bin/activate
    ```

Install the requirements
```bash
pip install -r requirements.txt
```

To leave the env
```bash
deactivate
```

### Git Flow
Git Flow é um modelo de fluxo de trabalho que simplifica e organizar o versionamento de ramificações de um projeto de desenvolvimento no Git. 

O Git Flow pode ser utilizado em qualquer projeto de software e está alinhado à prática de DevOps de entrega contínua.
 o Git Flow atribui funções bem específicas para diferentes ramificações e define quando elas devem interagir. 
Além disso, conta com ramificações individuais para preparar, manter e registrar lançamentos.
O Git Flow funciona através do uso de ramificações (branches) do projeto, 
Podendo ser comparado a uma árvore com seus galhos. 
Nesse fluxo de trabalho, as branches podem ser divididas em três tipos: 
- Main
- Develop
- Feature
As Fetures são branches de suporte que são descartadas após cumprirem seu propósito. 
Para cada uma das branches , existem algumas regras específicas que precisam ser seguidas para manter a otimização do versionamento:
Main é a ramificação principal que contém o código-fonte em produção. 
Não é permitido realizar alterações (commit) diretamente na main. A Master ainda é utilizada para enviar os commits dos releases para a produção;

Develop: criada a partir da Main, e reúne os códigos e se comunica com a Main. Ela contém o código-fonte mais atual e todas as novas features estáveis que serão mescladas posteriormente;

Feature: criada a partir da ramificação Develop, é uma branch temporária que carrega uma nova funcionalidade para o projeto, ela sempre acabará sendo mesclada à própria Develop através de merge. 
Git Flow

- Branch main
Branch principal do repositório, ela e representa a linha de produção estável do nosso projeto. 
Nela contém apenas o código que foi completamente testado e aprovado para ser implantado em produção. 
Os Commits nesta branch são feitos por meio de merges vindos da Branch Dev.

- Branch develop: 
Branch develop é a branch de desenvolvimento principal do nosso projeto.
É a partir dessa branch que novas funcionalidades e correções de bugs são desenvolvidas.
Ela deve sempre estar organizada, com os códigos testados, porém não necessariamente estável o suficiente para implantação em produção. 
Commits diretos na branch develop são evitados, e o trabalho é feito principalmente em branches de features.

- Branches de features: 
Branches criadas a partir da branch develop e são usadas para desenvolver as novas funcionalidades do projeto, ou até mesmo realizar modificações. 
Uma vez concluída, a branch da feature, é mergeada de volta para a branch develop.
