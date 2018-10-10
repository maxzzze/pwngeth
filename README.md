# pwngeth

Sometimes Ethereum nodes are vulnerable to a JSON-RPC exploit - this is a
handful of scripts to secure those funds.

Requirements:
* Shodan API key to generate targets
* Elasticsearch running locally
* Other requirements outlined in `setup.py`


## CLI
```console
(venv) ➜  pwngeth git:(master) ✗ generate-targets-pg -h
usage: generate-targets-pg [-h] -c CONFIG --shodan_key SHODAN_KEY

Args that start with '--' (eg. --shodan_key) can also be set in a config file
(specified via -c). The config file uses YAML syntax and must represent a YAML
'mapping' (for details, see http://learn.getgrav.org/advanced/yaml). If an arg
is specified in more than one place, then commandline values override config
file values which override defaults.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config file path
  --shodan_key SHODAN_KEY
                        Shodan API key
```


Article outlining the exploit: https://thehackernews.com/2018/06/ethereum-geth-hacking.html

*DISCLAIMER*
> I am not responsible for any funds which are secured using these
> scripts. They are meant as educational purposes only.
