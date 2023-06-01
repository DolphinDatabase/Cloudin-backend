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

### Setup k3d cluster

## Instalar o Docker:

**Instalação do Docker no Windows:**

  - Acesse o site oficial do Docker para Windows: https://www.docker.com/products/docker-desktop
  - Clique no botão "Download" para baixar o instalador do Docker para Windows.
  - Execute o instalador baixado e siga as instruções do assistente de instalação. Durante o processo de instalação, você pode ser solicitado a habilitar a virtualização do hardware em seu sistema.

  Após a conclusão da instalação, o Docker será iniciado automaticamente. Aguarde até que o ícone do Docker na bandeja do sistema indique que o Docker está em execução.

  Verifique a instalação do Docker executando o comando ```docker version``` em um terminal. Isso exibirá a versão do Docker instalada e confirmará que a instalação foi bem-sucedida.
  Verifique se o Docker não está instalado executando o comando docker version. Se não estiver instalado, siga as instruções apropriadas para o seu sistema operacional e instale o Docker.

**Instalação do Docker no Linux:**

  Abra um terminal no Linux. Execute os seguintes comandos, um por vez, para instalar o Docker:

  ```bash
  sudo apt update
  sudo apt install docker.io
  ```

  Após a conclusão da instalação, inicie o serviço Docker executando o seguinte comando:

  ```bash
  sudo systemctl start docker
  ```

  Adicione seu usuário ao grupo "docker" para que você possa executar comandos Docker sem precisar de privilégios de superusuário. Execute o seguinte comando:

  ```bash
  sudo usermod -aG docker $USER
  ```

  Faça logout e login novamente para aplicar as alterações de grupo. Verifique a instalação do Docker executando o comando ```docker version``` em um terminal. Isso exibirá a versão do Docker instalada e confirmará que a instalação foi bem-sucedida.
  Instalar o k3d:

  O k3d é uma ferramenta para criar clusters Kubernetes em Docker. Para instalá-lo, siga as instruções apropriadas para o seu sistema operacional, disponíveis na documentação oficial do k3d: https://k3d.io/#installation.

**Instalação do k3d no windows**

  Abra um terminal do PowerShell ou do CMD e execute o seguinte comando para baixar o executável do k3d:

  ```bash
  curl -LO https://github.com/rancher/k3d/releases/latest/download/k3d-windows-amd64.exe
  ```

  Renomeie o arquivo baixado para ```k3d.exe```

  ```bash
  ren k3d-windows-amd64.exe k3d.exe
  ```

  Mova o arquivo ```k3d.exe``` para um diretório incluído no seu PATH de sistema, como ```C:\Windows``` ou ```C:\Windows\System32```.

  Verifique a instalação do k3d executando o comando ```k3d version``` em um terminal. Isso exibirá a versão do k3d instalada e confirmará que a instalação foi bem-sucedida.

**Instalação do k3d no Linux:**

  Execute os seguintes comandos para baixar e instalar o k3d:

  ```bash
  curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash
  ```

  Verifique a instalação do k3d executando o comando ```k3d version``` em um terminal. Isso exibirá a versão do k3d instalada e confirmará que a instalação foi bem-sucedida.

  **Instalação do kubectl no Windows:**

  Abra um navegador da web e acesse o seguinte link: https://dl.k8s.io/release/v1.21.0/bin/windows/amd64/kubectl.exe

  Faça o download do arquivo ```kubectl.exe``` clicando com o botão direito do mouse no link e selecionando "Salvar link como". Escolha um local no seu sistema para salvar o arquivo.

  Mova o arquivo ```kubectl.exe``` para um diretório incluído no seu PATH de sistema, como ```C:\Windows``` ou ```C:\Windows\System32```.

  Abra um terminal do PowerShell ou do CMD.

  Verifique a instalação do ```kubectl``` executando o comando ```kubectl version --client``` em um terminal. Isso exibirá a versão do ```kubectl``` instalada e confirmará que a instalação foi bem-sucedida.

