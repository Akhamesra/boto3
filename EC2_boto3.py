import boto3
import logging
from botocore.exceptions import ClientError

logging.basicConfig(filename="ec2_log.log",level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s : %(message)s')
logger = logging.getLogger(__name__)

class ec2:
    def __init__(self):
        self.ec2 = boto3.resource('ec2')

    def create_instance(self,image='ami-0e742cca61fb65051',instance_type='t2.micro',keyname='MyEC2Key',security_group = ['sg-02c096e9f2732cd7e']):
        instance_params = {'ImageId':image,'InstanceType':instance_type,'KeyName':keyname,'SecurityGroupIds':security_group}
        try:
            instance = self.ec2.create_instances(**instance_params,MinCount=1,MaxCount=1)[0]
            print('Creating Instance')
            instance.wait_until_running()
            print('Instance Created\n')
        except ClientError as ce:
            print('Could not create an instance')
            logger.error(f"Could create instance. Error - {ce.response['Error']['Code']} : {ce.response['Error']['Message']}")

    def get_all_instances(self):
        instances = self.ec2.instances.all()
        return instances

    def get_filtered_instances(self,key,value):
        mod_key = 'tag:'+key
        filters =[{'Name':mod_key,'Values':[value]}]
        instances = self.ec2.instances.filter(Filters=filters)
        return instances
    
    def start_all(self,instances):
        for instance in instances:
            if instance.state['Name'] =='running':
                print(f'Instance is already running, ID : {instance.id}')
            else:
                try:
                    instance.start()
                    print('Instance Starting ..')
                    instance.wait_until_running()
                    print('Instanc Started\n')
                except ClientError as ce:
                    print(f'Failed to start an insatnce, ID : {instance.id}')
                    logger.error(f"Could not start the instance {instance.id} Error - {ce.response['Error']['Code']} : {ce.response['Error']['Message']} ")

    def stop_all(self,instances):
        for instance in instances:
            if instance.state['Name']=='running':
                try:
                    instance.stop()
                    print("Stopping ..")
                    instance.wait_until_stopped()
                    print("Instance Stopped\n")
                except ClientError as ce:
                    logger.error(f"Could not stop the instance {instance.id} Error - {ce.response['Error']['Code']} : {ce.response['Error']['Message']} ")
            else:
                logger.info(f'Instance Already Stopped. ID : {instance.id}, Public IP : {instance.public_ip_address},Tags : {instance.tags}')
                print(f"{instance.id} : Instance is already stopped")

    def print_instance_details(self,instances):
        for instance in instances:
            print(f'ID : {instance.id}')
            print(f'Private IP : {instance.private_ip_address}')
            print(f'Public IP : {instance.public_ip_address}')
            print(f'Tags : {instance.tags}')
            print()

if __name__ == '__main__':
    ec2 = ec2()
    ec2.create_instance()
    instances = ec2.get_all_instances()
    ec2.print_instance_details(instances)
    # ec2.start_all(instances)
    # ec2.stop_all(instances)
    

