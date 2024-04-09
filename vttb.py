#visuall_text_to_braille
import requests
#TOKEN = "6878835899:AAER8UWrYAUTSmyfIwTe2IC0yomJ6FbXmWg"
TOKEN = "6364470508:AAGN7OX8K12GH1CpPDOwxGfOqU7MVT63w_o"
#chat_id = "298040358"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
package = requests.get(url).json()
chat_id = package['result'][0]['message']['chat']['id']
text = package['result'][0]['message']['text']

dict = {
    'a': '⠁',
    'b': '⠃',
    'c': '⠉',
    'd': '⠙',
    'e': '⠑',
    'f': '⠋',
    'g': '⠛',
    'h': '⠓',
    'i': '⠊',
    'j': '⠚',
    'k': '⠅',
    'l': '⠇',
    'm': '⠍',
    'n': '⠝',
    'o': '⠕',
    'p': '⠏',
    'q': '⠟',
    'r': '⠗',
    's': '⠎',
    't': '⠞',
    'u': '⠥',
    'v': '⠧',
    'w': '⠺',
    'x': '⠭',
    'y': '⠽',
    'z': '⠵'
}

#user_text = input('enter the word')
user_text = text
word = user_text
braille = ''
for x in word:
	b = dict[x.lower()]
	braille = braille + b

print(braille)
w = braille
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={w}"
requests.get(url).json() # this sends the message
