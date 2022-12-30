import boto3
import urllib3
import json
import time
http = urllib3.PoolManager()
start = time.time()
ec2 = boto3.resource('ec2')
a = ec2.instances.all()

def send(id,state):
    url = "https://cloocus.webhook.office.com/webhookb2/7f4b560b-bcd8-4caf-8f72-027e59ce5d9b@355deae4-a1d6-4d5e-be34-0ad0c20aaa0f/IncomingWebhook/bd0511f2b9394418ba953b04a2b992a2/255aa5e3-f570-43f6-b96c-f296572ca249"
    encoded_msg =  json.dumps(
        {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7", 
            "summary": "AWS status check",
            "sections": [{
                "activityTitle": "AWS status check",
                "activitySubtitle": "your instance is die",
                "activityImage": "https://blog.kakaocdn.net/dn/dcg8Y7/btrr9fboqwp/3FCRJk326nkyReQE6O8mJK/img.jpg",
                "facts": [{
                    "name": "instance-id",
                    "value": id,
                }, 
                {
                    "name": "Status",
                    "value": state,
                }],
            }],
        }
        )
    response = http.request('POST', url,headers={'Content-Type': 'application/json'} ,body=encoded_msg)
    

cnt = 0

for instance in ec2.instances.all():
    if instance.state['Name'] != 'running':
        send(instance.id, instance.state['Name'])
        cnt += 1

print("결과 : ", cnt, "개가 비정상 입니다.", "소요 시간:", time.time()-start)

