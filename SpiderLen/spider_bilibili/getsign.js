"use strict";
var page = require('webpage').create();

var system = require('system');

var BilibiliWebSiteURL = "";


if(system.args.length === 1){
	console.log("Has No args");
	phantom.exit();
} else {
	BilibiliWebSiteURL = system.args[1];
	
	page.onResourceRequested = function (data,req){
		console.log(data.url);
		console.log(req.url);
	};

	page.onResourceReceived = function (res){
		var Url = res.url;
		console.log(Url);
		if (Url.indexOf("interface.bilibili.com/v2/playurl?cid=")>0){
			console.log(Url);
		}
	};
	
	page.open(BilibiliWebSiteURL, function (status){
		if (status !== 'success'){
			console.log('fail to load the address');
		}
		console.log("Bilibilititle:" + page.title);
		console.log("BilibiliURL:" + page.url);
		phantom.exit();
	});	
	
}

