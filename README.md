# ICP RGB-D Registration using FAST + Optical Flow

Implementação de uma variante do algoritmo **ICP (Iterative Closest Point)** utilizando **FAST Feature Detection** e **Optical Flow** para registro 3D baseado em imagens **RGB-D**.

Projeto desenvolvido para a disciplina de **Visão Computacional**.

---

## Objetivo

Este projeto tem como objetivo realizar o alinhamento entre quadros consecutivos de um dataset RGB-D através de um pipeline composto por:

1. Detecção de características usando FAST;
2. Rastreamento entre quadros usando Optical Flow;
3. Conversão dos pontos 2D para coordenadas 3D utilizando profundidade;
4. Registro espacial utilizando ICP;
5. Visualização da nuvem de pontos e trajetória estimada.

---

## Pipeline

```text
RGB Frame
   ↓
FAST
   ↓
Optical Flow
   ↓
RGB-D → Projeção 3D
   ↓
ICP (Registro)
   ↓
Visualização + Trajetória
```

---

## Estrutura do Projeto

```text
icp-rgbd-fast-flow/

dataset/
├── rgb/
└── depth/

src/
├── main.py
├── feature_tracker.py
├── icp_registration.py
└── visualizer.py

requirements.txt
README.md
.gitignore
```

---

## Tecnologias

- Python 3.12+
- OpenCV
- NumPy
- Matplotlib

---

## Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd icp-rgbd-fast-flow
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Dataset

Este projeto utiliza imagens **RGB-D**.

O dataset utilizado durante os testes foi:

**TUM RGB-D Dataset**

Estrutura esperada:

```text
dataset/
├── rgb/
│   ├── frame1.png
│   ├── frame2.png
│   └── ...
│
└── depth/
    ├── frame1.png
    ├── frame2.png
    └── ...
```

⚠️ O dataset não está incluído neste repositório.

---

## Como Executar

Entre na pasta:

```bash
cd src
```

Execute:

```bash
python main.py
```

---

## Saídas do Sistema

### Janela RGB

Exibe:

- FAST (Amarelo)
- Optical Flow (Verde/Azul)
- Número do Frame
- Erro ICP
- Quantidade de pares 3D

---

### Visualização 3D

Exibe:

- Azul → Nuvem alvo
- Verde → Nuvem alinhada pelo ICP
- Vermelho → Trajetória acumulada

---

## Exemplo de Saída

```text
Frame: 100
FAST: 1327
Flow: 1216
Pares 3D: 1216
Erro: 0.011841
```

---

## Arquitetura

### `feature_tracker.py`

Responsável por:

- Leitura RGB-D
- FAST
- Optical Flow
- Projeção 3D

---

### `icp_registration.py`

Responsável por:

- Registro ICP
- Transformação espacial
- Cálculo de erro

---

### `visualizer.py`

Responsável por:

- Visualização RGB
- Visualização 3D
- Trajetória

---

### `main.py`

Responsável por:

- Controle do pipeline
- Processamento contínuo dos frames

---

## Resultados Esperados

O sistema realiza:

✅ Detecção de pontos de interesse  
✅ Rastreamento temporal  
✅ Conversão para coordenadas 3D  
✅ Registro espacial  
✅ Estimativa de trajetória

---

## Autores

- Bruno Iraê dos Reis

- Leonardo Henrique Caturyty da Silva Cavalcante

Projeto acadêmico — Visão Computacional