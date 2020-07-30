
#Output provisions a load balanced wed server
#Connect to myaccount
#create a ELB load balancer, if exists dont create 
# Create a EC2 instance , if exists dont create
#get instance for displaying the instance id
# deploy ngnix into the infrasturcture 
#it should open a static home page which says static CISCO SPL
#createsubnet , created a single VPC in that created two subnets with different availability zones , attach internetgatewayid
#create a ELB 
#access keyid : AKIAIIXMGYV6OMXR74HQ
#Secret Access Key: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
# configure aws : >>aws configure (give access key , secret key , region , output type)
#pip install boto3
#import boto3
#creating a connection (ec2 = boto3.resource('ec2'))
#launching new instance : ec2.create_instances(ImageId='<ami-image-id>', MinCount=1, MaxCount=1)
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migrationec2.html#launching-new-instances
#ami id : ami-0a63f96e85105c6d3
#


import boto3

def connecttomyaccount():
    print("connecting to my account")
    ec2 = boto3.resource('ec2')
    #it to use ny connection for creating an instance

    #print(s1)
    
    createsubnet(ec2)
    

def createsubnet(s3):


    vpc = s3.create_vpc(CidrBlock='10.0.0.0/16')
    vpc.create_tags(Tags=[{"Key":"TestVPC2","Value":"default_vpc2"}])
    vpc.wait_until_available()
    print(vpc.id)
    ig = s3.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=ig.id)
    print(ig.id)
    subnet = s3.create_subnet(VpcId=vpc.id, CidrBlock='10.0.0.0/24', AvailabilityZone='us-east-2b')
    subnet2 = s3.create_subnet(CidrBlock = '10.0.2.0/24', VpcId= vpc.id, AvailabilityZone='us-east-2a')
    print(subnet2.id)  
    

    createELB(subnet.id , subnet2.id, s3)

def createELB(s4,s5,ec2):
    print("creating ELB Load balancer")
    client = boto3.client('elbv2')
   # aws elbv2 create-load-balancer --name my-load-balancer --subnets subnet-12345678 subnet-23456789 --security-groups sg-1234567

    response = client.create_load_balancer(
        Name='CiscoELB',
        Subnets=[s4 , s5]
    )  
    createEC2(ec2,s5) 
    
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
      
def createEC2(s1,SubnetId):
    print("creating EC2 instance")
    response=s1.create_instances(ImageId='ami-0a63f96e85105c6d3', MinCount=1, MaxCount=1,InstanceType='t2.micro',SubnetId= SubnetId,)
    print(response[0].id)
    #getInstances(s1)
    registerEC2withELB(s1,response[0].id)

    
    

def getInstances(s2):
    instances = s2.instances
    print('displaying the instances',instances)
    

def deployngnix():
    print("deploying ngnix")

def homepage():

    return "CISCO SPL"

def main():

    print("provisioning load balancer web server")
    connecttomyaccount()
    #createELB()
    #createEC2()
    #createsubnet()
    deployngnix()
    homepage()

main()

