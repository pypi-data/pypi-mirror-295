# Changelog

<!--next-version-placeholder-->

## v0.4.0 (2024-09-12)

### Feature

* Added 'maintenance' and 'unmaintenance' subcommands: ([`c444a3b`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/c444a3b577bec036df3c066acebf72e8c7f008d5))

## v0.3.7 (2024-08-23)

### Fix

* Don't use `._api_key` externally, used property setter to make it easier (.api_key = 'abc') ([`b430995`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/b430995b3c34f7a842f5019728d0937ae18c2de9))

## v0.3.6 (2024-04-15)

### Fix

* Set default of apikey to empty string instead of None ([`c46ed10`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/c46ed10a7bb1bb23eb71a224a463348d7b012c30))

## v0.3.5 (2024-04-09)

### Fix

* **deps:** Include two missing dependencies ([`09fb42e`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/09fb42e88c5c79dc02fc8cf80e31173a1d03b14f))

## v0.3.4 (2024-03-15)
### Fix
* Delayed init of UptimeRobot instance, since this depends on TomlConfig which is not always available ([`c73daee`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/c73daeed3ffec5766247795c1b97e44b84773e9b))

## v0.3.3 (2024-02-09)


## v0.3.2 (2024-02-09)


## v0.3.1 (2024-02-09)


## v0.3.1 (2024-02-09)
### Fix
* **auto-add:** Pre-select already added domains ([`8fa7b03`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/8fa7b03e54b51c92d1202fd50af3e768af59483b))


## v0.3.0 (2024-02-02)
### Feature
* After auto-add, the user is queried to add these monitors to a public dashboard ([`da5eaa9`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/da5eaa9b59669fce7ef74bc1179393907abe1066))
* Work in progress to add dashboards (PSPs) to the uptimerobot API ([`8b5c583`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/8b5c583383a356b6186d83edc0ff414897e6697a))

## v0.2.5 (2024-01-25)

### Fix

* **auto-add:** Don't query users for domains to add if the provided api key is empty ([`7139460`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/713946079823dcde55bf3deb40e2b71cfe3cc92c))

## v0.2.4 (2024-01-25)

### Fix

* If API key in .env is left empty, don't crash with an error but show a warning instead ([`2ff8713`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/2ff87131aa1ff450b1f7226eeb12a0530b38a9dd))

## v0.2.3 (2024-01-25)

### Fix

* **auto-add:** Better prompt for domain selection; made --quiet still output but without color ([`306a5ea`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/306a5ea5c4d021894940e94f5b1041aabde4022b))

## v0.2.2 (2024-01-25)

### Fix

* Add --quiet to auto-add to ignore warnings/errors quietly ([`36e2d6a`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/36e2d6abd9fb08970c184df93025883c325e1dd7))

## v0.2.1 (2024-01-25)

### Fix

* ImportError: No module named 'termcolor._types' ([`24aa55f`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/24aa55f069ee2970a17788c37ff1437e14d93d11))

## v0.2.0 (2024-01-25)

### Documentation

* Explained how to use it as a library ([`23646c6`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/23646c62246102f6dbc72e849842d621632fd368))

## v0.1.1 (2024-01-25)

### Fix

* **autoadd:** Add flag in .env to prevent asking the same question again ([`e6d5894`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/e6d58946b4e2e4f88557e1daec5c4cf2c5754e82))

## v0.1.0 (2024-01-25)

### Feature

* Add --fmt to output as JSON or YAML for most relevant cases ([`2ce4c17`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/2ce4c17ed4cdc6fb465ac50eeeedefa83b18458b))
* Started on pytest but free tier api is limited to 10 req/min ([`1a1099a`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/1a1099a2954229ea2a1bed7e25fd342c2149da44))
* Add edit and reset monitor; added docstrings ([`3a21c27`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/3a21c270f8ddfce8218abc6a6b19808f2be99ce7))
* Initial version with some endpoints implemented ([`856b589`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/856b5891fde5e773c986f43d34abbb38fe87d2ef))

### Documentation

* Added more basic info ([`f9c0089`](https://github.com/educationwarehouse/edwh-uptime-plugin/commit/f9c008935f736daec63627dc94088c393c99bd88))