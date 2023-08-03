import logging
import azure.functions as func
import pandas as pd # é necessario instalar a lib xlrd
import json
import os

'''
Referência
https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=linux%2Cportal%2Cv2%2Cbash&pivots=programming-language-python
'''

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Rota POST do otimizador
    if req.method == 'POST':
        status_code = 400
        if 'file' in req.files:
            file = req.files['file']
            if file.content_type == 'application/vnd.ms-excel':
                # leitura do arquivo (apenas para log)
                file_content = file.read()
                df = pd.read_excel(file_content, engine='xlrd')
                print(df.head())

                message = f"File {file.filename} successfully received and processed."
                print(message)
                status_code = 200
            else:
                message = f"Please upload a valid XLS file. Submitted format: {file.content_type}."
        else:
            message = "File not uploaded."
            
        obj = {"message": message}
        return func.HttpResponse(json.dumps(obj, indent=4), status_code=status_code)

    # Envio de arquivo - matriz OD
    elif req.method == 'GET':
        xls_file_path = os.path.join(os.getcwd(), 'Files', 'ODmatrix.xls')

        try:
            with open(xls_file_path, "rb") as xls_file:
                xls_data = xls_file.read()

                headers = {
                    "Content-Type": "application/vnd.ms-excel",
                    "Content-Disposition": "attachment; filename=ODmatrix.xls"
                }

                return func.HttpResponse(xls_data, headers=headers, status_code=200)
        except FileNotFoundError:
            message = "File not found."
            obj = {"message": message}
            return func.HttpResponse(json.dumps(obj, indent=4), status_code=404)

    # Somente para teste na rota GET
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
