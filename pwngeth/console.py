from pwngeth.securefunds import secure_funds_main
from pwngeth.gentargets import gen_targets_main
from configargparse import ArgumentParser, YAMLConfigFileParser



def generate_targets():
    p = ArgumentParser(
        'pwngeth generate targets cli',
        config_file_parser_class=YAMLConfigFileParser
    )

    p.add_argument(
        '-c',
        '--config',
        required=True,
        is_config_file=True,
        help='config file path')

    p.add_argument(
        '--shodan_key',
         required=True,
         help='Shodan API key'
    )
    options = p.parse_args()
    gen_targets_main(options.shodan_key)


def pwn_targets():
    p = ArgumentParser(
        'pwngeth pwn targets cli',
        config_file_parser_class=YAMLConfigFileParser
    )

    p.add_argument(
        '-c',
        '--config',
        required=True,
        is_config_file=True,
        help='config file path')

    p.add_argument(
        '--secure_address',
         required=True,
         help='Secure eth wallet address'
    )
    options = p.parse_args()
    secure_funds_main(options.secure_address)
