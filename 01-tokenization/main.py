import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, I am Piyush Garg"
tokens = enc.encode(text)

print("Tokens:", tokens)

tokens = [13225, 11, 357, 939, 398, 3403, 1776, 170676]
decoded = enc.decode(tokens)

print("Decoded Text:", decoded)