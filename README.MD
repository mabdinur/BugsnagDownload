Things to keep in mind:

1. Change the filters in the 'post_request_events_download' field to match your desired error case. Full documentation on the different types of filters and 
parameters that can be used can be found here: https://bugsnagapiv2.docs.apiary.io/#introduction/filtering/event-fields

2. The authorization key is valid until December 20, 2019. To generate a new admin bugsnag key, request admin permissions on bugsnag from DevOps and then 
generate a new auth key on your account settings page. Use this link: https://app.bugsnag.com/settings/wonolo/my-account/auth-tokens

3. Organization name is linked to the Wonolo bugsnag account, this id should never be changed. This id can be retreived using a valid bugsnag auth-token 
(mentioned above) and the following command:

 curl --get 'https://api.bugsnag.com/user/organizations' \
        --header 'Authorization: token 0000gh00-00be-0000-b0000-f0b0b000deb0' \
        --header 'X-Version: 2' 

4. Events can be queried using the event api however the results are paginated with a maximum of 100 events per request with a limit of 10 requests per minute. Using this api is not reccomened for querying large number of events. Instead of using the limited event api this script uses the event data request api to request a bulk download of all events which match a specific search critiera found in config["post_request_events_download"]. This request often takes 10-15 minutes to download larger datasets. Documentation on this api can be found here: https://bugsnagapiv2.docs.apiary.io/#reference/organizations/event-data-requests/create-an-event-data-request




