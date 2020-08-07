
#Output provisions a load balanced wed server
#Connect to myaccount
#create a ELB load balancer, if exists dont create 
# Create a EC2 instance , if exists dont create
# deploy ngnix into the infrasturcture 
#it should open a static home page which says static CISCO SPL
#access keyid
#Secret Access Key
# configure aws : >>aws configure (give access key , secret key , region , output type)
#pip install boto3
#import boto3
#creating a connection (ec2 = boto3.resource('ec2'))
#launching new instance : ec2.create_instances(ImageId='<ami-image-id>', MinCount=1, MaxCount=1)
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migrationec2.html#launching-new-instances
#ami id : ami-0a63f96e85105c6d3

import boto3

def connecttomyaccount():
    print("connecting to my account")
    ec2 = boto3.resource('ec2')
    #it to use ny connection for creating an instanc
    createsubnet(ec2)

def createsubnet(ec2):
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc.create_tags(Tags=[{"Key":"TestVPC2","Value":"default_vpc2"}])
    vpc.wait_until_available()
    print(vpc.id)
    ig = ec2.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=ig.id)
    print(ig.id)
    subnet = ec2.create_subnet(VpcId=vpc.id, CidrBlock='10.0.0.0/24', AvailabilityZone='us-east-2b')
    subnet2 = ec2.create_subnet(CidrBlock = '10.0.2.0/24', VpcId= vpc.id, AvailabilityZone='us-east-2a')
    print(subnet2.id)  

    createELB(subnet.id , subnet2.id, ec2)

def createELB(subnet1,subnet2,ec2):
    print("creating ELB Load balancer")
    client = boto3.client('elbv2')
   # aws elbv2 create-load-balancer --name my-load-balancer --subnets subnet-12345678 subnet-23456789 --security-groups sg-1234567

    response = client.create_load_balancer(
        Name='CiscoELB',
        Subnets=[subnet1 , subnet2]
    )  
    createEC2(ec2,subnet1) 
    
def registerEC2withELB(elb,InstanceId):
    client = boto3.client('elbv2')

    response = client.register_instances_with_load_balancer(
    LoadBalancerName='CiscoELB',
    Instances=[
        {
            'InstanceId': InstanceId
        },
    ]
)    
      
def createEC2(ec2,SubnetId):
    print("creating EC2 instance if doesn't exist")
    instances = getInstances(ec2)
    if instances.length > 0:
        print("skip creation")
    else:
        response=ec2.create_instances(ImageId='ami-0a63f96e85105c6d3', MinCount=1, MaxCount=1,InstanceType='t2.micro',SubnetId= SubnetId,)
        print(response[0].id)
        registerEC2withELB(ec2,response[0].id)
    

def getInstances(s2):
    instances = s2.instances
    print('displaying the instances',instances)
    
def main():

    print("provisioning load balancer web server")
    connecttomyaccount()
    
main()
