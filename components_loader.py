import json

DATABASE = "components.json"

### READ
def CheckJSON(file):
    pFile = open(file, mode='r')
    json_data = json.load(pFile)
    pFile.close()

    counter = 0
    for item in json_data:
        counter += 1
        print("ITEM: " + str(counter))
        print("Name: " + item['Name'])

        print("Binary_URL: ")
        for bin_item in item['Binary_URL']:
            print('  ' + bin_item['bin_name'] + ' : ' + bin_item['URL'])

        print("Additions: ")
        print("  Config: " + item['Config'][0])
        print("<-->")

# Time to check it
CheckJSON(DATABASE)