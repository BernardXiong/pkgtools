Package Manager
===============


Commands
--------

Package Manager::
    
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

    # Rollback/Commit
    pkg rollback                # Rollback to previous state of installed packages
    pkg commit                  # Commit current state of installed packages

Repository Manager::
    
    pkgrepo init                # Initialize Package Repository
    pkgrepo update              # Update Package Repository

Package Builder::
    
    pkgmk build [<package>]     # Build package from source
    pkgmk build [<collection>]  # Build all packages in collection from source
    pkgmk edit <pacakge>        # Edit package's Pkgfile for editing
    pkgmk clean [<package>]     # Remove build artifacts and cleanup

Ports Management::
    
    ports add <url> [<name>]    # Add new ports collection from uri
    ports update [<name>]       # Update a collection of ports
    ports delete <name>         # Delete a ports collection
    ports search <pattern>      # Search ports collections for pattern
    ports list                  # List ports collections and ports
