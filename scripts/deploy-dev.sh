pip freeze > requirements.txt
sed -e "s/boto3==1.9.120//g" -i.backup requirements.txt
serverless deploy -v --aws-profile asoba --stage dev
