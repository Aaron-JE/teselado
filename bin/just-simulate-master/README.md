# just-simulate

This project is intended to provide support for logistics simulation, from
customers places orders to their favourite restaurants, to couriers picking
up those orders and deliver them to customers. It provides some abstractions
and basic behaviours of agents and components, and should be easy to extend
and tailor to different use cases. It is still a work in progress, but you
should be able to run a few scenarios with the current version. Head to the
[tutorial](/tutorial/README.md) for a gentle intro to the code.

### Installation

`Pipenv` is the recommended way of installing this project but you could also
use `pip` with `virtualenv` if you prefer.

```
$ brew install pipenv
$ cd /path/to/just-simulate
$ pipenv install
$ pipenv shell
$ pip install -e .
```

