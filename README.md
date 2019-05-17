* Create Virtual Environment
        
        virtualenv venv --python=python
        WINDOWS: venv\Scripts\activate.bat
        LINUX: source venv-idea/bin/activate

* Create Sample Serverless Project
        
        serverless create --template aws-python --path analytics_ingest

* Install python dependencies and freeze
        
        pip install ...
        pip freeze > requirements.txt

* Install NPM Serverless Packages

        npm init
        npm install --save serverless-python-requirements
        serverless plugin install --name serverless-step-functions
        serverless plugin install --name serverless-pseudo-parameters

    Add plugins in `serverless.yml`

        plugins:
            - serverless-python-requirements
            - serverless-pseudo-parameters

* Deploy to AWS

        serverless deploy -v --aws-profile asoba --stage dev
        
        serverless deploy -v --aws-profile asoba --stage prod
