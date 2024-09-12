import sys
import os

# Adiciona o diretório nox_py_sdk ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nox_py_sdk')))

from nox_py_sdk.checkout_api import CheckoutApi

def test_checkout_api():
    api_token = '0093e230-445e-41ec-88e1-b8ddce19808d'
    checkout_api = CheckoutApi(api_token)
    
    # Teste o método get_checkouts
    # print("Testando get_checkouts...")
    # try:
    #     checkouts = checkout_api.get_checkouts()
    #     print("Checkouts obtidos com sucesso:", checkouts)
    # except Exception as e:
    #     print("Erro ao obter checkouts:", e)

    #Teste o método get_checkout
    # print("Testando get_checkout...")
    # try:
    #     checkout = checkout_api.get_checkout('0989d6cc-b02c-493b-b953-dab39dbc214b')
    #     print("Checkout obtido com sucesso:", checkout)
    # except Exception as e:
    #     print("Erro ao obter o checkout:", e)

    # # Teste o método create_checkout
    # print("Testando create_checkout...")
    # try:
    #     # Exemplo de dados para criar um novo checkout
    #     new_checkout_data = {
    #         "colors": {
    #             "primary": "#000000",
    #             "secondary": "#FFFFFF",
    #             "text": "#333333",
    #             "button": "#FF0000",
    #             "textButton": "#FFFFFF"
    #         },
    #         "price": 100,
    #         "description": "Produto Teste",
    #         "redirect_url": "https://exemplo.com/sucesso",
    #         "payment_method": "credit_card",
    #         "is_enabled": True,
    #         "theme_color": "#0000FF"
    #     }
    #     new_checkout = checkout_api.create_checkout(new_checkout_data)
    #     print("Checkout criado com sucesso:", new_checkout)
    # except Exception as e:
    #     print("Erro ao criar checkout:", e)
    
    # # Teste o método update_checkout
    print("Testando update_checkout...")
    try:
        # Exemplo de dados para atualizar um checkout existente
        update_checkout_data = {}
        print(os.getcwd())
        with open('tests/about-us-2-fallback.jpg', 'rb') as img_file:
            print(img_file)
            update_response = checkout_api.update_checkout(12, update_checkout_data, file=img_file)
            print("Checkout atualizado com sucesso:", update_response)
    except Exception as e:
        print("Erro ao atualizar checkout:", e)

if __name__ == "__main__":
    test_checkout_api()
