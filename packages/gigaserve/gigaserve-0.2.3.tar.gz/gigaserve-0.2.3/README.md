# GigaServe 🦜️🏓 = LangServe + GigaChat

GigaServe — это python-библиотека, которая позволяет размещать на сервере цепочки и runnable-объекты GigaChain с предоставлением к ним доступа через REST API.

Библиотека GigaServe интегрирована с [FastAPI](https://fastapi.tiangolo.com/) и использует для валидации данных [Pydantic](https://docs.pydantic.dev/latest/).

## Особенности библиотеки

Библиотека дает следующие возможности:

- Автоматическое определение схем ввода и вывода основе объекта GigaChain. Схемы применяются для каждого запроса к API и обеспечивают подробные сообщения об ошибках.
- Страница API-документации с JSONSchema и Swagger.
- Эндпоинты с поддержкой множества одновременных запросов на одном сервере `/invoke`, `/batch` и `/stream`.
- Эндпоинт `/stream_log` для потоковой передачи всех или выбранных промежуточных шагов работы цепочки/агента.
- **новое** поддержка эндпоинта  `/stream_events` (с версии 0.0.40), который упрощает работу с потоковой передачей, так позволяет не парсить вывод `/stream_log`.
- Интерактивная песочница `/playground` с потоковым отображением и демонстрацией промежуточных шагов.
- Использование проверенных open-source библиотек Python таких, как FastAPI, Pydantic, uvloop и asyncio.
- Клиентский SDK, который позволяет обращаться к серверу GigaServe также как к локальному runnable-интерфейсу или напрямую с помощью HTTP API.

### Ограничения

- Колбэки клиента не поддерживаются для событий, происходящих на сервере.
- OpenAPI-спецификация не генерируется, если вы используете Pydantic V2. Это связанно с тем, что Fast API не поддерживает [смешивание пространств имен pydantic v1 и v2](https://github.com/tiangolo/fastapi/issues/10360). Подробнее в разделе ниже.

## Установка {#ustanovka}

Для одновременной установки клиента и сервера используйте команду:

```bash
pip install "gigaserve[all]"
```

Вы можете установить клиент и сервер по отдельности с помощью команд:

```sh
# Команда установки клиента
pip install "gigaserve[client]"

# Команда установки сервера
pip gigaserve "langserve[server]"
```

## GigaChain CLI 🛠️

GigaChain CLI — это утилита, которая поможет быстро настроить проект GigaServe. Для этого используйте следующую команду:

```sh
gigachain app new ../path/to/directory
```

При работе с GigaChain CLI всегда используйте последнюю версию утилиты. Вы можете установить ее с помощью команды:

```sh
pip install -U gigachain-cli
```

## Подготовка к работе

Для управления зависимостями GigaServe использует `poetry`.
Подробнее об это инструменте в [официальной документации](https://python-poetry.org/docs/).

### 1. Создайте новое приложение с помощью команды gigachain cli.

```sh
langchain app new my-app
```

### 2. Задайте runnable-объекты с помощью метода add_routes.

Отредактируйте соответствующим образом файл `server.py`.

```sh
add_routes(app. NotImplemented)
```

### 3. Используйте `poetry` для добавления сторонних пакетов.

```sh
poetry add [package-name] // e.g `poetry add langchain-openai`
```

### 4. Задайте необходимые переменные среды.

Например:

```sh
export OPENAI_API_KEY="sk-..."
```

### 5. Запустите приложение.

```sh
poetry run langchain serve --port=8100
```

## Примеры

Для быстрого старта GigaServe используйте [шаблоны GigaChain](https://github.com/ai-forever/gigachain/blob/master/templates/README.md).

Больше примеров шаблонов вы найдете в [репозитории](https://github.com/ai-forever/gigaserve/tree/main/examples).

| Описание                                                                                                                                                                                                                                                           | Ссылки                                                                                                                                                                                                                           |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **LLMs** Пример небольшого приложения, работающего с моделями OpenAI и Anthropic. Демонстрирует асинхронную работу, поддержку передачи пакетов и потоковой генерации.                                                                                                                                              | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/llm/server.py), [client](https://github.com/ai-forever/gigaserve/blob/main/examples/llm/client.ipynb)                                                       |
| **Ретривер** Простой сервер, который предоставляет доступ к ретриверу.                                                                                                                                                                                                | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/retrieval/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/retrieval/client.ipynb)                                           |
| **Разговорный ретривер** [Разговорный ретривер](https://python.langchain.com/docs/expression_language/cookbook/retrieval#conversational-retrieval-chain) развернутый с помощью GigaServe                                                                           | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/conversational_retrieval_chain/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/conversational_retrieval_chain/client.ipynb) |
| **Агент** без **истории разговора**, основанный на [инструментах OpenAI](https://python.langchain.com/docs/modules/agents/agent_types/openai_functions_agent)                                                                                                            | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/agent/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/agent/client.ipynb)                                                   |
| **Агент** с **историей разговора**, основанный на [инструментах OpenAI](https://python.langchain.com/docs/modules/agents/agent_types/openai_functions_agent)                                                                                                               | [server](https://github.com/ai-forever/gigaserve/blob/main/examples/agent_with_history/server.py), [client](https://github.com/ai-forever/gigaserve/blob/main/examples/agent_with_history/client.ipynb)                         |
| [RunnableWithMessageHistory](https://python.langchain.com/docs/expression_language/how_to/message_history) имплементация чата с историей на бэкенде. Разделение сессий с помощью параметра `session_id`, который задает пользователь.                                                                    | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/chat_with_persistence/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/chat_with_persistence/client.ipynb)                   |
| [RunnableWithMessageHistory](https://python.langchain.com/docs/expression_language/how_to/message_history) имплементация чата с историей на бэкенде. Разделение сессий с помощью параметров `conversation_id`, который задает пользователь, и `user_id`. Подробнее о том, как реализовать `user_id` в разделе Аутентификация. | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/chat_with_persistence_and_user/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/chat_with_persistence_and_user/client.ipynb) |
| [Configurable Runnable](https://python.langchain.com/docs/expression_language/how_to/configure). Создает ретривер, поддерживающий инзменение конфигурации названия индекса в процессе работы.                                                                                      | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/configurable_retrieval/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/configurable_retrieval/client.ipynb)                 |
| [Configurable Runnable](https://python.langchain.com/docs/expression_language/how_to/configure). Показывает настраиваемые поля и альтернативы для них.                                                                                                      | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/configurable_chain/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/configurable_chain/client.ipynb)                         |
| **APIHandler** Показывает как использовать `APIHandler` вместо `add_routes`. Таким образом разработчики могут более гибко настраивать эндпоинты. Хорошо работает с различными применениями FastAPI, но требует больше затрат на разработку.                                                        | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/api_handler_examples/server.py)                                                                                                                             |
| **LCEL пример** Показывает как с помощью LCEL работать с входными данными в виде словаря.                                                                                                                                                                                          | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/passthrough_dict/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/passthrough_dict/client.ipynb)                             |
| **Аутентификация** с `add_routes`: Простая аутентификация, которую можно применить ко всем эндпоинтам приложения. Не подходит как решение для реализации работы с несколькими пользователями.                                                                                           | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/global_deps/server.py)                                                                                                                                 |
| **Аутентификация** с `add_routes`: Простой механизм аутентификации, основанный на зависимостях пути. Не подходит как решение для реализации работы с несколькими пользователями.                                                                                                                    | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/path_dependencies/server.py)                                                                                                                           |
| **Аутентификация** с `add_routes`: Работа с отдельными пользователями и аутентификация для эндпоинтов, которые используют отдельную конфигурацию для каждого запроса. В данный момент не работает с OpenAPI документацией.                                                                                 | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/per_req_config_modifier/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/per_req_config_modifier/client.ipynb)     |
| **Аутентификация** с `APIHandler`: Работа с отдельными пользователями и аутентификация, которая демонстрирует реализацию поиска только по документам пользователя.                                                                                                                                           | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/api_handler/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/api_handler/client.ipynb)                             |
| **Виджеты** Разные виджеты, которые можно использовать с песочницей (загрузка файла и чат).                                                                                                                                                                              | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/widgets/chat/tuples/server.py)                                                                                                                              |
| **Виджеты** Виджет загрузки файла для песочницы GigaServe.                                                                                                                                                                                                      | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/file_processing/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/file_processing/client.ipynb)                               |

## Пример приложения

### Сервер

Пример ниже разворачивает чат-модели GigaChat и других LLM, а также цепочку, которая генерирует шутку по заданной теме (`topic`) с помощью модели Anthropic.

```python
#!/usr/bin/env python
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import GigaChat, ChatAnthropic, ChatOpenAI

from langserve import add_routes

app = FastAPI(
  title="GigaChain Server",
  version="1.0",
  description="Простой API-сервер, использующий runnable-интерфейсы GigaChain",
)

add_routes(
    app,
    GigaChat(credentials=<авторизационные данные>),
    path="/gigachat",
) 

add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)

add_routes(
    app,
    ChatAnthropic(model="claude-3-haiku-20240307"),
    path="/anthropic",
)

model = ChatAnthropic()
prompt = ChatPromptTemplate.from_template("расскажи шутку о {topic}")
add_routes(
    app,
    prompt | model,
    path="/joke",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
```

### Документация

Сгенерированная OpenAPI-документация к серверу, развернутому с помощью предыдущего примера, доступна по адресу:

```sh
curl localhost:8000/docs
```

При этом, адрес `localhost:8000` будет возвращать ошибку 404, пока вы не определите `@app.get("/")`.

> [!NOTE]
> При использовании pydantic v2 [документация не генерируется](#работа-с-pydantic) для эндпоинтов `/invoke`, `/batch`, `/stream` и `stream_log`.

### Клиент

Пример клиента на основе Python SDK:

```python
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langserve import RemoteRunnable

openai = RemoteRunnable("http://localhost:8000/openai/")
anthropic = RemoteRunnable("http://localhost:8000/anthropic/")
joke_chain = RemoteRunnable("http://localhost:8000/joke/")

# Синхронный вызов

joke_chain.invoke({"topic": "попугаи"})

# Асинхронный вызов
await joke_chain.ainvoke({"topic": "попугаи"})

prompt = [
    SystemMessage(content='Веди себя как кошка или попугай.'),
    HumanMessage(content='Привет!')
]

# Поддержка astream
async for msg in anthropic.astream(prompt):
    print(msg, end="", flush=True)

prompt = ChatPromptTemplate.from_messages(
    [("system", "Расскажи мне длинную историю о {topic}")]
)

# Определение собственных цепочек
chain = prompt | RunnableMap({
    "openai": openai,
    "anthropic": anthropic,
})

chain.batch([{ "topic": "попугаи" }, { "topic": "кошки" }])
```

Пример клиента на TypeScript (для работы клиента требуется LangChain.js версии 0.0.166 или выше):

```typescript
import { RemoteRunnable } from "@langchain/core/runnables/remote";

const chain = new RemoteRunnable({
  url: `http://localhost:8000/joke/`,
});
const result = await chain.invoke({
  topic: "кошки",
});
```

Клиент, использующий Python-библиотеку `requests`:

```python
import requests

response = requests.post(
    "http://localhost:8000/joke/invoke/",
    json={'input': {'topic': 'кошки'}}
)
response.json()
```

Использование cURL:

```sh
curl --location --request POST 'http://localhost:8000/joke/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "input": {
            "topic": "кошки"
        }
    }'
