# download data
gdown --id 13dF7KYDqfu_Qd2Dqc8ZkJy8P-ZHLUAAS
unzip dataset.zip
rm dataset.zip

# install librabries
pip install flask-cors
pip install flask-ngrok

# install ngrok token
curl https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.tgz -o ngrok.tgz
tar xvzf ngrok.tgz
./ngrok authtoken 24Gj4z8JODNMriG0cCB9NfWTRzg_3zzBeRVQnynadewEHQDaG