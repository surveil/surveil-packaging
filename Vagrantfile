VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "centos/7"
  config.vm.network "public_network"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  
   # Install Surveil
  config.vm.provision :shell, :inline => "yum install -y yum-utils vim"
  config.vm.provision :shell, :inline => "yum-config-manager --add-repo http://yum.surveil.savoirfairelinux.net/centos_7/"
  config.vm.provision :shell, :inline => "yum install -y https://rdoproject.org/repos/rdo-release.rpm"

end
