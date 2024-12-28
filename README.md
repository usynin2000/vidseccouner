
1. Get sepoliat eth tokens: https://cloud.google.com/application/web3/faucet/ethereum/sepolia
2. Get PRIVATE_KEY from Metamsk account, give to .env
3. Get INFURA_API_KEY from https://www.infura.io/
4. 

Add to .env
PRIVATE_KEY from metamask.




```shell
make up
```



for me:
docker run -p 3030:80 \
    -v $(pwd)/videos:/opt/static/videos \
    -v $(pwd)/nginx.conf:/usr/local/nginx/conf/nginx.conf \
    -v $(pwd)/logs:/var/log/nginx \
    --entrypoint sh nytimes/nginx-vod-module -c "mkdir -p /var/lib/nginx/body && chmod 777 /var/lib/nginx/body && exec /usr/local/nginx/sbin/nginx -g 'daemon off;'"


http://localhost:3030/videos/
