import subprocess

# mnemonic = subprocess.check_output([
#     'cardano-wallet', 'recovery-phrase', 'generate'
# ])

# print(mnemonic)

s = subprocess.check_output(["echo", "Hello World!"])
print("s = " + str(s))