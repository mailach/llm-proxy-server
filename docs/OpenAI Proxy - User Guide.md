# OpenAI Proxy

## OpenAI Proxy (gpt-4o, gpt-4o-mini, o3-mini)

Für praktische Projekte, in denen Modelle von OpenAI genutzt wird, bieten wir einen Proxy Server unter https://service.scadsai.uni-leipzig.de/sws-llm-proxy/ an.

## Unterstützte Modelle und Pricing

Price pro 1 Mio. tokens: (Stand: 03.2025)

| Model Snapshot           | Input | Output |
| ------------------------ | ----- | ------ |
| `o3-mini-2025-01-31`     | 1.10$ | 4.40$  |
| `gpt-4o-2024-11-20`      | 2.50$ | 10.00$ |
| `gpt-4o-mini-2024-07-18` | 0.15$ | 0.60$  |

Die aktuelle Liste der unterstützten Modelle und deren Preise finden Sie unter https://service.scadsai.uni-leipzig.de/sws-llm-proxy/.

### Account und Budget

Einen Account und entsprechende Zugangsdaten erhalten Sie beim Lehrpersonal. Ihrem Account ist ein festes Budget zugewiesen, und Ihren aktuellen Verbrauch können Sie unter https://service.scadsai.uni-leipzig.de/sws-llm-proxy/ einsehen. Sollten Sie Ihr Budget aufbrauchen, aber weitere Anfragen benötigen, wenden Sie sich bitte an das Lehrpersonal.

### API-Key

Unter https://service.scadsai.uni-leipzig.de/sws-llm-proxy/ können Sie Ihren API-Key kopieren oder sich einen neuen API-Key generieren. Dieser wird zur Authentifizierung gegenüber der `/chat/completions` API verwendet. Eine Authentifizierung mittels Nutzername und Passwort ist nicht möglich. Bitte bewahren Sie den Key sicher auf, achten Sie darauf, dass er nicht in öffentliche Repositories geladen wird.

### Verwendung mit Python OpenAI Library

Der Proxyserver kann mit der Python OpenAI Library wie folgt verwendet werden. Als OpenAI Key setzen Sie dann Ihren API-Key des Proxyservers entweder als Systemvariable (https://platform.openai.com/docs/libraries#create-and-export-an-api-key):

```python
from openai import OpenAI
client = OpenAI(base_url="https://service.scadsai.uni-leipzig.de/sws-llm-proxy/")
completion = client.chat.completions.create(
    model="model-snapshot",
    messages=[...]
)
```

... oder in einer .env Datei. Der API Key muss dann bei der Initialisierung des OpenAI clients als Parameter angegeben werden. Achten Sie hierbei darauf, die .env Datei in der .gitignore Datei zu vermerken.

### Requests und Parameter

Um die API anzusprechen, senden Sie einen POST-Request mit JSON content an https://service.scadsai.uni-leipzig.de/sws-llm-proxy/chat/completions

Dabei muss das enthaltene JSON wie folgt aussehen:

```json
{
  "model": "gpt-4o-mini-2024-07-18",
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "Who won the world series in 2020?" },
    {
      "role": "assistant",
      "content": "The Los Angeles Dodgers won the World Series in 2020."
    },
    { "role": "user", "content": "Where was it played?" }
  ],
  "temperature": 1.53,
  "top_p": 0.3,
  "max_tokens": 1000,
  "presence_penalty": 1.3,
  "frequency_penalty": 1.2,
  "stream": true,
  "response_format": { "type": "json_object" }
}
```

Die Properties temperature, top_p, max_tokens, presence_penalty, frequency_penalty und stream sind dabei optional. Beschreibungen, Defailtwerte sowie weitere Details entnehmen Sie bitte der OpenAI Dokumentation (https://platform.openai.com/docs/guides/gpt/chat-completions-api).

Sie müssen Ihrer Anfrage zusätzlich einen validen API-Key hinzufügen. Im Folgenden finden Sie Beispiele in Python und mit cURL:

```python
data = {
  "model" : "gpt-4o-mini-2024-07-18",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ],
}
url = "https://service.scadsai.uni-leipzig.de/sws-llm-proxy/chat/completions"
api_key = "my-api-key"
req = requests.post(url, headers={'Authorization': 'Bearer ' + api_key}, json=data)
```

cURL:

```bash
curl -X POST https://service.scadsai.uni-leipzig.de/sws-llm-proxy/chat/completions -H 'Authorization: Bearer my-api-key' -H 'Content-Type: application/json' -d '{"model" : "gpt-4o-mini-2024-07-18", "messages": [{"role": "user", "content": "Who won the world series in 2020?"}, {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."}, {"role": "user", "content": "Where was it played?"}]}'

```
