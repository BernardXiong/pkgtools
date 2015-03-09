Package Manager
===============


Commands
--------

::
    
    pkg search <pattern>        # Search for packages by glob pattern
    pkg update                  # Update package database
    pkg install <package>       # Install package
    pkg install -r <package>    # Install package and all dependencies
    pkg upgrade <package>       # Upgrade package
    pkg upgrade -r <package>    # Upgrade package and all dependencies
    pkg upgrade -n -r <package> # Upgrade package and all dependencies. Also installs new
                                  dependencies as needed.
    pkg uninstall <package>     # Uninstall package
    pkg uninstall -r <package>  # Uninstall package and all dependencies
    pkg lock <package>          # Prevent package from being upgraded
    pkg unlock <package>        # Unlock package

    # Nice to have
    pkg rollback                # Rollback to previous state of installed packages
    pkg commit                  # Commit current state of installed packages
