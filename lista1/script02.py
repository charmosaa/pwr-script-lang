print(
    '''
    witaj w shopindoo
    blablablabla
    blabla...
    wypełnij formularz i dostań znieżkę
    '''
)
name = input("podaj imię: ")
email = input("podaj email: ")

product_name = 'buty'
price = float(199.99)
in_stock = True
discount = 20
final_price = price * (100-discount)/100

print(f'Witaj {name}!')
print(f'regularna cena produktu {product_name} to {price}')
print(f'jednak specjalnie dla ciebie cena dzisiaj wynosi {final_price:.2f}!!!')
