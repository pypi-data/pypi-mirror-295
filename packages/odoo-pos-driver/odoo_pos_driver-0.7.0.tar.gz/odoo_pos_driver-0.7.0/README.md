# Odoo POS Driver

This tools is intented to by used with the Odoo Point of sale application. It replaces the IoT Box tools / "hw_" modules,
or pywebdriver tool.

Once installed locally in the cashier computer, devices will be discovered by the tool, once plugged, and communication
can be done with the Odoo Point of Sale module.

## Run

```shell
odoo-tools-grap\
  --address 0.0.0.0\              # address where the web service will be available
  --port 8069\                    # port where the web service will be available
  --secure\                       # use https (or http, if ``--unsecure`` is selected)
  --refresh-devices-delay 60\     # New USB devices will be detected every 60 seconds.
  --log-level INFO\               # TRACE / DEBUG / INFO / SUCCESS / WARNING / ERROR / CRITICAL.
                                  # Use INFO + in production to avoid delays in execution.
  --arguments EXTRA_ARGUMENTS     # Json formatted data to pass to devices.
                                  # Ex: {"scale": {"polynomial": 123456}}
                                  # will pass the polynomial value to the scale device.
```
## Usage

Go the home page of the tool, via https://localhost:8069.
Pages are available to test connections, see errors, etc.

![home_page](https://gitlab.com/grap-rhone-alpes/odoo-pos-driver/-/raw/main/odoo_pos_driver/static/home_page.png)


## Installation (to run manually)

* install the latest released version:

```shell
pipx install odoo-pos-driver
```

* _or_ Install the latest version:

```shell
pipx install git+https://gitlab.com/grap-rhone-alpes/odoo-pos-driver.git
```

Note: use ``--python python3.9`` (or higher) option, if your default python environment is under python 3.9 version.

## Installation (as a service) (BETA)

This will create a service (via systemd) that will execute odoo-pos-driver in the background and launches at startup.

```shell
wget https://gitlab.com/grap-rhone-alpes/odoo-pos-driver/-/raw/main/install_debian.sh
# Optional adapt the installation script before execution:
# - add python specific version in pipx installation
# - add specific argument in the call of odoo-pos-driver in the .service file
sudo sh install_debian.sh
```

Once installed, you can run the following system command.

```shell
# Get status of the service
sudo systemctl status odoo-pos-driver.service

# Follow the logs of the service
sudo journalctl -fu odoo-pos-driver.service
```

Note: For the time being, the script is not very well, because it requires to
install the library as a sudoer.

## Odoo modules

Compatibility of the library with Odoo Modules, depending on the version.

### V16

- Printer (+ Cashbox): ``point_of_sale`` (Odoo CE)

- Display: ``pos_odoo_driver_display`` (https://github.com/grap/odoo-addons-pos)

- Payment: ``pos_odoo_driver_payment`` (https://github.com/grap/odoo-addons-pos)

- Scale: TODO

## Compatible devices

<table style="width: 100%;">
    <tbody>
        <tr>
            <th colspan="2">Printers</th>
        </tr>
        <tr>
            <td>Epson - TM-T20III</td>
            <td>
              <img src="https://gitlab.com/grap-rhone-alpes/odoo-pos-driver/-/raw/main/odoo_pos_driver/static/devices/printer__epson__tm_t20.png" width="200" height="200" />
            </td>
        </tr>
        <tr>
            <th colspan="2">Display</th>
        </tr>
        <tr>
            <td>Aures - OCD 300</td>
            <td>
              <img src="https://gitlab.com/grap-rhone-alpes/odoo-pos-driver/-/raw/main/odoo_pos_driver/static/devices/display__aures__ocd_300.png" width="200" height="200" />
            </td>
        </tr>
        <tr>
            <th colspan="2">Payment Terminal</th>
        </tr>
        <tr>
            <td>Ingenico - Move/5000</td>
            <td>
              <img src="https://gitlab.com/grap-rhone-alpes/odoo-pos-driver/-/raw/main/odoo_pos_driver/static/devices/payment__ingenico__move_5000.png" width="200" height="200" />
            </td>
        </tr>
        <tr>
            <th colspan="2">Scale</th>
        </tr>
        <tr>
            <td>Mettler Toledo - Ariva S</td>
            <td>
              <img src="https://gitlab.com/grap-rhone-alpes/odoo-pos-driver/-/raw/main/odoo_pos_driver/static/devices/scale__mettler_toledo__ariva_s.png" width="200" height="200" />
            </td>
        </tr>
    </tbody>
</table>



# Credits

## Authors

* GRAP <https://www.grap.coop>

## Contributors

* Sylvain LE GAL <sylvain.legal@grap.coop>

## Extra authorship

Much of the code in this project comes from other projects, including:

  * Odoo, by Odoo SA, https://github.com/odoo/odoo, specially from "hw_" modules.

  * Pywebdriver, by GRAP, https://github.com/pywebdriver/pywebdriver. Main contributors are:

    * Sylvain LE GAL <sylvain.legal@grap.coop>
    * Sylvain CALADOR <sylvain.calador@akretion.com>
    * Sébastien BEAU <sebastien.beau@akretion.com>
    * Carmen BIANCA BAKKER <carmen@coopiteasy.be>
    * Alexis DE LATTRE <alexis.delattre@akretion.com>
    * Quentin DUPONT <quentin.dupont@grap.coop>
    * Pierrick BRUN <pierrick.brun@akretion.com>
    * Hugues DE KEYZER  <hugues@coopiteasy.be>

  * pyposdisplay, by Akretion, https://github.com/akretion/pyposdisplay. Main contributors are:

    * Alexis DE LATTRE <alexis.delattre@akretion.com>
    * Sébastien BEAU <sebastien.beau@akretion.com>

  * pypostelium, by Akretion, https://github.com/akretion/pypostelium. Main contributors are:

    * Sylvain CALADOR <sylvain.calador@akretion.com>
    * Alexis DE LATTRE <alexis.delattre@akretion.com>

  * hw_dialog06_scale, by Coop It Easy, https://github.com/coopiteasy/iot/tree/12.0-dialog06/hw_dialog06_scale. Main contributors are:

    * Vincent Van Rossem <vincent.vanrossem@camptocamp.com>

## Images
* Icon created by AbtoCreative (Flaticon):
  - Application icon: https://www.flaticon.com/fr/icones-gratuites/hub-usb

* Icon created by ToZ Icon (Flaticon):
  - Credit Card Payment Terminal: https://www.flaticon.com/fr/icone-gratuite/terminal-de-paiement_6137350

* Icon created by Iconic Panda (Flaticon):
  - LCD Customer Display: https://www.flaticon.com/fr/icone-gratuite/lcd_9622586

* Icon created by Icongeek26 (Flaticon):
  - Thermal Receipt Printer: https://www.flaticon.com/fr/icone-gratuite/facture_1649343