```

## Эндпоинты

С помощью примера ниже вы можете добавить на сервер заранее подготовленные эндпоинты для работы с runnable-интерфейсами:

```python
...
add_routes(
    app,
    runnable,
    path="/my_runnable",
)
```

Список эндпоинтов:

- `POST /my_runnable/invoke` — вызвать runnable-интерфейс для единичных входных данных;
- `POST /my_runnable/batch` — вызвать runnable-интерфейс для набора входных данных;
- `POST /my_runnable/stream` — вызвать для единичных входных данных с потоковым выводом;
- `POST /my_runnable/stream_log` — вызвать для единичных входных данных с потоковым выводом, включая вывод промежуточных шагов по ходу генерации;
- `POST /my_runnable/astream_events` - вызвать для единичных входных данных и передавать поток событий, по мере их генерации, в том числе для промежуточных шагов;
- `GET /my_runnable/input_schema` — получить JSON-схему входных данных runnable-интерфейса;
- `GET /my_runnable/output_schema` — получить JSON-схему выходных данных runnable-интерфейса;
- `GET /my_runnable/config_schema` — получить JSON-схему параметров конфигурации runnable-интерфейса;

> [!NOTE]
> Эндпоинты работают в соответствии с интерфейсом [LangChain Expression Language (LCEL)](https://python.langchain.com/docs/expression_language/interface) — DSL для создания цепочек.

## Песочница

Страница песочницы доступна по адресу `/my_runnable/playground`.
На ней представлен простой интерфейс, который позволяет настроить параметры runnable-интерфейса и сделать запрос к нему с потоковым выводом и демонстрацией промежуточных шагов.

<p align="center">
<img src="https://github.com/ai-forever/gigaserve/assets/3205522/5ca56e29-f1bb-40f4-84b5-15916384a276" width="50%"/>
</p>

### Виджеты

Песочница поддерживает [виджеты](#playground-widgets) и может использоваться для тестирования ваших цепочек с разными входными данными.

Кроме этого, если цепочка может настраиваться, песочница предоставляет задать параметры цепочки и поделиться ссылкой на полученную конфигурацию.

### Обмен конфигурацией цепочки

In addition, for configurable runnables, the playground will allow you to configure the
runnable and share a link with the configuration:

<p align="center">
<img src="https://github.com/ai-forever/gigaserve/assets/3205522/86ce9c59-f8e4-4d08-9fa3-62030e0f521d" width="50%"/>
</p>


## Песочница для чата

GigaServe поддерживает отдельную версию песочницы с поддержкой чата, которая работает по адресу `/my_runnable/playground/`.
В отличие от общей песочницы в этом варианте поддерживаются только определенные типы runnable-объектов, в которых схема входных данных должна быть представлена в виде словаря который:

- либо содержит один ключ со списком сообщений чата. a single key, and that key's value must be a list of chat messages;
- либо содержит два ключа: один со списком сообщений чата, а другой с самым последним сообщением.

Рекомендуется использовать первый вариант.

Также, runnable-объект должен возвращать `AIMessage` или строку.

Чтобы включить такую песочницу нужно указать `playground_type="chat"` при добавлении пути:

```python
# Объявление цепочки
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Ты полезный, профессиональный помощник по имени Толя."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | ChatAnthropic(model="claude-2")


