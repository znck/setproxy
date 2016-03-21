# SetProxy

Painless proxy configuration.

![SetProxy](cover.png)

<p align="center">
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square" alt="Software License" />
  </a>
  <a href="https://github.com/znck/setproxy/releases">
    <img src="https://img.shields.io/github/release/setproxy/plug.svg?style=flat-square" alt="Latest Version" />
  </a>

  <a href="https://github.com/znck/setproxy/issues">
    <img src="https://img.shields.io/github/issues/znck/setproxy.svg?style=flat-square" alt="Issues" />
  </a>
</p>

## Installation

Run this in your terminal to get the latest SetProxy version:
```bash
# Using curl.
curl -sS https://raw.githubusercontent.com/znck/setproxy/v0.0.1/install.sh | sudo -E bash
# Using wget.
wget -O - -o /dev/null https://raw.githubusercontent.com/znck/setproxy/v0.0.1/install.sh | sudo -E bash
```

## Usage

SetProxy command line interface.

```
$ setproxy -h
usage: setproxy [-h] [-u USER] [-p PASSWORD] [--http] [--https] [--ftp]
                [--socks] [--no-http] [--no-https] [--no-ftp] [--no-socks]
                [--clear] [-t] [-d]
                server [port]

Easy proxy configuration

positional arguments:
  server                Proxy server address. ex: 202.141.80.19 or
                        tamdil.iitg.ernet.in
  port                  Proxy port. commonly used ports are 3128, 8080 and
                        1080.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Username for proxy authentication.
  -p PASSWORD, --password PASSWORD
                        Password for proxy authentication.
  --http                Enable http proxy setting (Default: Enabled)
  --https               Enable https proxy setting (Default: Enabled)
  --ftp                 Enable ftp proxy setting
  --socks               Enable socks proxy setting
  --no-http             Disable http proxy setting
  --no-https            Disable https proxy setting
  --no-ftp              Disable ftp proxy setting (Default: Disabled)
  --no-socks            Disable socks proxy setting (Default: Disabled)
  --clear               Delete old proxy settings, while creating new.
  -t, --test            Display old proxy settings
  -d, --delete          Delete old proxy settings
```
> TODO: Update usage docs.

## Change log

Please see [CHANGELOG](CHANGELOG.md) for more information what has changed recently.

## Testing

> Accepting PR :p

## Contributing

Please see [CONTRIBUTING](CONTRIBUTING.md) and [CONDUCT](CONDUCT.md) for details.

## Security

If you discover any security related issues, please email :author_email instead of using the issue tracker.

## Credits

- [Rahul Kadyan][link-author]
- [All Contributors][link-contributors]

## License

The MIT License (MIT). Please see [License File](LICENSE) for more information.

[link-author]: http://znck.me
[link-contributors]: ../../contributors
