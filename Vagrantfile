VAGRANTFILE_API_VERSION = "2"
# Help
def help()
puts <<-EOF
vagrant [--install-type=<base|full>] [--debug-tools]

-h, --help:
    show help

-i, --install-type [type]:
    base: Add Only mandatory repositories (default)
    full: Perform Surveil full installation

-d, --debug-tools:
    Install debug tools (usefull for devs)
EOF
end

# Handle options
require 'getoptlong'
opts = GetoptLong.new(
        [ '--install-type', '-i', GetoptLong::OPTIONAL_ARGUMENT ],
        [ '--debug-tools', '-d', GetoptLong::NO_ARGUMENT ],
        [ '--help', '-h', GetoptLong::NO_ARGUMENT ]
)
install_type = 'base'
debug_tools = 0
opts.each do |opt, arg|
    case opt
        when '--install-type'
            install_type = arg
        when '--debug-tools'
            debug_tools = 1
        when '--help'
            help
            exit
        else
            help
            exit
    end
end

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.vm.box = "centos/7"
    config.vm.network "public_network"
    config.vm.synced_folder ".", "/vagrant", disabled: true
  
    # Disabling SELinux
    config.vm.provision :shell, :inline => "echo 0 >  /sys/fs/selinux/enforce"
    config.vm.provision :shell, :inline => "sed 's/SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config"

    # Install repos
    config.vm.provision :shell, :inline => "yum install -y yum-utils vim"
    config.vm.provision :shell, :inline => "yum-config-manager --add-repo http://yum.surveil.savoirfairelinux.net/centos_7/"
    config.vm.provision :shell, :inline => "yum install -y https://rdoproject.org/repos/rdo-release.rpm"

    # Install debug tools
    if debug_tools == 1
        config.vm.provision :shell, :inline => "yum install -y net-tools mongodb python-pip --nogpgcheck"
        config.vm.provision :shell, :inline => "pip install ipdb"
    end

    # Install surveil
    if install_type == 'full'
        config.vm.provision :shell, :inline => "yum install -y surveil-full --nogpgcheck"
        config.vm.provision :shell, :inline => "systemctl start surveil-full.target"
    end

end