class InputChat(BaseModel):
    """Ввод для эндпоинта чата."""

    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="Сообщения чата в текущем разговоре.",
    )


add_routes(
    app,
    chain.with_types(input_type=InputChat),
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
    playground_type="chat",
)
```

<!--
If you are using LangSmith, you can also set `enable_feedback_endpoint=True` on your route to enable thumbs-up/thumbs-down buttons
after each message, and `enable_public_trace_link_endpoint=True` to add a button that creates a public traces for runs.
Note that you will also need to set the following environment variables:

```bash
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_PROJECT="YOUR_PROJECT_NAME"
export LANGCHAIN_API_KEY="YOUR_API_KEY"
```

Here's an example with the above two options turned on:

<p align="center">
<img src="./.github/img/chat_playground.png" width="50%"/>
</p>

Note: If you enable public trace links, the internals of your chain will be exposed. We recommend only using this setting
for demos or testing.
-->

## Работа с классическими цепочками

GigaServe работает как с runnable-интерфейсами (написанным с помощью [LangChain Expression Language](https://python.langchain.com/docs/expression_language/)), так и с классическими цепочками (посредством наследования от `Chain`).

При работе с классическими цепочками учитывайте, что некоторые входные схемы для таких цепочек могут вызывать ошибки, т.к. могут быть некорректными или неполными.
Такие ошибки можно предотвратить, если обновить атрибут `input_schema` таких цепочек в GigaChain.

## Развертывание

Ниже описаны способы развертывания на AWS, Google Cloud Platforms (GCP) и Azure.

### AWS

Для развертывания на AWS вы можете использовать [AWS Copilot CLI](https://aws.github.io/copilot-cli/).

```bash
copilot init --app [application-name] --name [service-name] --type 'Load Balanced Web Service' --dockerfile './Dockerfile' --deploy
```

Подробнее — в [официальной документации](https://aws.amazon.com/containers/copilot/).

### GCP

Для развертывания на GCP Cloud Run используйте команду:

```sh
gcloud run deploy [your-service-name] --source . --port 8001 --allow-unauthenticated --region us-central1 --set-env-vars=GIGACHAT_API_KEY=your_key
```

### Azure

Вы можете развернуть сервер на Azure с помощью Azure Container Apps:

```sh
az containerapp up --name [container-app-name] --source . --resource-group [resource-group-name] --environment  [environment-name] --ingress external --target-port 8001 --env-vars=OPENAI_API_KEY=your_key
```

Подробная информация в [официальной документации](https://learn.microsoft.com/en-us/azure/container-apps/containerapp-up).


## Работа с Pydantic

GigaServe поддерживает Pydantic v2 с некоторыми ограничениями:

- При использовании Pydantic v2 документация OpenAPI не генерируется. Это связанно с тем, что Fast API не поддерживает [смешивание пространств имен pydantic v1 и v2](https://github.com/tiangolo/fastapi/issues/10360).
- GigaChain использует пространство имен версии v1 в Pydantic v2.

За исключением указанных ограничений, эндпоинты API, страница песочницы и другие функции должны работать корректно.

## Дополнительные возможности

## Добавление аутентификации

О том, как добавить аутентификацию на свой сервер GigaServe — в разделах документации FastAPI, посвященных [безопасности](https://fastapi.tiangolo.com/tutorial/security/) и [использованию связующего ПО](https://fastapi.tiangolo.com/tutorial/middleware/).

Примеры ниже показывают как реализовать логику аутентификации в GigaServe с помощью примитивов FastAPI.

Вам предстоит самостоятельно реализовать логику для аутентификации, таблицы пользователей и др.

Если вы не уверены в своих силах, вы можете попробовать готовое решение [Auth0](https://auth0.com/).

#### Использование add_routes

[Примеры аутентификации](https://github.com/langchain-ai/langserve/tree/main/examples/auth) с помощью `add_routes`.

| Описание                                                                                                                                                                        | Ссылки                                                                                                                                                                                                                           |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Аутентификация** с `add_routes`: Простая аутентификация, которую можно применить ко всем эндпоинтам приложения. Не подходит как решение для реализации работы с несколькими пользователями.                                                                                           | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/global_deps/server.py)                                                                                                                                 |
| **Аутентификация** с `add_routes`: Простой механизм аутентификации, основанный на зависимостях пути. Не подходит как решение для реализации работы с несколькими пользователями.                                                                                                                    | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/path_dependencies/server.py)                                                                                                                           |
| **Аутентификация** с `add_routes`: Работа с отдельными пользователями и аутентификация для эндпоинтов, которые используют отдельную конфигурацию для каждого запроса. В данный момент не работает с OpenAPI документацией.                                                                                 | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/per_req_config_modifier/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/per_req_config_modifier/client.ipynb)     |

Вы также можете использовать [промежуточное ПО FastAPI](https://fastapi.tiangolo.com/tutorial/middleware/).

Преимущество использования глобальных зависимостей и зависимостей путей в том, что такая аутентификация будет корректно поддерживаться в OpenAPI-документации.
В то же време эти подходы не подходят для работы с отдельными пользователями. Например, для создания приложения, которое будет искать информацию только в документах отдельного пользователя.

Для реализации такой логики вы можете использовать `per_req_config_modifier` или `APIHandler` (см. ниже).

If you need to implement per user logic, you can use the `per_req_config_modifier` or `APIHandler` (below) to implement this logic.

**Работа с отдельным пользователем**

Если вам нужна авторизация, которая зависит от пользователя, при использовании `add_routes` задайте `per_req_config_modifier`.

Вызываемый объект получает необработанный объект `Request` и может извлекать из него данные для аутентификации и авторизации.

#### Использование APIHandler

Если вы хорошо знакомы с FastAPI и Python, вы можете использовать [APIHandler](https://github.com/langchain-ai/langserve/blob/main/examples/api_handler_examples/server.py) GigaServe.

| Описание                                                                                                                                                                                                 | Ссылки                                                                                                                                                                                                           |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Аутентификация** с `APIHandler`: Работа с отдельными пользователями и аутентификация, которая демонстрирует реализацию поиска только по документам пользователя.                                                                                                                                           | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/api_handler/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/auth/api_handler/client.ipynb)                             |
| **APIHandler** Показывает как использовать `APIHandler` вместо `add_routes`. Таким образом разработчики могут более гибко настраивать эндпоинты. Хорошо работает с различными применениями FastAPI, но требует больше затрат на разработку.                                                        | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/api_handler_examples/server.py)                                                                                                                             |

Этот подход сложнее, но при этом предоставляет полный контроль в определении эндпоинтов, что в свою очередь позволяет реальзовать любую логику аутентификации.

### Работа с файлами

Обработка файлов — это типичная задача для больших языковых моделей.
Существуют различные архитектурные подходы для решения этой задачи:

- Файл может быть загружен на сервер с помощью одного эндпоинта и обработан с помощью другого;
- Файл может быть представлен как в виде бинарного значения, так и в виде ссылки, например, на содержимое файла, размещенное в хранилище s3.
- Эндпоинт может быть блокирующим или неблокирующим.
- Сложную обработку можно выделить в отдельный пул процессов. 

Выбирайте подход в соответствии со своими задачами.

> [!NOTE]
> GigaServe не поддерживает тип `multipart/form-data`.
> Для загрузки бинарного значения файла в runnable-интерфейс используйте кодировку base64.
>
> [Пример загрузки файла закодированного с помощью base64](https://github.com/ai-forever/gigaserve/tree/main/examples/file_processing).
>
> Вы также можете загружать файлы с помощью ссылок (например, в хранилище s3) или загружать их на отдельный эндпоинт как `multipart/form-data`.

### Настраиваемые типы входных и выходных данных

Типы входных и выходных данных определяются для всех runnable-интерфейсов. Они доступны в аттрибутах `input_schema` и `output_schema`. GigaServe использует эти типы для валидации данных и генерации документации.

Вы можете переопределить наследованные типы с помощью метода `with_types`.

Общий пример работы с типами:

```python
from typing import Any

