# slack-events-handler

## What is it?
A serverless app that receives notifications from Slack's Events API. It figures out what image file was added on the
Slack channel and imports it to an SFTP server or S3 Bucket.

## !! Important !!
* This code should work for both Google Cloud Functions (GCF) and Amazon Web Services (AWS) Lambda.
* The GCF implementation requires the dependency `functions-framework` but it isn't necessary with AWS Lambda.
* Unfortunately at this time there is no universal Slack app to go with this code.
You will have to create your own Slack app ([instructions below](#slack-app-setup)).
* The activating module with the `callback` function is `main.py`. GCF requires this.

## Setup 
1. Create a new JSON file called `app-credentials.json` based off of `app-credentials-layout.json`, 
changing `null` to the actual values, where necessary[^1].
    * `slack_app_id` - The APP ID of the Slack app (required to confirm that the event notification is from an expected app)
    * `slack_bot_token` - The bot token of the app (required to make requests back to Slack)
    * `sftp_host` - Host of the SFTP server
    * `sftp_username` - SFTP Username
    * `sftp_password` - SFTP Password
    * `sftp_port` - SFTP Port (defaults to 22)
2. Specify where you want to save the image files by modifying the `SOURCE_CONNECTION` in the 
`config.py` file. Use `s3` or `sftp`. (Currently there are only two options available.)
3. Zip the `slack-events-plugin` directory and upload it to Google Cloud Functions or AWS Lambda (directions
are online).
4. Create the source directory where you want to download the image files (`S3` or `SFTP`).

[^1] Right now the S3 Bucket works in AWS Lambda through being in the same VPC

(last modified 2024.11.13)

### Slack App setup
1. Create a New Slack App
2. Go to Slack Apps and click on “CREATE NEW APP”
3. Click on “From Scratch”
4. Add a unique app name
5. Set the workspace where you want to create the app
6. Click “Create App”
7. Configure the New Slack App
8. On the left menu, click on Features → Oauth & Permissions
9. In the Scopes section and under Bot Token Scopes add these permissions:
   * channels:history
   * channels:read
   * files:read
   * groups:history
   * groups:read
   * mpim:read
10. On the left menu, click on Features → Event Subscriptions
11. Enable Events
12. Add url of the Google Cloud Service or AWS Lambda to the Request URL & verify the url
13. Click on the carrot next to Subscribe to Bot Events
14. Click on “Add Bot User Event”
15. Add “file_shared” event
16. Save Changes
17. On the left menu, click on Settings → Install App
18. Click to install the app in your workspace
19. Allow Permission for the App to install
20. Register Slack App Data to the “Slack Event-Handler” Service
21. Collect Slack App Data and add it to the `app-credentials.json` file 

(last modified 2024.9.9)

### Add Bot to Corresponding Channels in the Workspace
1. Get confirmation that the credential information has been added to the “Slack Event-Handler” service
2. Go to the channel that you want to add the App Bot to
3. Click on the “Run Shortcut” button 
4. Click on “Add apps to this channel”
5. Click on the name of your app
6. Repeat steps “2-5” for each additional channel

(last modified 2024.9.9)
