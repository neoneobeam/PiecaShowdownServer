/** @type {import('../play.pokemonshowdown.com/src/client-main').PSConfig} */
Config = Config || {};

/* version */ Config.version = "0";

Config.bannedHosts = ['cool.jit.su', 'pokeball-nixonserver.rhcloud.com'];

Config.whitelist = [
	//'10.0.0.22'

	// The full list is maintained outside of this repository so changes to it
	// don't clutter the commit log. Feel free to copy our list for your own
	// purposes; it's here: https://play.pokemonshowdown.com/config/config.js

	// If you would like to change our list, simply message Zarel on Smogon or
	// Discord.
];

// `defaultserver` specifies the server to use when the domain name in the
// address bar is `Config.routes.client`.
Config.defaultserver = {
	id: 'showdown',
	//host: 'sim3.psim.us',
	// edited by neo, makes the server's client be the custom one
	host: '_name_of_link_goes_here_.trycloudflare.com',
	port: 443,
	httpport: 8000,
	altport: 80,
	registered: true
};

// also added by neo (was having some trouble getting to the part in the html/internal js
// where it sets these vars)
Config.server = {
	id: 'showdown',
	//host: 'sim3.psim.us',
	host: '_name_of_link_goes_here_.trycloudflare.com',
	port: 443,
	httpport: 8000,
	altport: 80,
	registered: true
}


Config.roomsFirstOpenScript = function () {
};

Config.customcolors = {
	'zarel': 'aeo'
};
/*** Begin automatically generated configuration ***/
Config.version = "0.11.2";

Config.routes = {
	root: 'pokemonshowdown.com',
	client: 'play.pokemonshowdown.com',
	dex: 'dex.pokemonshowdown.com',
	replays: 'replay.pokemonshowdown.com',
	users: 'pokemonshowdown.com/users',
	teams: 'teams.pokemonshowdown.com',
};
/*** End automatically generated configuration ***/
