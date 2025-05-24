from fastapi import FastAPI, Request

def handler(request: Request):
    print("MEOWOWOWOWOW")
    print(vars(request))

    return 200