**Instalação do kubectl no Linux:**

  Execute os seguintes comandos para baixar o kubectl e torná-lo executável:

  ```bash
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  chmod +x kubectl
  ```

  Mova o arquivo ```kubectl``` para um diretório incluído no seu PATH de sistema, como ```/usr/local/bin```:

  ```bash
  sudo mv kubectl /usr/local/bin
  ```

  Verifique a instalação do ```kubectl``` executando o comando ```kubectl version --client``` em um terminal. Isso exibirá a versão do ```kubectl``` instalada e confirmará que a instalação foi bem-sucedida.

**Instalação do Helm no Windows:**

  Abra um navegador da web e acesse o seguinte link: https://get.helm.sh/helm-v3.7.0-windows-amd64.zip

  Faça o download do arquivo ```helm-v3.7.0-windows-amd64.zip``` clicando no link. Escolha um local no seu sistema para salvar o arquivo.

  Extraia o conteúdo do arquivo ZIP para um diretório de sua escolha.

  Abra um terminal do PowerShell ou do CMD.

  Navegue até o diretório onde você extraiu o arquivo ZIP do Helm.

  Verifique se a instalação do Helm foi bem-sucedida executando o comando ```helm version``` em um terminal. Isso exibirá a versão do Helm instalada e confirmará que a instalação foi concluída com êxito.

**Instalação do Helm no Linux:**

  Execute os seguintes comandos para baixar e instalar o Helm:

  ```bash
  curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
  ```

  Verifique se a instalação do Helm foi bem-sucedida executando o comando ```helm version``` em um terminal. Isso exibirá a versão do Helm instalada e confirmará que a instalação foi concluída com êxito.

**Criar um cluster Kubernetes com o k3d:**

  Execute o seguinte comando para criar um cluster Kubernetes com o k3d:

  ```bash
  k3d cluster create --config k3d-simple-cluster.yaml
  ```

  Você terá um log parecido com isso:

  ```bash
  INFO[0000] Using config file k3d-simple-cluster.yaml (k3d.io/v1alpha2#simple) 
  WARN[0000] Default config apiVersion is 'k3d.io/v1alpha4', but you're using 'k3d.io/v1alpha2': consider migrating.
  INFO[0000] portmapping '80:80' targets the loadbalancer: defaulting to [servers:**:proxy agents:**:proxy]
  INFO[0000] Prep: Network
  INFO[0000] Created network 'k3d-my-cluster'
  INFO[0000] Created image volume k3d-my-cluster-images
  INFO[0000] Starting new tools node...
  INFO[0001] Starting Node 'k3d-my-cluster-tools'
  INFO[0001] Creating node 'k3d-my-cluster-server-0'
  INFO[0003] Creating node 'k3d-my-cluster-agent-0'
  INFO[0003] Creating node 'k3d-my-cluster-agent-1'
  INFO[0005] Creating node 'k3d-my-cluster-agent-2'
  INFO[0005] Creating LoadBalancer 'k3d-my-cluster-serverlb'
  INFO[0005] Using the k3d-tools node to gather environment information
  INFO[0007] Starting new tools node...
  INFO[0007] Starting Node 'k3d-my-cluster-tools'
  INFO[0009] Starting cluster 'my-cluster'
  INFO[0009] Starting servers...
  INFO[0009] Starting Node 'k3d-my-cluster-server-0'
  INFO[0015] Starting agents...
  INFO[0015] Starting Node 'k3d-my-cluster-agent-1'
  INFO[0015] Starting Node 'k3d-my-cluster-agent-0'
  INFO[0015] Starting Node 'k3d-my-cluster-agent-2'
  INFO[0027] Starting helpers...
  INFO[0027] Starting Node 'k3d-my-cluster-serverlb'      
  INFO[0038] Injecting records for hostAliases (incl. host.k3d.internal) and for 6 network members into CoreDNS configmap...
  INFO[0051] Cluster 'my-cluster' created successfully!   
  INFO[0051] You can now use it like this:
  kubectl cluster-info
  ```

  Execute ```kubectl apply --filename test-cluster/``` para aplicar um exmplo de deployment de uma aplicação e acessar fora do cluster na localhost.
