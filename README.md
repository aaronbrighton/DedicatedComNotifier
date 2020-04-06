Description
===========

Dedicated.com is a "budget" dedicated servers provider with datacenters across North America.  Certain server configurations can be hard to come by and when availability does open up, they are quickly allocated.  This AWS Lambda function notifies the user by SMS when their specific configuration becomes available.

How to use
==========

1. Create a Python 3.8 Lambda function in AWS with permissions to send SMS messages using SNS service.

2. Determine the server configuration you want to monitor.  To do this view the source of the following Instance Deployment Servers configuration page using inspector in web developer tools in your browser: https://dedicated.com/dedicated-servers, and look for the configuration name (pulled from the image tag alt attribute) and the locality name, for example:

```
<img src="assets/images/intel-xeon.png" alt="Intel® Xeon™ E3-1270 | 8GB - 128GB SSD">
<li class="nyc" data-location="NYC">
```

Configuration: Intel® Xeon™ E3-1270 | 8GB - 128GB SSD
Locality: NYC

3. Create a CloudWatch Rule in AWS that run's on a schedule (of your choosing), configured to execute your Lambda function with a JSON string passed to it that includes your desired config, locality, and SMS enabled phone number to be notified at:

```
{
  "config": "Intel® Xeon™ E3-1270 | 8GB - 128GB SSD",
  "local": "NYC",
  "phone": "+15555555555"
}
```
