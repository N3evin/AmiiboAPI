# Infomation
Please use the following form when doing a pull request for amiibo database. Do update the `amiibo.json` and  `game_info.json` file to prevent error and make sure proper testing had been done. If unsure on `game_info.json` please use the following format attached below and just set the games as empty array, as it will be auto generated. Tick the `checklist` before submitting to ensure you have all the required information.

# Pull request form
### Checklist
 - [ ] The ids provided are not spoof.
 - [ ] The ids provided are all in lowercase.
 - [ ] The `game_info.json` had been updated with the corresponding ids.
 - [ ] Images of amiibo had been provided with the highest quality.

### Link to amiibo.life for amiibo
- link_1
- link_2
- link_3

# Example for empty game_info
```json
"0x02ed0001015a0502":
{
	"games3DS": [],
	"gamesWiiU": [],
	"gamesSwitch": []
}
```