from fastapi import FastAPI
from langchain.schema.runnable import RunnableLambda

app = FastAPI()


def func(x: Any) -> int:
    """Ошибочно заданная функция, которая принимает любые данные, хотя должна принимать int."""
    return x + 1


runnable = RunnableLambda(func).with_types(
    input_type=int,
)

add_routes(app, runnable)
```

### Пользовательские типы

Для десериализации данных в pydantic-модель, а не `dict`, унаследуйтесь от `CustomUserType`.
При наследовании от этого типа сервер не будет преобразовывать данные в `dict`, а будет сохранять их как pydantic-модель.

```python
from fastapi import FastAPI
from langchain.schema.runnable import RunnableLambda

from langserve import add_routes
from langserve.schema import CustomUserType

app = FastAPI()


class Foo(CustomUserType):
    bar: int


def func(foo: Foo) -> int:
    """Пример функции, которая ожидает тип Foo, представленный в виде моде pydantic model"""
    assert isinstance(foo, Foo)
    return foo.bar

# Обратите внимание, что входные и выходные типы наследуются автоматически!
# Вам не нужно их указывать
# runnable = RunnableLambda(func).with_types( # <-- Не нужно в данном случае
#     input_schema=Foo,
#     output_schema=int,
#
add_routes(app, RunnableLambda(func), path="/foo")
```

> [!NOTE]
> Тип `CustomUserType` поддерживается только на стороне сервера и определяет поведение при декодировании данных.

### Виджеты интерактивной страницы

На странице песочницы вы можете создавать различные виджеты, демонстрирующие работу runnable-интерфейсов вашего бекенда.

Примеры:

| Описание                                                                                                                                                                                                                                                           | Ссылки                                                                                                                                                                                                                           |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Виджеты** Разные виджеты, которые можно использовать с песочницей (загрузка файла и чат).                                                                                                                                                                              | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/widgets/chat/tuples/server.py)                                                                                                                              |
| **Виджеты** Виджет загрузки файла для песочницы GigaServe.                                                                                                                                                                                                      | [server](https://github.com/ai-forever/gigaserve/tree/main/examples/file_processing/server.py), [client](https://github.com/ai-forever/gigaserve/tree/main/examples/file_processing/client.ipynb)                               |

#### Схема

- Виджет задается на уровне поля и поставляется как часть JSON-схемы вводного типа.
- Виджет должен содержать ключ `type`, значением которого является один из известного списка виджетов.
- Другие ключи виджета будут связаны со значениями, описывающими пути в JSON-объекте.

Общая схема:

```typescript
type JsonPath = number | string | (number | string)[];
type NameSpacedPath = { title: string; path: JsonPath }; // title используется для имитации JSON-схемы, но можно использовать namespace
type OneOfPath = { oneOf: JsonPath[] };

