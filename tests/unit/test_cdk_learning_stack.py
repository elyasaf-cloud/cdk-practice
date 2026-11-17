# import aws_cdk as cdk

# from aws_cdk.assertions import Template

# from cdk_learning.bucket_stack import CdkLearningStack


# def test_s3_bucket_created():

#     app = cdk.App()

#     stack = CdkLearningStack(
#         app,
#         "TestStack"
#     )

#     template = Template.from_stack(stack)

#     template.resource_count_is(
#         "AWS::S3::Bucket",
#         1
#     )

# def test_s3_bucket_properties():

#     app = cdk.App()

#     stack = CdkLearningStack(
#         app,
#         "TestStack"
#     )

#     template = Template.from_stack(stack)

#     template.has_resource_properties(
#         "AWS::S3::Bucket",
#         {
#             "VersioningConfiguration": {
#                 "Status": "Enabled"
#             },
#             "PublicAccessBlockConfiguration": {
#                 "BlockPublicAcls": True,
#                 "BlockPublicPolicy": True,
#                 "IgnorePublicAcls": True,
#                 "RestrictPublicBuckets": True
#             }
#         }
#     )