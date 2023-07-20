import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if req.method == 'POST':
        if 'file' in req.files:
            file = req.files['file']
            if file.content_type == 'application/vnd.ms-excel':
                file_content = file.read()
                return func.HttpResponse(f"Arquivo XLS {file.filename} recebido e processado com sucesso.", status_code=200)
            else:
                return func.HttpResponse("Por favor, envie um arquivo XLS válido.", status_code=400)
        else:
            return func.HttpResponse("Nenhum arquivo XLS enviado na requisição.", status_code=400)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