type Widget = {
    type: string // Какой-то хорошо известный тип, например, base64file, chat и др.
    [key: string]: JsonPath | NameSpacedPath | OneOfPath;
};
```

### Доступные виджеты

В настоящее время пользователи могут самостоятельно указывать два виджета:\

* виджет загрузки файла;
* виджет чата.

Остальные виджеты интерфейса песочницы создаются и управляются автоматически с помощью графического интерфейса основанного на конфигурационной схеме runnable-объекта.
При создании настраиваемых runnable-объектов песочница должна автоматически создавать подходящие виджеты, с помощью которых вы сможете контролировать работу runnable.

#### Виджет загрузки файла

Виджет позволяет загружать файлы в интерфейсе песочницы. Работает для файлов в виде base64-строки.

Фрагмент примера:

```python
try:
    from pydantic.v1 import Field
except ImportError:
    from pydantic import Field

from langserve import CustomUserType


# ВНИМАНИЕ: Наследуйтесь от CustomUserType, а не от BaseModel. В противном случае
#            сервер декодирует данные в dict, а не модель pydantic.
class FileProcessingRequest(CustomUserType):
    """Request including a base64 encoded file."""

    # Дополнительное поле используется, чтобы задать виджет в интерфейсе интерактивной страницы.
    file: str = Field(..., extra={"widget": {"type": "base64file"}})
    num_chars: int = 100

