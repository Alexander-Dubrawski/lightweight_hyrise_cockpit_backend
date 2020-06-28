# Synthetic Cockpit

## Setup

You may need to install a different python version (`3.8.2`, e.g. using [`pyenv`](https://github.com/pyenv/pyenv#installation)).
Installing pyenv can be done with the following commands:

<details>
<summary>macOS</summary>

```bash
brew install pyenv
```

</details>

<details>
<summary>Ubuntu</summary>

```bash
# Update package list
sudo apt-get update

# Dependencies commonly missing, causing issues with pyenv
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

# Pyenv install script
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

Put the following in your `.bashrc` (or `.zshrc`, etc.):

```bash
export PATH="/home/$USER/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Restart your shell:

```bash
exec "$SHELL"
```

</details>

Subsequently, the required version of Python can be installed and set with:

```bash
# Install Python 3.8.2
pyenv install 3.8.2

# Set the local (directory) Python version to 3.8.2
cd Cockpit
pyenv local 3.8.2
```

Now, initialize and sync your virtual environment:

```bash
python -m pip install pipenv
exec "$SHELL"
pipenv --three --python=`which python`
pipenv sync
```

## Usage 

You can start the components as follow: 

* flask app: `pipenv run python -m backend.app.cli`
* database manager: `pipenv run python -m backend.database_manager.cli`
* workload generator: `pipenv run python -m backend.workload_generator.cli`

To run the benchmarks you need to have the following components installed:

* WRK https://github.com/wg/wrk
* ps 

You can run the benchmarks for example as follow 
`pipenv run python -m benchmark.wsgi_benchmark`

