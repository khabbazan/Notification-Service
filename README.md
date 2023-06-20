# Notification Subscriber


### Description


This project aims to send notifications using the [Kavenegar](https://kavenegar.com/) service for SMS and Google/[Chabok](https://chabok.io/) for web push notifications. The project has four methods for sending notifications:


1. Single SMS: This method sends a single SMS notification to a specified phone number using the Kavenegar service.

2. Group SMS: This method sends an SMS notification to a group of phone numbers using the Kavenegar service.

3. OTP SMS: This method sends a one-time password (OTP) to a specified phone number using the Kavenegar service.

4. Group OTP SMS: This method sends an OTP to a group of phone numbers using the Kavenegar service.

5. Single Web Push: This method sends a single web push notification to a specified device using either the Google or Chabok service.

6. Group Web Push: This method sends a web push notification to a group of devices using either the Google or Chabok service.



### Gateways


| Send | Exchange | Routing key |
| -------  | ------- |  ------- |
| sms single  | sms | send.single.* |
| sms group  | sms | send.group.* |
| otp single  | sms | send.single.otp.* |
| otp group | sms | send.group.otp.* |
| get vapid public key  | webpush | get.public.vapid.* |
| single google webpush  | webpush | send.google.* |
| single chabok webpush  | webpush | send.single.chabok.* |
| group chabok webpush | webpush | send.group.chabok.* |



### Execute


1. Open a terminal and navigate to the root directory of your Python project.


2. Navigate to the "openssl" directory using the following command:
    ```sh
        cd openssl
    ```
3. Generate a private key using the following command:
    ```sh
        openssl ecparam -name prime256v1 -genkey -noout -out vapid_private.pem
    ```
    This command generates a private key file named vapid_private.pem using the prime256v1 elliptic curve algorithm.

4. Convert the private key to a 32-byte key and write it to the private.key file using the following command:
    ```sh
        openssl ec -in ./vapid_private.pem -outform DER | tail -c +8 | head -c 32 | base64 | tr -d '=' | tr '/+' '_-' >> private.key
    ```
    This command reads the vapid_private.pem file, extracts a 32-byte key from it, encodes the key in base64 format, and writes it to the private.key file. The tail and head commands are used to extract the key bytes and the tr command is used to replace the base64 characters that are not compatible with URLs.

5. Generate a public key from the private key and write it to the public.key file using the following command:
    ```sh
        openssl ec -in ./vapid_private.pem -pubout -outform DER | tail -c 65 | base64 | tr -d '=' | tr '/+' '_-' >> public.key
    ```
    This command reads the vapid_private.pem file, generates a public key from it, encodes the public key in base64 format, and writes it to the public.key file. The tail command is used to extract the base64-encoded public key bytes and the tr command is used to replace the base64 characters that are not compatible with URLs.

6. Make sure that the openssl directory is located in the root directory of your project before running these commands. Once you have created the public.key and private.key files, you can execute this project in the root directory of your project with this command:
    ```sh
        python .
    ```





### Directory structure


```bash
.
├── dist
├── examiner
├── openssl
├── setup
└── src
    ├── core
    ├── gateways
    ├── helpers
    └── resources


```

- dist : The dist directory contains the Dockerfile which is used to build a Docker image of the project.
- examiner : This directory contains scripts and templates for testing the message publishing functionality of the project.
- openssl : The openssl directory contains the necessary files and scripts for generating SSL certificates like public key and private key for webpush .
- setup : The setup directory typically contains configuration files and scripts for setting up the development environment, packaging the code, and releasing the project.
- src : The src directory contains the source code for the microservice, organized into subdirectories based on functionality. The subdirectories include:
    - core : including settings and configuration for RabbitMQ.
    - gateways : contains code for interacting with external systems, such as exchanges and routing keys.
    - helpers : contains utility code for use throughout the application.
    - resources : contains the core functionality of the project, such as validating and sending notifications.
