### Idea

I had this idea to create a microservice that is able to return signatures of common Windows API functions. This might be used for a debugger to know at runtime what the parameters are for a function at its breakpoint.
This code simply abuses `clangd` with a placeholder `c` template file to requests the signature of the given function name.

I have no idea yet if this is actually a good idea to build further on, but lets see ;)

### Build

Build using docker

```sh
docker build -t 'win-api-info-service' .
```

### Run

Run using docker

```sh
docker run --rm -d -p 4444:4444 'win-api-info-service'
```

### Request

Request using `curl`

```sh
curl -X 'POST' -H 'Content-Type: application/json' --data-binary $'{\"name\":\"CreateFile\"}' http://127.0.0.1:4444/api/signature
```

Result

```json
{
  "name": "CreateFile",
  "signatures": [
    {
      "label": "CreateFileA(LPCSTR lpFileName, DWORD dwDesiredAccess, DWORD dwShareMode, LPSECURITY_ATTRIBUTES lpSecurityAttributes, DWORD dwCreationDisposition, DWORD dwFlagsAndAttributes, HANDLE hTemplateFile) -> HANDLE",
      "parameters": [
        {
          "label": "LPCSTR lpFileName"
        },
        {
          "label": "DWORD dwDesiredAccess"
        },
        {
          "label": "DWORD dwShareMode"
        },
        {
          "label": "LPSECURITY_ATTRIBUTES lpSecurityAttributes"
        },
        {
          "label": "DWORD dwCreationDisposition"
        },
        {
          "label": "DWORD dwFlagsAndAttributes"
        },
        {
          "label": "HANDLE hTemplateFile"
        }
      ]
    }
  ]
}
```