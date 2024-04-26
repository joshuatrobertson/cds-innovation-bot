import base64
import json


def extract_private_key(json_file_path, output_pem_file):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

        # Navigate to the private_key under boxAppSettings/appAuth
        private_key_data = data.get('boxAppSettings', {}).get('appAuth', {}).get('privateKey', None)

        if private_key_data:
            # Decode the base64 encoded private key
            rsa_private_key_data = base64.b64decode(private_key_data)

            # Write the private key to a PEM file
            with open(output_pem_file, 'wb') as pem_file:
                pem_file.write(rsa_private_key_data)
            print(f"Private key extracted and saved to {output_pem_file}")
        else:
            print("Private key data not found in the JSON file.")


# Example usage
json_file_path = r'C:\Users\josh\PycharmProjects\cds-innovation-bot\0_zmbs1kqk_config.json'
output_pem_file = 'private_key.pem'  # Replace with the desired output PEM file path

extract_private_key(json_file_path, output_pem_file)
