# pwngeth

Sometimes Ethereum nodes are vulnerable to a JSON-RPC exploit - this is a
handful of scripts to secure those funds.

Requirements:
* Shodan API key to generate targets
* Elasticsearch running locally
* Other requirements outlined in `setup.py`


## CLI

Generating targets works by querying shodan for `geth`, checking nodes which
are misconfigured by performing admin level tasks, and then checking if they
are located on the main Ethereum network (running a v1 ethereum node). Nodes
which are valid targets will be index into elasticsearch in an index named:
`hackgeth_main`. All other nodes which are misconfigured but not running v1
software will be indexed into `hackgeth_shodan_main`.

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

Pwning works by first querying the `hackgeth_shodan_main` index for valid
targets. Once found, it will spin up a process which will try to secure the
funds for 300 seconds. Fund securing will only work if the secure funds web3
request is made while the wallet is unlocked by a user with the wallet key.
The goal of the process is to basically make so many requests that we wait until
the wallet is unlocked.

```console
(venv) ➜  pwngeth git:(master) ✗ pwn-targets-pg -h
usage: pwn-targets-pg [-h] -c CONFIG --secure_address SECURE_ADDRESS

Args that start with '--' (eg. --secure_address) can also be set in a config
file (specified via -c). The config file uses YAML syntax and must represent a
YAML 'mapping' (for details, see http://learn.getgrav.org/advanced/yaml). If
an arg is specified in more than one place, then commandline values override
config file values which override defaults.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config file path
  --secure_address SECURE_ADDRESS
                        Secure eth wallet address
```

Article outlining the exploit: https://thehackernews.com/2018/06/ethereum-geth-hacking.html

### TODO
* Make the pwn timeout configurable

*DISCLAIMER*
> I am not responsible for any funds which are secured using these
> scripts. They are meant as educational purposes only.
