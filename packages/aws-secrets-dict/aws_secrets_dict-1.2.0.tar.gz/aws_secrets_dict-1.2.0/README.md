
# AWS Secrets Dict

aws_secrets_dict is a Dictionary-based class acting as a wrapper for the [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/). It allows you to Get, Update, & Delete secrets using the notation/syntax of a python dictionary.

## Example Usage
```
from aws_secrets_dict import AwsSecrets

# Need AWS Key & Secret
my_key = "Your AWS Secrets Access Key, or set 'AWS_SECRETS_KEY' env variable"
my_secret = "Your AWS Secrets Secret Key or set 'AWS_SECRETS_SECRET' env variable"
aws_region = "Your AWS Region or set 'AWS_REGION' env variable. If not set/specified, defaults to us-east-2"

mysecrets = AwsSecrets(my_key, my_secret, aws_region)

mysecrets['One'] = 1
mysecrets[2] = "Two"
mysecrets["2"] = 22222
mysecrets['Greeting'] = "Hello"

mysecrets['One']
# 1
mysecrets[2]
# "Two"
mysecrets["2"]
# 22222
mysecrets['Greeting']
# "Hello"
```

## Notes
The class will use the json module to serialize the keys & values, which allows it to distinguish between types when setting keys & retrieving values. Make sure that your keys/values can all be serialized into json.
