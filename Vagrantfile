VAGRANTFILE_API_VERSION = "2"

# Handle options
require 'getoptlong'
opts = GetoptLong.new(
        [ '--install-type', GetoptLong::OPTIONAL_ARGUMENT ]
)
install_type = 'base'
opts.each do |opt, arg|
 case opt
   when '--install-type'
    install_type = arg
 end
end

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "centos/7"
  config.vm.network "public_network"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  
  # Disabling SELinux
  config.vm.provision :shell, :inline => "echo 0 >  /sys/fs/selinux/enforce"

  # Install repos
  config.vm.provision :shell, :inline => "yum install -y yum-utils vim"
  config.vm.provision :shell, :inline => "yum-config-manager --add-repo http://yum.surveil.savoirfairelinux.net/centos_7/"
  config.vm.provision :shell, :inline => "yum install -y https://rdoproject.org/repos/rdo-release.rpm"

  # Install debug tools
  config.vm.provision :shell, :inline => "yum install -y net-tools mongodb python-pip --nogpgcheck"
  config.vm.provision :shell, :inline => "pip install ipdb"

  # Install surveil
  if install_type == 'full'
    config.vm.provision :shell, :inline => "yum install -y surveil-full --nogpgcheck"
    config.vm.provision :shell, :inline => "systemctl start surveil-full.target"
  end

end
