import httplib2
import json

def get_cep_info(cep: str):
    url = ('https://viacep.com.br/ws/' + cep + '/json/')
    h = httplib2.Http()
    reponse, content = h.request(url,'GET')
    result = json.loads(content)
    return result

print(get_cep_info("13289734"))
