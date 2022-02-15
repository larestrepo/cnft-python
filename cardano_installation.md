1. Cardano Node

Installation

You can build your cardano node manually or with any of the tools available. Just keep in mind that the files location could change depending of the option you choose. In our case, we are using cntools to build the cardano node ([Cntools]https://cardano-community.github.io/guild-operators/) and so all the paths are relative to cntools files structure.

    mkdir "$HOME/tmp";cd "$HOME/tmp"
    curl -sS -o prereqs.sh https://raw.githubusercontent.com/cardano-community/guild-operators/master/scripts/cnode-helper-scripts/prereqs.sh
    chmod 755 prereqs.sh

    ./prereqs.sh
    . "${HOME}/.bashrc"

    cd ~/git
    git clone https://github.com/input-output-hk/cardano-node
    cd cardano-node
    git fetch --tags --all
    git pull

    git checkout $(curl -s https://api.github.com/repos/input-output-hk/cardano-node/releases/latest | jq -r .tag_name)
    $CNODE_HOME/scripts/cabal-build-all.sh

    cardano-cli version
    cardano-node version

Start the node

    cd $CNODE_HOME/scripts
    ./cnode.sh

    Deploy as a systemd

    cd $CNODE_HOME/scripts
    ./cnode.sh -d
    sudo systemctl start cnode.service

    cd $CNODE_HOME/scripts
    ./gLiveView.sh

2. Cardano wallet

Installation

    cd ~/git
    git clone https://github.com/input-output-hk/cardano-wallet
    cd cardano-wallet

    git fetch --tags --all
    git pull
    git checkout $(curl -s https://api.github.com/repos/input-output-hk/cardano-wallet/releases/latest | jq -r .tag_name)
    
 Install stack
 
    curl -sSL https://get.haskellstack.org/ | sh
    
(Optional) At the end, there is one message to add to PATH

    echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
    stack build --test --no-run-tests --copy-bins --local-bin-path ~/.cabal/bin  2>&1 | tee /tmp/build.log

Start cardano wallet

    cardano-wallet serve \
    --port 8090 \
    --testnet $CNODE_HOME/files/byron-genesis.json \
    --database $CNODE_HOME/priv/wallet/db \
    --node-socket $CARDANO_NODE_SOCKET_PATH

Testing the wallet

    cardano-wallet network information
