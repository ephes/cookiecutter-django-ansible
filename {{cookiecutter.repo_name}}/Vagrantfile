# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Define multiple machines

  # define production box
  config.vm.define "production" do |production|
    production.vm.box = "ubuntu/trusty64"

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    #config.vm.network "forwarded_port", guest: 443, host: 4430
    # Usually ports 8080 and 8081 will be used, adapt this by setting environment
    # variables PORT_1 and PORT_2
    if ENV['PORT_1']
    	$port_1=ENV['PORT_1']
    else
    	$port_1='8080'
    end
    if ENV['PORT_2']
      $port_2=ENV['PORT_2']
    else
      $port_2='8081'
    end

    # 80 -> 8080 and 443 -> 8081 for production
    production.vm.network "forwarded_port", guest: 80, host: $port_1
    production.vm.network "forwarded_port", guest: 443, host: $port_2
    production.vm.network "forwarded_port", guest: 22, host: 2222, id: 'ssh'

    # Provider-specific configuration so you can fine-tune various
    # backing providers for Vagrant. These expose provider-specific options.
    # Example for VirtualBox:
    #
    production.vm.provider "virtualbox" do |vb|
    #   # Don't boot with headless mode
    #   vb.gui = true
    #
    #   # Use VBoxManage to customize the VM. For example to change memory:
      vb.customize ["modifyvm", :id, "--memory", "1024"]
      vb.cpus = 2
    end

    # provisioning for production
    production.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/site.yml"
      ansible.vault_password_file = "ansible/.vault_pass.txt"
      ansible.inventory_path = "ansible/inventory"
      ansible.limit = "vagrantbox_prod"
      # ansible.verbose = "vvvv"
    end
  end

  # define develop box
  config.vm.define "develop" do |develop|
    develop.vm.box = "ubuntu/trusty64"

    develop.vm.provider "virtualbox" do |vb|
    #   # Don't boot with headless mode
    #   vb.gui = true
    #
    #   # Use VBoxManage to customize the VM. For example to change memory:
      vb.customize ["modifyvm", :id, "--memory", "1024"]
      vb.cpus = 1
    end

    # 8000 -> 8000 for develop
    develop.vm.network "forwarded_port", guest: 8000, host: 8000
    develop.vm.network "forwarded_port", guest: 22, host: 2223, id: 'ssh'

    # provisioning for develop
    develop.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/vagrant_develop.yml"
      ansible.vault_password_file = "ansible/.vault_pass.txt"
      ansible.inventory_path = "ansible/inventory"
      ansible.limit = "vagrantbox_dev"
      # ansible.verbose = "vvvv"
    end
  end

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu/trusty64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false
  config.vm.boot_timeout = 600

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # The preferred network interface is eth0, but you can override this by 
  # setting the environment variable PREFERRED_NETWORK_INTERFACE
  if ENV['PREFERRED_NETWORK_INTERFACE']
  	$preferred_network_interface=ENV['PREFERRED_NETWORK_INTERFACE']
  else
  	$preferred_network_interface='eth0'
  end
  config.vm.network "public_network", bridge: $preferred_network_interface

  # remove known host entries after destroy
  config.trigger.after :destroy do
    puts "Removing known host entries"
    `sed -i'foo' '/^.127.0.0.1/d' ~/.ssh/known_hosts`
  end
end
