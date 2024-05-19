# bitsky

Bitbucket to Skype webhook

## Configure credentials

Create an account for Skype and create `src/config.ini`

Create a Skype group 

Find `ConversationId` on web.skype.com using Network Tools on your browser.

```
[config]
email = user@email.com
password = supersecretpassword
group = 12:34567890abcdefghijklmnopqrstuvwx@thread.skype
```

You can also add multiple accounts. For example on using Uptime Kuma 

```
uptime_email = uptime-kuma@email.com
uptime_password = supersecretpassword
uptime_group = 19:2345ab6cd6789e0f1g23h4h5i6j7890c@thread.skype
```

## Development

Simulate webhook trigger from Bitbucket

```
$ git clone https://github.com/kleo/bitsky

$ cd bitsky

$ python -m venv --copies venv

$ source venv/bin/activate

$ pip install -r requirements.txt

$ python src/bitsky.py

$ curl http://localhost:5000/build -H 'Content-Type:application/json' -d @requests/build/build-inprogress.json
```

## Port forward 

Using ngrok for bitbucket webhook testing

```
$ ngrok http 5000

$ curl https://123a-45-678-901-234.ngrok-free.app/build -H 'Content-Type:application/json' -d @requests/build/build-successful.json
```

Copy ngrok url to Bitbucket Repository > Webhooks > Edit webhook

## Build Docker image

docker build and push

```
$ docker build -t registry.example.com/bitsky:latest .

$ docker push registry.example.com/bitsky:latest
```

## Run using Docker

```
$ docker pull registry.example.com/bitsky:latest

$ docker run --restart=always -p 127.0.0.1:8000:80 registry.example.com/bitsky:latest
```

## Reverse proxy configuration

Using Caddy

```
webhook.example.com {

    reverse_proxy /push 127.0.0.1:8000
	reverse_proxy /build 127.0.0.1:8000
	reverse_proxy /pr 127.0.0.1:8000
	reverse_proxy /health 127.0.0.1:8000

	# reverse_proxy /uptime 127.0.0.1:8000

	log {
		output file /var/log/webhook.example.com.log {
			roll_size 10mb
			roll_keep 20
			roll_keep_for 720h
		}
	}
}
```

## Acknowledgements

[Terrance](https://github.com/Terrance) author of [SkPy](https://github.com/Terrance/SkPy)

## TODO

- Support Bitbucket webhook secret
- Support other triggers
