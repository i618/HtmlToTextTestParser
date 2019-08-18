from main import MainInformation

print('Input url:')
url = input()
info = MainInformation(url)
info.saveToFile()
print('Done')
