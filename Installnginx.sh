ssh -i "spl.pem" ubuntu@ec2-18-216-0-219.us-east-2.compute.amazonaws.com << EOF
    sudo wget http://nginx.org/keys/nginx_signing.key
    sudo apt-key add nginx_signing.key
    cd /etc/apt
    sudo apt-get update
    sudo apt-get install nginx
    sudo service nginx start
EOF
