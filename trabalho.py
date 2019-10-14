import requests #biblioteca que faz nosso get e post http
import json #biblioteca que nos permite lidar com json em python
import hashlib #biblioteca para criptografia (chave sha1)
#import os


#aqui definimos nome do arquivo que vamos usar pro nosso json
filename = 'answer.json'

#define o token
token = '3b9d13ab83b180cc0fbbccc16c8645bb785d43ab'


#junta string to url com token
urlget = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=3b9d13ab83b180cc0fbbccc16c8645bb785d43ab' 
print(urlget)

#manda o get pro servidor e salva resposta na variavel r
#r = requests.get('https://postman-echo.com/get?foo1=bar1&foo2=bar2')
r = requests.get(urlget) 

print(r.status_code)

# cria arquivo answer.json, poe conteudo da variavel r no arquivo
with open(filename, 'w') as outfile:
    json.dump(r.json(), outfile)
    

    

    
#funcao de criptografar texto com negocio de cesar

def encrypt(text,s): 
    result = "" 
  
    # itera sobre tamanho do texto
    for i in range(len(text)): 
        #pega o caracter i do texto
        char = text[i] 
  
       
  
        # se for letra minuscula faz essas contas pra criptografar 10 pro lado e poe na string resultado
        if (char.islower()): 
            result += chr((ord(char) + s - 97) % 26 + 97) 
        
        # se for letra maiuscula faz essas contas pra criptografar 10 pro lado e poe na string resultado
        elif (char.isupper()): 
            result += chr((ord(char) + s-65) % 26 + 65) 
        
        # se nao for maiuscula nem minuscula nao muda o caracter (so poe na string resultado)
        else:
            result += char
            
      #returna a string criptografada
    return result

# por causa das propriedades do alphabeto, descriptografar e a mesma coisa que criptografar com 26-s
def decrypt(text, s):
    return encrypt(text, 26-s)





#abre json que criamos e pega conteudos e poe na variavel data
with open(filename, "r") as jsonFile:
    data = json.load(jsonFile)

#pega numero de casas e texto cifrado do nosso json
casas = data["numero_casas"]
texto_cifrado = data["cifrado"]

texto_cifrado = texto_cifrado.lower()

#decifra texto com funcao definida acima
texto_decifrado = decrypt(texto_cifrado, casas)

#usa biblioteca hashlib pra pegar chave sha1 do texto
#(biblioteca so aceita textos com encode por isso mandamos encode no texto antes de passar)
m = hashlib.sha1(texto_decifrado.encode('utf-8'))
#o hexdigest nos da o output
texto_sha1 = m.hexdigest()

#poe nossos valores calculados nos campos corretos do json
data["decifrado"] = texto_decifrado
data["resumo_criptografico"] = texto_sha1

#abre o nosso arquivo answer.json e poe ali o nosso novo json (sobreescreve o velho)
with open(filename, "w") as jsonFile:
    json.dump(data, jsonFile)



#aqui denoovo definimos o url do post
urlpost = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=3b9d13ab83b180cc0fbbccc16c8645bb785d43ab'


#posturl = "https://postman-echo.com/post"

#botamos nosso arquivo nesse mapa, com a chave correspondente 'answer' (como pedido no pdf)
files = {
         # 'answer': (os.path.basename(filename), open(filename, 'rb'), 'application/octet-stream')
        'answer': open(filename, 'rb')
    }

#ja que mandamos um mapa, a biblioteca requests manda o post no formato desejado
r = requests.post(urlpost, files=files)

print(r.json())
