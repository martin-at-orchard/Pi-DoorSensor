# Pi-DoorSensor

The Raspberry Pi Door Sensor is used at the residence to alert staff to a door opening or closing by both visual and audio alerts.

The following is needed:
* Raspberry Pi (4 GByte 4B recommended)
* USB 3 SSD (could use a micro SD card)
* HDMI monitor
* Speakers connected to the 3.5mm audio jack
* Keyboard (only for initial setup)

## Pi Setup

These setup instructions allow you to take a brand new Raspbery Pi and get the application working.

Additional wiring will be required to connect the magnetic door switches to the GPIO pins.
The appliction uses internal pull-up resistors to pull the GPIO pins high
which is connected to one side of the magnetic door switch. The other side of the switch is connected to ground.

### Install the operating system

* Download Rapsberry Pi OS (32-bit) Lite from [the Raspberry Pi Website](https://www.raspberrypi.org/downloads/raspberry-pi-os/)
* Install it on the SSD using [belenaEtcher](https://www.balena.io/etcher/) or some other software
* Connect the Raspberry Pi to:
  * HDMI Monitor (need mini HDMI to HDMI cable)
  * Powered Speakers to the 3.5mm audio jack
  * SSD connected to powered SATA to USB 3 connector
  * USB Keyboard
  * Ethernet connection
  * USB 3 Power Supply (minimum 2.5A)
* Boot the Raspberry Pi
  * **NOTE:** If using older firmware or an older Raspberry Pi OS you might need to configure the Raspberry Pi to be able to boot from SSD or use a micro SD card
  
### Configure the Operating System

* Login to the Raspberry Pi once it has finished booting
  * User: pi
  * Password: raspberry
* Start up the Raspberry Pi configuration program
  ```script
  sudo raspi-config
  ```
  * Cursor down to `1 Change User Password`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** At the `You will now be asked to enter a new password for the pi user` press `Enter`
    ** Enter the new password and confirmation of the password
    ** At the `Password changed successfully` press `Enter`
    
  * Cursor down to `2 Network Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `N1 Hostname`, press `Tab` to highlight `<Select>` then press `Enter`
    ** At the hostname instructions, press `Enter`
    ** At the `Please enter a hostname` enter an appropriate hostname `doorsensorpi` for example, press `Tab` to highlight `<Ok>` then press `Enter`
  
  * **Note:** Optionally set up the Wireless LAN. Cursor down to `2 Network Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `N2 Wireless LAN`, press `Tab` to highlight `<Select>` then press `Enter`
    ** Cursor down to select the country in which the Pi is to be used (`CA Canada`), press `Tab` to highlight `<Ok>` then press `Enter`
    ** At the WiLAN country confirmation press `Enter`
    ** Enter the SSID, press `Tab` to highlight `<Ok>` then press `Enter`
    ** Enter the passphrase, press `Tab` to highlight `<Ok>` then press `Enter`
    
  * Cursor down to `5 Interfacing Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `P2 SSH`, press `Tab` to highlight `<Select>` then press `Enter`
    ** At the `Would you like the SSH server to be enabled?`, press `Tab` to highlight `<Yes>` then press `Enter`
    ** At the `The SSH server is enabled` press `Enter`

  * Cursor down to `7 Advanced Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `A4 Audio`, press `Tab` to highlight `<Select>` then press `Enter`
    ** Cursor down to `1 Headphones`, press `Tab` to highlight `<Ok>` then press `Enter`
    
  * **Note** Optionally change the locale from British English. Cursor down to `4 Localization Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `I1 Change Locale`, press `Tab` to highlight `<Select>` then press `Enter`
    ** Cursor or page down to find `en_CA.UTF-8 UTF-8` (or other locale), then press the `space bar` to enable
    ** Cursor down to find `en_GB.UTF-8 UTF-8`, then press the `space bar` to disable
    ** Press `Tab` to highlight `<Ok>` then press `Enter`
    ** Cursor down to `en_CA.UTF-8`, press `Tab` to highlight `<Ok>` then press `Enter`
    ** **NOTE:** The border of the configuration program might look odd, ignore it
    
  * **Note** Optionally change the timezone from GMT. Cursor down to `4 Localization Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `I2 Change Time Zone`, press `Tab` to highlight `<Select>` then press `Enter`
    ** Cursor down to `America` (or other location), press `Tab` to highlight `<Ok>` then press `Enter`
    ** Cursor or page down to `Vancouver` (or other timezone), press `Tab` to highlight `<Ok>` then press `Enter`
 
  * **Note** Optionally change the keyboard from English. Cursor down to `4 Localization Options`, press `Tab` to highlight `<Select>` then press `Enter`
  
    ** Cursor down to `I3 Change Keyboard Layout`, press `Tab` to highlight `<Select>` then press `Enter`
    ** Pick an appropirate keyboard.
    
  * Press `Tab` twice to highlight `<Finish>` then press Enter
  * If the system prompts you to reboot press Enter to reboot
    If not at the prompt enter `sudo reboot` to reboot the Pi
    
### Update and install all required software

Everything from this point can be performed via the keyboard attached to the Raspberry Pi or via SSH
* On Windows use [PuTTY](https://www.putty.org/) to perform SSH
* On Linux or Mac OS/X use Terminal to perform SSH

* Update and Upgrade the Rasperry Pi
  * `sudo apt update && sudo apt upgrade -y`
  
* Install the database (MariaDB or other SQL database)
  * `sudo apt install mariadb-server -y`
  
* Configure the database
  * `sudo mysql_secure_installation`
  * At the `Enter current password for root (enter for none):` press `Enter`
  * Press `Y` to set a new password and enter a new root database password
  * Press `Y` four (4) times to:
    * Remove anonymous users
    * Disallow root login remotely
    * Remove the test database
    * Reload the privileges
  * Login to the database, set up the new database table and user to access it
    * `sudo mysql -uroot -p`
    * Press `Enter` at the password prompt
    * Create a new database table (catesa)
      * `CREATE DATABASE catesa;`
    * Create a new database user (staff)
      * `CREATE USER 'staff'@'localhost' IDENTIFIED BY 'DATABASE-PASSWORD';` ** MAKE SURE TO CHANGE THE PASSWORD
    * Allow the new database user to manage the table
      * `GRANT ALL PRIVILEGES ON catesa.* TO 'staff'@'localhost';`
    * Reload the privileges
      * `FLUSH PRIVILEGES;`
    * Exit and test that the new user can login
      * `exit`
      * `mysql -ustaff -p`
      * At the `Enter password:` prompt enter the `DATABASE-PASSWORD` and you should be in MariaDB
      * `exit`
      
* Install nginx (or apache) webserver on the Raspberry Pi
  * `sudo apt install nginx -y`
    
* Start up nginx
  * `sudo /etc/init.d/nginx start`
  * In a web browser go to http://IP-ADDRESS-OF-PI
  * If everything is running correctly you will see the welcome to nginx page
    
* Install PHP
  * `sudo apt install php-fpm -y`
    
* Enable PHP on nginx
  * `sudo nano /etc/nginx/sites-enabled/default`
  * Find the line 
    ```
    index index.html index.htm ...
    ```
    and change it to 
    ```
    index index.php index.html index.htm ...
    ```
  * Find the section `pass the PHP scripts to FastCGI server` and remove the comments to enable it
    **NOTE:** The PHP version might change from 7.3 depending on when the installation is done
    * The final section should look like:
      ```
      # pass the PHP scripts to FastCGI server
      #
      location ~ \.php$ {
              include snippets/fastcgi-php.conf;
              # With php-fpm (or other unix socktes):
              fastcgi_pass unix:/var/run/php/php7.3-fpm.sock;
              # With php-cgi (or other tcp sockets):
              # fastcgi_pass 127.0.0.1:9000;
      }
      ```
  * Reload nginx
    `sudo /etc/init.d/nginx reload`
      
  * Test that PHP is working 
    * `sudo mv /var/www/html/index.nginx-debian.html /var/www/html/index.php`
    * `sudo nano /var/www/html/index.php`
      * Add `<?php echo phpinfo(); ?>` just before the `</body>` tag, save and exit the editor
    * Refresh your web browser and you should see the nginx welcome page followed by the PHP information
      
* Install PhpMyAdmin
  * `sudo apt install phpmyadmin -y`
  * Press `Y` and `Enter` at the prompt
  * Select `apache2` as the webserver even if using nginx
    Cursor to apache2, press `spacebar` to select, `Tab` to highlight `<Ok>` and press `Enter`
  * Tab to `<Yes>` then press `Enter`
  * Enter and confirm the password for the phpmyadmin user (**MUST** be different from the root or staff user)
  * Create a hidden link for phpmyadmin
    `sudo ln -s /usr/share/phpmyadmin /var/www/html/pmahidden` 
  * Check that PhpMyAdmin is working
    * In your web browser go to http://IP-ADDRESS-OF-PI/pmahidden
    * Log into PhpMyAdmin using the `staff` and `DATABASE-PASSWORD`
* Configure the database tables
  
  * Create the gpio table

    ```sql
    CREATE TABLE `gpio` (
      `id` int(10) UNSIGNED NOT NULL,
      `pin` int(10) UNSIGNED NOT NULL,
      `name` varchar(100) NOT NULL
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;

    ALTER TABLE `gpio`
      ADD PRIMARY KEY (`id`);
    ```

  * Insert the data into the gpio table

    ```sql
    INSERT INTO `gpio` (`id`, `pin`, `name`) VALUES
      (0, 27, 'GPIO 00 (ID_SD)'),
      (1, 28, 'GPIO 01 (ID_SC)'),
      (2, 3, 'GPIO 02 (SDA1, I2C)'),
      (3, 5, 'GPIO 03 (SCL1, I2C)'),
      (4, 7, 'GPIO 04 (GPCLCK0)'),
      (5, 29, 'GPIO 05'),
      (6, 31, 'GPIO 06'),
      (7, 26, 'GPIO 07 (SPI0_CE1_N)'),
      (8, 24, 'GPIO 08 (SPI0_CE0_N)'),
      (9, 21, 'GPIO 09 (SPI0_MISO)'),
      (10, 19, 'GPIO 10 (SPI0_MOSI)'),
      (11, 23, 'GPIO 11 (SPI0_CLK)'),
      (12, 32, 'GPIO 12 (PWM0)'),
      (13, 33, 'GPIO 13 (PWM1)'),
      (14, 8, 'GPIO 14 (TXD0, UART)'),
      (15, 10, 'GPIO 15 (RXD0, UART)'),
      (16, 36, 'GPIO 16'),
      (17, 11, 'GPIO 17'),
      (18, 12, 'GPIO 18 (PWM0)'),
      (19, 35, 'GPIO 19 (PCM_FS)'),
      (20, 38, 'GPIO 20 (PCM_DIN)'),
      (21, 40, 'GPIO 21 (PCM_DOUT)'),
      (22, 15, 'GPIO 22'),
      (23, 16, 'GPIO 23'),
      (24, 18, 'GPIO 24'),
      (25, 22, 'GPIO 25'),
      (26, 37, 'GPIO 26'),
      (27, 13, 'GPIO 27');

    ALTER TABLE `gpio`
      MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
    ```

  * Create the rooms table

    ```sql
    CREATE TABLE `rooms` (
      `id` int(10) UNSIGNED NOT NULL,
      `enabled` int(10) UNSIGNED NOT NULL DEFAULT 1,
      `gpio` int(10) UNSIGNED NOT NULL,
      `displayorder` int(10) UNSIGNED NOT NULL,
      `name` varchar(100) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    ALTER TABLE `rooms`
      ADD PRIMARY KEY (`id`),
      ADD KEY `fk_g_id` (`gpio`);
    ```

  * Insert the data into the rooms table

    ```sql
    INSERT INTO `rooms` (`id`, `enabled`, `gpio`, `displayorder`, `name`) VALUES
    (1, 1, 4, 1, 'Room 1'),
    (2, 1, 5, 2, 'Room 2'),
    (3, 1, 6, 3, 'Room 3'),
    (4, 1, 12, 4, 'Room 4'),
    (5, 1, 13, 5, 'Room 5'),
    (6, 1, 16, 8, 'Room 6'),
    (7, 1, 17, 10, 'Room 7'),
    (8, 1, 18, 11, 'Room 8'),
    (9, 1, 19, 12, 'Room 9'),
    (10, 1, 20, 14, 'Room 10'),
    (11, 1, 21, 15, 'Room 11'),
    (12, 1, 22, 16, 'Room 12'),
    (13, 1, 23, 17, 'Room 13'),
    (14, 1, 24, 18, 'Laundry Room'),
    (15, 1, 25, 19, 'TV Room'),
    (16, 1, 26, 6, 'Room 5P'),
    (17, 1, 27, 9, 'Room 6P'),
    (18, 1, 1, 100, 'GPIO 1'),
    (19, 1, 2, 101, 'GPIO 2'),
    (20, 1, 3, 102, 'GPIO 3'),
    (21, 1, 7, 103, 'GPIO 7'),
    (22, 1, 8, 104, 'GPIO 8'),
    (23, 1, 9, 105, 'GPIO 9'),
    (24, 1, 10, 106, 'GPIO 10'),
    (25, 1, 11, 107, 'GPIO 11'),
    (26, 1, 14, 108, 'GPIO 14'),
    (27, 1, 15, 109, 'GPIO 15'),
    (28, 1, 28, 110, 'GPIO 0');

    ALTER TABLE `rooms`
      MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;
    
    ALTER TABLE `rooms` 
      ADD CONSTRAINT `fk_g_id` FOREIGN KEY (`gpio`) REFERENCES `gpio`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
    ```

  * Create the results table

    ```sql
    CREATE TABLE `results` (
        `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
        `room` INT UNSIGNED NOT NULL,
        `status` INT UNSIGNED NOT NULL,
        `date` DATETIME NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE = InnoDB;

    ALTER TABLE `results`
      ADD CONSTRAINT `fk_ro_id` FOREIGN KEY (`room`) REFERENCES `rooms`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
    ```

* Setup Python 3 for MariaDb, GPIO access
  ```script
  sudo apt install python3-pip -y
  sudo pip3 install mariadb
  sudo pip3 install RPi.GPIO
  ```
  
* Install the MP3 audio player
  `sudo apt install mpg123 -y`
    
### Configure the application

* Create a work directory
  `mkdir ~/work`
* Create a door sensor subdirectory
  `mkdir ~/work/doorsensor`
  `cd ~/work/doorsensor`
* Copy all the code files from the GIT repository (use git clone or download the zipped files)
* Make the python files executable
  `chmod +x *.py`
* Create a file `config.json` (**NOTE:** This file should **NOT** be committed into the GIT repository)
  ```json
  {
      "user": "staff",
      "password": "DATABASE-PASSWORD",
      "host": "localhost",
      "database": "catesa"
  }
  ```

* Start up the program 
  `./doorsensor`

## DEBUGGING

### PhpMyAdmin and PHP 7.3

There is a bug with the current PhpMyAdmin (4.6.6deb5) and the current PHP (7.3.19-1~deb10u1)
that displays an error when displaying the results of a query or browsing a table.
Apparently this is fixed in PhpMyAdmin 4.8.3 and above, but this isn't available through
the normal `apt install` process right now.

They can be fixed by this **HACK**

In the directory `/usr/share/phpmyadmin/libraries` make changes to the following files

**plugin_interface.lib.php**
Change line **551**
From `if ($options != null && count($options) > 0) {`
To   `if ($options != null && (is_array($options) || $options instanceof Countable) && count($options) > 0) {`

**sql.lib.php**
Change line **613**
From `|| (count($analyzed_sql_results['select_expr'] == 1)`
To   `|| ((count($analyzed_sql_results['select_expr']) == 1)`

**Restart nginx**
```script
sudo /etc/init.d/nginx restart
```
