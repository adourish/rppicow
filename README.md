# Raspberry Pico W
## Display tasks on E-Paper

## issues
### MQTT
I have abandoned trying to get the Google APIs to work in my micro controller app. 1) The only way to get a short lived token is to use the gcloud console 2) they provide a service account thing, but it doesnt have permission to talk to my google tasks 3) if i want to get access to the google tasks api using the gcloud console (scopes) I have to submit a youtube video showing what my project is all about and why i need it 4) they have nothing like a PAT where I can simply generate a PAT and then get access to my google data. I also know a lot more about Google tasks API than I ever wanted to know. for that reason I am now using Todoist app for my tasks. it seems to integrate with Google calendar just as well as Google tasks api