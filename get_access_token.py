import sys  # for command line arguments
import requests

def file2string_list(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace('\n', '').strip()
        return lines

def get_app_access_token(app_id, app_secret):           
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    #print file.text #to test what the FB api responded with
    result = file.text.split("=")[1]
    #print file.text #to test the TOKEN
    return result

if __name__ == "__main__":
    print("Fetching access token for app...")

    app_id, app_secret = file2string_list(sys.argv[1])
    access_token = get_app_access_token(app_id, app_secret)

    with open('access_token.txt', 'w') as outfile:
        outfile.write(access_token)
        outfile.close()

    print("Finished fetching access_token for app.")
    sys.exit(0)
