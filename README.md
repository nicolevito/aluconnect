# AluConnect

**AluConnect** é um backend desenvolvido em **Python 3.10 com Django e Django REST Framework, integrado a PostgreSQL, RabbitMQ e Celery, todo o projeto feito com docker.**, voltado para gerenciamento de cursos, progresso de alunos e emissão de certificados.

## 1️⃣ Funcionalidades e Resultados do Case

O projeto implementa as seguintes funcionalidades:

**Gerenciamento de Cursos e Aulas:** CRUD completo de cursos e lições.

**Progresso do Aluno:** Registro automático do progresso em aulas, com verificação de conclusão do curso.

**Certificados:** Geração automática de certificados ao concluir o curso, utilizando integração opcional com OpenAI para textos motivacionais.

**Autenticação e Perfis de Usuário:** Sistema customizado de perfis, vinculado ao usuário Django padrão.

**API RESTful:** Endpoints claros para integração com front-end ou outros serviços.

**Resultados obtidos:**

Cobertura de testes em 70% do código, incluindo testes unitários e de views.

Fluxo completo de registro de progresso e geração de certificados testado e funcional.

Estrutura modular que permite escalabilidade e manutenção fácil.

## 2️⃣ Passo a Passo para Executar o Projeto

Clone o repositório:

git clone https://github.com/seu-usuario/AluConnect.git
cd AluConnect/src

# subir containers 

sudo docker compose up -d --build

# executar testes 

docker compose run --rm --entrypoint "" web pytest --cov=. --cov-report=term

# verificar logs do docker

docker compose logs -f

# Configure variáveis de ambiente em um arquivo .env:

DJANGO_SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/aluconnect
RABBITMQ_URL=amqp://guest:guest@localhost:5672//
OPENAI_API_KEY=your_openai_api_key



O backend estará disponível em http://localhost:8000. Tendo varias possibilidades de teste via curl ou com teste automatizado com cobertura de 74% do projeto.


## 3️⃣ Como Rodar Testes

Rodar todos os testes:

pytest


# Gerar relatório de cobertura:

pytest --cov=.
coverage html


O relatório HTML será gerado na pasta htmlcov e pode ser aberto no navegador.

## 4️⃣ Principais Decisões de Design

Arquitetura Modular: Cada app (courses, lessons, progress, certificates, students) é independente, facilitando manutenção e testes.

Uso de Celery e RabbitMQ: Para tarefas assíncronas, como geração de certificados, garantindo que processos longos não bloqueiem o backend.

Serializer e Views baseadas em DRF: API clara e consistente, com endpoints bem definidos.

Custom UserProfile: Extensão do modelo de usuário Django para armazenar informações específicas de alunos.

Fallback para geração de certificados: Caso o OpenAI não esteja disponível, é usado texto padrão para garantir funcionalidade.

Testes automatizados: Cobertura de endpoints críticos e lógica de negócios, garantindo confiabilidade.