```

> [!NOTE]
> [Подробный пример загрузки файла](https://github.com/ai-forever/gigaserve/tree/main/examples/file_processing).

<p align="center">
<img src="https://github.com/ai-forever/gigaserve/assets/3205522/52199e46-9464-4c2e-8be8-222250e08c3f" width="50%"/>
</p>

### Виджет чата {#vidzhet-chata}

Пример виджета в [репозитории](https://github.com/ai-forever/gigaserve/blob/main/examples/widgets/server.py).

Чтобы задать виджет чата передайте `"type": "chat"`:

* Поле `input` — JSONPath к полю запроса, которое содержит новое входящее сообщение.
* Поле `output` — JSONPath к полю ответа, которое содержит одно или несколько сообщений.

Не указывайте эти поля, если входящие и исходящие данные должны быть представлены в исходном виде.
Например, если нужно представить исходящие данные в виде списка сообщений.

Пример:

```py
class ChatHistory(CustomUserType):
    chat_history: List[Tuple[str, str]] = Field(
        ...,
        examples=[[("human input", "ai response")]],
        extra={"widget": {"type": "chat", "input": "question", "output": "answer"}},
    )
    question: str


def _format_to_messages(input: ChatHistory) -> List[BaseMessage]:
    """Представление вводда в виде списка собщений."""
    history = input.chat_history
    user_input = input.question

    messages = []

    for human, ai in history:
        messages.append(HumanMessage(content=human))
        messages.append(AIMessage(content=ai))
    messages.append(HumanMessage(content=user_input))
    return messages


model = ChatOpenAI()
chat_model = RunnableParallel({"answer": (RunnableLambda(_format_to_messages) | model)})
add_routes(
    app,
    chat_model.with_types(input_type=ChatHistory),
    config_keys=["configurable"],
    path="/chat",
)
```

### Включение и отключение эндпоинтов {#vklyuchenie-i-otklyuchenie-endpointov}

Начиная с версии GigaServe 0.0.33, можно включать и отключать открытые эндпоинты.
Используйте атрибут `enabled_endpoints`, если вы хотите предотвратить перезапись эндпонтов при обновлении версии библиотеки.

Пример ниже включает варианты эндпоинтов `invoke`, `batch` и `config_hash`.

```python
add_routes(app, chain, enabled_endpoints=["invoke", "batch", "config_hashes"], path="/mychain")
```

Пример ниже отключает страницу песочницы для цепочки.

```python
add_routes(app, chain, disabled_endpoints=["playground"], path="/mychain")
```

## Безопасность

В версиях библиотеки 0.0.13—0.0.15 песочница, доступная по адресу `/playground`, позволяет получить доступ к произвольным файлам на сервере. Такое поведение [исправлено в версии библиотеки 0.0.16 и выше](https://github.com/langchain-ai/langserve/pull/98).
