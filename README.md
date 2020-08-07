Objective Deploy ngnix webserver on EC2 frontending with ELB in single click

Using tool.py the complete infrastructure can be setup for hosting ngnix

python tool.py

Libraries
  boto3
  
Using installngnix.sh the ngnix server with static page can be deployed 

chmod u+x installngnix.sh
./installngnix.sh


A combination of Python for infrastructure hosting and Bash for ngnix installation was used since it simplifies the process and helps in reusability

The python infrastucture provisioning  tool can be added with more capability and scaled
Bash script for ngnix installation can be reused with python tool
