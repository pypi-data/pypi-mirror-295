# VMTUI

*a text user interface to control libvirt VMs on a per user basis.*

## libvirt polkit configuration

`VMTUI` is intended as a simple interface to allow unprivileged user accounts to control (i.e. (re)start, shutdown, install) their personal virtual machines.
To make use of this, libvirt must be configured to use polkit. The package provides a helper script `gen_libvirt_polkit_acl` that allows the generation of an ACL policy based on a yaml database.

The `libvirtd.conf` file must be modified [src](https://fedoraproject.org/wiki/QA:Testcase_Virt_ACLs)

`/etc/libvirt/libvirtd.conf`:

~~~conf
access_drivers = [ "polkit" ]
~~~

In this example, a user account must belong to the `adm_vmhost` group to get full priviliges.
User accounts with personal VMs must belong to the `user_vm` group.

`/etc/polkit-1/rules.d/100-libvirt-acl.rule`:

~~~javascript
polkit.addRule(function(action, subject) {
    if (subject.isInGroup("adm_vmhost")) {
        // Grant full access to all libvirt actions related to domains
        if (action.id.startsWith("org.libvirt.api.domain")) {
            return polkit.Result.YES;
        }

        // Grant access to manage networks and storage as well
        if (action.id.startsWith("org.libvirt.api.network") ||
            action.id.startsWith("org.libvirt.api.storage")) {
            return polkit.Result.YES;
        }
    }
});

polkit.addRule(function(action, subject) {
    if ( subject.isInGroup("user_vm") ) {
        if (action.id.startsWith("org.libvirt.api.domain") && action.lookup("connect_driver")=="QEMU") {
            var dom = action.lookup("domain_name");
            if( (subject.user == "alice" && dom == "rocky9-2") ||
                (subject.user == "bob" && dom == "rocky9-3") || // these are the "entry types that must be read from a file, either to grant access to a user or a group
                false // makes generation easier
            ) {
                return polkit.Result.YES;
                } else {
                return polkit.Result.NO;
            }
        } else if ( action.id.startsWith("org.libvirt.api.network") ) {
            if ( action.id.endsWith("getattr") ||
                 action.id.endsWith("read") ||
                 action.id.endsWith("create")
                ) {
                return polkit.Result.YES;
            } else {
                return polkit.Result.NO;
            }
        }
    }
}
);
~~~

> The example grants the user `alice` access to the domain `rocky9-2`, while `bob` is allowed to manage `rocky9-3`.

To simplify the generation of the polkit ACL use the `s` script and provide a `user_acl.yaml`:

~~~yaml
libvirt_acl:
  admin_groups: # configure groups that have full access
    - adm_vmhost
  domains: # domain specific ACL
    rocky9: # grant users alice and bob and members of the group mod_vmhost access to 'rocky9''
      users:
        - alice
        - bob
      groups:
        - mod_vmhost
    rocky9-2: # grant alice access to rocky9-2 
      users:
        - alice
    rocky9-3: # grant bob access to rocky9-3
      users:
        - bob
~~~

To generate the ACL (as root):

~~~bash
gen_libvirt_polkit_acl --acl user_acl.yaml 
~~~

It might be necessary to restart libvirt and polkit.

~~~bash
systemctl restart polkit
systemctl restart libvirtd
~~~

## SSH configuration for vmtui

You can limit ssh access to vmtui with the following configuration (limits members of the `user_vm` group to `vmtui`).
It is recommended to use a virtual environment.

`/etc/ssh/sshd_config.d/10-vmtui-conf`

~~~conf
Match Group user_vm
    ForceCommand $path_to_virt_env/bin/python -m vmtui.vmtui -c $config_path
~~~
