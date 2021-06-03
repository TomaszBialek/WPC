#!/bin/bash

export AWS_DEFAULT_REGION=eu-central-1

BUCKET_NAME=tbialek.bucket0
FUNCTION_NAME=215903__create-animation

## build
rm lambda.zip || true


zip -r lambda.zip ./* \
    --exclude 'lambda.zip' \
    --exclude 'deploy.sh'

## release
aws s3 cp ./lambda.zip s3://${BUCKET_NAME}/code/${FUNCTION_NAME}/lambda.zip

## update code
aws lambda update-function-code --function-name ${FUNCTION_NAME} --s3-bucket ${BUCKET_NAME} --s3-key code/${FUNCTION_NAME}/lambda.zip --publish