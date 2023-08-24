# stackson
distributing work tasks to nodes

This is just a play thing, i want to distribute work tasks to headless devices
So Im starting with a simple agent that gathers data about a host, and it can take on simple commands and even short python scripts.

It has a deploy function so if you point it at another host is will SSH to it and replicate another python script there which is intended to install the agent
Ive only spent a couple of hours on it today so i will work to make it better as i find time. Encryption is high on the list of items to look at. 

The configureable item atm is really just the broker. You have to send payloads to it using what ever mqtt client you have atm 
type options are "deploy", "command" and "python" - the result of the command is sent back to mqtt as text, you can subscribe to that topic and see the responses

{
  "type": "deploy",
  "data": {
    "code": "print('Hello, world!')", # only used if your sending a python script
    "host": "192.168.0.40",
    "username" : "sent in clear text",
    "password" : "sent in clear text",
    "commands" : [  ] # only used if your sending a command

  }
}
